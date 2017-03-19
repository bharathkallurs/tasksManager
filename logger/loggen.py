import os
import logging as log
from datetime import datetime


def set_log_params(log_file=None, level=log.DEBUG):
	"""
	Set logging parameters for task application
	:param log_file: Place to tail current logs. Defaults to None
	:param level: logging level. DEBUG, INFO, etc
	:return: None
	"""
	current_time = str(datetime.now().strftime('%Y%m%d_%H%M%S'))
	if not log_file:
		dir_path = os.path.dirname(os.path.realpath(__file__))
		log_file = dir_path + "/logs/tasker_%s.log" % current_time
		if not os.path.exists(dir_path + '/logs/'):
			os.makedirs(dir_path + '/logs/')

	log.basicConfig(filename=log_file,
	                format='%(levelname)s:%(asctime)s:%(message)s',
	                level=level)
	log.info("Starting Task App Logger at %s", current_time)
