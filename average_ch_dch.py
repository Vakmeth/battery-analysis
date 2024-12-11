import pandas as pd
import warnings
import statistics as st

import helper_functions as hf

# Suppress the DtypeWarning related to mixed data types in the CSV file
warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)  

def calculate_avg_value(cell_dataframes, cycles, instruction_name, attribute_name):
    cell_sum = []
    for cell_index, cell in enumerate(cell_dataframes):
        cycle_sum = []
        for cycle in cycles:
            significant_data = cell
            if cell_index == 0:
                significant_data = cell[cell['Instruction Name'] == instruction_name]
                significant_data = significant_data[significant_data['Cycle'] == cycle]
                cycle_sum.append(significant_data[attribute_name].max())
            else:
                significant_data = cell[cell['Instruction Name.' + str(cell_index)] == instruction_name]
                significant_data = significant_data[significant_data['Cycle.' + str(cell_index)] == cycle]
                cycle_sum.append(significant_data[attribute_name + '.' + str(cell_index)].max())
        cell_sum.append(st.mean(cycle_sum))  
    return st.mean(cell_sum)

# Define file to analyse and relevant cycles in it
file_path = '/home/megli2/Downloads/24-003_PhysicalTwin_Diagnostic_Test14525.csv'
cycles = [2., 3., 4.]

# Read csv data into pandas dataframe and reduce it to the needed values
battery_dataframe = pd.read_csv(file_path)
reduced_dataframe_battery = hf.reduced_dataframe(battery_dataframe, cycles)

# Split dataframe into dataframes per cell
cell_dataframes = hf.get_cell_dataframes(battery_dataframe)

# Calculate charge from each cell and print results
average_charge = calculate_avg_value(cell_dataframes, cycles, 'V Charge', 'Charge Capacity (mAh)')
average_discharge = calculate_avg_value(cell_dataframes, cycles, 'I Disch.', 'Discharge Capacity (mAh)')
print("Average Charge: " + str(average_charge) + " mAh")
print("Average Discharge: " + str(average_discharge) + " mAh")