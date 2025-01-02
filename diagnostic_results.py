import pandas as pd
import ch_dch_plot as cdp
import matplotlib.pyplot as plt

# Define file to analyse and read out dataframe from it
file_path_cell_1 = 'data_export/Cell2_Diagnostic_Test14893.csv'
file_path_cell_2 = 'data_export/Cell3_Diagnostic_Test14917.csv'
file_path_cell_3 = 'data_export/Cell5_Diagnostic_Test15138.csv'
cell_dataframe_1 = pd.read_csv(file_path_cell_1)
cell_dataframe_2 = pd.read_csv(file_path_cell_2)
cell_dataframe_3 = pd.read_csv(file_path_cell_3)

cell_dataframes = [cell_dataframe_1, cell_dataframe_2]

# Plot ch/dch ploting
fig, ax = plt.subplots(figsize=(5, 2.7))
ax.set_xlabel("Time")
ax.set_ylabel("Capacity")

for cell_dataframe in cell_dataframes:
    cycles = [ 2, 3, 4 ]
    for cycle in cycles:
        data = cdp.plot_ch_dch(cell_dataframe, cycle) 

        # Plot CH and DCH figure for this cycle
        ax.plot(data["ch"]["time_points"], data["ch"]["capacity_points"], color='blue')
        ax.plot(data["dch"]["time_points"], data["dch"]["capacity_points"], color='green')

# Show plotted figure
plt.show()