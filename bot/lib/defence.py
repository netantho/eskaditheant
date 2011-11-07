import sys
import os
sys.path.append(os.path.abspath('../'))

import variables

class Defence():
	def __init__(self, ants, movement):
		"""
		Constructor
		
		\param self
		\param object instance of the ants class
		\param object instance of the movement class
		"""
		self.ants = ants
		self.movement = movement
	
	def unblock_own_hill(self):
		"""
		Check if there's an ant on my hill and if so, move it
		
		\param self
		"""
		# unblock own hill
		for hill_loc in self.ants.my_hills():
			if hill_loc in self.ants.my_ants() and hill_loc not in variables.orders.values():
				for direction in ('s','e','w','n'):
					if self.movement.do_move_direction(hill_loc, direction):
						break