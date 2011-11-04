class Movement():
	def __init__(self, ants):
		"""
		Constructor
		
		\param self
		"""
		pass
	
	def do_move_direction(self, ants, orders, loc, direction):
		"""
		Move an ant one tile in a direction
		
		\param self
		\param object instance of the ants class
		\param array orders already issued
		\param (x, y) coordinates of the current location
		\param char n|s|w|e direction of the movement
		\return bool True if unoccupied and not already targeted, else False
		"""
		new_loc = ants.destination(loc, direction)
		# unoccupied : without food or ant
		# We don't want to go where another ant has already gone, and not the last location
		if (ants.unoccupied(new_loc) and (new_loc not in orders)):
			# Go !
			ants.issue_order((loc, direction))
			# Save the order
			orders[new_loc] = loc
			return (orders, True)
		else:
			return (orders, False)
	
	def do_move_location(self, ants, orders, targets, loc, dest):
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
		directions = ants.direction(loc, dest)
		for direction in directions:
			(orders, move_bool) = self.do_move_direction(ants, orders, loc, direction)
			if (move_bool):
				targets[dest] = loc
				return (orders, targets, True)
		return (orders, targets, False)