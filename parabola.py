def do_turn(game):
	moves_made = 0
	global bla
	try:
		bla
	except NameError:
		bla=1
	bla+=1
	game.debug(bla)
	my_pirates = game.my_pirates()
	pirates_with_treasures = game.my_pirates_with_treasures()
	for pirate in pirates_with_treasures:
		dest = game.get_sail_options(pirate, pirate.initial_loc, 1)
		moves_made += 1
		game.set_sail(pirate, dest[0])
	game.debug(pirates_with_treasures)
	game.debug(my_pirates[len(pirates_with_treasures)])
	treasure = find_closest_treasure(game, my_pirates[len(pirates_with_treasures)])
	game.debug(treasure)
	dest = game.get_sail_options(my_pirates[len(pirates_with_treasures)], treasure, 6-moves_made)
	game.set_sail(my_pirates[len(pirates_with_treasures)], dest[0])
def find_closest_treasure(game, pirate):
	if len(game.treasures()) > 0:
		distances = [ game.distance(pirate, treasure) for treasure in game.treasures() ]
		val, idx = min(((val, idx) for idx, val in enumerate(distances)))
		return game.treasures()[idx]
	else:
		return pirate.initial_loc
	
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