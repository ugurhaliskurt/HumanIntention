#Author Ugur Halis Kurt
#This file is reponsible for representing human movements by DMP weights
#Input: User movement data (position velocity and accelaretion)
#Output: Individual DMP graphics
#input_folder_path: The input file path for DMP algotihm
#output_folder_path: The output file path of DMP algorithm

from oct2py import octave #Bridge library to run octave and python code together
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

def mode_rows(a):
    a = np.ascontiguousarray(a)
    void_dt = np.dtype((np.void, a.dtype.itemsize * np.prod(a.shape[1:])))
    _,ids, count = np.unique(a.view(void_dt).ravel(), \
                                return_index=1,return_counts=1)
    largest_count_id = ids[count.argmax()]
    most_frequent_row = a[largest_count_id]
    return most_frequent_row

figure_number = 4 #The number of graphics for each axis. If kernel Number is 40, each figure shows 10 kernels weights.
all_user = []

left_weights_x = []
users_left_x = []
left_weights_y = []
users_left_y = []

right_weights_x = []
users_right_x = []
right_weights_y = []
users_right_y = []

df_total_weigts = pd.DataFrame()

kernel_number = 40.0 # kernel number for DMP algorithm
axis_number = 2 # 2D movement


input_folder_path = 'DMP_Data/'
output_folder_path = 'DMP_Result/'
# Open one of the files,
for data_file in sorted(os.listdir(input_folder_path)):
    train_data = pd.read_csv(input_folder_path+data_file)
    all_user.append(train_data["user_ID"].iloc[0])
    for k in range(axis_number):
        tau = int((train_data["time"].iloc[-1]-train_data["time"].iloc[0]) / 2)
        column = 'x_Pos'
        if(k == 0):
            my_data = train_data[['x_Pos','xd','xdd']].iloc[0:]
        elif(k == 1):
            my_data = train_data[['y_Pos','yd','ydd']].iloc[0:]
            column = 'y_Pos'
        try:
            weights = octave.learn_dcp_batch_tmp(my_data.as_matrix(),tau,kernel_number,my_data[column].iloc[-1])
        except:
            try:
                tau = tau + 0.005
                weights = octave.learn_dcp_batch_tmp(my_data.as_matrix(),tau,kernel_number,my_data[column].iloc[-1])
            except:
                tau = tau - 0.01
                weights = octave.learn_dcp_batch_tmp(my_data.as_matrix(),tau,kernel_number,my_data[column].iloc[-1])

        if (train_data["decision"].iloc[1] == True and k== 0):
            right_weights_x.append(mode_rows(weights))
            users_right_x.append(train_data["user_ID"].iloc[0])
        elif (train_data["decision"].iloc[1] == False and k== 0):
            left_weights_x.append(mode_rows(weights))
            users_left_x.append(train_data["user_ID"].iloc[0])
        elif (train_data["decision"].iloc[1] == True and k== 1):
            right_weights_y.append(mode_rows(weights))
            users_right_y.append(train_data["user_ID"].iloc[0])
        else:
            left_weights_y.append(mode_rows(weights))
            users_left_y.append(train_data["user_ID"].iloc[0])


def groupedbarplot(x_data, y_data_list,y_data_std, y_data_names, colors, x_label, y_label, title):
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
        ax.errorbar(x_data + alteration[i], y_data_list[i], y_data_std[i], color = '#297083', ls = 'none', lw = 1, capthick = 1)
        ax.bar(x_data + alteration[i], y_data_list[i], color = colors[i], label = y_data_names[i], width = ind_width)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title(title)
    ax.legend(loc = 'upper right')
    plt.savefig("DMP_Result/"+title)

df_right_weights_x = pd.DataFrame(right_weights_x)
df_right_weights_x["user_ID"] = users_right_x
df_left_weights_x = pd.DataFrame(left_weights_x)
df_left_weights_x["user_ID"] = users_left_x
df_right_weights_y = pd.DataFrame(right_weights_y)
df_right_weights_y["user_ID"] = users_right_y
df_left_weights_y = pd.DataFrame(left_weights_y)
df_left_weights_y["user_ID"] = users_left_y

