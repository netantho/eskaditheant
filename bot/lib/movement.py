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
		if (not variables.pathfinding.has_key((loc, dest))):
			pathfinding = self.pathfinding.astar(locr, locc, destr, destc)
			if (not pathfinding):
				variables.targets[dest] = None
				return False
				
			variables.pathfinding[loc, dest] = self.pathfinding.coordinates_to_directions(pathfinding)
		
		direction = variables.pathfinding[loc, dest].pop(0)
		variables.pathfinding[self.direction_to_coordinate(loc, direction), dest] = variables.pathfinding[loc, dest]
		del variables.pathfinding[loc, dest]

		
		#directions = self.pathfinding.coordinates_to_directions(pathfinding)
		#logging.debug("directions")
		#logging.debug(directions)
		#for direction in directions:
			#if self.do_move_direction(loc, direction):
				#variables.targets[dest] = loc
				#return True
			##Bug duplicate order
			#elif self.shift_ant(self.direction_to_coordinate(loc, direction)):
				#return True
		
		if self.do_move_direction(loc, direction):
			variables.targets[dest] = loc
			return True
		elif loc in self.ants.my_ants() and self.shift_ant(self.direction_to_coordinate(loc, direction)):
			return True
		else:
			logging.error("do_move_location stuck from "+str(loc)+", wants to go "+direction)
		
		logging.error("do_move_location from "+str(loc)+" to "+str(dest)+" impossible")
		variables.targets[dest] = None
		return False
	
	def direction_to_coordinate(self, loc, direction):
		""""
		Converts an initial location and a direction into a new location
		
		\param tuple (r,c) initial location
		\param string n|s|e|w direction
		\return tuple (r,c) resulting location
		"""
		(r,c) = loc
		if direction == "n":
			return (r-1,c)
		elif direction == "s":
			return (r+1,c)
		elif direction == "w":
			return (r,c-1)
		elif direction == "e":
			return (r,c+1)
		logging.error("direction_to_coordinate invalid direction "+direction)
		return False
	
	def shift_ant(self, ant_loc):
		"""
		Recursive method to shift an ant from one tile and shift others to do so if necessary
		
		\param self
		\param tuple (r,c) location of the ant to shift
		\return bool True if success, False is failure
		"""
		# invalid ant
		if ant_loc not in self.ants.my_ants():
			logging.error("Failed to shift the ant on "+str(ant_loc)+": no ant there")
			return False
		moved_ant = False
		for direction in ('s', 'w', 'e', 'n'):
			moved_ant = self.do_move_direction(ant_loc, direction)
			if moved_ant:
				return True
		if (not moved_ant):
			(r,c) = ant_loc
			# south
			if (r+1,c) in self.ants.my_ants() and self.shift_ant((r+1,c)):
				return True
			# east
			elif (r,c+1) in self.ants.my_ants() and self.shift_ant((r,c+1)):
				return True
			# north
			elif (r-1,c) in self.ants.my_ants() and self.shift_ant((r-1,c)):
				return True
			# west
			elif (r,c-1) in self.ants.my_ants() and self.shift_ant((r,c-1)):
				return True
			logging.error("Fail to shift the ant on "+str(ant_loc)+": no free space")
			return False