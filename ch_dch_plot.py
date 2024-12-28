import helper_functions as hf
import json

def plot_ch_dch(battery_dataframe, cycle):
    # Charge capacity plot
    # -------------------------------------------------------------#
    steps  = [21, 22]

    # Coordinate arrays and value to measure
    ch_capacity_points = []
    ch_time_points = []
    ch_measure_value = 'Charge Capacity (mAh)'

    # Define coordinates
    for step in steps:
        hf.set_coordinate_points(battery_dataframe, step, cycle, ch_capacity_points, 
                                ch_time_points, 0, ch_measure_value)
    hf.set_coordinate_points(battery_dataframe, steps[-1], cycle, ch_capacity_points, 
                            ch_time_points, -1, ch_measure_value)

    # -------------------------------------------------------------#


    # Discharge capacity plot
    # -------------------------------------------------------------#
    steps  = [23, 24]

    # Coordinate arrays and value to measure
    dch_capacity_points = []
    dch_time_points = []
    dch_measure_value = 'Discharge Capacity (mAh)'

    # Define coordinates
    for step in steps:
        hf.set_coordinate_points(battery_dataframe, step, cycle, dch_capacity_points, 
                                dch_time_points, 0, dch_measure_value)
    hf.set_coordinate_points(battery_dataframe, steps[-1], cycle, dch_capacity_points, 
                            dch_time_points, -1, dch_measure_value)

    # -------------------------------------------------------------#

    data = {
        "ch": {
            "time_points": ch_time_points,
            "capacity_points": ch_capacity_points,
        },
        "dch": {
            "time_points": dch_time_points,
            "capacity_points": dch_capacity_points,
        }
    }
    return data