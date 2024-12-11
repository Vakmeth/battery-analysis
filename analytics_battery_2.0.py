import pandas as pd
import warnings
import numpy as np
import statistics as st
from colorama import Fore, Back, Style, init

# Suppress the DtypeWarning related to mixed data types in the CSV file
warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)

# Method to split our main dataframe into dataframes for each cell
def get_cell_dataframes(df):
    # Pattern according to we filter the columns (Cell, Cell.1, Cell.2, Cell.3, etc.)
    pattern = "^Cell(?:\.\d+)?$"

    # All cell names (Cell, Cell.1, Cell.2, etc.)
    cell_columns = [col for col in df.columns if pd.Series([col]).str.match(pattern).any()]

    # The last attribute (column) of a cell
    end_col_prefix = df.columns[df.columns.get_loc(cell_columns[1]) - 1]

    ''''
    We set it directly as end column since the last attribute of the first cell has no
    '.1, .2, .n' identifier on it
    '''
    end_col = end_col_prefix

    '''
    We split the dataframe from Cell.n to the last attributes so we have a dataframe 
    for each cell
    '''
    cell_dataframes = []
    for i in range(len(cell_columns)):
        start_col = cell_columns[i]
        if i != 0:
            end_col = end_col_prefix +  '.' + str(i)    
        cols = df.loc[:, start_col:end_col].columns   
        split_dataframe = df[cols]
        cell_dataframes.append(split_dataframe)
    return cell_dataframes

def reduced_dataframe(battery_dataframe, cycles):
    reduced_dataframe = battery_dataframe
    for index in range(0, 5):
        if index == 0:
            reduced_dataframe = reduced_dataframe[reduced_dataframe['Instruction Name'] != 'Idle']
            reduced_dataframe = reduced_dataframe[reduced_dataframe['Cycle'].isin(cycles)]
        else:    
            reduced_dataframe = reduced_dataframe[reduced_dataframe['Instruction Name.' + str(index)] != 'Idle']
            reduced_dataframe = reduced_dataframe[reduced_dataframe['Cycle.' + str(index)].isin(cycles)]
    return reduced_dataframe   

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
reduced_dataframe_battery = reduced_dataframe(battery_dataframe, cycles)

# Split dataframe into dataframes per cell
cell_dataframes = get_cell_dataframes(battery_dataframe)

# Calculate charge from each cell and print results
average_charge = calculate_avg_value(cell_dataframes, cycles, 'V Charge', 'Charge Capacity (mAh)')
average_discharge = calculate_avg_value(cell_dataframes, cycles, 'I Disch.', 'Discharge Capacity (mAh)')
print("Average Charge: " + str(average_charge) + " mAh")
print("Average Discharge: " + str(average_discharge) + " mAh")