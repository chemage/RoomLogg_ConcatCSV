# Script `transform_raw_data.py`

[Home](README.md)

## Overview

This script transforms data from the different RoomLogg PRO CSV into a single CSV.

## Requirements

### RoomLogg PRO

Data must be stored on a MicroSD card.

Copy CSV files as is.

Check that files are not corrupt, which can happen if the card was used before.

### Configuration File

the configuration file must look like this.

```json
{
	"rooms": {"1": "salon", "2": "chambre à coucher", "3": "cuisine", "4": "bureau", "5": "extérieur"},
	"num_sensors": 5,
	"fieldnames": ["DateTime", "Temperature(C)", "Humidity(%)", "Dewpoint(C)", "HeatIndex(C)"]
}
```

## Script Usage

```shell
$ python3 transform_raw_data.py -h
usage: transform_raw_data.py [-h] -s SOURCE_CSV [SOURCE_CSV ...] -d DESTINATION [-ns {1,2,3,4,5,6,7}] [-c CONFIG_FILE] [-ll LOG_LEVEL]
                             [-lf LOG_FILE]

options:
  -h, --help            show this help message and exit
  -s SOURCE_CSV [SOURCE_CSV ...], --source-csv SOURCE_CSV [SOURCE_CSV ...]
                        Source CSV file(s) to read from (supports wildcards)
  -d DESTINATION, --destination DESTINATION
                        Destination folder to write to
  -ns {1,2,3,4,5,6,7}, --num-sensors {1,2,3,4,5,6,7}
                        Number of sensors (default: 5).
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        Configuration file (default: config.json).
  -ll LOG_LEVEL, --log-level LOG_LEVEL
                        Log level for script execution (default: 20).
  -lf LOG_FILE, --log-file LOG_FILE
                        Log file (default: transform_raw_data.py.log).
```

### Example 1

This will show all debug logs.

```shell
.venv/bin/python ./transform_raw_data.py -s ~/Documents/Appart/RoomLogg/2024_ALL/room_?.csv -d ~/Documents/Appart/RoomLogg/2024_ALL/ -ll 0
```

## Exit Codes

|Code|Description|
|---|---|
|0|SUCCESS|
|1001|Not enough source files. At least x files are required (x depends on number of sensors)|

## CaveAts

### Glob Issue

When using a wildcard pattern which doesn't match, there is no specific error.

This example does not match if the files are *.CSV.

```shell
.venv/bin/python ./transform_raw_data.py -s ~/Documents/Appart/RoomLogg/2024_ALL/room_?.csv -d ~/Documents/Appart/RoomLogg/2024_ALL/
```

The output will read as follows.

```log
$ python3 transform_raw_data.py -s ~/Documents/Appart/RoomLogg/2*/*.csv -d all.xlsx
-------------------------------------------------------------------------------
Welcome to the CSV Concatenate Script.
Log file is 'transform_raw_data.py.log'
Error: there must be at least 5 source CSV files.
Make sure that the file pattern matches your files with the 'ls' command.
Script execution completed with exit code 1001.
```
