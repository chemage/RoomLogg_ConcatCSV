#!.venv/bin/python
# file : transform_raw_data.py
# Transform RoomLogg PRO CSV data to Excel keeping only temperatures.
# requires python >= 3.10

# system modules
import sys, os, pathlib
import logging
import argparse
import glob

# pip modules
import pandas as pd

# custom modules
import marcelbroccoli.errorcodes as marcelec
import marcelbroccoli.functions as marcelfn
import marcelbroccoli.logger as marcellg

# meta definitions
__author__ = "Marcel Gerber"
__date__ = "2024-05-03"

# custom error codes
errorcode = marcelec.SUCCESS
ERR_INSUFF_SRC = 1001

# initialize variables for function defaults
logger = logging.getLogger(__file__)

# command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--source-csv', type=str, nargs='+', required=True, help='Source CSV file(s) to read from (supports wildcards)')
parser.add_argument('-d', '--destination', type=str, required=True, help='Destination folder to write to')
parser.add_argument('-ns', '--num-sensors', type=int, choices=range(1, 8), default=5, help='Number of sensors (default: %(default)i).')
# parser.add_argument('-c', '--config-file', type=str, default='config.json', help='Configuration file (default: %(default)s).')
parser.add_argument('-ll', '--log-level', type=int, default=logging.INFO, help='Log level for script execution (default: %(default)i).')
parser.add_argument('-lf', '--log-file', type=str, default=f'{os.path.basename(__file__)}.log', help='Log file (default: %(default)s).')


'''
Main Attraction
'''
if __name__ == '__main__':

	# parse command-line arguments
	args = parser.parse_args()
	num_sensors = args.num_sensors
	dest_path = args.destination
  
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
	if len(source_csv_files) < num_sensors:
		logger.error("Error: there must be num_sensors source CSV files.")
		if type(source_csv_files) is list and glob.escape(source_csv_files[0]) != source_csv_files:
			logger.info("Make sure that the file pattern matches your files with the 'ls' command.")
		errorcode += ERR_INSUFF_SRC

	# proceed if no initial errors
	if errorcode == marcelec.SUCCESS:
		fieldnames = ['DateTime']
		for i in range(1, num_sensors+1): fieldnames.append(f"Temp_{i}")
		df_all = pd.DataFrame(columns=['DateTime'])

		# read source files
		dict_df = {}
		for src in source_csv_files:
			logger.info(f"Processing file '{src}'.")
			room_id = int(os.path.basename(src)[5])
			count = 0
			try:
				pd_room = pd.read_csv(src, sep=',', header=0, names={
						"DateTime": "Time", 
						f"Temp_{room_id}": "Temperature(C)", 
						f"Humidity_{room_id}": "Humidity(%)", 
						f"Dewpoint_{room_id}": "Dewpoint(C)", 
						f"HeatIndex_{room_id}": "HeatIndex(C)"
					})
				if room_id in dict_df:
					dict_df[room_id] = pd.concat([dict_df[room_id], pd_room])
				else:
					dict_df[room_id] = pd_room
			except Exception as e:
				logger.error(f"Issue with row. {e}")

		# clean data
		for room_id in range(1, num_sensors+1):
			# drop duplicates
			dict_df[room_id].drop_duplicates()

			# export to channel to file
			dest_file = os.path.join(dest_path, f"{room_id}.csv")
			dict_df[room_id].to_csv(dest_file, encoding='utf-8', index=False)

		# merge dataframes together
		for room_id in range(1, num_sensors+1):
			logger.info(f"Merging channel '{room_id}'.")
			room_id = room_id
			df_all = pd.merge(df_all, dict_df[room_id], on='DateTime', how='outer')
		
		# export to file
		# dest_file = os.path.join(dest_path, "all.xlsx")
		# logger.info(f"Export to file '{dest_file}'.")
		# # df_all.to_excel(dest_file, sheet_name='RoomLogg PRO', index=False)
		dest_file = os.path.join(dest_path, "all.csv")
		logger.info(f"Export to file '{dest_file}'.")
		df_all.to_csv(dest_file, encoding='utf-8',index=False)

	# end of script
	logger.info("Script execution completed with exit code {}.".format(errorcode))
	sys.exit(errorcode)
