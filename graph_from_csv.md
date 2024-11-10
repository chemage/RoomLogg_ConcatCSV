# Script `graph_from_csv.py`

[Home](README.md)

## Overview

This script creates and displays a graph using the consolidated files per room.

It uses `plotly` to build a dynamic plot.

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
$ .venv/bin/python graph_from_csv.py -h
usage: graph_from_csv.py [-h] -s SOURCE_CSV [SOURCE_CSV ...] [-c CONFIG_FILE] [-l LOG_LEVEL]

options:
  -h, --help            show this help message and exit
  -s SOURCE_CSV [SOURCE_CSV ...], --source-csv SOURCE_CSV [SOURCE_CSV ...]
                        Source CSV file(s) to read from (supports wildcards)
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        Configuration file (default: config.json).
  -l LOG_LEVEL, --log-level LOG_LEVEL
                        Log level for script execution.
```

### Example 1

This will show all debug logs.

```shell
.venv/bin/python graph_from_csv.py -s ~/Documents/Appart/RoomLogg/2024_ALL/room_?.csv
```

## Exit Codes

|Code|Description|
|---|---|
|0|SUCCESS|
|1001|Not enough source files. At least x files are required (x depends on number of sensors)|
