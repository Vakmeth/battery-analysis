import pandas as pd
import warnings
import numpy as np
import statistics as st

import helper_functions as hf

def calculate_change(cell_dataframes, cycles, instruction, target_value):
    cell_sum = []
    for cell_index, cell in enumerate(cell_dataframes):
        cycle_sum = []
        for cycle in cycles:
            significant_data = cell
            if cell_index == 0:
                significant_data = significant_data[significant_data['Cycle'] == cycle]
                significant_data = significant_data[significant_data['Instruction Name'] == instruction]

                # Get beginning and end values
                cycle_beginning_value = significant_data[target_value].iloc[0]
                cycle_ending_value = significant_data[target_value].iloc[-1]

                cycle_sum.append(abs(cycle_beginning_value - cycle_ending_value))
            else:
                significant_data = significant_data[significant_data['Cycle.' + str(cell_index)] == cycle]
                significant_data = significant_data[significant_data['Instruction Name.' + str(cell_index)] == instruction]

                 # Get currents
                cycle_beginning_value = significant_data[target_value + '.' + str(cell_index)].iloc[0]
                cycle_ending_value = significant_data[target_value + '.' + str(cell_index)].iloc[-1]

                cycle_sum.append(abs(cycle_beginning_value - cycle_ending_value))
        cell_sum.append(st.mean(cycle_sum))  
    return st.mean(cell_sum)

# Suppress the DtypeWarning related to mixed data types in the CSV file
warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)  

# Define file to analyse and relevant cycles in it
file_path = '24-003_PhysicalTwin_Diagnostic_Test14525.csv'
cycles = [ 2., 3., 4., 5.]

# Read csv data into pandas dataframe and reduce it to the needed values
battery_dataframe = pd.read_csv(file_path)
reduced_dataframe_battery = hf.reduced_dataframe(battery_dataframe, cycles)

# Split dataframe into dataframes per cell
cell_dataframes = hf.get_cell_dataframes(battery_dataframe)

# Calculate charge from each cell and print results
average_charge =  calculate_change(cell_dataframes, cycles, 'V Charge', 'Charge Capacity (mAh)')
average_discharge =  calculate_change(cell_dataframes, cycles, 'I Disch.', 'Discharge Capacity (mAh)')
print("Average change in ch: " + str(average_charge) + " mAh")
print("Average change in dc: " + str(average_discharge) + " mAh")