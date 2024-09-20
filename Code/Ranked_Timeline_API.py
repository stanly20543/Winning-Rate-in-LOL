import requests
import csv
import time

api_key = "RGAPI-4a3c5239-74a3-4c57-91a8-5015ba91201f"

my_info={
"puuid": "ERllPprlSNxloKesGudzbahqJIipiCuXde6ij11u6qmvFnAcKsenurqbnRJnSYuMDk4DjPwePoRm5Q",
"gameName": "嘎嘎嗚拉拉",
"tagLine": "1460"
}

def tier_player_info(region, mode, tier, division, page):
    api_url = f"https://{region}.api.riotgames.com/lol/league-exp/v4/entries/{mode}/{tier}/{division}?page={str(page)}&api_key={api_key}"
    while True:
        resp = requests.get(api_url)
        if resp.status_code == 429:
            time.sleep(10)
            continue
        return resp.json()

def summoner_info(region, summonerID):
    api_url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/{summonerID}?api_key={api_key}"
    while True:
        resp = requests.get(api_url)
        if resp.status_code == 429:
            time.sleep(10)
            continue
        return resp.json()

def matches_ID(region, PUUID, count):
    api_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{PUUID}/ids?type=ranked&start=0&count={str(count)}&api_key={api_key}"
    while True:
        resp = requests.get(api_url)
        if resp.status_code == 429:
            time.sleep(10)
            continue
        return resp.json()

def match_detail_summary(region, ma_ID):
    api_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{ma_ID}?api_key={api_key}"
    while True:
        resp = requests.get(api_url)
        if resp.status_code == 429:
            time.sleep(10)
            continue
        return resp.json()
    
def match_detail_timeline(region, ma_ID):
    api_url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{ma_ID}/timeline?api_key={api_key}"
    while True:
        resp = requests.get(api_url)
        if resp.status_code == 429:
            time.sleep(10)
            continue
        return resp.json()


TW_ranked_players = tier_player_info("TW2", "RANKED_SOLO_5x5", "BRONZE", "I", 1)

KR_ranked_players = tier_player_info("KR", "RANKED_SOLO_5x5", "BRONZE", "I", 1)

