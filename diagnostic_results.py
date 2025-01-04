import pandas as pd
import ch_dch_plot as cdp
import matplotlib.pyplot as plt
import random
import statistics as st
import numpy as np

# Define file to analyse and read out dataframe from it
file_path_cell_1 = 'data_export/Cell2_Diagnostic_Test14893.csv'
file_path_cell_2 = 'data_export/Cell3_Diagnostic_Test14917.csv'
file_path_cell_3 = 'data_export/Cell5_Diagnostic_Test15138.csv'
cell_dataframe_1 = pd.read_csv(file_path_cell_1)
cell_dataframe_2 = pd.read_csv(file_path_cell_2)
cell_dataframe_3 = pd.read_csv(file_path_cell_3)

cell_dataframes = [cell_dataframe_1, cell_dataframe_2]

# Define analyzed cycles
CYCLES = [2, 3, 4]

# CH / DCH 
# -------------------------------------------------- #
fig, ax = plt.subplots(figsize=(5, 2.7))
ax.set_xlabel("Time")
ax.set_ylabel("Capacity")

for cell_dataframe in cell_dataframes:
    for cycle in CYCLES:
        data = cdp.plot_ch_dch(cell_dataframe, cycle) 
        
        # Plot CH and DCH figure for this cycle
        ax.plot(data["ch"]["time_points"], data["ch"]["capacity_points"], color='blue')
        ax.plot(data["dch"]["time_points"], data["dch"]["capacity_points"], color='green')

# -------------------------------------------------- # 


# SOC 
# -------------------------------------------------- #
fig2, ax2 = plt.subplots(figsize=(5, 2.7))
ax2.set_xlabel("Time")
ax2.set_ylabel("SOC")

for cell_dataframe in cell_dataframes:
    random_color = (random.random(), random.random(), random.random())
    for cycle in CYCLES:
        # Filter data
        filtered_frame = cell_dataframe[cell_dataframe['Cycle'] == cycle]
        soc_dataframe = filtered_frame[filtered_frame['Step'].isin([21, 23])]
        INITIAL_SOC = 0

        # Integrate current
        current = soc_dataframe['Current (mA)']
        DELTA_T = 1 / 3600
        # Calculate total charge using numerical integration
        total_charge = sum(I * DELTA_T for I in current)

        # Calculate nominal capacity
        nominal_capacity = soc_dataframe['Charge Capacity (mAh)'].mean()
        soc_values = []

        for row in soc_dataframe.iterrows():
            soc_values.append(INITIAL_SOC + total_charge / nominal_capacity)
            INITIAL_SOC = soc_values[-1]
        
        plt.plot(soc_dataframe['Total Time (Seconds)'], soc_values, 
                label='State of Charge (SOC)', color=random_color)

# -------------------------------------------------- # 


# OCV (with first cell)
# -------------------------------------------------- #
filtered = cell_dataframe_1[cell_dataframe_1['Step'].isin([23])]
data = filtered[filtered['Cycle'] == 2]
data['Total Time (Seconds)'] = range(1, len(data) + 1)

# Constants (set these based on your system)

C_nominal = 109.0  # Nominal battery capacity in Ah
SOC_initial = 0  # Initial SOC in percentage

# Convert current from mA to A, and time from seconds
data['Current_A'] = data['Current (mA)'] / 1000
data['Time_h'] = data['Total Time (Seconds)'] / 3600
data['voltage_V'] = data['Voltage (mV)'] / 1000

# Calculate charge consumed (cumulative sum of Current * Time interval)
data['Charge_Consumed_Ah'] = np.cumsum(data['Current_A'] * np.diff([0] + list(data['Time_h'])))

# Calculate SOC
data['SOC'] = SOC_initial - (data['Charge_Consumed_Ah'] / C_nominal) * 100

# Ensure SOC does not go below 0
data['SOC'] = np.maximum(data['SOC'], 0)

# Plot U/V vs SOC
plt.figure(figsize=(10, 6))
plt.plot(data['SOC'][::-1], data['voltage_V'], label='Voltage vs SOC', color='blue')
plt.xlabel('SOC (%)')
plt.ylabel('Voltage (V)')
plt.title('Voltage vs State of Charge (SOC)')

# -------------------------------------------------- #


# SHOW PLOT
# -------------------------------------------------- #
plt.grid(True)
plt.show()
plt.legend()