class Person(object):
	def __init__(self,pid,name,age,sex):
		self.pid=pid
		self.name=name
		self.age=age
		self.sex=sex

	def eating(self):
		return 'People need to eat!'

	def sleeping(self):
		return 'People need to sleep!'

	def walking(self):
		return 'People can walk!'

		
