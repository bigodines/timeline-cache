import redis
import unittest

from server import TimelineItem as Item
from storage import *

class RedisStorageTest(unittest.TestCase):
	def setUp(self):
		self.redis_obj = redis.Redis(host='localhost',port=6379,db=9)
		self.redis_obj.flushdb()
		self.storage = RedisStorage(self.redis_obj)

	def tearDown(self):
		self.redis_obj.flushdb()
		for c in self.redis_obj.connection_pool.get_all_connections():
			c.disconnect()

		self.storage = None


	def test_single_push(self):
		item = Item('foo', 'author')
		x = self.storage.push('foo', item)
		self.assertEquals(1, x)

	def test_single_push_and_get(self):
		item = Item('foo', 'author')
		self.storage.push('foo', item)
		x =self.storage.get('foo')
		self.assertEquals(item.id, x.id)
		self.assertEquals(item.timestamp, x.timestamp)

	def test_many_pushes_one_get(self):
		one = Item('itemId', 'foobar')
		self.storage.push('my_items', one)
		two = Item('itemId2', 'foobar2')
		self.storage.push('my_items',two)
		resp = self.storage.get('my_items')
		
		
		

if __name__ == "__main__":
	unittest.main()