for j in (pd.Series(all_user).unique().astype('int')):
    length_right_x = len(df_right_weights_x.loc[df_right_weights_x.user_ID == j])
    length_left_x = len(df_left_weights_x.loc[df_left_weights_x.user_ID == j])

    length_right_y = len(df_right_weights_y.loc[df_right_weights_y.user_ID == j])
    length_left_y = len(df_left_weights_y.loc[df_left_weights_y.user_ID == j])

    mean_right_weights_x = (df_right_weights_x.loc[df_right_weights_x.user_ID == j].drop(["user_ID"], axis=1).mean())
    mean_left_weights_x = (df_left_weights_x.loc[df_left_weights_x.user_ID == j].drop(["user_ID"], axis=1).mean())

    mean_right_weights_y = (df_right_weights_y.loc[df_right_weights_y.user_ID == j].drop(["user_ID"], axis=1).mean())
    mean_left_weights_y = (df_left_weights_y.loc[df_left_weights_y.user_ID == j].drop(["user_ID"], axis=1).mean())

    std_right_weights_x = (df_left_weights_x.loc[df_right_weights_x.user_ID == j].drop(["user_ID"], axis=1).std())
    std_left_weights_x = (df_left_weights_x.loc[df_left_weights_x.user_ID == j].drop(["user_ID"], axis=1).std())

    std_right_weights_y = (df_right_weights_y.loc[df_right_weights_y.user_ID == j].drop(["user_ID"], axis=1).std())
    std_left_weights_y =(df_left_weights_y.loc[df_left_weights_y.user_ID == j].drop(["user_ID"], axis=1).std())


    for i in range (figure_number):
#x axis graphs
        groupedbarplot(x_data = np.arange(int((i * kernel_number/figure_number)+1),int(((i+1) * kernel_number/figure_number)+1),1)
               , y_data_list = [mean_right_weights_x.iloc[int((i * (kernel_number)/figure_number)):int((i+1) * (kernel_number)/figure_number)], mean_left_weights_x.iloc[int(i * kernel_number/figure_number):int((i+1) * kernel_number/figure_number)]]
               , y_data_std = [std_right_weights_x.iloc[int(i * kernel_number/figure_number):int((i+1) * kernel_number/figure_number)], std_left_weights_x.iloc[int(i * kernel_number/figure_number):int((i+1) * kernel_number/figure_number)]]
               , y_data_names = ['Right_'+str(length_right_x), 'Left_'+str(length_left_x)]
               , colors = ['#539caf', '#7663b0']
               , x_label = 'Kernels'
               , y_label = 'Weights'
               , title = 'User_ID_'+str(j)+'_X axis'+str(i))
#y axis graphs
        groupedbarplot(x_data = np.arange(int((i * kernel_number/figure_number)+1),int(((i+1) * kernel_number/figure_number)+1),1)
               , y_data_list = [mean_right_weights_y.iloc[int((i * (kernel_number)/figure_number)):int((i+1) * (kernel_number)/figure_number)], mean_left_weights_y.iloc[int(i * kernel_number/figure_number):int((i+1) * kernel_number/figure_number)]]
               , y_data_std = [std_right_weights_y.iloc[int(i * kernel_number/figure_number):int((i+1) * kernel_number/figure_number)], std_left_weights_y.iloc[int(i * kernel_number/figure_number):int((i+1) * kernel_number/figure_number)]]
               , y_data_names = ['Right_'+str(length_right_y), 'Left_'+str(length_left_y)]
               , colors = ['#539caf', '#7663b0']
               , x_label = 'Kernels'
               , y_label = 'Weights'
               , title = 'User_ID_'+str(j)+'_Y axis'+str(i))
