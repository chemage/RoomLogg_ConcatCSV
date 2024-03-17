#!.venv/bin/python
# file : <script_name>
# <script_description>
# requires python >= 3.10

# system modules
from __future__ import print_function
import sys, os
import logging
import argparse

# pip modules

# custom modules
import marcelbroccoli.errorcodes as marcelec
import marcelbroccoli.functions as marcelfn
import marcelbroccoli.logger as marcellg

# meta definitions
__author__ = "<author>"
__date__ = "<date>"

# custom error codes
errorcode = marcelec.SUCCESS

# initialize variables for function defaults
logger = logging.getLogger(__file__)

# command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config-file', type=str, default='config.json', help='Configuration file (default: config.json).')
parser.add_argument('-l', '--log-level', type=str, default=logging.ERROR, help='Log level for script execution.')


'''
Main Attraction
'''
if __name__ == '__main__':

	# parse command-line arguments
	args = parser.parse_args()
  
	# set working dir
	working_dir = os.path.abspath(os.path.dirname(__file__))
	os.chdir(working_dir)

	# load .env
	errorcode += marcelfn.load_env()

	# load config file
	cfg = marcelfn.load_config_file(args.config_file)

	# define log file
	if 'LOG_FILE' in os.environ: log_file = os.environ['LOG_FILE']
	else: log_file = 'clean_remote_folders_sms.log'
	log_file = os.path.abspath(log_file)

	# setup logger
	errorcode += logger.configure(logfile=log_file, name=__name__, level=LOG_LEVEL, dtformat="%Y-%m-%d %H:%M:%S.%f")
	
	# start log
	logger.info("Welcome to the Logger Test Script.")
	logger.info("Log file is '{}'".format(log_file))
	logger.debug("Log level: {}".format(marcellg.logger.level))

	# end of script
	logger.info("Script execution completed with exit code {}.".format(errorcode))
	sys.exit(errorcode)
