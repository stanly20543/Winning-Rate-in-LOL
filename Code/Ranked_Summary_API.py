import requests
import csv
import time
import os

# Access environment variable
import os

api_key = os.getenv('RIOT_API_KEY')

# print(api_key)


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

# matches = matches_ID("asia", "feUPOIOiVAEcEBK_43YySQ8nGISdp7o3RdWkS4KeHwsc5-FvBA2W6La29nvYEY-aASostChoNe2ICA", 20)
# match_detail_timeline("asia", matches[0])

TW_ranked_players = tier_player_info("TW2", "RANKED_SOLO_5x5", "MASTER", "I", 1)


KR_ranked_players = tier_player_info("KR", "RANKED_SOLO_5x5", "MASTER", "I", 1)

csv_file_path = 'Ranked_test'
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['matchID', 'puuid', 'win', 'team', 'teamposition', 'individualposition', 'championid', 'champion', 'level', 'kills', 'death', 'assists', 'goldEarned', 'TeamDragons', 'TeamHordes', 'TeamRiftHerald', 'baron'])
    for _ in TW_ranked_players[:50]:
        summonerId = _["summonerId"]
        summonerpuuid = summoner_info("TW2", summonerId)["puuid"]
        matches = matches_ID("sea", summonerpuuid, 50)
        number = TW_ranked_players.index(_)
        print(f"TW_Player:{number+1}", "/", len(TW_ranked_players[:50]), summonerpuuid)
        print("Total Matches:", len(matches))
        i = 1

        for match in matches:
            m_info = match_detail_summary("sea", match)["info"]
            teams = m_info["teams"]
            particiipants = m_info["participants"]
            print("Match: ", i, match)
            i += 1

            for _ in particiipants:
                if particiipants.index(_) < 5:
                    writer.writerow([match, _["puuid"], _["teamId"], _["win"], _["teamposition"], _["individualPosition"], _["championId"], _["championName"], _["champLevel"], _["kills"], _["deaths"], _["assists"], _["goldEarned"], teams[0]["objectives"]["dragon"]["kills"], teams[0]["objectives"]["horde"]["kills"], teams[0]["objectives"]["riftHerald"]["kills"], teams[0]["objectives"]["baron"]["kills"]])
                else:
                    writer.writerow([match, _["puuid"], _["teamId"], _["win"], _["teamposition"], _["individualPosition"], _["championId"], _["championName"], _["champLevel"], _["kills"], _["deaths"], _["assists"], _["goldEarned"], teams[1]["objectives"]["dragon"]["kills"], teams[1]["objectives"]["horde"]["kills"], teams[1]["objectives"]["riftHerald"]["kills"], teams[0]["objectives"]["baron"]["kills"]])

    for _ in KR_ranked_players[:50]:
        summonerId = _["summonerId"]
        summonerpuuid = summoner_info("KR", summonerId)["puuid"]
        matches = matches_ID("asia", summonerpuuid, 50)
        number = KR_ranked_players.index(_)
        print(f"KR_Player:{number+1}", "/", len(KR_ranked_players[:50]), summonerpuuid)
        print("Total Matches:", len(matches))
        i = 1

        for match in matches:
            m_info = match_detail_summary("asia", match)["info"]
            teams = m_info["teams"]
            particiipants = m_info["participants"]
            print("Match: ", i, match)
            i += 1

            for _ in particiipants:
                if particiipants.index(_) < 5:
                    writer.writerow([match, _["puuid"], _["teamId"], _["win"], _["teamposition"], _["individualPosition"], ["championId"], _["championName"], _["champLevel"], _["kills"], _["deaths"], _["assists"], _["goldEarned"], teams[0]["objectives"]["dragon"]["kills"], teams[0]["objectives"]["horde"]["kills"], teams[0]["objectives"]["riftHerald"]["kills"], teams[0]["objectives"]["baron"]["kills"]])
                else:
                    writer.writerow([match, _["puuid"], _["teamId"], _["win"], _["teamposition"], _["individualPosition"], ["championId"], _["championName"], _["champLevel"], _["kills"], _["deaths"], _["assists"], _["goldEarned"], teams[1]["objectives"]["dragon"]["kills"], teams[1]["objectives"]["horde"]["kills"], teams[1]["objectives"]["riftHerald"]["kills"], teams[0]["objectives"]["baron"]["kills"]])


# for match in matches:
#     print("\n")
#     y = match_detail_summary("sea", match)["info"]["participants"]
#     print("matchID: ",match_detail_summary("sea", match)["metadata"]["matchId"])
#     x = match_detail_summary("sea", match)["metadata"]["matchId"]
#     for _ in y:
#         print(x, _["puuid"], _["win"], _["individualPosition"], _["championName"], _["champLevel"], _["kills"], _["deaths"], _["assists"])
       

# csv_file_path = 'LOL_test2_Data.csv'
# with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerow(['matchID', 'puuid', 'win', 'position', 'champion', 'level', 'kills', 'death', 'assists'])
#     for match in matches:
#         y = match_detail_summary("sea", match)["info"]["participants"]
#         x = match_detail_summary("sea", match)["metadata"]["matchId"]
#         for _ in y:
#             writer.writerow([x, _["puuid"], _["win"], _["individualPosition"], _["championName"], _["champLevel"], _["kills"], _["deaths"], _["assists"]])









