import re
from collections import defaultdict

meios_de_morte = {
    "MOD_UNKNOWN": "Unknown",
    "MOD_SHOTGUN": "Shotgun",
    "MOD_GAUNTLET": "Gauntlet",
    "MOD_MACHINEGUN": "Machinegun",
    "MOD_GRENADE": "Grenade",
    "MOD_GRENADE_SPLASH": "Grenade Splash",
    "MOD_ROCKET": "Rocket",
    "MOD_ROCKET_SPLASH": "Rocket Splash",
    "MOD_PLASMA": "Plasma",
    "MOD_PLASMA_SPLASH": "Plasma Splash",
    "MOD_RAILGUN": "Railgun",
    "MOD_LIGHTNING": "Lightning",
    "MOD_BFG": "BFG",
    "MOD_BFG_SPLASH": "BFG Splash",
    "MOD_WATER": "Water",
    "MOD_SLIME": "Slime",
    "MOD_LAVA": "Lava",
    "MOD_CRUSH": "Crush",
    "MOD_TELEFRAG": "Telefrag",
    "MOD_FALLING": "Falling",
    "MOD_SUICIDE": "Suicide",
    "MOD_TARGET_LASER": "Target Laser",
    "MOD_TRIGGER_HURT": "Trigger Hurt",
    "MOD_CHAINGUN": "Chaingun",
    "MOD_PROXIMITY_MINE": "Proximity Mine",
    "MOD_KAMIKAZE": "Kamikaze",
    "MOD_JUICED": "Juiced",
    "MOD_GRAPPLE": "Grapple"
}

def parse_log_file(file_path):
    games = {}
    current_game = None
    kills = defaultdict(int)
    kills_by_means = defaultdict(int)

    with open(file_path, 'r') as file:
        for line in file:
            if 'InitGame' in line:
                if current_game:
                    games[current_game]["kills_by_means"] = dict(kills_by_means)
                game_id = line.split(':')[0].strip()
                games[game_id] = {"total_kills": 0, "players": set(), "kills": {}, "kills_by_means": {}}
                current_game = game_id
                kills = defaultdict(int)
                kills_by_means = defaultdict(int)
            elif 'Kill' in line:
                parts = re.split(r'\s+(killed|by)\s+', line)
                if len(parts) >= 4:
                    killer = parts[0].strip()
                    victim = parts[2].strip()
                    cause_of_death = parts[3].strip().split(',')[0].strip()
                    if cause_of_death != '<world>':
                        kills_by_means[meios_de_morte.get(cause_of_death, "Unknown")] += 1
                    games[current_game]["total_kills"] += 1
                    games[current_game]["players"].update([killer, victim])
                    if killer != '<world>':
                        games[current_game]["kills"][killer] = games[current_game]["kills"].get(killer, 0) + 1
    return games

def extract_game_number(game_id):
    parts = game_id.split('_')
    if len(parts) >= 2:
        return int(parts[1])
    else:
        return -1


def print_game_reports(games):
    sorted_games = sorted(games.items(), key=lambda x: extract_game_number(x[0]))
    for game_id, game_data in sorted_games:
        print(f'"{game_id}" : {{')
        print(f'   "total_kills" : {game_data["total_kills"]},')
        print(f'   "players" : {list(game_data["players"])},')
        print('   "kills" : {')
        for player, kills in game_data["kills"].items():
            print(f'       "{player}" : {kills},')
        print('   },')
        print('   "kills_by_means" : {')
        for mean, count in game_data["kills_by_means"].items():
            print(f'       "{mean}" : {count},')
        print('   }')
        print('}')


if __name__ == "__main__":
    log_file_path = "qgames.log"
    games = parse_log_file(log_file_path)
    print_game_reports(games)
