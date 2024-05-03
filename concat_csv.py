#!.venv/bin/python
# file : concat_csv.py
# Concatenate CSV of the same format
# requires python >= 3.10

# system modules
from __future__ import print_function
import sys, os, pathlib
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
# parser.add_argument('-c', '--config-file', type=str, default='config.json', help='Configuration file (default: %(default)s).')
parser.add_argument('-ll', '--log-level', type=int, default=logging.INFO, help='Log level for script execution (default: %(default)i).')
parser.add_argument('-lf', '--log-file', type=str, default=f'{os.path.basename(__file__)}.log', help='Log file (default: %(default)s).')


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

	# setup logger
	log_file = args.log_file
	errorcode += logger.configure(logfile=log_file, name=__name__, level=args.log_level, dtformat="%Y-%m-%d %H:%M:%S.%f")
	
	# start log
	logger.info("Welcome to the CSV Concatenate Script.")
	logger.info(f"Log file is '{log_file}'")
	logger.debug(f"Log level: {marcellg.logger.level}")

	# check source
	source_csv_files = args.source_csv
	if len(source_csv_files) < 2:
		logger.error("Error: there must be at least 2 source CSV files.")
		if type(source_csv_files) is list and glob.escape(source_csv_files[0]) != source_csv_files:
			logger.info("Make sure that the file pattern matches your files with the 'ls' command.")
		errorcode += ERR_INSUFF_SRC

	# proceed if no initial errors
	if errorcode == marcelec.SUCCESS:
		all = []

		# read files
		for src in source_csv_files:
			room_id = os.path.basename(src)[6]
			count = 0
			logger.debug(f"Processing file '{src}'.")
			with open(src) as csvfile:
				try:
					csvsrc = csv.DictReader(csvfile, delimiter=',')
					# fieldnames = csvsrc.fieldnames
					# fieldnames.append('RoomId')
					for row in csvsrc:
						# skip existing records
						item = next((item for item in all if item['datetime'] == row['Time']), None)
						if item:
							item['temp_'+room_id] = row['Temperature(C)']
						else:
							data = {'datetime': row['Time'], 'temp_'+room_id: row['Temperature(C)']}
							all.append(data)
						# row['RoomId'] = room_id
				except Exception as e:
					logger.warn(f"Unable to read file '{src}'. Skipping file.")

		# print(all)
		# sort
		# sorted(all)

		# write to new file
		fieldnames = ['datetime', 'temp_1', 'temp_2', 'temp_3', 'temp_4', 'temp_5']
		with open(args.destination_csv, 'w', newline='') as csvfile:
			csvdst = csv.DictWriter(csvfile, delimiter=';', quoting=csv.QUOTE_ALL, fieldnames=fieldnames)
			csvdst.writeheader()
			for row in all:
				csvdst.writerow(row)

	# end of script
	logger.info("Script execution completed with exit code {}.".format(errorcode))
	sys.exit(errorcode)
