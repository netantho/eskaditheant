import sys
import os
sys.path.append(os.path.abspath('../'))

import variables

import logging

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
	
	def unblock_own_hill_simple(self):
		"""
		Check if there's an ant on my hill and if so, move it in one of the 4 directions
		
		\param self
		"""
		if self.ants.time_remaining() > variables.idle_time_remaining:
			# unblock own hill
			for hill_loc in self.ants.my_hills():
				if hill_loc in self.ants.my_ants() and hill_loc not in variables.orders.values():
					for direction in ('s','e','w','n'):
						logging.debug(direction)
						if self.movement.do_move_direction(hill_loc, direction):
							break
	
	def unblock_own_hill_complex(self):
		"""
		Check if there's an ant on my hill and if so, move it
		
		\param self
		"""
		if self.ants.time_remaining() > variables.idle_time_remaining:
			# unblock own hill
			for hill_loc in self.ants.my_hills():
				if hill_loc in self.ants.my_ants() and hill_loc not in variables.orders.values():
					self.movement.shift_ant(hill_loc)