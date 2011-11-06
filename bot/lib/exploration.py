import sys
import os
sys.path.append(os.path.abspath('../'))

import variables

class Exploration():
	def __init__(self, ants):
		"""
		Constructor
		
		\param self
		\param object instance of the ants class
		"""
		self.ants = ants
		pass
	
	def generate_unseen(self):
		"""
		Return an array of couples of the unexplored tiles
		
		\param self
		\return array couples of the unexplored tiles
		"""
		unseen = []
		for row in range(self.ants.rows):
			for col in range(self.ants.cols):
				unseen.append((row, col))
		return unseen