#!.venv/bin/python
# file : concat_csv.py
# Concatenate CSV of the same format
# requires python >= 3.10

# system modules
from __future__ import print_function
import sys, os
import logging
import argparse
import csv, glob

# pip modules

# custom modules
import marcelbroccoli.errorcodes as marcelec
import marcelbroccoli.functions as marcelfn
import marcelbroccoli.logger as marcellg

# meta definitions
__author__ = "Marcel Gerber"
__date__ = "2024-03-17"

# custom error codes
errorcode = marcelec.SUCCESS
ERR_INSUFF_SRC = 1001

# initialize variables for function defaults
logger = logging.getLogger(__file__)

# command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--source-csv', type=str, nargs='+', required=True, help='Source CSV file(s) to read from (supports wildcards)')
parser.add_argument('-d', '--destination-csv', type=str, required=True, help='Destination CSV file to write to')
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
	# errorcode += marcelfn.load_env()

	# load config file
	# cfg = marcelfn.load_config_file(args.config_file)

	# define log file
	if 'LOG_FILE' in os.environ: log_file = os.environ['LOG_FILE']
	else: log_file = 'clean_remote_folders_sms.log'
	log_file = os.path.abspath(log_file)

	# setup logger
	errorcode += logger.configure(logfile=log_file, name=__name__, level=args.log_level, dtformat="%Y-%m-%d %H:%M:%S.%f")
	
	# start log
	logger.info("Welcome to the CSV Concatenate Script.")
	logger.info("Log file is '{}'".format(log_file))
	logger.debug("Log level: {}".format(marcellg.logger.level))

	# check source
	if len(args.source_csv) < 2:
		logger.error("Error: there must be at least 2 source CSV files.")
		errorcode += ERR_INSUFF_SRC

	# proceed if no initial errors
	if errorcode == marcelec.SUCCESS:
		all = []

		# read files
		for src in args.source_csv:
			room_id = os.path.basename(src)[6]
			count = 0
			with open(src) as csvfile:
				csvsrc = csv.DictReader(csvfile, delimiter=',')
				fieldnames = csvsrc.fieldnames
				fieldnames.append('RoomId')
				for row in csvsrc:
					row['RoomId'] = room_id
					all.append(row)

		# print(all)
		# sort
		# sorted(all)

		# write to new file
		with open(args.destination_csv, 'w', newline='') as csvfile:
			csvdst = csv.DictWriter(csvfile, delimiter=';', quoting=csv.QUOTE_ALL, fieldnames=fieldnames)
			csvdst.writeheader()
			for row in all:
				csvdst.writerow(row)

	# end of script
	logger.info("Script execution completed with exit code {}.".format(errorcode))
	sys.exit(errorcode)
