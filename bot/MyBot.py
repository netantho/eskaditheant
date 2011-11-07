#!/usr/bin/env python
from ants import *

import sys
sys.path.append("lib")

import variables

from exploration import Exploration
from movement import Movement
from orders import Orders
from food import Food
from attack import Attack
from defence import Defence

from datetime import date
import time
import logging

logging.basicConfig(filename='logs/bot'+str(date.today())+'_'+str(time.time())+'.log',level=logging.DEBUG)

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
		self.orders = Orders(ants)
		self.food = Food(ants, self.movement)
		self.attack = Attack(ants, self.movement)
		self.defence = Defence(ants, self.movement)
		self.exploration = Exploration(ants, self.movement)
		# store unexplored locations
		self.exploration.generate_unseen()
	
	def do_turn(self, ants):
		"""
		do turn is run once per turn the ants class has the game state and is updated by the Ants.run method
		
		\param self
		\param object instance of the ants class
		"""
		
		# clean the mess of the old turns
		variables.orders = {}
		variables.targets = {}
		
		self.orders.prevent_stepping_hill()
		self.food.grab_visible_food()
		self.hills = self.attack.save_enemy_hills(self.hills)
		self.attack.attack_hills(self.hills)
		self.exploration.remove_seen()
		self.exploration.explore()
		self.defence.unblock_own_hill_complex()


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
