import math

def do_turn_tzi(game):
	my_pirates = game.my_pirates_without_treasures()
	my_pirates.reverse()
	game.debug(game.get_opponent_name())
	global locations
	locations = []
	global moves
	moves = 6
	game.debug(moves)
	for pirate in game.my_pirates_with_treasures():
		if enemyinrange_tzi(game, pirate) and pirate.defense_reload_turns == 0:
			game.defend(pirate)
		else:
			if pirate.turns_to_sober == 0:
				destinations = game.get_sail_options(pirate, pirate.initial_loc, 1)
				found = False
				for i in destinations:
					if not found:
						if not game.is_occupied(i) and i not in locations:
							game.set_sail(pirate, i)
							moves = moves-1
							locations.append(i)
							game.debug(moves)
							found = True
	for pirate in my_pirates:
		if enemyinrange_tzi(game, pirate) and pirate.reload_turns == 0 :
			try_attack_tzi(game, pirate)
		else:
			if moves > 0 and pirate.turns_to_sober == 0:
				treasure = find_closest_treasure_tzi(game, pirate)
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
	game.debug(moves)

def do_turn(game):
	if str(game.get_opponent_name()) == '23':
		do_turn_tzi(game)
	elif str(game.get_opponent_name()) == '25':
		pirate = game.my_pirates()[0]
		pirate1 = game.my_pirates()[1]
		pirate0_acted = False
		pirate1_acted = False
		moves = 6
		treasure = game.treasures()[6]
		if enemy_attacker_inrange(game, pirate) and pirate.defense_reload_turns == 0:
			game.defend(pirate)
			pirate0_acted = True
			game.debug("reload for pirate%d: %d"%(pirate.id,pirate.reload_turns))

		if pirate1.location != (2,11):
			destinations = game.get_sail_options(pirate1, (2,11), 2)
			for i in destinations:
				if not game.is_occupied(i):
					game.set_sail(pirate1, i)
					moves -= 2
					pirate1_acted = True
					break
		if enemyinrange_tzi(game, pirate1) and pirate1.reload_turns == 0 and not pirate1_acted:
			try_attack_tzi(game, pirate1)
			pirate1_acted = True
		if pirate.has_treasure and not pirate0_acted:
			destinations = game.get_sail_options(pirate, pirate.initial_loc, 1)
			for i in destinations:
				if not game.is_occupied(i):
					game.set_sail(pirate, i)
					moves -= 1
					break
		elif not pirate.has_treasure and not pirate0_acted:
			destinations = game.get_sail_options(pirate, treasure, moves)
			for i in destinations:
				if not game.is_occupied(i):
					game.set_sail(pirate, i)
					break		

	# elif str(game.get_opponent_name()) == 'demobot6':
	# 	game.debug("bot6")
	# 	dobot6(game)
	elif str(game.get_opponent_name()) == '22':
		game.debug("name: %s"%game.get_opponent_name())
		global moves_made
		moves_made = 0
		my_pirates = game.my_pirates()
		pirates_with_treasure = game.my_pirates_with_treasures()
		global pirates_to_move
		global bla
		global pirates_attackers
		global pirate_is_attacking
		try:
			game.debug(pirate_is_attacking)
		except NameError:
			pirate_is_attacking = {'0':True,'1':True,'2':True,'3':True}
			game.debug(pirate_is_attacking)
		try:
			pirates_attackers
		except NameError:
			pirates_attackers = []
		try:
			pirates_to_move = my_pirates[:len(pirates_with_treasure)+len(game.my_drunk_pirates())+1] if game.get_my_score() < 4 else my_pirates
			pirates_attackers = [pirate for pirate in pirates_to_move if pirate not in pirates_with_treasure and pirate in game.my_sober_pirates() and pirate_is_attacking[str(pirate.id)]]
		except Exception as e:
			if e is NameError:
				pirates_to_move = [my_pirates[0]]
			elif e is IndexError:
				pirates_to_move = my_pirates
		try:
			bla += 1
		except NameError:
			game.stop_point("Now stop... Hammer time!")
			for pirate in game.my_pirates():
				if enemy_attacker_inrange(game, pirate):
					game.defend(pirate)
					if pirate in pirates_to_move:
						pirates_to_move.pop(pirates_to_move.index(pirate))
				bla = 1
		game.debug("Attackers: %s" % str(["pirate%d"%pirate.id for pirate in pirates_attackers]))
		game.debug("turn num: %d"%bla)
		active_pirates = [pirate for pirate in pirates_to_move if pirate in game.my_sober_pirates() and not pirate.has_treasure]
		acted_pirates = []
		
		pirates_to_remove = []
		for pirate_attacker in pirates_attackers:
			enemy = closest_enemy_with_treasure(game, pirate_attacker)
			if enemy:
				game.debug("Active: %d Attackers: %d"%(len(active_pirates),len(pirates_attackers)))
				moves_to_make = int(6-moves_made-len(pirates_with_treasure))/len(active_pirates+pirates_attackers)
				game.debug("moves_to_make: %d" % moves_to_make)
				game.debug("closest_enemy_with_treasure to pirate%d: %s" % (pirate_attacker.id, str(enemy)))
				if not do_attack(game, pirate_attacker, enemy, moves_to_make):
					moves_made += moves_to_make
				else:
					pirates_to_remove.append(pirate_attacker)
			else:
				pirates_to_remove.append(pirate_attacker)
				
		for pirate in pirates_to_remove:
			pirate_is_attacking[str(pirate_attacker.id)] = False
			active_pirates.append(pirate)
			pirates_attackers.pop(pirates_attackers.index(pirate))
			game.debug("attackers: %s"%str(pirates_attackers))

		pirate_index = 0
		pirates_to_move = pirates_with_treasure + active_pirates
		for pirate in pirates_to_move:
			if pirate in game.my_sober_pirates():
				game.debug("%d moves_made" % moves_made)
				if enemy_attacker_inrange(game, pirate) and pirate.defense_reload_turns == 0:
					game.defend(pirate)
					game.debug("reload for pirate%d: %d"%(pirate.id,pirate.reload_turns))
				elif pirate in pirates_with_treasure and moves_made < 6-pirate.carry_treasure_speed:
					dest_to_home = game.get_sail_options(pirate, pirate.initial_loc, pirate.carry_treasure_speed)[0]
					moves_made += pirate.carry_treasure_speed
					game.set_sail(pirate, dest_to_home)
				elif pirate in active_pirates and moves_made < 6:
					moves_to_make = int((6-moves_made)/(len(active_pirates))) if pirate_index < 6 else (6-moves_made)
					treasure = game.get_sail_options(pirate, find_closest_treasure(game, pirate), moves_to_make)[0]
					moves_made += moves_to_make
					
					game.set_sail(pirate, treasure)
		game.debug("%d moves_made in the end" % moves_made)
	else:
		do_turn_matara(game)
