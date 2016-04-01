def do_turn(game):
    start_loc(game, game.my_pirates()[0])
    #game.debug(str(start_loc(game, game.my_pirates()[0])))
    game.debug(str(available_pirates(game)))
    if available_pirates(game) == 0:
        pirate = null
    if available_pirates(game) >= 1:
        do_pirate1(game, game.my_pirates()[0])
        game.debug(find_closest_enemy(game, game.my_pirates()[0]))
    if available_pirates(game) >= 2:
        pirate1 = game.my_pirates()[1]
        do_pirate2(game, pirate1)
    if available_pirates(game) >= 3:
        pirate2 = game.my_pirates()[2]
        do_pirate3(game, pirate2)
    if available_pirates(game) >= 4:
        pirate3 = game.my_pirates()[3]
        do_pirate4(game, pirate3)

def pirate_initial_estimated_parallel_loation(game, pirate):
    return (pirate.initial_loc[0], pirate.initial_loc[1] - 20)
    
    

def find_closest_treasure(game, pirate):
    if len(game.treasures()) > 0:
      distances = [ game.distance(pirate, treasure) for treasure in game.treasures() ]
      val, idx = min(((val, idx) for idx, val in enumerate(distances)))
      return game.treasures()[idx]
    else:
      return pirate.initial_loc

def find_closest_enemy(game, pirate):
    if len(game.treasures()) > 0:
      distances = [ game.distance(pirate, enemy) for enemy in game.enemy_pirates() ]
      val, idx = min(((val, idx) for idx, val in enumerate(distances)))
      return game.enemy_pirates()[idx]
    else:
      return pirate.initial_loc

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

def start_loc(game, pirate):
    rows = game.get_rows() - 1
    cols = game.get_cols() - 1
    pirate_loc = pirate.initial_loc
    pirate_row_pos = pirate.initial_loc[0]
    pirate_col_pos = pirate.initial_loc[1]
    game.debug("Pirate initial loc: " + str(pirate_loc))
    game.debug("Pirate row num: " + str(pirate_row_pos))
    game.debug("Pirate cols num: " + str(pirate_col_pos))
    game.debug("Rows: " + str(rows))
    game.debug("Cols: " + str(cols))
    middle = (17, 20)
    top = False
    bottom = False
    right = False
    left = False
    if cols / 2 < pirate_col_pos:
        right = True
        left = False
    if cols / 2 > pirate_col_pos:
        left = True
        right = False
    if rows / 2 < pirate_row_pos:
        bottom = True
        top = False
    if rows / 2 > pirate_row_pos:
        bottom = False
        top = True
    if top and left:
        return 0
    if top and right:
        return 1
    if bottom and left:
        return 2
    if bottom and right:
        return 3
    else:
        return -1
    
def available_pirates(game):
    return len(game.my_pirates()) 

def do_pirate1(game, pirate):
    treasure = find_closest_treasure(game, pirate)
    if not pirate.has_treasure:
        if len(game.treasures()) > 0:
            if len(game.my_pirates()) == 1:
                destinations = game.get_sail_options(pirate, treasure.location, 6)
            else:
                destinations = game.get_sail_options(pirate, treasure.location, 1)
        else:
            destinations = game.get_sail_options(pirate, pirate.initial_loc, 1)
    else:
        destinations = game.get_sail_options(pirate, pirate.initial_loc, 1)
    found = False
    for i in destinations:
        if not found:
            if (not game.is_occupied(i)):
                game.set_sail(pirate, i)
                found = True
                    
def do_pirate2(game, pirate):
    treasure = find_closest_treasure(game, pirate)
    if not pirate.has_treasure:
        if len(game.treasures()) > 0:
            if len(game.my_pirates()) == 2:
                destinations = game.get_sail_options(pirate, treasure.location, 3)
            else:
                destinations = game.get_sail_options(pirate, treasure.location, 1)
        else:
            destinations = game.get_sail_options(pirate, pirate.initial_loc, 1)
    else:
        destinations = game.get_sail_options(pirate, pirate.initial_loc, 1)
    found = False
    for i in destinations:
        if not found:
            if (not game.is_occupied(i)):
                game.set_sail(pirate, i)
                found = True
def do_pirate3(game, pirate):
    treasure = find_closest_treasure(game, pirate)
    if not pirate.has_treasure:
        if len(game.treasures()) > 0:
            if len(game.my_pirates()) == 3:
                destinations = game.get_sail_options(pirate, treasure.location, 2)
            else:
                destinations = game.get_sail_options(pirate, treasure.location, 1)
        else:
            destinations = game.get_sail_options(pirate, pirate.initial_loc, 1)
    else:
        destinations = game.get_sail_options(pirate, pirate.initial_loc, 1)
    found = False
    for i in destinations:
        if not found:
            if (not game.is_occupied(i)):
                game.set_sail(pirate, i)
                found = True
def do_pirate4(game, pirate):
    treasure = find_closest_treasure(game, pirate)
    if not pirate.has_treasure:
        if len(game.treasures()) > 0:
            if len(game.my_pirates()) == 4:
                destinations = game.get_sail_options(pirate, treasure.location, 1)
            else:
                destinations = game.get_sail_options(pirate, treasure.location, 1)
        else:
            destinations = game.get_sail_options(pirate, pirate.initial_loc, 1)
    else:
        destinations = game.get_sail_options(pirate, pirate.initial_loc, 1)
    found = False
    for i in destinations:
        if not found:
            if (not game.is_occupied(i)):
                game.set_sail(pirate, i)
                found = True
    
