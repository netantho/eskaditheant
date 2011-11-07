import sys
import os
sys.path.append(os.path.abspath('../'))

import variables

class Movement():
	def __init__(self, ants):
		"""
		Constructor
		
		\param self
		\param object instance of the ants class
		"""
		self.ants = ants
	
	def do_move_direction(self, loc, direction):
		"""
		Move an ant one tile in a direction
		
		\param self
		\param (x, y) coordinates of the current location
		\param char n|s|w|e direction of the movement
		\return bool True if unoccupied and not already targeted, else False
		"""
		
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
		\param (x, y) coordinates of the current location
		\param (x, y) coordinates of the destination location
		\return True if the destination is possible, else False
		"""
		
		directions = self.ants.direction(loc, dest)
		for direction in directions:
			if self.do_move_direction(loc, direction):
				variables.targets[dest] = loc
				return True
		return False
	
	def shift_ant(self, ant_loc):
		"""
		Recursive method to shift an ant from one tile and shift others to do so if necessary
		
		\param self
		"""
		moved_ant = False
		for direction in ('s','e'):
			moved_ant = self.do_move_direction(ant_loc, direction)
			if moved_ant:
				break
		if (not moved_ant):
			(x,y) = ant_loc
			self.shift_ant((x+1,y))