def find_closest_treasure(game, pirate):
	if len(game.treasures()) > 0:
		distances = [game.distance(pirate, treasure) for treasure in game.treasures()]
		val, idx = min(((val, idx) for idx, val in enumerate(distances)))
		return game.treasures()[idx]
	else:
		return pirate.initial_loc
	

def enemy_attacker_inrange(game, pirate):
	for enemy in [x for x in game.enemy_pirates_without_treasures() if x in game.enemy_sober_pirates() and x.reload_turns == 0]:
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
	
	
def do_attack(game, pirate, enemy, moves):
	game.debug("moves from do attack: %d" % moves)
	if game.in_range(pirate, enemy):
		if enemy.defense_reload_turns != 60 and pirate.reload_turns == 0:
			game.debug("attacking %s"%enemy)
			game.attack(pirate, enemy)
			return True
	else:
		game.debug("enemy of pirate%d: %s"%(pirate.id,str(enemy)))
		destinations = game.get_sail_options(pirate, enemy, moves)
		game.debug("destinations: %s" % destinations)
		game.set_sail(pirate, destinations[0])
	return False

def closest_enemy(game, pirate):
	distances = [ game.distance(pirate, enemy) for enemy in game.enemy_pirates() ]
	if len(distances) > 0:
		val, idx = min(((val, idx) for idx, val in enumerate(distances)))
		return game.enemy_pirates()[idx]
	return False

