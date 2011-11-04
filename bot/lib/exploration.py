class Exploration():
	def __init__(self):
		"""
		Constructor
		
		\param self
		"""
		pass
	
	def generate_unseen(self, ants):
		"""
		Return an array of couples of the unexplored tiles
		
		\param self
		\param object instance of the ants class
		\return array couples of the unexplored tiles
		"""
		unseen = []
		for row in range(ants.rows):
			for col in range(ants.cols):
				unseen.append((row, col))
		return unseen