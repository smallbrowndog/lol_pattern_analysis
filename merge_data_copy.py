# 내가 짜서 틀린 코드

import pandas as pd
import json

def merge_combat():
    combat = {}
    combat['killsRatio'] = target.iloc[0]['at14']['kills'] / (target.iloc[0]['at14']['kills'] + opponent.iloc[0]['at14']['kills'])
    combat['deathsRatio'] = target.iloc[0]['at14']['deaths'] / (target.iloc[0]['at14']['deaths'] + opponent.iloc[0]['at14']['deaths'])
    combat['assistsRatio'] = target.iloc[0]['at14']['assists'] / (target.iloc[0]['at14']['assists'] + opponent.iloc[0]['at14']['assists'])
    combat['solokillsRatio'] = target.iloc[0]['at14']['solokills'] / (target.iloc[0]['at14']['solokills'] + opponent.iloc[0]['at14']['solokills'])
    combat['solodeathsRatio'] = target.iloc[0]['at14']['solodeaths'] / (target.iloc[0]['at14']['solodeaths'] + opponent.iloc[0]['at14']['solodeaths'])
    combat['dpm'] = target.iloc[0]['at14']['totalDamageDealtToChampions'] / (target.iloc[0]['at14']['totalDamageDealtToChampions'] + opponent.iloc[0]['at14']['totalDamageDealtToChampions'])
    combat['dtpm'] = target.iloc[0]['at14']['totalDamageTaken'] / (target.iloc[0]['at14']['totalDamageTaken'] + opponent.iloc[0]['at14']['totalDamageTaken'])
    combat['targetKDA'] = {'kills': target.iloc[0]['at14']['kills'], 'deaths': target.iloc[0]['at14']['deaths'], 'assists': target.iloc[0]['at14']['assists']}
    combat['targetSoloKD'] = {'solokills': target.iloc[0]['at14']['solokills'], 'solodeaths': target.iloc[0]['at14']['solodeaths']}
    combat['opponentKDA'] = {'kills': opponent.iloc[0]['at14']['kills'], 'deaths': opponent.iloc[0]['at14']['deaths'], 'assists': opponent.iloc[0]['at14']['assists']}
    combat['opponentSoloKD'] = {'solokills': opponent.iloc[0]['at14']['solokills'], 'solodeaths': opponent.iloc[0]['at14']['solodeaths']}
    return combat

def merge_manage():
    manage = {}
    manage['cspm'] = target.iloc[0]['cspm']
    manage['gpm'] = target.iloc[0]['gpm']
    manage['xpm'] = target.iloc[0]['xpm']
    manage['dpd'] = target.iloc[0]['dpd']
    manage['dpg'] = target.iloc[0]['dpg']
    return manage

def merge_diff():
    diff = {}
    diff['dpm'] = target.iloc[0]['dpm'] - opponent.iloc[0]['dpm']
    diff['dtpm'] = target.iloc[0]['dtpm'] - opponent.iloc[0]['dtpm']
    diff['cspm'] = target.iloc[0]['cspm'] - opponent.iloc[0]['cspm']
    diff['gpm'] = target.iloc[0]['gpm'] - opponent.iloc[0]['gpm']
    diff['xpm'] = target.iloc[0]['xpm'] - opponent.iloc[0]['xpm']
    diff['dpd'] = target.iloc[0]['dpd'] - opponent.iloc[0]['dpd']
    diff['dpg'] = target.iloc[0]['dpg'] - opponent.iloc[0]['dpg']
    return diff

def merge_data(target, opponent):
    merged_data = {
        "GamaName" : target.iloc[0]['riotIdGameName'],
        "matches" : []
    }

    match = {}
    match["matchId"] = target.iloc[0]['matchId']
    match["gameCreation"] = int(target.iloc[0]['gameCreation'])
    match["gameDuration"] = float(target.iloc[0]['gameDuration'])
    match["riotIdGameName"] = target.iloc[0]['riotIdGameName']
    match["participantId"] = int(target.iloc[0]['participantId'])
    match["opponentRiotIdGameName"] = opponent.iloc[0]['riotIdGameName']
    match["opponentParticipantId"] = int(opponent.iloc[0]['participantId'])
    match["targetTeamId"] = int(target.iloc[0]['teamId'])
    match["targetWin"] = bool(target.iloc[0]['win'])

    at14 = {}
    at14["gameDuration"] = target.iloc[0]['at14']['gameDuration']
    at14["combat"] = merge_combat()
    at14["manage"] = merge_manage()
    at14["diff"] = merge_diff()
    match["at14"] = at14

    af14 = {}
    af14["gameDuration"] = target.iloc[0]['af14']['gameDuration']
    af14["combat"] = merge_combat()
    af14["manage"] = merge_manage()
    af14["diff"] = merge_diff()
    match["af14"] = af14

    merged_data["matches"].append(match)
    return merged_data

df_target   = pd.read_json("./extract_full_data.json")
df_opponent = pd.read_json("./extract_full_data_o.json")

total_data = []

target = pd.DataFrame(df_target.iloc[0]['match'])
opponent = pd.DataFrame(df_opponent.iloc[0]['match'])

gamer_data = merge_data(target, opponent)
print(gamer_data)

total_data.append(gamer_data)

with open('merged_data_full.json', 'w', encoding='utf-8') as f:
    json.dump(total_data, f, ensure_ascii=False, indent=4)