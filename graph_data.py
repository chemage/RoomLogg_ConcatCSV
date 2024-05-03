#!.venv/bin/python
# file : graph_data.py
# Create a graph from concatenated CSV.
# Base from ChatGPT.
# requires python >= 3.10

# system modules
import os
import matplotlib.pyplot as plt
import csv
from datetime import datetime

# Read data from CSV file
data_file = "/home/mgerber/Documents/Appart/RoomLogg/all.csv"

dates = []
temps = [[] for _ in range(5)]

count_errors = 0
with open(data_file, 'r') as file:
	reader = csv.reader(file)
	next(reader)  # Skip header
	for row in reader:
		dates.append(datetime.strptime(row[0], "%Y/%m/%d %H:%M"))
		for i in range(5):
			try:
				temps[i].append(float(row[i + 1]))
			except ValueError as ve:
				count_errors += 1
				# print(f"Error at line number {reader.line_num}. {ve}")

# show errors found in file
print(f"Found {count_errors} errors in CSV file.")

# Plot data
plt.figure(figsize=(10, 6))
plt.plot(dates, temps[0], label='temp_1')
plt.plot(dates, temps[1], label='temp_2')
plt.plot(dates, temps[2], label='temp_3')
plt.plot(dates, temps[3], label='temp_4')
plt.plot(dates, temps[4], label='temp_5')

# Add labels and legend
plt.xlabel('Date and Time')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Data')
plt.legend()

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Show plot
plt.tight_layout()
plt.show()
