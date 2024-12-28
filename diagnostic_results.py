import pandas as pd
import ch_dch_plot as cdp
import matplotlib.pyplot as plt

# Define file to analyse and read out dataframe from it
file_path = 'data_export/Cell2_Diagnostic_Test14893.csv'
battery_dataframe = pd.read_csv(file_path)

# Plot ch/dch ploting
fig, ax = plt.subplots(figsize=(5, 2.7))
ax.set_xlabel("Time")
ax.set_ylabel("Capacity")

cycles = [ 2, 3, 4 ]
for cycle in cycles:
    data = cdp.plot_ch_dch(battery_dataframe, cycle) 

    # Plot CH and DCH figure for this cycle
    ax.plot(data["ch"]["time_points"], data["ch"]["capacity_points"], color='blue')
    ax.plot(data["dch"]["time_points"], data["dch"]["capacity_points"], color='green')


# Show plotted figure
plt.show()