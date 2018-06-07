#Author Ugur Halis Kurt
#This file is responsible for visualization of complation time of left and right movement.
#Input: Data gathering levels data
#Output: Graph of complation time based on user id
#Input Path: data_gathering_levels_data.csv
#Output Path: individual_Plot_Time/Time/

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("data_gathering_levels_data.csv",delimiter=",")


left_time_avearage = []

right_time_avearage = []

lefts = 0
rights = 0

players = [3,15,24,26]

for i in (players):
    user_data = data.loc[data.user_ID == i]
    right_time = 0
    right_counter = 0

    left_time = 0
    left_counter = 0
    for j in (user_data["motion_ID"].unique().astype('int')):
        motion_data = user_data.loc[user_data.motion_ID == j]
        if (motion_data.loc[motion_data.first_valid_index(),'direction'] == True):
            right_time = right_time + motion_data.loc[motion_data.last_valid_index(),'time']
            right_counter = right_counter + 1
        else:
            left_time = left_time + motion_data.loc[motion_data.last_valid_index(),'time']
            left_counter = left_counter + 1
    if(right_counter == 0 or left_counter == 0):
        right_time_avearage.append(0)
        left_time_avearage.append(0)
        continue
    elif(right_time/right_counter < left_time/left_counter):
        rights = rights +1
    else:
        lefts = lefts + 1
    right_time_avearage.append(right_time/(right_counter*1000))
    left_time_avearage.append(left_time/(left_counter*1000))
    print("Average right time for user : "+str(i) + " = "+ str(right_time/right_counter))
    print("Average left time for user : "+str(i) + " = "+ str(left_time/left_counter))

def groupedbarplot(x_data, y_data_list, y_data_names, colors, x_label, y_label, title):
    _, ax = plt.subplots()
    # Total width for all bars at one x location
    total_width = 0.8
    # Width of each individual bar
    ind_width = total_width / len(y_data_list)
    # This centers each cluster of bars about the x tick mark
    alteration = np.arange(-(total_width/2), total_width/2, ind_width)

    # Draw bars, one category at a time
    for i in range(0, len(y_data_list)):
        # Move the bar to the right on the x-axis so it doesn't
        # overlap with previously drawn ones
        ax.bar(x_data + alteration[i], y_data_list[i], color = colors[i], label = y_data_names[i], width = ind_width)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title(title)
    ax.legend(loc = 'lower right')
    plt.savefig("individual_Plot_Time/Time/"+title)


groupedbarplot(x_data = players
               , y_data_list = [right_time_avearage,left_time_avearage]
               , y_data_names = ['Right', 'Left']
               , colors = ['#539caf', '#7663b0']
               , x_label = 'UserNo'
               , y_label = 'Means of Time'
               , title = 'Mean values')

print("ugur")
