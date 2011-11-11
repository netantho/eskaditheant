import sys
import os
sys.path.append(os.path.abspath('../'))

import variables

import logging

class Movement():
	def __init__(self, ants, pathfinding, graph):
		"""
		Constructor
		
		\param self
		\param object instance of the ants class
		"""
		self.ants = ants
		self.pathfinding = pathfinding
		self.graph = graph
	
	def do_move_direction(self, loc, direction):
		"""
		Move an ant one tile in a direction
		
		\param self
		\param (r, c) coordinates of the current location
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
		\param (r, c) coordinates of the current location
		\param (r, c) coordinates of the destination location
		\return True if the destination is possible, else False
		"""
		
		#directions = self.ants.direction(loc, dest)
		#directions = self.pathfinding.coordinates_to_directions(self.pathfinding.bfs(loc, dest, self.graph))
		(locr, locc) = loc
		(destr, destc) = dest
		directions = self.pathfinding.coordinates_to_directions(self.pathfinding.astar(locr, locc, destr, destc))
		logging.debug("directions")
		logging.debug(directions)
		for direction in directions:
			if self.do_move_direction(loc, direction):
				variables.targets[dest] = loc
				return True
		logging.debug("do_move_location false")
		variables.targets[dest] = None
		return False
	
	def shift_ant(self, ant_loc):
		"""
		Recursive method to shift an ant from one tile and shift others to do so if necessary
		
		\param self
		"""
		# invalid ant
		if ant_loc not in self.ants.my_ants():
			return False
		moved_ant = False
		for direction in ('s', 'w', 'e', 'n'):
			moved_ant = self.do_move_direction(ant_loc, direction)
			if moved_ant:
				return True
		if (not moved_ant):
			(r,c) = ant_loc
			#south
			if self.shift_ant((r+1,c)):
				return True
			#est
			elif self.shift_ant((r,c+1)):
				return True
			#west
			elif self.shift_ant((r-1,c)):
				return True
			#north
			if self.shift_ant((r,c-1)):
				return True
			return False