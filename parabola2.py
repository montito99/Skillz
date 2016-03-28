def do_turn(game):
	if(len(game.all_my_pirates()) == 1):
		pirate = game.my_pirates()[0]
		if(enemyinrange(game,pirate) and not pirate.has_treasure):
				game.debug(pirate.reload_turns)
				try_attack(game,pirate)
		elif (len(game.enemy_drunk_pirates()) > 0):
			treasure = find_closest_treasure(game,pirate)
			destinations = game.get_sail_options(pirate, treasure, 6)
			game.set_sail(pirate, destinations[0])
		elif (pirate.has_treasure):
			destinations = game.get_sail_options(pirate, pirate.initial_loc, 1)
			found = False
			for i in destinations:
				if not found:
					if (not game.is_occupied(i)):
						game.set_sail(pirate, i)
						found = True
		else:
			destinations = game.get_sail_options(pirate, (15,18), 6)
			game.set_sail(pirate, destinations[0])
	elif(len(game.all_my_pirates()) == 2):
		pirate = game.my_pirates()[0]
		pirate1 = game.my_pirates()[1]
		if(enemyinrange(game,pirate1)):
			game.debug(pirate1.reload_turns)
			try_attack(game,pirate1)
		elif(len(game.enemy_drunk_pirates()) >0):
			treasure = find_closest_treasure(game,pirate)
			destinations = game.get_sail_options(pirate, treasure, 6)
			game.set_sail(pirate, destinations[0])
		elif (pirate.has_treasure):
			destinations = game.get_sail_options(pirate, pirate.initial_loc, 1)
			found = False
			for i in destinations:
				if not found:
					if (not game.is_occupied(i)):
						game.set_sail(pirate, i)
						found = True
	elif(len(game.all_my_pirates()) == 3):
		pirate = game.my_pirates()[2]
		treasure = find_closest_treasure(game, pirate)
		if(pirate.has_treasure):
			destinations = game.get_sail_options(pirate, treasure, 1)
			found = False
			for i in destinations:
				if not found:
					if (not game.is_occupied(i)):
						game.set_sail(pirate, i)
						found = True
		else:
			destinations = game.get_sail_options(pirate, treasure, 6)
			found = False
			for i in destinations:
				if not found:
					if (not game.is_occupied(i)):
						game.set_sail(pirate, i)
						found = True
	elif(len(game.treasures()) == 1) and (len(game.all_my_pirates()) == 4):
		game.debug('lonely')
		pirate = game.my_pirates()[0]
		pirate1 = game.my_pirates()[1]
		location = game.treasures()[0].location
		location = (location[0]|+1,location[1])
		game.debug("%s 0"%enemyinrange(game, pirate))
		game.debug("%s 1"%enemyinrange(game, pirate1))
		if enemyinrange(game, pirate) and game.get_defense_expiration_turns() == 0:
			game.debug("enemy in range")
			try_attack(game, pirate)
		if pirate not in game.my_drunk_pirates():
			destinations = game.get_sail_options(pirate, (2,16), 6)
			game.set_sail(pirate, destinations[0])
		elif pirate in game.my_drunk_pirates():
			destinations = game.get_sail_options(pirate1, (2,16), 6)
			game.set_sail(pirate1, destinations[0])
		if (pirate.has_treasure):
			if game.get_defense_expiration_turns(pirate) == 0:
				game.defend(pirate1)
			destinations = game.get_sail_options(pirate, pirate.initial_loc, 1)
			found = False
			for i in destinations:
				if not found:
					if (not game.is_occupied(i)):
						game.set_sail(pirate, i)
						found = True
		if pirate1.has_treasure:
			destinations = game.get_sail_options(pirate1, pirate1.initial_loc, 1)
			found = False
			for i in destinations:
				if not found:
					if (not game.is_occupied(i)):
						game.set_sail(pirate1, i)
						found = True

		
		
	else:
		cols = game.get_cols()
		middle = cols / 2
		if (game.my_pirates()[0].initial_loc[1] < middle):
			if(game.get_turn() == 1):
				pirate = game.my_pirates()[2]
				treasure = find_closest_treasure(game,pirate)
				destinations = game.get_sail_options(pirate, treasure.location, 3)
				game.set_sail(pirate, destinations[0])
				movePiratestart(game,game.my_pirates()[3])
			else:
				for i in game.my_pirates():
					pirate = i
					if pirate == game.my_pirates()[3]:
						movePirateSmile(game,pirate)
					else:
						treasure = find_closest_treasure(game, pirate)
						do_collect2(game, pirate, treasure)
		else:
			for i in game.my_pirates():
				pirate = i
				if pirate == game.my_pirates()[3]:
					movePirateSmile(game,pirate)
				else:
					treasure = find_closest_treasure(game, pirate)
					do_collect(game, pirate, treasure)
		
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

def do_collect2(game, pirate, treasure):
	if not pirate.has_treasure:
		if pirate == game.my_pirates()[1]:
			if len(game.treasures()) > 0:
				if(game.my_pirates()[0].has_treasure):
					destinations = game.get_sail_options(pirate, treasure.location, 3)
				else:
					destinations = game.get_sail_options(pirate, treasure.location, 1)
		if pirate == game.my_pirates()[0]:
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
	if not pirate.has_treasure:
		for enemy in game.enemy_pirates():
			if (game.in_range(pirate, enemy)):
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
def movePiratestart(game,pirate):
	cols = game.get_cols()
	middle = cols / 2
	if (pirate.initial_loc[1] > middle):
		if(pirate.location == (2, 6)):
			try_attack(game, pirate)
		else:
			destinations = game.get_sail_options(pirate, (2, 6), 3)
			found = False
			for i in destinations:
				if not found:
					if (not game.is_occupied(i)):
						game.set_sail(pirate, i)
						found = True
	elif (pirate.initial_loc[1] < middle):
		if(pirate.location == (4, 25)):
			try_attack(game, pirate)
		else:
			destinations = game.get_sail_options(pirate, (4, 25), 3)
			found = False
			for i in destinations:
				if not found:
					if (not game.is_occupied(i)):
						game.set_sail(pirate, i)
						found = True

def movePirateSmile(game, pirate):
	cols = game.get_cols()
	middle = cols / 2
	if (pirate.initial_loc[1] > middle):
		if(pirate.location == (17,4)):
			game.debug(pirate.reload_turns)
			try_attack(game, pirate)
		else:
			if(enemyinrange(game,pirate)):
				game.debug(pirate.reload_turns)
				try_attack(game,pirate)
			else:
				destinations = game.get_sail_options(pirate, (17,4), 1)
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
	


