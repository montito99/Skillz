def do_turn(game):
	moves_made = 0
	my_pirates = game.my_pirates()
	pirates_with_treasure = game.my_pirates_with_treasures()
	global pirates_to_move
	global bla
	try:
		pirates_to_move = my_pirates[:len(pirates_with_treasure)+1]
	except Exception as e:
		if e is NameError:
			pirates_to_move = [my_pirates[0]]
		elif e is IndexError:
			pirates_to_move = my_pirates
	try:
		bla += 1
	except NameError:
		bla = 1
	game.debug("turn num: %d"%bla)
	active_pirates = [pirate for pirate in pirates_to_move if pirate in game.my_sober_pirates() and not pirate.has_treasure]
	
	game.debug(pirates_to_move)
	pirates_to_move = pirates_with_treasure + active_pirates
	for pirate in pirates_to_move:
		game.debug("%d moves_made" % moves_made)
		game.debug(moves_made)
		if enemy_attacker_inrange(game, pirate) and pirate.defense_reload_turns == 0:
			game.defend(pirate)
		elif pirate in pirates_with_treasure:
			dest_to_home = game.get_sail_options(pirate, pirate.initial_loc, pirate.carry_treasure_speed)[0]
			moves_made += pirate.carry_treasure_speed
			game.set_sail(pirate, dest_to_home)
		elif pirate in active_pirates and moves_made < 6:
			treasure = game.get_sail_options(pirate, find_closest_treasure(game, pirate), int((6-moves_made)/len(active_pirates)))[0]
			moves_made += int((6-moves_made)/len(active_pirates))
			
			game.set_sail(pirate, treasure)
	game.debug("%d moves_made in the end" % moves_made)
	
def find_closest_treasure(game, pirate):
	if len(game.treasures()) > 0:
		distances = [ game.distance(pirate, treasure) for treasure in game.treasures() ]
		val, idx = min(((val, idx) for idx, val in enumerate(distances)))
		return game.treasures()[idx]
	else:
		return pirate.initial_loc
	

def enemy_attacker_inrange(game, pirate):
	for enemy in [x for x in game.enemy_pirates_without_treasures() if x in game.enemy_sober_pirates()]:
		if game.in_range(pirate, enemy):
			return True
		return False

	"""

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

"""