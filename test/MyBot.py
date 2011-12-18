from movement import Movement

class MyBot():
	def __init__(self):
		self.movement = Movement(self)
	
	def machin(self):
		a = 1
		print str(a)+"\n"
		self.movement.add()
		print str(a)+"\n"
		
mybot = MyBot()
mybot.machin()