from math import ceil as up
def do_turn(game):
	enemies = game.enemy_pirates_with_treasures()
	game.debug(game.get_opponent_name())
	moves_made = 0
	my_pirates = game.my_pirates()
	pirates_with_treasure = game.my_pirates_with_treasures()
	global pirates_to_move
	global bla
	global pirates_attackers
	global Pattack
	Pattack = False
	try:
		pirates_attackers
	except NameError:
		pirates_attackers = []
	try:
		pirates_to_move = my_pirates[:len(pirates_with_treasure)+len(game.my_drunk_pirates())+1]
	except Exception as e:
		if e is NameError:
			pirates_to_move = [my_pirates[0]]
		elif e is IndexError:
			pirates_to_move = my_pirates
	try:
		bla += 1
	except NameError:
		game.stop_point("Now stop... Hammer time!")
		for pirate in game.all_my_pirates():
			if enemy_attacker_inrange(game, pirate):
				game.defend(pirate)
				if pirate in pirates_to_move:
					pirates_to_move.pop(pirates_to_move.index(pirate))
				
			bla = 1
	game.debug("turn num: %d"%bla)
	active_pirates = [pirate for pirate in pirates_to_move if pirate in game.my_sober_pirates() and not pirate.has_treasure]
	
	pirates_to_move = pirates_with_treasure + active_pirates
	game.debug(pirates_to_move)
	for pirate in pirates_to_move:
		pirate_index = 1
		if pirate in game.my_sober_pirates():
			enemy = closest_enemy_with_treasure(game, pirate)
			if enemy:
				game.debug("closest_enemy_with_treasure to pirate%d: %s" % (pirate.id, str(enemy)))
			game.debug("%d moves_made" % moves_made)
			if enemy_attacker_inrange(game, pirate) and pirate.defense_reload_turns == 0:
				game.defend(pirate)
			elif enemy_attacker_inrange(game, pirate) and pirate.defense_reload_turns != 0 and pirate.reload_turns == 0 and not pirate.has_treasure:
				do_attack(game, pirate, enemies)
			elif pirate in pirates_with_treasure:
				if move_pirate(game, pirate, pirate.initial_loc, pirate.carry_treasure_speed):
					moves_made += pirate.carry_treasure_speed
			elif pirate in active_pirates and moves_made < 6:
				moves_to_make = int((6-moves_made)/len(active_pirates)) if pirate_index < 6 else (6-moves_made)
				treasure = find_closest_treasure(game, pirate)
				if move_pirate(game, pirate, treasure, moves_to_make):
					moves_made += moves_to_make
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
			game.debug("defending pirate%d from: %s"%(pirate.id,str(enemy))) 
			return True
		return False

def closest_enemy_with_treasure(game, pirate):
	distances = [ game.distance(pirate, enemy) for enemy in game.enemy_pirates_with_treasures() ]
	if len(distances) > 0:
		val, idx = min(((val, idx) for idx, val in enumerate(distances)))
		return game.enemy_pirates()[idx]
	return False
	
def move_pirate(game, pirate, destination, moves):
	destinations = game.get_sail_options(pirate, destination, moves)
	for dest in destinations:
		if not game.is_occupied(dest):
			game.set_sail(pirate, dest)
			return True
	return False
	
def do_attack(game, pirate, enemies):
	#enemies = game.enemy_pirates_with_treasures()
    if pirate.treasure_value > 0: continue
    for enemy in enemies:
		if game.in_range(pirate, enemy):
			game.attack(pirate, enemy)
        else:
            destinations = game.get_sail_options(pirate, enemy, game.actions_per_turn - actions)
            game.set_sail(pirate, destinations[0])
			actions += min(game.actions_per_turn - actions, game.distance(pirate, destinations[0]))
            break
	
	"""
def can_attack(game, pirate, enemy, steps):
	turns_to_enemy_home = up(game.distance(enemy, enemy.initial_loc) / enemy.carry_treasure_speed)
	turns_to_enemy = up(game.distance(pirate, enemy) / pirate.steps)
	return turns_to_enemy_home < turn_to_enemy - pirate.attack_radius


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
