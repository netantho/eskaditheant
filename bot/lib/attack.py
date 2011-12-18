import sys
import os
sys.path.append(os.path.abspath('../'))

import variables

class Attack():
	def __init__(self, ants, movement):
		"""
		Constructor
		
		\param self
		\param object instance of the ants class
		\param object instance of the movement class
		"""
		self.ants = ants
		self.movement = movement
	
	def save_enemy_hills(self, hills):
		"""
		Save the unknown and visible enemy hills
		
		\param self
		\param list of (r,c) enemies' hills
		\return list of (r,c) updated enemies' hills
		"""
		for hill_loc, hill_owner in self.ants.enemy_hills():
			if hill_loc not in hills:
				yield hill_loc
		
	def attack_hills(self, hills):
		"""
		Calculate distances between ants and hills and give orders to attack
		
		\param self
		\param list of (r,c) ennemies' hills
		"""
		# compute the distances to the hills and sort it
		if self.ants.time_remaining() > variables.idle_time_remaining:
			ant_dist = []
			for hill_loc in hills:
				for ant_loc in self.ants.my_ants():
					if ant_loc not in variables.orders.values():
						dist = self.ants.distance(ant_loc, hill_loc)
						ant_dist.append((dist, ant_loc))
			ant_dist.sort()
			# give orders to attack the ennemy's hills
			for dist, ant_loc in ant_dist:
				self.movement.do_move_location(ant_loc, hill_loc)