start_time = time.time()
csv_file_path = 'BRONZE_Timeline.csv'

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['matchID', 'timestamp', 'puuid', "teamID", 'ID', "win", "championId", 'championName', "TeamPosition", "individualPosition", 'totalGold', 'currentGold', 'xp', 'level', 'dragon', 'horde', 'riftherald', 'baron_nasher'])

    for _ in TW_ranked_players[:20]:
        summonerId = _["summonerId"]
        summonerpuuid = summoner_info("TW2", summonerId)["puuid"]
        matches = matches_ID("sea", summonerpuuid, 30)
        number = TW_ranked_players.index(_)
        print(f"TW_Player:{number+1}", "/", len(TW_ranked_players[:20]), ":", summonerpuuid)
        print("Total Matches:", len(matches))
        i = 1
        try:
            for match in matches:
                print("Match: ", i, match)
                m_summary = match_detail_summary("sea", match)["info"]
                particiipants = m_summary["participants"]
                m_timeline = match_detail_timeline("sea", match)
                x = m_timeline["metadata"]
                frames = m_timeline["info"]["frames"]
                i += 1

                # if frames[0]["participantFrames"] == None :
                #     print("pass")
                #     continue

                # else:
                obj =  {
                        "1" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
                        "2" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
                        "3" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
                        "4" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
                        "5" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
                        "6" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
                        "7" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
                        "8" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
                        "9" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
                        "10" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
                        }
            
                for _ in frames:
                    for event in _["events"]:
                        try:
                            if event["monsterType"]:
                                obj[f"{event["killerId"]}"][f"{event["monsterType"]}"] += 1

                        except:
                            continue

                    writer.writerows([
                        [x["matchId"], _["timestamp"],x["participants"][0], "100", _["participantFrames"]["1"]["participantId"], particiipants[0]["win"], particiipants[0]["championId"], particiipants[0]["championName"], particiipants[0]["teamPosition"], particiipants[0]["individualPosition"], _["participantFrames"]["1"]["totalGold"], _["participantFrames"]["1"]["currentGold"], _["participantFrames"]["1"]["xp"], _["participantFrames"]["1"]["level"], obj["1"]["DRAGON"], obj["1"]["HORDE"], obj["1"]["RIFTHERALD"], obj["1"]["BARON_NASHOR"]], 
                        [x["matchId"], _["timestamp"],x["participants"][1], "100", _["participantFrames"]["2"]["participantId"], particiipants[1]["win"], particiipants[1]["championId"], particiipants[1]["championName"], particiipants[1]["teamPosition"], particiipants[1]["individualPosition"], _["participantFrames"]["2"]["totalGold"], _["participantFrames"]["2"]["currentGold"], _["participantFrames"]["2"]["xp"], _["participantFrames"]["2"]["level"], obj["2"]["DRAGON"], obj["2"]["HORDE"], obj["2"]["RIFTHERALD"], obj["2"]["BARON_NASHOR"]],
                        [x["matchId"], _["timestamp"],x["participants"][2], "100", _["participantFrames"]["3"]["participantId"], particiipants[2]["win"], particiipants[2]["championId"], particiipants[2]["championName"], particiipants[2]["teamPosition"], particiipants[2]["individualPosition"], _["participantFrames"]["3"]["totalGold"], _["participantFrames"]["3"]["currentGold"], _["participantFrames"]["3"]["xp"], _["participantFrames"]["3"]["level"], obj["3"]["DRAGON"], obj["3"]["HORDE"], obj["3"]["RIFTHERALD"], obj["3"]["BARON_NASHOR"]],
                        [x["matchId"], _["timestamp"],x["participants"][3], "100", _["participantFrames"]["4"]["participantId"], particiipants[3]["win"], particiipants[3]["championId"], particiipants[3]["championName"], particiipants[3]["teamPosition"], particiipants[3]["individualPosition"], _["participantFrames"]["4"]["totalGold"], _["participantFrames"]["4"]["currentGold"], _["participantFrames"]["4"]["xp"], _["participantFrames"]["4"]["level"], obj["4"]["DRAGON"], obj["4"]["HORDE"], obj["4"]["RIFTHERALD"], obj["4"]["BARON_NASHOR"]],
                        [x["matchId"], _["timestamp"],x["participants"][4], "100", _["participantFrames"]["5"]["participantId"], particiipants[4]["win"], particiipants[4]["championId"], particiipants[4]["championName"], particiipants[4]["teamPosition"], particiipants[4]["individualPosition"], _["participantFrames"]["5"]["totalGold"], _["participantFrames"]["5"]["currentGold"], _["participantFrames"]["5"]["xp"], _["participantFrames"]["5"]["level"], obj["5"]["DRAGON"], obj["5"]["HORDE"], obj["5"]["RIFTHERALD"], obj["5"]["BARON_NASHOR"]],
                        [x["matchId"], _["timestamp"],x["participants"][5], "200", _["participantFrames"]["6"]["participantId"], particiipants[5]["win"], particiipants[5]["championId"], particiipants[5]["championName"], particiipants[5]["teamPosition"], particiipants[5]["individualPosition"], _["participantFrames"]["6"]["totalGold"], _["participantFrames"]["6"]["currentGold"], _["participantFrames"]["6"]["xp"], _["participantFrames"]["6"]["level"], obj["6"]["DRAGON"], obj["6"]["HORDE"], obj["6"]["RIFTHERALD"], obj["6"]["BARON_NASHOR"]],
                        [x["matchId"], _["timestamp"],x["participants"][6], "200", _["participantFrames"]["7"]["participantId"], particiipants[6]["win"], particiipants[6]["championId"], particiipants[6]["championName"], particiipants[6]["teamPosition"], particiipants[6]["individualPosition"], _["participantFrames"]["7"]["totalGold"], _["participantFrames"]["7"]["currentGold"], _["participantFrames"]["7"]["xp"], _["participantFrames"]["7"]["level"], obj["7"]["DRAGON"], obj["7"]["HORDE"], obj["7"]["RIFTHERALD"], obj["7"]["BARON_NASHOR"]],
                        [x["matchId"], _["timestamp"],x["participants"][7], "200", _["participantFrames"]["8"]["participantId"], particiipants[7]["win"], particiipants[7]["championId"], particiipants[7]["championName"], particiipants[7]["teamPosition"], particiipants[7]["individualPosition"], _["participantFrames"]["8"]["totalGold"], _["participantFrames"]["8"]["currentGold"], _["participantFrames"]["8"]["xp"], _["participantFrames"]["8"]["level"], obj["8"]["DRAGON"], obj["8"]["HORDE"], obj["8"]["RIFTHERALD"], obj["8"]["BARON_NASHOR"]],
                        [x["matchId"], _["timestamp"],x["participants"][8], "200", _["participantFrames"]["9"]["participantId"], particiipants[8]["win"], particiipants[8]["championId"], particiipants[8]["championName"], particiipants[8]["teamPosition"], particiipants[8]["individualPosition"], _["participantFrames"]["9"]["totalGold"], _["participantFrames"]["9"]["currentGold"], _["participantFrames"]["9"]["xp"], _["participantFrames"]["9"]["level"], obj["9"]["DRAGON"], obj["9"]["HORDE"], obj["9"]["RIFTHERALD"], obj["9"]["BARON_NASHOR"]],
                        [x["matchId"], _["timestamp"],x["participants"][9], "200", _["participantFrames"]["10"]["participantId"], particiipants[9]["win"], particiipants[9]["championId"], particiipants[9]["championName"], particiipants[9]["teamPosition"], particiipants[9]["individualPosition"], _["participantFrames"]["10"]["totalGold"], _["participantFrames"]["10"]["currentGold"], _["participantFrames"]["10"]["xp"], _["participantFrames"]["10"]["level"], obj["10"]["DRAGON"], obj["10"]["HORDE"], obj["10"]["RIFTHERALD"], obj["10"]["BARON_NASHOR"]]
                        ])
        except Exception as e:
            # Print the error message
            print(f"An error occurred: {e}")
            # Print the error type (code)
            print(f"Error type: {type(e).__name__}")
            continue    
                    
    for _ in KR_ranked_players[:20]:
        summonerId = _["summonerId"]
        summonerpuuid = summoner_info("KR", summonerId)["puuid"]
        matches = matches_ID("asia", summonerpuuid, 30)
        number = KR_ranked_players.index(_)
        print(f"KR_Player:{number+1}", "/", len(KR_ranked_players[:20]), ":", summonerpuuid)
        print("Total Matches:", len(matches))
        i = 1
        try:
            for match in matches:
                m_summary = match_detail_summary("asia", match)["info"]
                particiipants = m_summary["participants"]
                m_timeline = match_detail_timeline("asia", match)
                x = m_timeline["metadata"]
                frames = m_timeline["info"]["frames"]
                print("Match: ", i, ":", x["matchId"])
                i += 1

                # if frames[0]["participantFrames"] == None:
                #     print("pass")
                #     continue

                # else:
                obj =  {
                        "1" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
                        "2" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
                        "3" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
                        "4" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
                        "5" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
                        "6" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
                        "7" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
                        "8" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
                        "9" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
                        "10" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
                        }
                
                for _ in frames:
                    for event in _["events"]:
                        try:
                            if event["monsterType"]:
                                obj[f"{event["killerId"]}"][f"{event["monsterType"]}"] += 1

                        except:
                            continue

                    writer.writerows([
                        [x["matchId"], _["timestamp"],x["participants"][0], "100", _["participantFrames"]["1"]["participantId"], particiipants[0]["win"], particiipants[0]["championId"], particiipants[0]["championName"], particiipants[0]["teamPosition"], particiipants[0]["individualPosition"], _["participantFrames"]["1"]["totalGold"], _["participantFrames"]["1"]["currentGold"], _["participantFrames"]["1"]["xp"], _["participantFrames"]["1"]["level"], obj["1"]["DRAGON"], obj["1"]["HORDE"], obj["1"]["RIFTHERALD"], obj["1"]["BARON_NASHOR"]], 
                        [x["matchId"], _["timestamp"],x["participants"][1], "100", _["participantFrames"]["2"]["participantId"], particiipants[1]["win"], particiipants[1]["championId"], particiipants[1]["championName"], particiipants[1]["teamPosition"], particiipants[1]["individualPosition"], _["participantFrames"]["2"]["totalGold"], _["participantFrames"]["2"]["currentGold"], _["participantFrames"]["2"]["xp"], _["participantFrames"]["2"]["level"], obj["2"]["DRAGON"], obj["2"]["HORDE"], obj["2"]["RIFTHERALD"], obj["2"]["BARON_NASHOR"]],
                        [x["matchId"], _["timestamp"],x["participants"][2], "100", _["participantFrames"]["3"]["participantId"], particiipants[2]["win"], particiipants[2]["championId"], particiipants[2]["championName"], particiipants[2]["teamPosition"], particiipants[2]["individualPosition"], _["participantFrames"]["3"]["totalGold"], _["participantFrames"]["3"]["currentGold"], _["participantFrames"]["3"]["xp"], _["participantFrames"]["3"]["level"], obj["3"]["DRAGON"], obj["3"]["HORDE"], obj["3"]["RIFTHERALD"], obj["3"]["BARON_NASHOR"]],
                        [x["matchId"], _["timestamp"],x["participants"][3], "100", _["participantFrames"]["4"]["participantId"], particiipants[3]["win"], particiipants[3]["championId"], particiipants[3]["championName"], particiipants[3]["teamPosition"], particiipants[3]["individualPosition"], _["participantFrames"]["4"]["totalGold"], _["participantFrames"]["4"]["currentGold"], _["participantFrames"]["4"]["xp"], _["participantFrames"]["4"]["level"], obj["4"]["DRAGON"], obj["4"]["HORDE"], obj["4"]["RIFTHERALD"], obj["4"]["BARON_NASHOR"]],
                        [x["matchId"], _["timestamp"],x["participants"][4], "100", _["participantFrames"]["5"]["participantId"], particiipants[4]["win"], particiipants[4]["championId"], particiipants[4]["championName"], particiipants[4]["teamPosition"], particiipants[4]["individualPosition"], _["participantFrames"]["5"]["totalGold"], _["participantFrames"]["5"]["currentGold"], _["participantFrames"]["5"]["xp"], _["participantFrames"]["5"]["level"], obj["5"]["DRAGON"], obj["5"]["HORDE"], obj["5"]["RIFTHERALD"], obj["5"]["BARON_NASHOR"]],
                        [x["matchId"], _["timestamp"],x["participants"][5], "200", _["participantFrames"]["6"]["participantId"], particiipants[5]["win"], particiipants[5]["championId"], particiipants[5]["championName"], particiipants[5]["teamPosition"], particiipants[5]["individualPosition"], _["participantFrames"]["6"]["totalGold"], _["participantFrames"]["6"]["currentGold"], _["participantFrames"]["6"]["xp"], _["participantFrames"]["6"]["level"], obj["6"]["DRAGON"], obj["6"]["HORDE"], obj["6"]["RIFTHERALD"], obj["6"]["BARON_NASHOR"]],
                        [x["matchId"], _["timestamp"],x["participants"][6], "200", _["participantFrames"]["7"]["participantId"], particiipants[6]["win"], particiipants[6]["championId"], particiipants[6]["championName"], particiipants[6]["teamPosition"], particiipants[6]["individualPosition"], _["participantFrames"]["7"]["totalGold"], _["participantFrames"]["7"]["currentGold"], _["participantFrames"]["7"]["xp"], _["participantFrames"]["7"]["level"], obj["7"]["DRAGON"], obj["7"]["HORDE"], obj["7"]["RIFTHERALD"], obj["7"]["BARON_NASHOR"]],
                        [x["matchId"], _["timestamp"],x["participants"][7], "200", _["participantFrames"]["8"]["participantId"], particiipants[7]["win"], particiipants[7]["championId"], particiipants[7]["championName"], particiipants[7]["teamPosition"], particiipants[7]["individualPosition"], _["participantFrames"]["8"]["totalGold"], _["participantFrames"]["8"]["currentGold"], _["participantFrames"]["8"]["xp"], _["participantFrames"]["8"]["level"], obj["8"]["DRAGON"], obj["8"]["HORDE"], obj["8"]["RIFTHERALD"], obj["8"]["BARON_NASHOR"]],
                        [x["matchId"], _["timestamp"],x["participants"][8], "200", _["participantFrames"]["9"]["participantId"], particiipants[8]["win"], particiipants[8]["championId"], particiipants[8]["championName"], particiipants[8]["teamPosition"], particiipants[8]["individualPosition"], _["participantFrames"]["9"]["totalGold"], _["participantFrames"]["9"]["currentGold"], _["participantFrames"]["9"]["xp"], _["participantFrames"]["9"]["level"], obj["9"]["DRAGON"], obj["9"]["HORDE"], obj["9"]["RIFTHERALD"], obj["9"]["BARON_NASHOR"]],
                        [x["matchId"], _["timestamp"],x["participants"][9], "200", _["participantFrames"]["10"]["participantId"], particiipants[9]["win"], particiipants[9]["championId"], particiipants[9]["championName"], particiipants[9]["teamPosition"], particiipants[9]["individualPosition"], _["participantFrames"]["10"]["totalGold"], _["participantFrames"]["10"]["currentGold"], _["participantFrames"]["10"]["xp"], _["participantFrames"]["10"]["level"], obj["10"]["DRAGON"], obj["10"]["HORDE"], obj["10"]["RIFTHERALD"], obj["10"]["BARON_NASHOR"]]
                        ])  
        except Exception as e:
            # Print the error message
            print(f"An error occurred: {e}")
            # Print the error type (code)
            print(f"Error type: {type(e).__name__}")
            continue

