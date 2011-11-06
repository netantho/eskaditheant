import sys
import os
sys.path.append(os.path.abspath('../'))

import variables

class Movement():
	def __init__(self, ants):
		"""
		Constructor
		
		\param self
		"""
		self.ants = ants
		pass
	
	def do_move_direction(self, loc, direction):
		"""
		Move an ant one tile in a direction
		
		\param self
		\param object instance of the ants class
		\param array orders already issued
		\param (x, y) coordinates of the current location
		\param char n|s|w|e direction of the movement
		\return bool True if unoccupied and not already targeted, else False
		"""
		global orders
		
		new_loc = self.ants.destination(loc, direction)
		# unoccupied : without food or ant
		# We don't want to go where another ant has already gone, and not the last location
		if (self.ants.unoccupied(new_loc) and (new_loc not in variables.orders)):
			# Go !
			self.ants.issue_order((loc, direction))
			# Save the order
			variables.orders[new_loc] = loc
			return True
		else:
			return False
	
	def do_move_location(self, loc, dest):
		"""
		Simulate a manhattan pathfinding for food and issue the order if the destination is possible
		
		\param self
		\param object instance of the ants class
		\param array orders already issued
		\param hash location of the target food as the key, location of the assigned ant as the value
		\param (x, y) coordinates of the current location
		\param (x, y) coordinates of the destination location
		\return True if the destination is possible, else False
		"""
		global orders, targets
		
		directions = self.ants.direction(loc, dest)
		for direction in directions:
			if self.do_move_direction(loc, direction):
				variables.targets[dest] = loc
				return True
		return False