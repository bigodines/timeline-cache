import redis
import simplejson as json

from server import TimelineItem

class RedisStorage():
	LIST_SIZE = 9
	def __init__(self, client_instance=None):
		self.storage = client_instance

	def push(self, key, obj):
		obj = json.dumps(obj)
		pos = self.storage.lpush(key, obj)
		# cant let this list get too big
		self.storage.ltrim(key, 0, self.LIST_SIZE) 
		return pos
	
	def get(self, key):
		serialized =  self.storage.lrange(key, 0, self.LIST_SIZE)
		return [json.loads(x) for x in serialized]


	def multi_get(self, keys):
		pipe = self.storage.pipeline()
		for k in keys:
			pipe.lrange(k, 0, self.LIST_SIZE)

		serialized = pipe.execute()
		return serialized #[json.loads(x) for x in serialized]
		



class RedisStorageFactory():
	def __init__(self):
		pass