def dobot6(game):
	global bal
	pirate0 = game.my_pirates()[0]		
	try:
		bal
	except NameError:
		game.defend(pirate0)
		bal = 1
	game.debug("pirate0.enemy.defense_reload_turns"%str(pirate0.enemy.defense_reload_turns))
	if not pirate0.has_treasure:
		game.debug("looking for treasure")
		treasure = find_closest_treasure(game, pirate0)
		game.debug(treasure)
		dest = game.get_sail_options(pirate0, treasure, 6)
		game.set_sail(pirate, dest[0])
	else:
		dest = game.get_sail_options(pirate0, pirate0.initial_loc, 1)
		game.set_sail(dest[0])
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
					
def find_closest_treasure_tzi(game, pirate):
	if len(game.treasures()) > 0:
	  distances = [ game.distance(pirate, treasure) for treasure in game.treasures() ]
	  val, idx = min(((val, idx) for idx, val in enumerate(distances)))
	  return game.treasures()[idx]
	else:
	  return pirate.initial_loc
	
def try_attack_tzi(game, pirate):
	if not pirate.has_treasure:
		for enemy in game.enemy_pirates():
			if (game.in_range(pirate, enemy)):
				game.attack(pirate, enemy)
				return True
	return False

def enemyinrange_tzi(game, pirate):
		for enemy in game.enemy_pirates():
			if (game.in_range(pirate, enemy)):
				return True
		return False

		
def do_turn_matara(game):
	game.debug(game.get_opponent_name())
	global locations
	locations = []
	global moves
	moves = 6
	global previous
	game.debug(moves)	
	for pirate in game.my_pirates_with_treasures():
		if enemy_attacker_inrange(game, pirate) and pirate.defense_reload_turns == 0:
			game.defend(pirate)
		else:
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
									if pirate.turns_to_sober > 0:
										break
									else:
										game.set_sail(pirate, i)
										moves = moves-1
										locations.append(i)
										game.debug(moves)
										found = True
						except NameError:
							if pirate.turns_to_sober > 0:
								break
							else:
								game.set_sail(pirate, i)
								moves = moves-1
								locations.append(i)
								game.debug(moves)
								found = True
								game.debug('trynotworking')
			else:
				try:
					if previous is not None:
						previous = None
				except NameError:
					game.debug('nameerror')
	for pirate in game.my_pirates_without_treasures():
		if attackbest(game, pirate)==True:
			game.debug("Attacked")
		else:
			if moves > 0 and pirate.turns_to_sober == 0:
				if len(game.treasures())>0: #if there are treasures in the map
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
									if pirate.turns_to_sober > 0:
										break
									else:
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
										if pirate.turns_to_sober > 0:
											break
										else:
											game.set_sail(pirate, i)
											moves = moves - distance
											locations.append(i)
											game.debug(moves)
											found = True
				else: #the map is clear from treasures
					go = find_closest_enemy_initial(game,pirate)[1]
					if pirate.turns_to_sober == 0:
						destinations = game.get_sail_options(pirate, go, 1)
						found = False
						for i in destinations:
							if not found:
								if not game.is_occupied(i) and i not in locations:
									if pirate.turns_to_sober > 0:
										break
									else:
										game.set_sail(pirate, i)
										moves = moves - 1
										locations.append(i)
										game.debug(moves)
										found = True

	game.debug(locations)
	game.debug(moves)

def find_closest_enemy_initial(game,pirate):
	distances = [(game.distance(pirate,enemy.initial_loc), (enemy.initial_loc)) for enemy in game.enemy_pirates() if game.get_pirate_on(enemy.initial_loc) not in game.my_pirates()]
	to_return=distances[0]
	for d in distances:
		d=list(d)
		to_return=list(to_return)
		if d[0]<to_return[0]:
			to_return[0]=d[0]
			to_return[1]=d[1]
	return to_return

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
			
def attackbest(game, pirate):
	if pirate.reload_turns == 0 and pirate.turns_to_sober == 0:
		for enemy in game.enemy_pirates():
			if game.in_range(pirate, enemy) and enemy.has_treasure and enemy.defense_expiration_turns==0:
				game.attack(pirate, enemy)
				return True
		for enemy in game.enemy_pirates():
			if game.in_range(pirate, enemy) and enemy.defense_expiration_turns==0:
				game.attack(pirate, enemy)
				return True
		return False
	else:
		return False
