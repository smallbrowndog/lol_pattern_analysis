import pandas as pd
import json

def extract_data_table(gamerName, matches):
    extracted_list = []
    for match in matches:
        match_data = {}
        match_data['gamerName'] = str(gamerName)
        match_data['opponentGamerName'] = match['opponentRiotIdGameName']
        match_data['matchID'] = match['matchId']
        match_data['gameCreation'] = match['gameCreation']
        match_data['gameDuration'] = match['gameDuration']
        match_data['at14gameDuration'] = match['at14']['gameDuration']
        match_data['targetTeamId'] = match['targetTeamId']
        match_data['targetWin'] = match['targetWin']

         # at14
        match_data['at14killsRatio'] = match['at14']['combat']['killsRatio']
        match_data['at14deathsRatio'] = match['at14']['combat']['deathsRatio']
        match_data['at14assistsRatio'] = match['at14']['combat']['assistsRatio']
        match_data['at14solokillsRatio'] = match['at14']['combat']['solokillsRatio']
        match_data['at14solodeathsRatio'] = match['at14']['combat']['solodeathsRatio']
        match_data['at14dpm'] = match['at14']['combat']['dpm']
        match_data['at14dtpm'] = match['at14']['combat']['dtpm']
        match_data['at14cspmManage'] = match['at14']['manage']['cspm']
        match_data['at14gpmManage'] = match['at14']['manage']['gpm']
        match_data['at14xpmManage'] = match['at14']['manage']['xpm']
        match_data['at14dpdManage'] = match['at14']['manage']['dpd']
        match_data['at14dpgManage'] = match['at14']['manage']['dpg']
        match_data['at14dpmDiff'] = match['at14']['diff']['dpm']
        match_data['at14dtpmDiff'] = match['at14']['diff']['dtpm']
        match_data['at14cspmDiff'] = match['at14']['diff']['cspm']
        match_data['at14gpmDiff'] = match['at14']['diff']['gpm']
        match_data['at14xpmDiff'] = match['at14']['diff']['xpm']
        match_data['at14dpdDiff'] = match['at14']['diff']['dpd']
        match_data['at14dpgDiff'] = match['at14']['diff']['dpg']

        # af14
        match_data['af14killsRatio'] = match['af14']['combat']['killsRatio']
        match_data['af14deathsRatio'] = match['af14']['combat']['deathsRatio']
        match_data['af14assistsRatio'] = match['af14']['combat']['assistsRatio']
        match_data['af14solokillsRatio'] = match['af14']['combat']['solokillsRatio']
        match_data['af14solodeathsRatio'] = match['af14']['combat']['solodeathsRatio']
        match_data['af14dpm'] = match['af14']['combat']['dpm']
        match_data['af14dtpm'] = match['af14']['combat']['dtpm']
        match_data['af14cspmManage'] = match['af14']['manage']['cspm']
        match_data['af14gpmManage'] = match['af14']['manage']['gpm']
        match_data['af14xpmManage'] = match['af14']['manage']['xpm']
        match_data['af14dpdManage'] = match['af14']['manage']['dpd']
        match_data['af14dpgManage'] = match['af14']['manage']['dpg']
        match_data['af14dpmDiff'] = match['af14']['diff']['dpm']
        match_data['af14dtpmDiff'] = match['af14']['diff']['dtpm']
        match_data['af14cspmDiff'] = match['af14']['diff']['cspm']
        match_data['af14gpmDiff'] = match['af14']['diff']['gpm']
        match_data['af14xpmDiff'] = match['af14']['diff']['xpm']
        match_data['af14dpdDiff'] = match['af14']['diff']['dpd']
        match_data['af14dpgDiff'] = match['af14']['diff']['dpg']

    extracted_list.append(match_data)
    return extracted_list


df = pd.read_json("./merged_data_full.json")

full_table = []

for j in range(len(df)):
    gamerName = df.iloc[j]['GamerName']
    matches = df.iloc[j]['matches']
    gamertable = extract_data_table(gamerName, matches)
    full_table = full_table + gamertable

with open('final_target_data_sample.json', 'w', encoding='utf-8') as f:
    json.dump(full_table, f, ensure_ascii=False, indent=4)