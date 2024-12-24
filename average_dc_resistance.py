import pandas as pd
import warnings
import numpy as np
import statistics as st

import helper_functions as hf

# Suppress the DtypeWarning related to mixed data types in the CSV file
warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)  

def calculate_dcr(cell_dataframes, cycles):
    cell_sum = []
    for cell_index, cell in enumerate(cell_dataframes):
        cycle_sum = []
        for cycle in cycles:
            significant_data = cell
            if cell_index == 0:
                significant_data = significant_data[significant_data['Cycle'] == cycle]
                significant_data = significant_data[significant_data['Instruction Name'] == 'V Charge']

                # Get currents
                first_current = significant_data['Current (mA)'].iloc[0]
                second_current = significant_data['Current (mA)'].iloc[-1]

                # Get Volts 
                first_voltage = significant_data['Voltage (mV)'].iloc[0]
                second_voltage = significant_data['Voltage (mV)'].iloc[-1]

                cycle_sum.append((first_voltage - second_voltage) / (second_current - first_current))
            else:
                significant_data = significant_data[significant_data['Cycle.' + str(cell_index)] == cycle]
                significant_data = significant_data[significant_data['Instruction Name.' + str(cell_index)] == 'V Charge']

                 # Get currents
                first_current = significant_data['Current (mA).' + str(cell_index)].iloc[0]
                second_current = significant_data['Current (mA).' + str(cell_index)].iloc[-1]

                # Get Volts 
                first_voltage = significant_data['Voltage (mV).' + str(cell_index)].iloc[0]
                second_voltage = significant_data['Voltage (mV).' + str(cell_index)].iloc[-1]

                cycle_sum.append((first_voltage - second_voltage) / (second_current - first_current))
        cell_sum.append(st.mean(cycle_sum))  
    return st.mean(cell_sum)

# Define file to analyse and relevant cycles in it
file_path = '24-003_PhysicalTwin_Diagnostic_Test14525.csv'
cycles = [2., 3., 4.]

# Read csv data into pandas dataframe and reduce it to the needed values
battery_dataframe = pd.read_csv(file_path)
reduced_dataframe_battery = hf.reduced_dataframe(battery_dataframe, cycles)

# Split dataframe into dataframes per cell
cell_dataframes = hf.get_cell_dataframes(battery_dataframe)

average_dcr = calculate_dcr(cell_dataframes, cycles)

print(average_dcr)

