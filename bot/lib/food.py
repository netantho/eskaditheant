import sys
import os
sys.path.append(os.path.abspath('../'))

import variables

class Food():
	def __init__(self, ants, movement):
		"""
		Constructor
		
		\param self
		\param object instance of the ants class
		"""
		self.ants = ants
		self.movement = movement

	def distance_food(self):
		"""
		Generators to get the distance between ant locations and food locations
		
		\param self
		"""
		for food_loc in self.ants.food():
			for ant_loc in self.ants.my_ants():
				dist = self.ants.distance(ant_loc, food_loc)
				yield (dist, ant_loc, food_loc)

	def grab_visible_food(self, limit):
		"""
		Calculate distances between ants and food and give orders to grab
		
		\param self
		"""
		if self.ants.time_remaining() > variables.idle_time_remaining:
			# find close food
			ant_dist = list(self.distance_food())
			ant_dist.sort()
			
			# debug
			#logging.debug(targets)
			#logging.debug(ants.food())
			
			# give instructions to free ants to grab food
			for dist, ant_loc, food_loc in ant_dist:
				# assign an ant to grab food
				if food_loc not in variables.targets and food_loc not in variables.targets.values() and ant_loc not in variables.targets.values() and self.ants.time_remaining() > variables.idle_time_remaining and limit > 0:
					limit -= 1
					self.movement.do_move_location(ant_loc, food_loc, 'food')