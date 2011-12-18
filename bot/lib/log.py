from datetime import date
import os
import logging

class Log:
	def __init__(self):
		"""
		Open log file
		
		\param self
		"""
		log_file = 'logs/bot'+str(date.today())+'_'
		i=0
		while os.path.exists(log_file+str(i)+'.log'):
			i+=1

		logging.basicConfig(filename='logs/bot'+str(date.today())+'_'+str(i)+'.log',level=logging.DEBUG)