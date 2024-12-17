import requests
from ..config import HENRIK_TOKEN

def get_account_data(name, tag):
    response = requests.get(
        f"https://api.henrikdev.xyz/valorant/v2/account/{name}/{tag}",
        headers={"Authorization": HENRIK_TOKEN},
    )
    if response.status_code != 200:
        raise Exception("Could not find player")
    return response.json()['data']

def get_mmr_data(puuid):
    response = requests.get(
        f"https://api.henrikdev.xyz/valorant/v2/by-puuid/mmr/eu/{puuid}",
        headers={"Authorization": HENRIK_TOKEN},
    )
    if response.status_code != 200:
        return None
    return response.json()['data']

def get_matches_data(puuid):
    response = requests.get(
        f"https://api.henrikdev.xyz/valorant/v4/by-puuid/matches/eu/pc/{puuid}",
        headers={"Authorization": HENRIK_TOKEN},
    )
    if response.status_code != 200:
        return None
    return response.json()['data']

def get_mmr_history(puuid):
    response = requests.get(
        f"https://api.henrikdev.xyz/valorant/v2/by-puuid/mmr-history/eu/pc/{puuid}",
        headers={"Authorization": HENRIK_TOKEN},
    )
    if response.status_code != 200:
        return None
    return response.json()['data']

def process_matches_data(matches_data, puuid):
    processed_matches = []
    for match in matches_data[:5]:
        for player in match['players']:
            if player['puuid'] == puuid:
                map_name = match['metadata']['map']['name']
                gamemode = match['metadata']['queue']['name']
                
                blue_score = sum(1 for round_data in match.get('rounds', []) if round_data.get('winning_team') == 'Blue')
                red_score = sum(1 for round_data in match.get('rounds', []) if round_data.get('winning_team') == 'Red')
                
                team = player['team_id']
                if team == 'Blue':
                    score_display = f"{blue_score}-{red_score}"
                else:
                    score_display = f"{red_score}-{blue_score}"
                
                processed_matches.append({
                    'map': map_name,
                    'gamemode': gamemode,
                    'agent': player['agent']['name'],
                    'score': score_display,
                    'kills': player['stats']['kills'],
                    'deaths': player['stats']['deaths'],
                    'assists': player['stats'].get('assists', 0),
                    'team': player['team_id'],
                    'match_id': match['metadata']['match_id'],
                    'headshots': player['stats'].get('headshots', 0),
                    'bodyshots': player['stats'].get('bodyshots', 0),
                    'legshots': player['stats'].get('legshots', 0)
                })
    return processed_matches

def calculate_match_stats(matches_data):
    total_kills = sum(match['kills'] for match in matches_data)
    total_deaths = sum(match['deaths'] for match in matches_data)
    total_headshots = sum(match.get('headshots', 0) for match in matches_data)
    total_bodyshots = sum(match.get('bodyshots', 0) for match in matches_data)
    total_legshots = sum(match.get('legshots', 0) for match in matches_data)
    
    kd_ratio = round(total_kills / max(total_deaths, 1), 2)
    total_shots = total_headshots + total_bodyshots + total_legshots
    
    shot_percentages = {
        'hs_percentage': round((total_headshots / max(total_shots, 1)) * 100, 1),
        'body_percentage': round((total_bodyshots / max(total_shots, 1)) * 100, 1),
        'leg_percentage': round((total_legshots / max(total_shots, 1)) * 100, 1)
    }
    
    return kd_ratio, shot_percentages