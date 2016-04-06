def do_turn(game):
    game.debug(game.get_opponent_name())
    global locations
    locations = []
    global moves
    moves = 6
    global previous
    game.debug(moves)
    for pirate in game.my_pirates_with_treasures():
        if enemyinrange(game, pirate) and pirate.defense_reload_turns == 0:
            game.defend(pirate)
        else:
            if pirate.turns_to_sober == 0:
                destinations = game.get_sail_options(pirate, pirate.initial_loc, 1)
                game.debug(len(destinations))
                found = False
                for i in destinations:
                    if not found:
                        if not game.is_occupied(i) and i not in locations:
                            try:
                                if previous is not None:
                                    game.debug('tryworking')
                                    if i != previous:
                                        game.set_sail(pirate, i)
                                        moves = moves-1
                                        locations.append(i)
                                        game.debug(moves)
                                        found = True
                            except NameError:
                                game.set_sail(pirate, i)
                                moves = moves-1
                                locations.append(i)
                                game.debug(moves)
                                found = True
                                game.debug('trynotworking')
                if not found:
                    game.set_sail(pirate, (pirate.location[0]+1,pirate.location[1]))
                    moves = moves-1
                    locations.append((pirate.location[0]+1,pirate.location[1]))
                    previous = (pirate.location[0]+1,pirate.location[1])
                    game.debug(moves)
                    found = True
                else:
                    try:
                        if previous is not None:
                            previous = None
                    except NameError:
                        game.debug('nameerror')
    for pirate in game.my_pirates_without_treasures():
        if enemyinrange(game, pirate) and pirate.reload_turns == 0 :
            try_attack(game, pirate)
        else:
            if moves > 0 and pirate.turns_to_sober == 0:
                if find_closest_treasure(game,pirate).value >= find_most_valueable_treasure(game,pirate).value:
                    treasure = find_closest_treasure(game,pirate)
                else:
                    treasure = find_most_valueable_treasure(game, pirate)
                distance = game.distance(pirate, treasure)
                if distance >= moves:
                    destinations = game.get_sail_options(pirate, treasure, moves)
                    found = False
                    for i in destinations:
                        if not found:
                            if not game.is_occupied(i) and i not in locations:
                                game.set_sail(pirate, i)
                                moves = moves - moves
                                locations.append(i)
                                game.debug(moves)
                                found = True
                else:
                    if pirate.turns_to_sober == 0:
                        destinations = game.get_sail_options(pirate, treasure, distance)
                        found = False
                        for i in destinations:
                            if not found:
                                if not game.is_occupied(i) and i not in locations:
                                    game.set_sail(pirate, i)
                                    moves = moves - distance
                                    locations.append(i)
                                    game.debug(moves)
                                    found = True
    game.debug(locations)
    game.debug(moves)
    
def find_closest_treasure(game, pirate):
    if len(game.treasures()) > 0:
      distances = [ game.distance(pirate, treasure) for treasure in game.treasures() ]
      val, idx = min(((val, idx) for idx, val in enumerate(distances)))
      return game.treasures()[idx]
    else:
      return pirate.initial_loc

def find_most_valueable_treasure(game, pirate):
    if len(game.treasures()) > 0:
        for treasure in game.treasures():
            try:
                best
            except NameError:
                best = treasure
            if treasure.value > best.value:
                best = treasure
        return best
    
def try_attack(game, pirate):
    if not pirate.has_treasure:
        for enemy in game.enemy_pirates():
            if (game.in_range(pirate, enemy)):
                game.attack(pirate, enemy)
                return True
    return False

def enemyinrange(game, pirate):
        for enemy in game.enemy_pirates():
            if (game.in_range(pirate, enemy)):
                return True
        return False
