import redis
import simplejson as json

from server import TimelineItem

def decode_item(dct):
	if "__TimelineItem__" in dct:
		ret = TimelineItem()
		ret.id = dct['id']
		ret.author = dct['author']
		ret.timestamp = dct['timestamp']
		return ret
	return dct

def encode_item(item):
	if isinstance(item, TimelineItem):
		return {'__TimelineItem__': True,
				'id': item.id,
				'timestamp': item.timestamp,
				'author': item.author}
	raise TypeError("You must serialize a valid TimelineItem object")


class RedisStorage():
	def __init__(self, client_instance=None):
		self.storage = client_instance

	def push(self, key, obj):
		obj = json.dumps(obj, default=encode_item)
		pos = self.storage.lpush(key, obj)
		# cant let this list get too big
		self.storage.ltrim(key, 0, 9) 
		return pos
	
	def get(self, key):
		serialized =  self.storage.lpop(key)
		return json.loads(serialized, object_hook=decode_item)

	def multi_get(self, keys):
		pass



class RedisStorageFactory():
	def __init__(self):
		pass
