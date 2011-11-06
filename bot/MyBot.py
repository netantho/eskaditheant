#!/usr/bin/env python
from ants import *

import sys
sys.path.append("lib")

import variables

from exploration import Exploration
from movement import Movement

import logging

logging.basicConfig(filename='logs/bot.log',level=logging.DEBUG)

# define a class with a do_turn method
# the Ants.run method will parse and update bot input
# it will also run the do_turn method for us
class MyBot:
	"""
	Main Class of the bot
	"""
	
	def __init__(self):
		"""
		Constructor
		Define class level variable, will be remembered between turns
		
		\param self
		"""
		pass
	
	def do_setup(self, ants):
		"""
		do_setup is run once at the start of the game after the bot has received the game settings the ants class is created and setup by the Ants.run method.
		
		\param self
		\param object instance of the ants class
		"""
		# initialize data structures after learning the game settings
		self.hills = []
		self.movement = Movement(ants)
		# store unexplored locations
		self.exploration = Exploration(ants)
		self.unseen = self.exploration.generate_unseen()
	
	def do_turn(self, ants):
		"""
		do turn is run once per turn the ants class has the game state and is updated by the Ants.run method
		
		\param self
		\param object instance of the ants class
		"""
		
		# prevent stepping on own hill
		for hill_loc in ants.my_hills():
			variables.orders[hill_loc] = None
		# find close food
		ant_dist = []
		for food_loc in ants.food():
			for ant_loc in ants.my_ants():
				dist = ants.distance(ant_loc, food_loc)
				ant_dist.append((dist, ant_loc, food_loc))
		ant_dist.sort()
		
		# debug
		#logging.debug(targets)
		#logging.debug(ants.food())
		
		# give instructions to free ants to grab food
		for dist, ant_loc, food_loc in ant_dist:
			# assign an ant to grab food
			if food_loc not in variables.targets and ant_loc not in variables.targets.values():
				self.movement.do_move_location(ant_loc, food_loc)
		# attack hills
		# save the ennemy's hills
		for hill_loc, hill_owner in ants.enemy_hills():
			if hill_loc not in self.hills:
				self.hills.append(hill_loc)
		# compute the distances to the hills and sort it
		ant_dist = []
		for hill_loc in self.hills:
			for ant_loc in ants.my_ants():
				if ant_loc not in variables.orders.values():
					dist = ants.distance(ant_loc, hill_loc)
					ant_dist.append((dist, ant_loc))
		ant_dist.sort()
		# give orders to attack the ennemy's hills
		for dist, ant_loc in ant_dist:
			self.movement.do_move_location(ant_loc, hill_loc)
		# explore unseen areas
		# remove explored areas
		for loc in self.unseen[:]: # : to make sure this list is different from the one we are deleting from
			if ants.visible(loc):
				self.unseen.remove(loc)
		for ant_loc in ants.my_ants():
			if ant_loc not in variables.orders.values():
				unseen_dist = []
				# store and sort distances of unexplored areas
				for unseen_loc in self.unseen:
					dist = ants.distance(ant_loc, unseen_loc)
					unseen_dist.append((dist, unseen_loc))
				unseen_dist.sort()
				# give orders to explore
				for dist, unseen_loc in unseen_dist:
					if self.movement.do_move_location(ant_loc, unseen_loc):
						break
		# unblock own hill
		for hill_loc in ants.my_hills():
			if hill_loc in ants.my_ants() and hill_loc not in variables.orders.values():
				for direction in ('s','e','w','n'):
					if self.movement.do_move_direction(hill_loc, direction):
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
