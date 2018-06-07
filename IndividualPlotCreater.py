#Author Ugur Halis Kurt
#input: Data gathering levels data
#output: Visualization of movements based on User id (X-pos vs Y-Postion)

import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("/home/ugur/PycharmProjects/Motion/data_gathering_levels_data.csv",delimiter=",")

def plotMovement (my_data,user_Id):
    plt.clf()
    plt.xlabel('x_pos')
    plt.ylabel('y_pos')
    plt.ylim([-360,360])
    plt.xlim([-20,1260])

    for i in (my_data["motion_ID"].unique().astype('int')):
        my_data2 = my_data.loc[my_data.motion_ID == i]
        if(my_data2.loc[my_data2.first_valid_index(),'direction'] == True):
            plt.plot(my_data2['x_pos'], my_data2['y_pos'], c='blue', label="Right")
        else:
            plt.plot(my_data2['x_pos'], my_data2['y_pos'], c='red', label="Left")
    plt.savefig("/home/ugur/PycharmProjects/Motion/individual_Plots/"+str(user_Id)+".png")

for j in (data["user_ID"].unique().astype('int')):
    my_data = data.loc[data.user_ID == j]
    plotMovement(my_data,j)
