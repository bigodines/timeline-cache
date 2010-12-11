from twisted.trial import unittest
from twisted.test import proto_helpers

from server import *

# simple storage engine that will be used in our tests
class MemoryStorage():

	def __init__(self):
		self.data = {}
		
 	def push(self, key, value):
		try:
			self.data[key]
		except:
			self.data[key] = []

		self.data[key].append(''.join(value))

	def get(self, key):
		return self.data[key] or None

class TestTimelineProtocol(unittest.TestCase):
	def setUp(self):
		factory = TimelineFactory(MemoryStorage())
		self.proto = factory.buildProtocol(('127.0.0.1',0))
		self.tr = proto_helpers.StringTransport()
		self.proto.makeConnection(self.tr)

	def _do(self, line):
		self.tr.clear()
		self.proto.lineReceived(line)
		return self.tr.value()

	def test_has_storage_when_connectionMade_happypath(self):
		self.assertTrue(self.proto.storage is not None)
		try:
			self.proto.storage.push(0,["foo"])
		except:
			self.fail("it looks like you dont have a valid storage.")
	
	def test_parse(self):
		resp = self._do("dummy 1 foo")
		self.assertEquals("[1, foo]", resp)

	def test_push(self):
		resp = self._do("push 1 bar")
		self.assertEquals("OK", resp)

	def test_get(self):
		# custom setup
		s = None
		s = MemoryStorage()
		s.push('foo', 'bar')
		s.push('foo', 'baz')
		factory = TimelineFactory(s)
		self.proto = factory.buildProtocol(('127.0.0.1',0))
		self.tr = proto_helpers.StringTransport()
		self.proto.makeConnection(self.tr)
		self.tr.clear()
		self.proto.lineReceived("get foo")

		self.assertEquals("[foo, bar baz]", self.tr.value())
		

	def test_get_unsorted_timeline(self):
		# custom setup
		s = None
		s = MemoryStorage()
		s.push('foo', '1')
		s.push('marco', '2')
		s.push('foo', '3')
		s.push('marco', '4')
		s.push('foo', '5')
		s.push('mary', 'jane')
		factory = TimelineFactory(s)
		self.proto = factory.buildProtocol(('127.0.0.1',0))
		self.tr = proto_helpers.StringTransport()
		self.proto.makeConnection(self.tr)
		self.tr.clear()

		self.proto.lineReceived('timeline foo marco')
		stringResponse = self.tr.value()
		
		self.assertEquals(25,len(stringResponse)) # can't assume order in this type of test, as this is not an ordered timeline

	
