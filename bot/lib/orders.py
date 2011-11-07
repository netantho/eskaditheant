import sys
import os
sys.path.append(os.path.abspath('../'))

import variables

class Orders():
	def __init__(self, ants):
		"""
		Constructor
		
		\param self
		\param object instance of the ants class
		"""
		self.ants = ants
		
	def prevent_stepping_hill(self):
		"""
		Prevent stepping on own hill canceling such orders
		
		\param self
		"""
		for hill_loc in self.ants.my_hills():
			variables.orders[hill_loc] = None