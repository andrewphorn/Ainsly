
class LoggerClass(object):
	def log(self,text):
		print(text)

	def error(self,text):
		print('ERROR: %s' % text)