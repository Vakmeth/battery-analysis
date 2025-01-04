import pandas as pd

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

# Reduce unnecessary values from dataframe
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

# Plotting funciton
def set_coordinate_points(reduced_dataframe, step, cycle, capacity_points, time_points, index, measure_value):
    temporary_frame = reduced_dataframe[reduced_dataframe['Step'] == step]
    filtered_frame = temporary_frame[temporary_frame['Cycle'] == cycle]
    capacity_points.append(filtered_frame[measure_value].iloc[index])
    time_points.append(filtered_frame['Total Time (Seconds)'].iloc[index])
    if measure_value == 'Discharge Capacity (mAh)' and index == -1:
        capacity_points.append(0)
        time_points.append(filtered_frame['Total Time (Seconds)'].iloc[index])