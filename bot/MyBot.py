#!/usr/bin/env python
from ants import *
import logging

logging.basicConfig(filename='logs/bot.log',level=logging.DEBUG)

# define a class with a do_turn method
# the Ants.run method will parse and update bot input
# it will also run the do_turn method for us
class MyBot:
	def __init__(self):
		# define class level variables, will be remembered between turns
		# last location, new location as the key and old location as the value
		self.last_loc = {}
		pass
    
	# do_setup is run once at the start of the game
	# after the bot has received the game settings
	# the ants class is created and setup by the Ants.run method
	def do_setup(self, ants):
		# initialize data structures after learning the game settings
		# store unexplored locations
		self.hills = []
		self.unseen = []
		for row in range(ants.rows):
			for col in range(ants.cols):
				self.unseen.append((row, col))
    
	# do turn is run once per turn
	# the ants class has the game state and is updated by the Ants.run method
	# it also has several helper methods to use
	def do_turn(self, ants):
		# track all moves for one turn, prevent collisions
		# orders for the turn, new location as the key, old location as the value
		orders = {}
		def do_move_direction(loc, direction):
			'Return True if passable and not the last location, else False'
			new_loc = ants.destination(loc, direction)
			# unoccupied : without food or ant
			# We don't want to go where another ant has already gone, and not the last location
			if (ants.unoccupied(new_loc) and (new_loc not in orders) and (new_loc not in self.last_loc.values())):
				# Go !
				ants.issue_order((loc, direction))
				# Save the order
				orders[new_loc] = loc
				self.last_loc[new_loc] = loc
				# Delete outdated last locations
				if self.last_loc.has_key(loc):
					del self.last_loc[loc]
				return True
			else:
				return False
		# Pathfinding for food
		# targets for the turn, location of the target food as the key, location of the assigned ant as the value
		targets = {}
		def do_move_location(loc, dest):
			'Simulate the pathfinding for food, return True if the direction is possible, else false'
			directions = ants.direction(loc, dest)
			for direction in directions:
				if do_move_direction(loc, direction):
					targets[dest] = loc
					return True
			return False

		# prevent stepping on own hill
		for hill_loc in ants.my_hills():
			orders[hill_loc] = None
		# find close food
		ant_dist = []
		for food_loc in ants.food():
			for ant_loc in ants.my_ants():
				dist = ants.distance(ant_loc, food_loc)
				ant_dist.append((dist, ant_loc, food_loc))
		ant_dist.sort()
		#logging.debug(targets)
		#logging.debug(ants.food())
		# give instructions to free ants to grab food
		for dist, ant_loc, food_loc in ant_dist:
			# assign an ant to grab food
			if food_loc not in targets and ant_loc not in targets.values():
				do_move_location(ant_loc, food_loc)
		# attack hills
		# save the ennemy's hills
		for hill_loc, hill_owner in ants.enemy_hills():
			if hill_loc not in self.hills:
				self.hills.append(hill_loc)
		# compute the distances to the hills and sort it
		ant_dist = []
		for hill_loc in self.hills:
			for ant_loc in ants.my_ants():
				if ant_loc not in orders.values():
					dist = ants.distance(ant_loc, hill_loc)
					ant_dist.append((dist, ant_loc))
		ant_dist.sort()
		# give orders to attack the ennemy's hills
		for dist, ant_loc in ant_dist:
			do_move_location(ant_loc, hill_loc)
		# explore unseen areas
		# remove explored areas
		for loc in self.unseen[:]: # : to make sure this list is different from the one we are deleting from
			if ants.visible(loc):
				self.unseen.remove(loc)
		for ant_loc in ants.my_ants():
			if ant_loc not in orders.values():
				unseen_dist = []
				# store and sort distances of unexplored areas
				for unseen_loc in self.unseen:
					dist = ants.distance(ant_loc, unseen_loc)
					unseen_dist.append((dist, unseen_loc))
				unseen_dist.sort()
				# give orders to explore
				for dist, unseen_loc in unseen_dist:
					if do_move_location(ant_loc, unseen_loc):
						break
		# unblock own hill
		for hill_loc in ants.my_hills():
			if hill_loc in ants.my_ants() and hill_loc not in orders.values():
				for direction in ('s','e','w','n'):
					if do_move_direction(hill_loc, direction):
						break

            
if __name__ == '__main__':
	# psyco will speed up python a little, but is not needed
	try:
		import psyco
		psyco.full()
	except ImportError:
		pass
	
	try:
		# if run is passed a class with a do_turn method, it will do the work
		# this is not needed, in which case you will need to write your own
		# parsing function and your own game state class
		Ants.run(MyBot())
	except KeyboardInterrupt:
		print('ctrl-c, leaving ...')
