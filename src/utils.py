#!/usr/bin/python3

import logging

def get_log(log_file):
	
	"""
	Create logger.
	"""
	
	logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s]:  %(message)s")
	logger = logging.getLogger()

	fileHandler = logging.FileHandler(log_file)
	fileHandler.setLevel(logging.DEBUG)
	logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]:  %(message)s")
	fileHandler.setFormatter(logFormatter)
	logger.addHandler(fileHandler)
	
	logger.info("Created logfile "+log_file)

	return logger
