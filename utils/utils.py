import sys
import logging as log

from datetime import datetime
from flask import jsonify


def validate_date(date_str):
	"""
	Validate a given date against "YYYY-MM-DD" format
	:param date_str: date string
	:return: Raises a value error
	"""
	try:
		return (datetime.strptime(date_str, "%Y-%m-%d"), "Date format matched")
	except Exception as e:
		log.error(sys.exc_info()[0], e)
		return (None, "Date should be of YYYY-MM-DD format")

def get_response_json(status, msg):
	"""
	Returns a jsonified response object
	:param status:
	:param msg:
	:return: JSON
	"""
	response = dict()
	response['status'] = status
	response['result'] = msg
	return jsonify(**response)
