import sys
import os
sys.path.append(os.path.abspath('../'))

import variables

import logging
import random

class Exploration():
	def __init__(self, ants, movement):
		"""
		Constructor
		
		\param self
		\param object instance of the ants class
		\param object instance of the movement class
		"""
		self.ants = ants
		self.movement = movement
		self.unseen = []
	
	def generate_unseen(self):
		"""
		Append couples of the unexplored tiles to self.unseen
		
		\param self
		"""
		for row in xrange(self.ants.rows):
			for col in xrange(self.ants.cols):
				self.unseen.append((row, col))
	
	def remove_seen(self):
		"""
		Remove explored tiles in self.unseen
		
		\param self
		"""
		for loc in self.unseen[:]: # : to make sure this list is different from the one we are deleting from
			if self.ants.visible(loc):
				self.unseen.remove(loc)
	
	def explore(self):
		"""
		Calculate distances between ants and unexplored tiles and explore
		
		\param self
		"""
		for ant_loc in self.ants.my_ants():
			if ant_loc not in variables.orders.values():
				unseen_dist = []
				# store and sort distances of unexplored areas
				for unseen_loc in self.unseen:
					if unseen_loc not in variables.targets:
						dist = self.ants.distance(ant_loc, unseen_loc)
						unseen_dist.append((dist, unseen_loc))
				unseen_dist.sort()
				# give orders to explore
				for dist, unseen_loc in unseen_dist:
					if self.movement.do_move_location(ant_loc, unseen_loc):
						#logging.debug("Exploration, from ... to ...")
						#logging.debug(ant_loc)
						#logging.debug(unseen_loc)
						break
					else:
						random.shuffle(unseen_dist)