import pandas as pd
import json

def merge_combat(target, opponent):
    combat = {}
    # combat['killsRatio'] = target['kills'] / (target['kills'] + opponent['kills'])
    combat['killsRatio'] = 0 if target['kills'] == 0 and opponent['kills'] == 0 else target['kills'] / (target['kills'] + opponent['kills'])
    combat['deathsRatio'] = 0 if target['deaths'] == 0 and opponent['deaths'] == 0 else target['deaths'] / (target['deaths'] + opponent['deaths'])
    combat['assistsRatio'] = 0 if target['assists'] == 0 and opponent['assists'] == 0 else target['assists'] / (target['assists'] + opponent['assists'])
    combat['solokillsRatio'] = 0 if target['solokills'] == 0 and opponent['solokills'] == 0 else target['solokills'] / (target['solokills'] + opponent['solokills'])
    combat['solodeathsRatio'] = 0 if target['solodeaths'] == 0 and opponent['solodeaths'] == 0 else target['solodeaths'] / (target['solodeaths'] + opponent['solodeaths'])
    combat['dpm'] = target['dpm']
    combat['dtpm'] = target['dtpm']
    combat['targetKDA'] = {'kills': target['kills'], 'deaths': target['deaths'], 'assists': target['assists']}
    combat['targetSoloKD'] = {'solokills': target['solokills'], 'solodeaths': target['solodeaths']}
    combat['opponentKDA'] = {'kills': opponent['kills'], 'deaths': opponent['deaths'], 'assists': opponent['assists']}
    combat['opponentSoloKD'] = {'solokills': opponent['solokills'], 'solodeaths': opponent['solodeaths']}
    return combat

def merge_manage(target):
    manage = {}
    manage['cspm'] = target['cspm']
    manage['gpm'] = target['gpm']
    manage['xpm'] = target['xpm']
    manage['dpd'] = target['dpd']
    manage['dpg'] = target['dpg']
    return manage

def merge_diff(target, opponent):
    diff = {}
    diff['dpm'] = target['dpm'] - opponent['dpm']
    diff['dtpm'] = target['dtpm'] - opponent['dtpm']
    diff['cspm'] = target['cspm'] - opponent['cspm']
    diff['gpm'] = target['gpm'] - opponent['gpm']
    diff['xpm'] = target['xpm'] - opponent['xpm']
    diff['dpd'] = target['dpd'] - opponent['dpd']
    diff['dpg'] = target['dpg'] - opponent['dpg']
    return diff

def merge_data(target, opponent):
    merged_data = {
        "GamerName" : target.iloc[0]['riotIdGameName'],
        "matches" : []
    }

    for i in range(len(target)):
        match = {}
        match["matchId"] = target.iloc[i]['matchId']
        match["gameCreation"] = int(target.iloc[i]['gameCreation'])
        match["gameDuration"] = float(target.iloc[i]['gameDuration'])
        match["riotIdGameName"] = target.iloc[i]['riotIdGameName']
        match["participantId"] = int(target.iloc[i]['participantId'])
        match["opponentRiotIdGameName"] = opponent.iloc[i]['riotIdGameName']
        match["opponentParticipantId"] = int(opponent.iloc[i]['participantId'])
        match["targetTeamId"] = int(target.iloc[i]['teamId'])
        match["targetWin"] = bool(target.iloc[i]['win'])

        at14 = {}
        at14["gameDuration"] = target.iloc[i]['at14']['gameDuration']
        at14["combat"] = merge_combat(target.iloc[i]['at14'], opponent.iloc[i]['at14'])
        at14["manage"] = merge_manage(target.iloc[i]['at14'])
        at14["diff"] = merge_diff(target.iloc[i]['at14'], opponent.iloc[i]['at14'])
        match["at14"] = at14

        af14 = {}
        af14["gameDuration"] = target.iloc[i]['af14']['gameDuration']
        af14["combat"] = merge_combat(target.iloc[i]['af14'], opponent.iloc[i]['af14'])
        af14["manage"] = merge_manage(target.iloc[i]['af14'])
        af14["diff"] = merge_diff(target.iloc[i]['af14'], opponent.iloc[i]['af14'])
        match["af14"] = af14

        merged_data["matches"].append(match)

    return merged_data


df_target   = pd.read_json("./extract_full_data.json")
df_opponent = pd.read_json("./extract_full_data_o.json")

total_data = []
for j in range(len(df_target)):

    target = pd.DataFrame(df_target.iloc[j]['match'])
    opponent = pd.DataFrame(df_opponent.iloc[j]['match'])

    gamer_data = merge_data(target, opponent)
    print(gamer_data)

    total_data.append(gamer_data)

with open('merged_data_full.json', 'w', encoding='utf-8') as f:
    json.dump(total_data, f, ensure_ascii=False, indent=4)