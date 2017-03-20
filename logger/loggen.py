import os
import logging as log
from datetime import datetime
from shutil import copyfile


current_time = str(datetime.now().strftime('%Y%m%d_%H%M%S'))
dir_path = os.path.dirname(os.path.realpath(__file__))

def set_log_params(log_file=None, level=log.DEBUG):
	"""
	Set logging parameters for task application
	:param log_file: Place to tail current logs. Defaults to None
	:param level: logging level. DEBUG, INFO, etc
	:return: None
	"""
	global current_time, dir_path
	if not log_file:
		log_file = dir_path + "/logs/latest.log"
		if not os.path.exists(dir_path + '/logs/'):
			os.makedirs(dir_path + '/logs/')
		if os.path.exists(log_file):
			os.remove(log_file)

	log.basicConfig(filename=log_file,
	                format='%(levelname)s:%(asctime)s:%(filename)s:%(message)s',
	                level=level)
	log.info("Starting Task App Logger at %s", current_time)

def move_latest_log_to_persistent_file():
	"""
	Moving the latest.log to time based logger file
	:return: None
	"""
	global current_time, dir_path
	src = dir_path + "/logs/latest.log"
	dst = dir_path + "/logs/tasker_" + current_time + ".log"
	copyfile(src, dst)
