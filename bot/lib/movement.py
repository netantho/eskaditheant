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
		if self.ants.time_remaining() > variables.idle_time_remaining:
			new_loc = self.ants.destination(loc, direction)
			# unoccupied : without food or ant
			# We don't want to go where another ant has already gone, and not the last location
			if (self.ants.unoccupied(new_loc) and (new_loc not in variables.orders) and (loc not in variables.orders.values())):
				# Go !
				self.ants.issue_order((loc, direction))
				# Save the order
				variables.orders[new_loc] = loc
				return True
			else:
				return False
		return False
	
	def do_move_location(self, loc, dest, cat=None):
		"""
		Simulate a manhattan pathfinding for food and issue the order if the destination is possible
		
		\param self
		\param (r, c) coordinates of the current location
		\param (r, c) coordinates of the destination location
		\return True if the destination is possible, else False
		"""
		if self.ants.time_remaining() > variables.idle_time_remaining:
			#directions = self.ants.direction(loc, dest)
			#directions = self.pathfinding.coordinates_to_directions(self.pathfinding.bfs(loc, dest, self.graph))
			(locr, locc) = loc
			(destr, destc) = dest
			if ((loc, dest) not in variables.pathfinding):
				pathfinding = self.pathfinding.astar(locr, locc, destr, destc)
				if (not pathfinding):
					variables.targets[dest] = None
					return False
					
				variables.pathfinding[loc, dest] = list(self.pathfinding.coordinates_to_directions(pathfinding))
			
			if not variables.pathfinding[loc, dest]:
				return False
			
			direction = variables.pathfinding[loc, dest].pop(0)
			variables.pathfinding[self.ants.destination(loc, direction), dest] = variables.pathfinding[loc, dest]
			del variables.pathfinding[loc, dest]
			
			dest_loc = self.ants.destination(loc, direction)

			if self.do_move_direction(loc, direction):
				if cat == 'food':
					variables.targets[direction] = loc
				return True
			elif dest_loc in self.ants.my_ants() and self.shift_ant(dest_loc) and self.do_move_direction(loc, direction):
				if cat == 'food':
					variables.targets[direction] = loc
				return True
			
			logging.error("do_move_location stuck from "+str(loc)+", wants to go "+direction)
			logging.error("do_move_location from "+str(loc)+" to "+str(dest)+" impossible")
			variables.targets[dest] = None
			return False
		return False
	
	def shift_ant(self, ant_move_loc):
		"""
		Shift an ant from one tile and shift others to do so if necessary, only depth = 0
		TODO: Make it for depth >= 0
		
		\param self
		\param (r,c) location of the ant to shift
		\return bool True if success, False is failure
		"""
		if self.ants.time_remaining() > variables.idle_time_remaining:
			# If useless to use shift_ant
			if ant_move_loc not in self.ants.my_ants():
				return True

			for direction in ('n', 'e', 's', 'w'):
				if self.do_move_direction(ant_move_loc, direction):
					return True
			
			logging.debug("shift_ant: no immediate free space to move "+str(ant_move_loc)) 
			return False
		return False