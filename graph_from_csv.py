#!.venv/bin/python
# file : graph_from_csv.py
# Create graph from CSV
# requires python >= 3.10

# system modules
import sys, os
import logging
import argparse
import csv, glob

# pip modules
import pandas as pd
import plotly.express as px

# custom modules
import marcelbroccoli.errorcodes as marcelec
import marcelbroccoli.config as marcelcf
import marcelbroccoli.logger as marcellg

# meta definitions
__author__ = "Marcel Gerber"
__date__ = "2024-04-03"

# custom error codes
errorcode = marcelec.SUCCESS
ERR_INSUFF_SRC = 1001

# initialize variables for function defaults
logger = logging.getLogger(__file__)

# command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--source-csv', type=str, nargs='+', required=True, help='Source CSV file(s) to read from (supports wildcards)')
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

	# load config file
	cfg = marcelcf.load_config_file(args.config_file)
	num_sensors = cfg['num_sensors']

	# define log file
	if 'LOG_FILE' in os.environ: log_file = os.environ['LOG_FILE']
	else: log_file = f'{__file__}.log'
	log_file = os.path.abspath(log_file)

	# setup logger
	errorcode += logger.configure(logfile=log_file, name=__name__, level=args.log_level, dtformat="%Y-%m-%d %H:%M:%S.%f")
	
	# start log
	logger.info("Welcome to the CSV Concatenate Script.")
	logger.info("Log file is '{}'".format(log_file))
	logger.debug("Log level: {}".format(marcellg.logger.level))

	# check source
	source_csv_files = args.source_csv
	if len(source_csv_files) < num_sensors:
		logger.error("Error: there must be num_sensors source CSV files.")
		if type(source_csv_files) is list and glob.escape(source_csv_files[0]) != source_csv_files:
			logger.info("Make sure that the file pattern matches your files with the 'ls' command.")
		errorcode += ERR_INSUFF_SRC

	# proceed if no initial errors
	if errorcode == marcelec.SUCCESS:
		df_rooms = pd.DataFrame()

		# read source files
		for src in source_csv_files:
			logger.info(f"Processing file '{src}'.")
			room_id = int(os.path.basename(src)[5])
			room_name = cfg['rooms'][str(room_id)]
			count = 0
			try:
				df_room = pd.read_csv(src, sep=',', header=0, names=cfg['fieldnames'])
				df_room['DateTime'] = pd.to_datetime(df_room['DateTime'])
				df_room['Sensor'] = room_name
				df_rooms = pd.concat([df_rooms, df_room])
			except Exception as e:
				logger.error(f"Issue with row. {e}")
		
		# print(df_rooms)

		# Plot the data
		fig = px.line(df_rooms, x="DateTime", y="Temperature(C)", color="Sensor",
					title="Temperature Readings Over Time by Sensor",
					labels={"DateTime": "Date and Time", "Temperature(C)": "Temperature (°C)"},
					template="plotly_dark")

		# Show the plot
		fig.show()

