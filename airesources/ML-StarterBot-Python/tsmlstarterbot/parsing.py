import numpy as np

from tsmlstarterbot.common import *


def angle(x, y):
    radians = math.atan2(y, x)
    if radians < 0:
        radians = radians + 2 * math.pi
    return round(radians / math.pi * 180)


def find_winner(data):
    for player, stats in data['stats'].items():
        if stats['rank'] == 1:
            return player
    return -1


def angle_dist(a1, a2):
    return (a1 - a2 + 360) % 360


def find_target_planet(bot_id, current_frame, planets, move):
    """
    Find a planet to which the ship try to made a move to. We infer it by looking at the angle that the ship moved
    with and the angle between the ship and the planet.
    :param bot_id: id of our bot
    :param current_frame: current frame
    :param planets: planets data
    :param move: current move to analyze
    :return: id of the planet that ship was moving towards
    """

    if move['type'] == 'dock':
        # If the move was to dock, we know the planet we wanted to move towards
        return move['planet_id']
    if move['type'] != 'thrust':
        # If the move was not "thrust" (i.e. it was "undock"), we cannot find the planet
        return -1

    ship_angle = move['angle']
    ship_data = current_frame['ships'][bot_id][str(move['shipId'])]
    ship_x = ship_data['x']
    ship_y = ship_data['y']

    optimal_planet = -1
    optimal_angle = -1
    for planet_data in planets:
        planet_id = str(planet_data['id'])
        if planet_id not in current_frame['planets'] or current_frame['planets'][planet_id]['health'] <= 0:
            continue

        planet_x = planet_data['x']
        planet_y = planet_data['y']
        a = angle(planet_x - ship_x, planet_y - ship_y)
        if optimal_planet == -1 or angle_dist(ship_angle, a) < angle_dist(ship_angle, optimal_angle):
            optimal_planet = planet_id
            optimal_angle = a

    return optimal_planet


def format_data_for_training(data):
    """
    Convert from parsed data to numpy arrays ready to feed to network.
    """
    training_input = []
    training_output = []
    for d in data:
        features, expected_output = d

        if len(expected_output.values()) == 0:
            continue

        features_matrix = []
        for planet_id in range(PLANET_MAX_NUM):
            if str(planet_id) in features:
                features_matrix.append(features[str(planet_id)])
            else:
                features_matrix.append([0] * PER_PLANET_FEATURES)

        fm = np.array(features_matrix)

        output = [0] * PLANET_MAX_NUM
        for planet_id, p in expected_output.items():
            output[int(planet_id)] = p
        result = np.array(output)

        training_input.append(fm)
        training_output.append(result)

    return np.array(training_input), np.array(training_output)


def parse(all_games_json_data, bot_to_imitate=None):
    print("Parsing data...")

    parsed_games = 0

    training_data = []

    if bot_to_imitate is None:
        print("No bot name provided, choosing the bot with the highest number of games won...")
        players_games_count = {}
        for json_data in all_games_json_data:
            w = find_winner(json_data)
            p = json_data['player_names'][int(w)]
            if p not in players_games_count:
                players_games_count[p] = 0
            players_games_count[p] += 1

        bot_to_imitate = max(players_games_count, key=players_games_count.get)
    print("Bot to imitate: {}".format(bot_to_imitate))

    for json_data in all_games_json_data:

        frames = json_data['frames']
        moves = json_data['moves']
        width = json_data['width']
        height = json_data['height']

        max_rounds = max_number_of_rounds(width, height)

        # For each game see if bot_to_imitate played in it
        if bot_to_imitate not in set(json_data['player_names']):
            continue
        # We train on all the games of the bot regardless if it won or not.
        bot_to_imitate_id = str(json_data['player_names'].index(bot_to_imitate))

        parsed_games = parsed_games + 1
        # Ignore the last frame, no decision to be made there
        for idx in range(len(frames) - 1):
            current_moves = moves[idx]
            current_frame = frames[idx]

            if bot_to_imitate_id not in current_frame['ships'] or len(current_frame['ships'][bot_to_imitate_id]) == 0:
                continue

            planet_features = {}  # planet_id -> list of features per ship per planet
            current_planets = current_frame['planets']

            # find % allocation for all ships
            all_moving_ships = 0
            allocations = {}

            # for each planet we want to find how many ships are being moved towards it now
            for ship_id, ship_data in current_frame['ships'][bot_to_imitate_id].items():
                if ship_id in current_moves[bot_to_imitate_id][0]:
                    p = find_target_planet(bot_to_imitate_id, current_frame,
                                           json_data['planets'],
                                           current_moves[bot_to_imitate_id][0][ship_id],
                                           )
                    planet_id = int(p)
                    if planet_id < 0 or planet_id >= PLANET_MAX_NUM:
                        continue

                    if p not in allocations:
                        allocations[p] = 0
                    allocations[p] = allocations[p] + 1
                    all_moving_ships = all_moving_ships + 1

            if all_moving_ships == 0:
                continue

            # compute what % of the ships should be sent to given planet
            for planet_id, allocated_ships in allocations.items():
                allocations[planet_id] = allocated_ships / all_moving_ships

            # Compute features
            for planet_id in range(PLANET_MAX_NUM):

                if str(planet_id) not in current_planets:
                    continue
                planet_data = current_planets[str(planet_id)]

                gravity = 0
                planet_base_data = json_data['planets'][planet_id]
                winner_minimal_distance = 10000
                enemy_minimal_distance = 10000

                owned_by_winner = 1 if planet_data['owner'] == bot_to_imitate_id else -1
                owner_id = 0
                if planet_data['owner'] == bot_to_imitate_id:
                    owner_id = 1
                elif planet_data['owner'] is not None:
                    owner_id = -1

                point_in_time = idx / max_rounds

                average_distance = 0
                my_ships_health = 0

                for player_id, ships in current_frame['ships'].items():
                    for ship_id, ship_data in ships.items():
                        is_winner = 1 if player_id == bot_to_imitate_id else -1
                        dist2 = distance2(planet_base_data['x'], planet_base_data['y'], ship_data['x'], ship_data['y'])
                        dist = math.sqrt(dist2)
                        gravity = gravity + is_winner * ship_data['health'] / dist2
                        if is_winner == 1:
                            winner_minimal_distance = min(winner_minimal_distance, dist)
                            average_distance = average_distance + dist * ship_data['health']
                            my_ships_health = my_ships_health + ship_data['health']
                        else:
                            enemy_minimal_distance = min(enemy_minimal_distance, dist)

                distance_from_center = distance(planet_base_data['x'], planet_base_data['y'], width / 2, height / 2)
                average_distance = average_distance / my_ships_health

                is_active = 1.0 if planet_base_data['docking_spots'] > len(
                    planet_data['docked_ships']) or owner_id != 1 else 0.0

                planet_features[str(planet_id)] = [
                    planet_data['health'],
                    planet_base_data['docking_spots'] - len(planet_data['docked_ships']),
                    planet_data['remaining_production'],
                    planet_data['current_production'] * owned_by_winner,
                    gravity,
                    winner_minimal_distance,
                    enemy_minimal_distance,
                    owner_id,
                    point_in_time,
                    distance_from_center,
                    average_distance,
                    is_active]

            training_data.append((planet_features, allocations))

    if parsed_games == 0:
        raise Exception("Didn't find any matching games. a Try different bot.")

    print("Data parsed, parsed {} games, total frames: {}".format(parsed_games, len(training_data)))

    return format_data_for_training(training_data)
