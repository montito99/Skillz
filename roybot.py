def do_turn(game):
    start_loc(game, game.my_pirates()[0])
    game.debug(str(start_loc(game, game.my_pirates()[0])))
    game.debug(str(available_pirates(game)))
    

def find_closest_treasure(game, pirate):
    if len(game.treasures()) > 0:
      distances = [ game.distance(pirate, treasure) for treasure in game.treasures() ]
      val, idx = min(((val, idx) for idx, val in enumerate(distances)))
      return game.treasures()[idx]
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
