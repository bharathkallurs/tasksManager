import sys
import counter
import logging as log

from pymongo import ASCENDING
from datetime import datetime
from db import Db


# Setting TABLE_NAME to assigned table name in the mongodb instance of heroku
TABLE_NAME = "heroku_tr2f0kzz"

class TaskTable(Db):
	"""
	A class to tasks table and relevant methods
	"""
	def get_table_name(self):
		"""
		Returns table name
		:return: TABLE NAME
		"""
		return TABLE_NAME

	@staticmethod
	def add_task(task_name, task_end_date, task_description, task_owner):
		"""
		A method to add task to db
		:param task_name: name of the task
		:param task_end_date: end date of the task
		:param task_description: description of task
		:param task_owner: owner of the task
		:return: Success if task entered, else appropriate error
		"""
		log.info("Table Name chosen is = ", TABLE_NAME)
		task_id = counter.get_next_counter(TABLE_NAME)
		current_date = datetime.now()
		log.info("Setting task_id = %s", task_id)
		try:
			with TaskTable() as table:
				insert_json = {"task_name": task_name,
				              "task_end_date": task_end_date, # validated date
				              "task_create_date": current_date,
				              "task_description": task_description,
				              "task_owner": task_owner,
				              "task_id": task_id}
				if task_end_date < current_date:
					return (403, "End date should be greated than create date")
				table.insert(insert_json)
				log.info("Inserted task successfully to DB")
				log.info("Task = %s", insert_json)
				return (200, "Task Entered Successfully")
		except Exception as e:
			log.error(str(e))
			return (-101, "Task entry failed")

	@staticmethod
	def list_all_tasks():
		"""
		Lists all the tasks in the DB currently
		:return: JSON of all tasks
		"""
		out = []
		try:
			with TaskTable() as table:
				table.ensure_index([("task_id", ASCENDING)], unique=True)
				results = table.find({}, {"_id": False}).sort("task_id",
				                                             ASCENDING)
				if not results:
					log.info("No tasks to list")
					return (-102, None)
				for result in results:
					cr_date = result['task_create_date']
					result['task_create_date'] = cr_date.strftime("%Y-%m-%d")
					en_date = result['task_end_date']
					result['task_end_date'] = en_date.strftime("%Y-%m-%d")
					out.append(result)
				log.info("tasks list = %s", out)
				return (200, out)
		except Exception as e:
			log.error(str(e))
			return (-103, "Task list failed")

	@staticmethod
	def list_based_on_date(qdate, pdate=None, after=False):
		"""
		List tasks with end date before a given date.
		List tasks created after a given date.
		:param qdate: a date to query before/after for tasks
		:param pdate: a date to query for created tasks before a date
		:param after: bool set to False.
		:return:
		"""
		str_date = qdate.strftime("%Y-%m-%d")
		after_str = "created after"
		out = []
		output_msg = None
		try:
			with TaskTable() as table:
				table.ensure_index([("task_id", ASCENDING)], unique=True)
				if after:
					date_query = {"task_create_date": {"$gt": qdate}}
					if pdate:
						cl_date = pdate.strftime("%Y-%m-%d")
						date_query = {"task_create_date": {"$gt": qdate,
														   "$lt": pdate}}
						after_str = "started after %s and ending before %s" % \
						            (str_date, cl_date)
						output_msg = "No task " + after_str
				else:
					date_query = {"task_end_date": {"$lt": qdate}}
					after_str = "ending before"
				results = table.find(date_query, {"_id": False})
				if not results:
					output_msg = "No tasks to list %s this date" % after_str
					log.warning(output_msg)
					return (-102, None)
				for r in results:
					cr_date = r['task_create_date']
					r['task_create_date'] = cr_date.strftime("%Y-%m-%d")
					en_date = r['task_end_date']
					r['task_end_date'] = en_date.strftime("%Y-%m-%d")
					out.append(r)
				if out == []:
					return (404, output_msg)
				log.info("tasks list %s %s = %s", after_str, str_date, out)
				return (200, out)
		except Exception as e:
			log.error(str(e))
			return (-103, "Tasks listing failed")

	@staticmethod
	def get_task(task_id):
		"""
		Get a particular task based on name
		:param task_id: task id of the task
		:return: JSON for the particular task
		"""
		out = []
		try:
			with TaskTable() as table:
				result = table.find({"task_id": {"$eq": task_id}}, {"_id":
					                                                   False})
				if not result:
					log.error("404 - No task with %d task id", task_id)
					return (404, "No task with %d task_id" % task_id)
				log.info("Task is = %s", result)
				for r in result:
					cr_date = r['task_create_date']
					r['task_create_date'] = cr_date.strftime("%Y-%m-%d")
					en_date = r['task_end_date']
					r['task_end_date'] = en_date.strftime("%Y-%m-%d")
					out.append(r)
				if out == []:
					log.error("404 - No task with %d task_id", task_id)
					return (404, "No task with task_id %d" % task_id)
				return (200, out)
		except Exception as e:
			log.error(str(e))
			return (-103, "Task listing failed")

	@staticmethod
	def update_task(task_id, task_name, task_end_date, task_description,
	                task_owner):
		"""
		A method to update the task in db
		:param task_id: task id of the task
		:param task_name: name of the task
		:param task_end_date: end date of the task
		:param task_description: description of task
		:param task_owner: owner of the task
		:return: Success if task entered, else appropriate error
		"""
		current_date = datetime.now()
		update_json = dict()
		input_json = {
						"task_name": task_name,
					    "task_end_date": task_end_date,
					    "task_description": task_description,
					    "task_owner": task_owner
					}
		try:
			with TaskTable() as table:
				if not task_id:
					return (403, "Task id is a mandatory parameter")

				for k, v in input_json.iteritems():
					if v:
						update_json[k] = v
				log.info("Updating following records %s", update_json)
				if task_end_date < current_date:
					return (403, "End date should be greater than create date")
				result = table.update(spec={"task_id": task_id},
				                      document={"$set": update_json},
				                      upsert=False)

				if result['nModified'] == 1 and result['ok'] == 1:
					out = "Task updated successfully with all changes"
					log.info(out)
					return (200, out)
				log.error("-102 - Task update failed %s", result)
				return (-102, "Task update failed.")
		except Exception as e:
			log.error(str(e))
			return (-103, "Task update failed")

	@staticmethod
	def delete_task(task_id):
		"""
		Delete a particular task from the table
		:param task_id: Task id to be deleted
		:return: Number of documents removed
		"""
		try:
			with TaskTable() as table:
				result = table.remove({"task_id": {"$eq": task_id}})
				if result["ok"] != 1 and result['n'] == 0:
					log.error("Failed to delete task %s", task_id)
					return (-104, "Failed to delete task")
				log.info("Task with id %d deleted", task_id)
				return (200, "Task with id %d deleted" % task_id)
		except Exception as e:
			log.error(str(e))
			return (-104, "Task deleteion failed")


add_task = TaskTable.add_task
list_all_tasks = TaskTable.list_all_tasks
list_based_on_date = TaskTable.list_based_on_date
delete_task = TaskTable.delete_task
update_task = TaskTable.update_task