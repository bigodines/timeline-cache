from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor

import time

car = lambda x: x[0]
cdr = lambda x: x[1:]

class Timeline(Protocol):
	storage = None
	def connectionMade(self):
		self.storage = self.factory.storage_engine

	def lineReceived(self, data):
		data = data.split(" ")
		cmd = car(data)
		args = cdr(data)
		response = self._parse(cmd, args)
		self.transport.write(response)

	def _parse(self, cmd, args):
		if cmd == 'dummy':
			return '[%s, %s]' % (car(args), ''.join(cdr(args)))
		if cmd == 'push':
			return self.push(args)

		if cmd == 'get':
			return self.get(car(args))

		if cmd == 'timeline':
			return self.get_timeline(args)

	def push(self, data):
		key, value = car(data), cdr(data)
		self.storage.push(key, value)
		return "OK"
		
	def get(self, key):
		return "[%s, %s]" % (key, ' '.join(self.storage.get(key)))

	def get_timeline(self, users):
		ret = []
		for k in users:
			ret += self.storage.get(k)

		return ret

class TimelineFactory(Factory):
	protocol = Timeline

	def __init__(self, storage=None):
		if storage is None: raise
		self.storage_engine = storage
		


class TimelineItem():
	def __init__(self, myid="", author=""):
		self.id = myid
		self.author = author
		self.timestamp = time.time()