end_time = time.time()

elapsed_time = end_time - start_time

hours = int(elapsed_time // 3600)
minutes = int((elapsed_time % 3600) // 60)
seconds = elapsed_time % 60

print(f"Elapsed time: {hours} hours, {minutes} minutes, and {seconds:.2f} seconds")
                

# summoner = summoner_info('TW2',TW_ranked_players[0]["summonerId"])
# matches = matches_ID("sea", summoner["puuid"], 1)
# for match in matches:

# x = match_detail_timeline("sea", "TW2_219772755")["metadata"]
# y = match_detail_timeline("sea", "TW2_219772755")["info"]["frames"]
# for _ in y:
#     obj =  {
#             "1" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
#             "2" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
#             "3" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
#             "4" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
#             "5" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
#             "6" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
#             "7" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
#             "8" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
#             "9" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
#             "10" : {"DRAGON" : 0, "HORDE" : 0, "RIFTHERALD" : 0, "BARON_NASHOR" : 0},
#             }
    
#     for z in _["events"]:
#         try:
#             if z["monsterType"]:
#                 obj[f"{z["killerId"]}"][f"{z["monsterType"]}"] += 1
#             a.append([z["monsterType"], z["killerId"]])
#         except:
#             continue

#     print(x["matchId"], _["timestamp"],x["participants"][0] , _["participantFrames"]["1"]["participantId"], _["participantFrames"]["1"]["totalGold"], _["participantFrames"]["1"]["currentGold"], _["participantFrames"]["1"]["xp"], _["participantFrames"]["1"]["level"], obj["1"]["DRAGON"], obj["1"]["HORDE"], obj["1"]["RIFTHERALD"], obj["1"]["BARON_NASHOR"] )    
#     print(x["matchId"], _["timestamp"],x["participants"][1] , _["participantFrames"]["2"]["participantId"], _["participantFrames"]["2"]["totalGold"], _["participantFrames"]["2"]["currentGold"], _["participantFrames"]["2"]["xp"], _["participantFrames"]["2"]["level"], obj["2"]["DRAGON"], obj["2"]["HORDE"], obj["2"]["RIFTHERALD"], obj["2"]["BARON_NASHOR"] )    
#     print(x["matchId"], _["timestamp"],x["participants"][2] , _["participantFrames"]["3"]["participantId"], _["participantFrames"]["3"]["totalGold"], _["participantFrames"]["3"]["currentGold"], _["participantFrames"]["3"]["xp"], _["participantFrames"]["3"]["level"], obj["3"]["DRAGON"], obj["3"]["HORDE"], obj["3"]["RIFTHERALD"], obj["3"]["BARON_NASHOR"])    
#     print(x["matchId"], _["timestamp"],x["participants"][3] , _["participantFrames"]["4"]["participantId"], _["participantFrames"]["4"]["totalGold"], _["participantFrames"]["4"]["currentGold"], _["participantFrames"]["4"]["xp"], _["participantFrames"]["4"]["level"], obj["4"]["DRAGON"], obj["4"]["HORDE"], obj["4"]["RIFTHERALD"], obj["4"]["BARON_NASHOR"] )    
#     print(x["matchId"], _["timestamp"],x["participants"][4] , _["participantFrames"]["5"]["participantId"], _["participantFrames"]["5"]["totalGold"], _["participantFrames"]["5"]["currentGold"], _["participantFrames"]["5"]["xp"], _["participantFrames"]["5"]["level"], obj["5"]["DRAGON"], obj["5"]["HORDE"], obj["5"]["RIFTHERALD"], obj["5"]["BARON_NASHOR"])    
#     print(x["matchId"], _["timestamp"],x["participants"][5] , _["participantFrames"]["6"]["participantId"], _["participantFrames"]["6"]["totalGold"], _["participantFrames"]["6"]["currentGold"], _["participantFrames"]["6"]["xp"], _["participantFrames"]["6"]["level"], obj["6"]["DRAGON"], obj["6"]["HORDE"], obj["6"]["RIFTHERALD"], obj["6"]["BARON_NASHOR"] )    
#     print(x["matchId"], _["timestamp"],x["participants"][6] , _["participantFrames"]["7"]["participantId"], _["participantFrames"]["7"]["totalGold"], _["participantFrames"]["7"]["currentGold"], _["participantFrames"]["7"]["xp"], _["participantFrames"]["7"]["level"], obj["7"]["DRAGON"], obj["7"]["HORDE"], obj["7"]["RIFTHERALD"], obj["7"]["BARON_NASHOR"])    
#     print(x["matchId"], _["timestamp"],x["participants"][7] , _["participantFrames"]["8"]["participantId"], _["participantFrames"]["8"]["totalGold"], _["participantFrames"]["8"]["currentGold"], _["participantFrames"]["8"]["xp"], _["participantFrames"]["8"]["level"], obj["8"]["DRAGON"], obj["8"]["HORDE"], obj["8"]["RIFTHERALD"], obj["8"]["BARON_NASHOR"])    
#     print(x["matchId"], _["timestamp"],x["participants"][8] , _["participantFrames"]["9"]["participantId"], _["participantFrames"]["9"]["totalGold"], _["participantFrames"]["9"]["currentGold"], _["participantFrames"]["9"]["xp"], _["participantFrames"]["9"]["level"], obj["9"]["DRAGON"], obj["9"]["HORDE"], obj["9"]["RIFTHERALD"], obj["9"]["BARON_NASHOR"])    
#     print(x["matchId"], _["timestamp"],x["participants"][9] , _["participantFrames"]["10"]["participantId"], _["participantFrames"]["10"]["totalGold"], _["participantFrames"]["10"]["currentGold"], _["participantFrames"]["10"]["xp"], _["participantFrames"]["10"]["level"], obj["10"]["DRAGON"], obj["10"]["HORDE"], obj["10"]["RIFTHERALD"], obj["10"]["BARON_NASHOR"])    

# csv_file_path = 'LOL_test2_Data.csv'
# with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerow(['matchID', 'puuid', 'win', 'position', 'champion', 'level', 'kills', 'death', 'assists'])
#     for match in matches:
#         y = match_detail_summary("sea", match)["info"]["participants"]
#         x = match_detail_summary("sea", match)["metadata"]["matchId"]
#         for _ in y:
#             writer.writerow([x, _["puuid"], _["win"], _["individualPosition"], _["championName"], _["champLevel"], _["kills"], _["deaths"], _["assists"]])









