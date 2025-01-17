import pandas as pd
import warnings
import statistics as st
import helper_functions as hf

# Suppress the DtypeWarning related to mixed data types in the CSV file
warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)

def calculate_cell_values(cell_dataframes, cycles, instruction_name, attribute_name):
    cell_values = []
    for cell_index, cell in enumerate(cell_dataframes):
        cycle_values = []
        for cycle in cycles:
            if cell_index == 0:
                significant_data = cell[cell['Instruction Name'] == instruction_name]
                significant_data = significant_data[significant_data['Cycle'] == cycle]
                cycle_values.append(significant_data[attribute_name].max())
            else:
                significant_data = cell[cell['Instruction Name.' + str(cell_index)] == instruction_name]
                significant_data = significant_data[significant_data['Cycle.' + str(cell_index)] == cycle]
                cycle_values.append(significant_data[attribute_name + '.' + str(cell_index)].max())
        cell_values.append(st.mean(cycle_values))  # Average per cell
    return cell_values

# Define file to analyze and relevant cycles in it
file_path = '24-003_PhysicalTwin_Diagnostic_Test14525.csv'
cycles = [2., 3., 4.]

# Read csv data into pandas dataframe and reduce it to the needed values
battery_dataframe = pd.read_csv(file_path)
reduced_dataframe_battery = hf.reduced_dataframe(battery_dataframe, cycles)

# Split dataframe into dataframes per cell
cell_dataframes = hf.get_cell_dataframes(battery_dataframe)

# Calculate charge and discharge values from each cell
charge_per_battery = calculate_cell_values(cell_dataframes, cycles, 'V Charge', 'Charge Capacity (mAh)')
discharge_per_battery = calculate_cell_values(cell_dataframes, cycles, 'I Disch.', 'Discharge Capacity (mAh)')

# Print results for discharge
for index, discharge in enumerate(discharge_per_battery):
    print(f"Discharge battery {index}: {discharge:.2f} mAh")

print("-----------------------------------")
print(f"Average discharge of all batteries: {st.mean(discharge_per_battery):.2f} mAh\n")

# Print results for charge
for index, charge in enumerate(charge_per_battery):
    print(f"Charge battery {index}: {charge:.2f} mAh")

print("-----------------------------------")
print(f"Average charge of all batteries: {st.mean(charge_per_battery):.2f} mAh\n")

