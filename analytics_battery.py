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

# Get all cycles of dataframe
def get_cycles(df):
    return df['Cycle'].dropna().unique()

def calculate_average(cell_dataframe, cycles, cell_iteration, attribute):
    average_discharge_per_cycle = []
    for cycle in cycles:
        if cell_iteration != 0:
            cycle_cell_dataframe = cell_dataframe[cell_dataframe['Cycle.' + str(cell_iteration)] == cycle]
            average_discharge_per_cycle.append(cycle_cell_dataframe[attribute + '.' + str(cell_iteration)].mean())
        else:
            cycle_cell_dataframe = cell_dataframe[cell_dataframe['Cycle'] == cycle]
            average_discharge_per_cycle.append(cycle_cell_dataframe[attribute].mean())
    return st.mean(average_discharge_per_cycle)

def calculate_average_per_battery(cell_dataframes, cycles, attribute):
    sum_per_battery = []
    for index, cell in enumerate(cell_dataframes):
        sum_per_battery.append(calculate_average(cell, cycles, index, attribute))
    return sum_per_battery

file_path = '/home/megli2/Downloads/24-003_PhysicalTwin_Diagnostic_Test14525.csv'
battery_dataframe = pd.read_csv(file_path)
relevant_battery_dataframe = battery_dataframe[battery_dataframe['Step'] >= 21 ]
cell_dataframes = get_cell_dataframes(battery_dataframe)

# Calculate Discharge
cycles = [ 2., 3., 4. ]
discharge_per_battery = calculate_average_per_battery(cell_dataframes, cycles, 'Discharge Capacity (mAh)')
charge_per_battery = calculate_average_per_battery(cell_dataframes, cycles, 'Charge Capacity (mAh)')

# Print results discharge
for index, discharge in enumerate(discharge_per_battery):
    print("Discharge battery " + str(index) + ": " +  str(discharge) )

print("-----------------------------------")
print(Fore.RED + "Average discharge of all batteries: " + str(st.mean(discharge_per_battery)) + " (mAh)" + Style.RESET_ALL)
print("\n")

# Print results charge
for index, charge in enumerate(charge_per_battery):
    print("Charge battery " + str(index) + ": " +  str(charge) )

print("-----------------------------------")
print(Fore.GREEN + "Average charge of all batteries: " + str(st.mean(charge_per_battery)) + " (mAh)" + Style.RESET_ALL)
print("\n")


