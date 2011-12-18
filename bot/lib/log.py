from datetime import date
import os

class Log:
	def get_available_revision(self):
		"""
		Get the number of the first available revision of the log file
		
		\param self
		"""
		log_file = 'logs/bot'+str(date.today())+'_'
		i=0
		while os.path.exists(log_file+str(i)+'.log'):
			i+=1
		return i