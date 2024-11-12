import json

import pandas as pd

def extract_data(df_match, df_timeline, gamer_name, opposite=False):
    gamer_data =[]

    for j, match in enumerate(df_match['info'].values):
        # one_match = df_match.iloc[0]
        # print(one_match)
        # 분석하고자 하는 데이터의 matchId
        matchId = df_match['metadata'][j]['matchId']
        print(matchId)

        # 분석하고자 하는 데이터와 전체 데이터중 매칭하기
        for k, timeline in enumerate(df_timeline['metadata']):
            if timeline['matchId'] == matchId:
                match_timeline = df_timeline['info'][k]
                # print(matchId, timeline['matchId'])
                break

        # 미드인지 아닌지 확인하는 작업
        check_gamer_mid = False
        teamid = -1
        oteamid = -1

        for pid, participant in enumerate(match['participants']):
            # gamer_name을 이용해서 'riotIdGameName' 와 매치
            if participant['riotIdGameName'] == gamer_name:
                # 미드인지 확인해서 미드로 체크하고 teamid 를 변경
                if participant['teamPosition'] == 'MIDDLE':
                    check_gamer_mid = True
                    teamid = pid
            else:
                # 위와 동일
                if participant['teamPosition'] == 'MIDDLE':
                    oteamid = pid

        #print(check_gamer_mid, teamid, oteamid)
        if opposite:
            # 임시 저장소에 teamid를 저장한 후에
            tmp = teamid
            # 아래 코드처럼 teamid와 oteamid를 변경해준다
            teamid = oteamid
            oteamid = tmp



        target_data = {}
        # 위에서 불러온 teamid를 이용해 target_data 딕셔너리 타입으로 데이터 집어넣기
        if check_gamer_mid and match['gameDuration'] > 1200:
            match_p = match['participants'][teamid]
            match_o = match['participants'][oteamid]
            target_data["riotIdGameName"] = match_p['riotIdGameName']
            target_data["matchId"] = df_match['metadata'][0]['matchId']
            target_data["gameCreation"] = match['gameCreation']
            target_data["gameDuration"] = match_p['challenges']['gameLength']
            target_data["participantId"] = match_p['participantId']
            target_data["opponentpId"] = match_o['participantId']
            target_data["teamId"] = match_p['teamId']
            target_data["teamPosition"] = match_p['teamPosition']

            target_data['kda'] = match_p['challenges']['kda']
            target_data['kills'] = match_p['kills']
            target_data['deaths'] = match_p['deaths']
            target_data['assists'] = match_p['assists']
            target_data['win'] = match_p['win']

            # 전체 솔로킬 체크
            solo_kill, solo_death = 0, 0
            for frame in match_timeline['frames']:
                for event in frame['events']:
                    if (event['type'] == "CHAMPION_KILL") and ('assistingParticipantIds' not in event):  # 1 vs 1 구도
                        if (event['killerId'] == target_data['participantId']):
                            solo_kill += 1
                        elif (event['victimId'] == target_data['participantId']):
                            solo_death += 1

            target_data['solokills'] = solo_kill
            target_data['solodeaths'] = solo_death

            target_data['totalDamageDealtToChampions'] = match_p['totalDamageDealtToChampions']
            target_data['totalDamageTaken'] = match_p['totalDamageTaken']
            target_data['totalMinionsKilled'] = match_p['totalMinionsKilled']
            target_data['totalCS'] = target_data['totalMinionsKilled'] + match_p['totalEnemyJungleMinionsKilled']
            target_data['goldEarned'] = match_p['goldEarned']
            target_data['totalXP'] = match_timeline['frames'][-1]['participantFrames'][str(target_data['participantId'])][
                'xp']

            duration = target_data['gameDuration'] / 60
            target_data['dpm'] = target_data['totalDamageDealtToChampions'] / duration
            target_data['dtpm'] = target_data['totalDamageTaken'] / duration
            target_data['mpm'] = target_data['totalMinionsKilled'] / duration
            target_data['cspm'] = target_data['totalCS'] / duration
            target_data['xpm'] = target_data['totalXP'] / duration
            target_data['gpm'] = target_data['goldEarned'] / duration
            target_data['dpd'] = target_data['totalDamageDealtToChampions'] / (
                1 if target_data['deaths'] == 0 else target_data['deaths'])
            target_data['dpg'] = target_data['totalDamageDealtToChampions'] / target_data['goldEarned']

            # 14분전 데이터 모으기
            at14_target_data = {}
            match_timeline_at14 = match_timeline['frames'][:15]
            # 시간이 잘 맞나 확인
            # print(match_timeline_at14[-1]['timestamp']/60000)
            at14_kill, at14_death, at14_assist = 0, 0, 0
            at14_solo_kill, at14_solo_death = 0, 0
            for frame in match_timeline_at14:
                for event in frame['events']:
                    if (event['type'] == "CHAMPION_KILL") and ('assistingParticipantIds' not in event):
                        if (event['killerId'] == target_data['participantId']):
                            at14_solo_kill += 1
                            at14_kill += 1
                        elif (event['victimId'] == target_data['participantId']):
                            at14_solo_death += 1
                            at14_death += 1
                    elif (event['type'] == "CHAMPION_KILL"):
                        if target_data['participantId'] in event['assistingParticipantIds']:
                            at14_assist += 1
                        elif event['killerId'] == target_data['participantId']:
                            at14_kill += 1
                        elif event['victimId'] == target_data['participantId']:
                            at14_death += 1
            at14_target_data['kills'] = at14_kill
            at14_target_data['deaths'] = at14_death
            at14_target_data['assists'] = at14_assist
            at14_target_data['solokills'] = at14_solo_kill
            at14_target_data['solodeaths'] = at14_solo_death

            # 딱 14분 데이터 뽑기
            match_timeline_14 = match_timeline['frames'][14]
            match_timeline_14_target = match_timeline_14['participantFrames'][str(target_data['participantId'])]
            # 초단위로 나올 수 있도록
            at14_target_data['gameDuration'] = match_timeline_14['timestamp'] / 1000
            at14_target_data['totalDamageDealtToChampions'] = match_timeline_14_target['damageStats'][
                'totalDamageDoneToChampions']
            at14_target_data['totalDamageTaken'] = match_timeline_14_target['damageStats']['totalDamageTaken']
            at14_target_data['totalMinionsKilled'] = match_timeline_14_target['minionsKilled']
            at14_target_data['totalCS'] = at14_target_data['totalMinionsKilled'] + match_timeline_14_target[
                'jungleMinionsKilled']
            at14_target_data['totalXP'] = match_timeline_14_target['xp']
            at14_target_data['goldEarned'] = match_timeline_14_target['totalGold']

            at14_duration = at14_target_data['gameDuration'] / 60
            at14_target_data['dpm'] = at14_target_data['totalDamageDealtToChampions'] / at14_duration
            at14_target_data['dtpm'] = at14_target_data['totalDamageTaken'] / at14_duration
            at14_target_data['dpd'] = at14_target_data['totalDamageDealtToChampions'] / (
                1 if at14_target_data['deaths'] == 0 else at14_target_data['deaths'])
            at14_target_data['dpg'] = at14_target_data['totalDamageDealtToChampions'] / at14_target_data['goldEarned']
            at14_target_data['gpm'] = at14_target_data['goldEarned'] / at14_duration
            at14_target_data['xpm'] = at14_target_data['totalXP'] / at14_duration
            at14_target_data['mpm'] = at14_target_data['totalMinionsKilled'] / at14_duration
            at14_target_data['cspm'] = at14_target_data['totalCS'] / at14_duration

            # 14분후 데이터 모으기
            af14_target_data = {}

            af14_target_data['kills'] = target_data['kills'] - at14_target_data['kills']
            af14_target_data['deaths'] = target_data['deaths'] - at14_target_data['deaths']
            af14_target_data['assists'] = target_data['assists'] - at14_target_data['assists']
            af14_target_data['solokills'] = target_data['solokills'] - at14_target_data['solokills']
            af14_target_data['solodeaths'] = target_data['solodeaths'] - at14_target_data['solodeaths']

            af14_target_data['gameDuration'] = target_data['gameDuration'] - at14_target_data['gameDuration']
            af14_target_data['totalDamageDealtToChampions'] = target_data['totalDamageDealtToChampions'] - at14_target_data[
                'totalDamageDealtToChampions']
            af14_target_data['totalDamageTaken'] = target_data['totalDamageTaken'] - at14_target_data['totalDamageTaken']
            af14_target_data['totalMinionsKilled'] = target_data['totalMinionsKilled'] - at14_target_data[
                'totalMinionsKilled']
            af14_target_data['totalCS'] = target_data['totalCS'] - at14_target_data['totalCS']
            af14_target_data['totalXP'] = target_data['totalXP'] - at14_target_data['totalXP']
            af14_target_data['goldEarned'] = target_data['goldEarned'] - at14_target_data['goldEarned']

            af14_target_data['dpm'] = af14_target_data['totalDamageDealtToChampions'] / (
                        af14_target_data['gameDuration'] / 60)
            af14_target_data['dtpm'] = af14_target_data['totalDamageTaken'] / (af14_target_data['gameDuration'] / 60)
            af14_target_data['dpd'] = af14_target_data['totalDamageDealtToChampions'] / (
                1 if af14_target_data['deaths'] == 0 else af14_target_data['deaths'])
            af14_target_data['dpg'] = af14_target_data['totalDamageDealtToChampions'] / af14_target_data['goldEarned']
            af14_target_data['gpm'] = af14_target_data['goldEarned'] / (af14_target_data['gameDuration'] / 60)
            af14_target_data['xpm'] = af14_target_data['totalXP'] / (af14_target_data['gameDuration'] / 60)
            af14_target_data['cspm'] = af14_target_data['totalCS'] / (af14_target_data['gameDuration'] / 60)
            af14_target_data['mpm'] = af14_target_data['totalMinionsKilled'] / (af14_target_data['gameDuration'] / 60)

            target_data['at14'] = at14_target_data
            target_data['af14'] = af14_target_data
            print(f"{j+1}번째 게임 데이터\n{target_data}")
            print()
            gamer_data.append(target_data)
        else:
            print(f"{j+1}번째 게임 제외\n 미드인지의 여부 : {check_gamer_mid}, 게임 시간 : {match['gameDuration']/60} ")

    return gamer_data

df_match = pd.read_json("./solo_rank_30/너는 나의 자존심#KR1/너는 나의 자존심#KR1_matchData.json")
df_timeline = pd.read_json("./solo_rank_30/너는 나의 자존심#KR1/너는 나의 자존심#KR1_timelineData.json")

gamer_name = "너는 나의 자존심"
gamer_data = extract_data(df_match, df_timeline, gamer_name)

# 상대방 아이디로 매치해서 내가 찾은 플레이어를 상대방으로 만들기
opponent_data = extract_data(df_match, df_timeline, gamer_name, opposite=True)

with open('extracted_test_data.json', 'w', encoding='utf-8') as f:
    json.dump(gamer_data, f, ensure_ascii=False, indent=4)

with open('extracted_test_opponent_data.json', 'w', encoding='utf-8') as f:
    json.dump(opponent_data, f, ensure_ascii=False, indent=4)