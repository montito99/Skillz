def do_turn(game):
    try:
        moves
    except NameError:
        global moves = 0
    game.debug(moves)
    
    for pirate in game.my_pirates():
        if pirate.has_treasure and enemyinrange(game.pirate) and pirate.defense_reload_turns == 0:
            game.defend(pirate)
        elif pirate.has_treasure:
            destinations = game.get_sail_options(pirate, pirate.initial_loc, 1)
            found = False
            for i in destinations:
                if not found:
                    if (not game.is_occupied(i)):
                        game.set_sail(pirate, i)
                        moves += 1
                        found = True
        else:
            treasure = find_closest_treasure
            destinations = game.get_sail_options(pirate,treasure.location, 6)
            found = False
            for i in destinations:
                if not found:
                    if (not game.is_occupied(i)):
                        game.set_sail(pirate, i)
                        moves += 6
                        found = True
            
def find_closest_treasure(game, pirate):
    if len(game.treasures()) > 0:
      distances = [ game.distance(pirate, treasure) for treasure in game.treasures() ]
      val, idx = min(((val, idx) for idx, val in enumerate(distances)))
      return game.treasures()[idx]
    else:
      return pirate.initial_loc
def do_collect(game, pirate, treasure):
    if not pirate.has_treasure:
        if pirate == game.my_pirates()[0]:
            if len(game.treasures()) > 0:
                if(game.my_pirates()[1].has_treasure):
                    destinations = game.get_sail_options(pirate, treasure.location, 3)
                else:
                    destinations = game.get_sail_options(pirate, treasure.location, 1)
        if pirate == game.my_pirates()[1]:
            if len(game.treasures()) > 0:
                destinations = game.get_sail_options(pirate, treasure.location, 3)
        elif pirate == game.my_pirates()[2]:
            if(game.my_pirates()[3].location == (4, 25) or game.my_pirates()[3].location == (2, 6)):
                if len(game.treasures()) > 0:
                    destinations = game.get_sail_options(pirate, treasure.location, 2)
            else:
                if len(game.treasures()) > 0:
                    if(game.my_pirates()[0].has_treasure and game.my_pirates()[1].has_treasure):
                        destinations = game.get_sail_options(pirate, treasure.location, 3)
                    else:
                        destinations = game.get_sail_options(pirate, treasure.location, 1)

    else:
        destinations = game.get_sail_options(pirate, pirate.initial_loc, 1)
    if len(game.treasures()) > 0:
        found = False
        for i in destinations:
            if not found:
                if (not game.is_occupied(i)):
                    game.set_sail(pirate, i)
                    found = True
    else:
        destinations = game.get_sail_options(pirate, pirate.initial_loc, 1)
        found = False
        for i in destinations:
            if not found:
                if (not game.is_occupied(i)):
                    game.set_sail(pirate, i)
                    found = True
def try_attack(game, pirate):
    print 'tryattacking1'
    if not pirate.has_treasure:
        for enemy in game.enemy_pirates():
            print 'forhi'
            if (game.in_range(pirate, enemy)):
                print'ifhi'
                game.attack(pirate, enemy)
                return True
    return False
def movePirate3(game, pirate):
    cols = game.get_cols()
    middle = cols / 2
    if (pirate.initial_loc[1] > middle):
        if(pirate.location == (2, 6)):
            game.debug(pirate.reload_turns)
            try_attack(game, pirate)
        else:
            if(enemyinrange(game,pirate)):
                game.debug(pirate.reload_turns)
                try_attack(game,pirate)
            else:
                destinations = game.get_sail_options(pirate, (2, 6), 1)
                found = False
                for i in destinations:
                    if not found:
                        if (not game.is_occupied(i)):
                            game.set_sail(pirate, i)
                            found = True
    elif (pirate.initial_loc[1] < middle):
        if(pirate.location == (4, 25)):
            game.debug(pirate.reload_turns)
            try_attack(game, pirate)
        else:
            if(enemyinrange(game,pirate)):
                game.debug(pirate.reload_turns)
                try_attack(game,pirate)
            else:
                destinations = game.get_sail_options(pirate, (4, 25), 1)
                found = False
                for i in destinations:
                    if not found:
                        if (not game.is_occupied(i)):
                            game.set_sail(pirate, i)
                            found = True
def enemyinrange(game, pirate):
        for enemy in game.enemy_pirates():
            print 'forhi'
            if (game.in_range(pirate, enemy)):
                return True
        return False

