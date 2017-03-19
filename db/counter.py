from db import Db

TABLE_NAME = "counter"

"""
Counter
"""
class counter(Db):
	def get_table_name(self):
		return TABLE_NAME

	@staticmethod
	def get_next_counter(name, retry=0):
		with counter() as table:
			c = table.find_and_modify( query={ "_id" : name },
			                           update={ "$inc" : { "count" : 1 } },
			                           new=True, upsert=True)
		if c is not None:
			return c['count']
		if retry < 3:
			return get_next_counter(name, retry+1)
		return -1

get_next_counter = counter.get_next_counter