import pandas as pd
import ch_dch_plot as cdp
import matplotlib.pyplot as plt
import random
import statistics as st

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


# OCV
# -------------------------------------------------- #
# Define a current threshold near zero
# Battery parameters


# -------------------------------------------------- #


# SHOW PLOT
# -------------------------------------------------- #
plt.grid(True)
plt.show()
plt.legend()