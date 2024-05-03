#!.venv/bin/python
# file : graph_data.py
# Create a graph from concatenated CSV.
# Base from ChatGPT.
# requires python >= 3.10

# system modules
import os
import matplotlib.pyplot as plt
import csv
import pandas as pd
from datetime import datetime

# variables
data_file = "/home/mgerber/Documents/Appart/RoomLogg/all.xlsx"
num_sensors = 5

# read data file
temps = {}
for i in range(1, num_sensors+1):
	print(f"Read room ID {i}.")
	columns = ['DateTime', f"Temp_{i}"]
	temps[i] = pd.read_excel(data_file, usecols=columns)

# Plot data
plt.figure(figsize=(10, 6))
for i in range(1, num_sensors+1):
	print(f"Plot room ID {i}.")
	plt.plot(temps[i]['DateTime'], temps[i][f"Temp_{i}"], label=f'temp_{i}')

# plt.plot(dates, temps[1], label='temp_2')
# plt.plot(dates, temps[2], label='temp_3')
# plt.plot(dates, temps[3], label='temp_4')
# plt.plot(dates, temps[4], label='temp_5')

# Add labels and legend
print("Add plot legends and labels.")
plt.xlabel('Date and Time')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Data')
plt.legend()

# Rotate x-axis labels for better readability
print("Rotate graph.")
plt.xticks(rotation=45)

# Show plot
print("Show plot.")
plt.tight_layout()
plt.show()
