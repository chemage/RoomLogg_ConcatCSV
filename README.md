# Python CSV Concatenation Script

## Overview

## Requirements and Setup

### Create a new virtual environment

```shell
python -m venv .venv
source .venv/bin/activate
.venv/bin/python -m pip install pip --force
pip install -r requirements.txt
```

## Script Usage

```shell
$ ./concat_csv.py -h
usage: concat_csv.py [-h] -s SOURCE_CSV [SOURCE_CSV ...] -d DESTINATION_CSV [-ll LOG_LEVEL] [-lf LOG_FILE]

options:
  -h, --help            show this help message and exit
  -s SOURCE_CSV [SOURCE_CSV ...], --source-csv SOURCE_CSV [SOURCE_CSV ...]
                        Source CSV file(s) to read from (supports wildcards)
  -d DESTINATION_CSV, --destination-csv DESTINATION_CSV
                        Destination CSV file to write to
  -ll LOG_LEVEL, --log-level LOG_LEVEL
                        Log level for script execution (default: 10).
  -lf LOG_FILE, --log-file LOG_FILE
                        Log file (default: concat_csv.py.log).
```

### Example 1

This will show all debug logs.

```shell
./concat_csv.py -s ~/Documents/Appart/RoomLogg/2*/*.CSV -d ~/Documents/Appart/RoomLogg/all.csv -ll 0
```

## Exit Codes

|Code|Description|
|---|---|
|0|SUCCESS|
|1001|Not enough source files. At least 2 files are required|

## CaveAts

### Glob Issue

When using a wildcard pattern which doesn't match, there is no specific error.

This example does not match if the files are *.CSV.

```shell
./concat_csv.py -s ~/Documents/Appart/RoomLogg/2*/*.csv -d ~/Documents/Appart/RoomLogg/all.csv
```

The output will read as follows.

```log
$ ./concat_csv.py -s ~/Documents/Appart/RoomLogg/2*/*.csv -d all.csv
-------------------------------------------------------------------------------
Welcome to the CSV Concatenate Script.
Log file is 'concat_csv.py.log'
Error: there must be at least 2 source CSV files.
Make sure that the file pattern matches your files with the 'ls' command.
Script execution completed with exit code 1001.
```
