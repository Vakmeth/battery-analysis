import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Define file to analyse and relevant cycles in it
file_path = 'data_export/Cell2_Diagnostic_Test14893.csv'
steps  = [21, 22]

# Read csv data into pandas dataframe and reduce it to the needed values
battery_dataframe = pd.read_csv(file_path)
reduced_dataframe = battery_dataframe[battery_dataframe['Step'].isin(steps)]

# Datapoints to plot
capacity_points = []
time_points = []

for step in steps:
    temporary_frame = reduced_dataframe[reduced_dataframe['Step'] == step]
    filtered_frame = temporary_frame[temporary_frame['Cycle'] == 2]
    capacity_points.append(filtered_frame['Charge Capacity (mAh)'].iloc[0])
    time_points.append(filtered_frame['Total Time (Seconds)'].iloc[0])

temporary_frame = reduced_dataframe[reduced_dataframe['Step'] == 22]
filtered_frame = temporary_frame[temporary_frame['Cycle'] == 2]
capacity_points.append(filtered_frame['Charge Capacity (mAh)'].iloc[-1])   
time_points.append(filtered_frame['Total Time (Seconds)'].iloc[-1])

# Create a figure containing a single Axes.
fig, ax = plt.subplots(figsize=(5, 2.7))
ax.plot(time_points, capacity_points)
ax.set_xlabel("Time")
ax.set_ylabel("Capacity")
plt.show()