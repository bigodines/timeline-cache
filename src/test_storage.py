import redis
import unittest

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
		item = { 'key': 'foo', 'value': 'bar' }
		x = self.storage.push('foo', item)
		self.assertEquals(1, x)

	def test_single_push_and_get(self):
		item = { 'key': 'foo', 'value': 'bar' }
		self.storage.push('foo', item)
		x = self.storage.get('foo')
		self.assertEquals(item['key'], x[0]['key'])
		self.assertEquals(item['value'], x[0]['value'])

	def test_many_pushes_one_get(self):
		one = { 'key': 'itemId', 'value': 'foobar' }
		self.storage.push('my_items', one)
		two = { 'key': 'itemId2', 'value': 'baz' }
		self.storage.push('my_items',two)
		resp = self.storage.get('my_items')
		# TODO: assert

	def test_list_cant_get_too_big(self):
		for x in range(20):
			self.storage.push('some_key', x)

		resp = self.storage.get('some_key')
		self.assertEquals(10, len(resp))

	def test_multi_get(self):
		v1 = {'meta':123, 'data':456}
		v2 = {'meta':444, 'data':333}
		v3 = {'meta':555, 'data':111}
		self.storage.push('a', v1)
		self.storage.push('b', v2)
		self.storage.push('a', v3)

		res = self.storage.multi_get(['a','b'])
		self.assertEquals(3, len(res))

	def test_multi_get_returns_sorted_list(self):
		v1 = {'meta':123, 'data':456}
		v2 = {'meta':444, 'data':333}
		v3 = {'meta':555, 'data':111}
		v4 = {'meta':999, 'data': 'whatever'}
		v5 = {'meta':856, 'data': 'foooo'}
		v6 = {'meta':777, 'data': 123456 }
		v7 = {'meta':12, 'data': 'im_not_gonna_return'}
		self.storage.push('user_a', v1)
		self.storage.push('user_b', v2)
		self.storage.push('user_a', v3)
		self.storage.push('user_a', v4)
		self.storage.push('user_b', v5)
		self.storage.push('user_b', v6)
		self.storage.push('user_XX', v7)

		res = self.storage.multi_get(['user_b','user_a'])
#		print res
		self.assertEquals(6, len(res))
		self.assertEquals(999, res[0]['meta'])
		self.assertEquals(856, res[1]['meta'])
		self.assertEquals(123, res[5]['meta'])

if __name__ == "__main__":
	unittest.main()
