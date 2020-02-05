def do_turn(game):
    game.debug(game.get_opponent_name())
    global locations
    locations = []
    global moves
    moves = 6
    game.debug(moves)
    pirate = game.my_pirates()[0]
    global treasure
    treasure = False
    
    if pirate in game.my_pirates_without_treasures() and pirate.location!=(10,10):
	destinations = game.get_sail_options(pirate, (10,10), 6)
	found= False
	for i in destinations:
            if not found:
                if not game.is_occupied(i) and i not in locations:
                    game.set_sail(pirate, i)
                    moves = moves-1
                    locations.append(i)
                    game.debug(moves)
                    found = True
                    
    else:
        treasure = True
	destinations = game.get_sail_options(pirate, pirate.initial_loc, 1)
	found1= False
	found2 = False
	for i in destinations:
            if enemyinrange(game, pirate) and pirate.defense_reload_turns == 0:
                game.defend(pirate)
                pirate2 = game.my_pirates()[1]
                destinations = game.get_sail_options(pirate2, game.enemy_pirates()[0].location , 6)
                if not found:
                if not game.is_occupied(i) and i not in locations:
                    game.set_sail(pirate, i)
                    moves = moves-1
                    locations.append(i)
                    game.debug(moves)
                    found = True
                break
            if not found:
                if not game.is_occupied(i) and i not in locations:
                    game.set_sail(pirate, i)
                    moves = moves-1
                    locations.append(i)
                    game.debug(moves)
                    found = True
	
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
