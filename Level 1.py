import math

def do_turn(game):
	game.debug(game.get_opponent_name())
	global locations
	locations = []
	global moves
	moves = 6

	for pirate in game.my_pirates_with_treasures(): #the pirates with treasures
		if enemy_attacker_inrange(game, pirate) and pirate.defense_reload_turns == 0: #if pirate need to defense
			game.defend(pirate)
			continue
		elif moves>0:
			destinations = game.get_sail_options(pirate, pirate.initial_loc, 1)
			game.debug(len(destinations))
			found = False
			for i in destinations:
				if not found:
					if not game.is_occupied(i) and i not in locations:
						try:
							if pirate.turns_to_sober > 0:
								break
							elif moves>0:
								game.set_sail(pirate, i)
								game.debug("line26: pirate%d about to make 1 moves"%pirate.id)
								moves = moves-1
								game.debug("moves in line204: %d"%moves)
								locations.append(i)
								found = True
						except NameError as e:
							if pirate.turns_to_sober > 0:
								break
							elif moves>0:
								game.set_sail(pirate, i)
								moves = moves-1
								locations.append(i)
								found = True
								game.debug(e)
	for pirate in game.my_pirates_without_treasures():
		if attackbest(game, pirate)==True:
			game.debug("Pirate%d Attacked"%pirate.id)
			continue
		result = kamikaza(game,pirate,moves)
		game.debug("result: %s"%str(result))
		if type(result) is int:
			game.debug("hello from line47")
			game.debug("Pirate %d did Kamikaza"%pirate.id)
			moves=result
			continue
		else:
			game.debug("line51: Pirate %d"%pirate.id)
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
									elif moves > 0:
										game.debug("line66: pirate%d about to make %d moves"%(pirate.id, moves))
										game.set_sail(pirate, i)
										moves = 0

										locations.append(i)
										found = True
						if found:
							continue
					else:
						if pirate in game.my_sober_pirates():
							destinations = game.get_sail_options(pirate, treasure, distance)
							found = False
							for i in destinations:
								if not found:
									if not game.is_occupied(i) and i not in locations:
										if pirate.turns_to_sober > 0:
											break
										elif moves>0:
											game.set_sail(pirate, i)
											game.debug("line85: pirate%d about to make %d moves"%(pirate.id, distance))
											moves = moves - distance
											locations.append(i)
											found = True
							if found:
								continue
				else: #the map is clear from treasures
					go = find_closest_enemy_initial(game,pirate)[1]
					if pirate.turns_to_sober == 0:
						destinations = game.get_sail_options(pirate, go, 1)
						found = False
						for i in destinations:
							if not found:
								if not game.is_occupied(i) and i not in locations:
									if pirate.turns_to_sober > 0:
										continue
									elif moves>0:
										game.set_sail(pirate, i)
										game.debug("line103: pirate%d about to make %d moves"%(pirate.id, 1))
										moves = moves - 1
										locations.append(i)
										found = True
						if found:
							continue
	game.debug(locations)
	game.debug("moves made in the end: %d"%(6-moves))

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

def closest_enemy(game, pirate):
	distances = [ game.distance(pirate, enemy) for enemy in game.enemy_pirates() ]
	if len(distances) > 0:
		val, idx = min(((val, idx) for idx, val in enumerate(distances)))
		return game.enemy_pirates()[idx]
	return False

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

def kamikaza(game,pirate,moves):
	if pirate.turns_to_sober == 0 and moves>0:
		find=False
		for enemy in game.enemy_pirates():
			if game.in_range(pirate, enemy) and enemy.has_treasure:
				find=True
				best_attack=enemy
				break
		if find==True:
			for enemy in game.enemy_pirates():
				if game.in_range(pirate, enemy) and enemy.has_treasure:
					if enemy.treasure_value>best_attack.treasure_value:
						best_attack=enemy
			to_return = go_to_enemy(game,pirate,best_attack,moves)
			return to_return
		else:
			return False
	else:
		return False	
def go_to_enemy(game,pirate,enemy,moves):
	distance = game.distance(pirate, enemy)
	if distance >= moves:
		destinations = game.get_sail_options(pirate,enemy, moves)
		found = False
		for i in destinations:
			if not found:
				if (game.get_pirate_on(i) not in game.my_pirates()) and (i not in locations):		
					if pirate.turns_to_sober > 0:
						break
					elif moves > 0:
						game.debug("line204: pirate%d about to make %d moves"%(pirate.id, moves))
						game.set_sail(pirate, i)
						moves =0#make moves equal to 0
						locations.append(i)
						found = True
						game.debug("pirate%d runs after: %s"%(pirate.id,enemy))
		if found==True:
			return moves
		else:
			return False
	else:
		destinations = game.get_sail_options(pirate,enemy, distance)
		found = False
		for i in destinations:
			if not found:
				if (game.get_pirate_on(i) not in game.my_pirates()) and (i not in locations):
					if pirate.turns_to_sober > 0:
						break
					elif moves>0:
						game.set_sail(pirate, i)
						game.debug("line221: pirate%d about to make %d moves"%(pirate.id, moves))
						moves = moves - distance
						locations.append(i)
						found = True	
		if found==True:
			return moves
		else:
			return False
