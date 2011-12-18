#!/usr/bin/env python
from ants import *

import sys
import time
import logging
from datetime import date

import lib
import variables
import sys

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
		
		if variables.log_enabled:
			self.log = lib.log.Log()
			logging.basicConfig(filename='logs/bot'+str(date.today())+'_'+str(self.log.get_available_revision())+'.log',level=logging.DEBUG)
		logging.debug("Args: "+str(sys.argv))
	
	def do_setup(self, ants):
		"""
		do_setup is run once at the start of the game after the bot has received the game settings the ants class is created and setup by the Ants.run method.
		
		\param self
		\param object instance of the ants class
		"""
		# initialize data structures after learning the game settings
		self.hills = []

		self.orders = lib.orders.Orders(ants)
		self.pathfinding = lib.pathfinding.Pathfinding(ants)
		
		# generate the graph of the map
		self.graph = self.pathfinding.generate_graph()
		
		self.movement = lib.movement.Movement(ants, self.pathfinding, self.graph)
		self.food = lib.food.Food(ants, self.movement)
		self.attack = lib.attack.Attack(ants, self.movement)
		self.defence = lib.defence.Defence(ants, self.movement)
		self.exploration = lib.exploration.Exploration(ants, self.movement)

		# store unexplored locations
		self.exploration.unseen = list(self.exploration.generate_unseen())
	
	def do_turn(self, ants):
		"""
		do turn is run once per turn the ants class has the game state and is updated by the Ants.run method
		
		\param self
		\param object instance of the ants class
		"""
		
		variables.idle_time_remaining = variables.idle_time_ini * ants.turntime + len(list(ants.my_ants())) * variables.idle_time_per_ant
		
		# logging start of the turn
		logging.debug("Turn "+str(ants.turn_current)+" idle_time_remaining: "+str(variables.idle_time_remaining))
		
		# clean the mess of the old turns
		variables.orders = {}
		variables.targets = {}
		
		#logging.debug("rows: "+str(ants.rows))
		#logging.debug("cols: "+str(ants.cols))
		
		#my_ants = ants.my_ants()
		#path = self.pathfinding.coordinates_to_directions(self.pathfinding.bfs(my_ants[0], (1,1), self.graph))
		#logging.debug(path)

		#for row in ants.map:
			#logging.debug(row)

		self.orders.prevent_stepping_hill()
		self.food.grab_visible_food()
		self.hills = list(self.attack.save_enemy_hills(self.hills))
		self.attack.attack_hills(self.hills)
		self.exploration.remove_seen()
		self.exploration.explore()
		self.defence.unblock_own_hill_complex()
		
		# logging end of the turn
		logging.debug("Turn "+str(ants.turn_current)+" finished with "+str(ants.time_remaining())+" time remaining\n")


if __name__ == '__main__':
	# psyco will speed up python a little, but is not needed
	# be aware that psyco is currently unavailable for python >= 2.7
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
