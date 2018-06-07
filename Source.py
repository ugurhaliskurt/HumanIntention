#Author Ugur Halis Kurt
#This file separates data gathering levels and fun levels and it also visualizes every movement in the game.
#input : raw data of the serious game.
#outputs: data gathering levels data and plots of all movements
#input path: rawData.txt
#output path data: data_gathering_levels_data.csv
#output path graphs: plots/

import pandas as pd
import matplotlib.pyplot as plt

sample_time = 10
x_pos = 0
y_pos = 1

data = pd.read_csv("rawData.txt",delimiter=",")
data_gathering_leves_data = pd.DataFrame(columns=['x_pos','y_pos','via_point','motion_ID','user_ID','direction','level'])
final_data = data

leves_with_no_data = [0,13,36,59]

def draw_plot (user_ID,motion_ID):
    fig = plt.figure(figsize=(12, 12))
    labels = ["velocity_x","velocity_y","acceleration_x","acceleration_y"]
    my_data2 = final_data.loc[final_data.motion_ID == motion_ID]
    my_data = my_data2.loc[my_data2.user_ID == user_ID]
    for sp in range(0,4):
        ax = fig.add_subplot(2,2,sp+1)
        ax.plot(my_data['time'], my_data[labels[sp]], c='blue', label=labels[sp])
        ax.set_title(labels[sp])
    plt.show()


def draw_xy (user_ID,motion_ID):
    global data_gathering_leves_data
    my_data3 = final_data.loc[final_data.motion_ID == motion_ID]
    my_data2 = my_data3.loc[my_data3.via_point == 0]
    my_data = my_data2.loc[my_data2.user_ID == user_ID]
    plt.clf()
    plt.plot(my_data['x_pos'], my_data['y_pos'], c='blue')
    plt.xlabel('x_pos')
    plt.ylabel('y_pos')
    plt.ylim([-450,450])
    plt.xlim([-20,1260])
    if my_data["gradient"].sum() < 20:
        if(my_data["level"].iloc[0] not in leves_with_no_data):
            data_gathering_leves_data = data_gathering_leves_data.append(my_data[['x_pos','y_pos','via_point','motion_ID','user_ID','direction','level','time']], ignore_index=True)
        plt.savefig("plots/"+str(user_ID)+"_"+str(motion_ID)+"_normal.png")
    else:
        plt.savefig("plots/"+str(user_ID)+"_"+str(motion_ID)+"_faulty.png")
shape = data.shape
def add_gradient_column():
    final_data.loc[0,"gradient"] = 0
    for index in range(shape[0] - 1):
        if data.iloc[index,x_pos] == 0 or final_data.loc[index,"motion_ID"] != final_data.loc[index+1,"motion_ID"]\
                or final_data.loc[index,"user_ID"] != final_data.loc[index+1,"user_ID"]:
            continue
        distance_x = data.iloc[index + 1,x_pos] - data.iloc[index,x_pos]
        distance_y = data.iloc[index + 1,y_pos] - data.iloc[index,y_pos]
        if distance_x < 0:
            distance_y = (distance_y+1) * 50
        if(distance_x != 0 and final_data.loc[index,"via_point"] == 0):
            final_data.loc[index+1,"gradient"]= abs(distance_y / distance_x)

def add_velocity_acceleration():
    final_data.loc[0,"time"] = 0
    for index in range(shape[0] - 1):
        if final_data.loc[index,"motion_ID"] != final_data.loc[index+1,"motion_ID"]\
                or final_data.loc[index,"user_ID"] != final_data.loc[index+1,"user_ID"]:
            final_data.loc[index+1,"time"] = 0
            continue
        distance_x = data.iloc[index + 1,x_pos] - data.iloc[index,x_pos]
        distance_y = data.iloc[index + 1,y_pos] - data.iloc[index,y_pos]
        final_data.loc[index+1,"velocity_x"]= distance_x / sample_time
        final_data.loc[index+1,"velocity_y"]= distance_y / sample_time
        final_data.loc[index+1,"time"]= final_data.loc[index,"time"] +10

    final_data["acceleration_x"] = final_data["velocity_x"].diff() / sample_time
    final_data["acceleration_y"] = final_data["velocity_y"].diff() / sample_time

add_velocity_acceleration()
add_gradient_column()

dsd = final_data["user_ID"].unique().astype('int32')
for j in (final_data["user_ID"].unique().astype('int')):
    my_data = final_data.loc[final_data.user_ID == j]
    for i in (my_data["motion_ID"].unique().astype('int')):
        my_data2 = my_data.loc[my_data.motion_ID == i]
        print(my_data2["gradient"].sum())
        draw_xy(j,i)
draw_plot(0,0)

submission = pd.DataFrame(data_gathering_leves_data)
submission.to_csv("data_gathering_levels_data.csv",index=False)
