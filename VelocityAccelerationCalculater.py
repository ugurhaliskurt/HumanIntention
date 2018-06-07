#Author Ugur Halis Kurt
#This file is reponsible for creating DMP data from data gathering levels data
#It is prestage of DMP.py file
#This file also responsible for creating X-pos vs Time, Y-pos vs Time, velocity-X vs Time and Velocity-Y vs Time graphs
#Input: Data gathering levels data
#Output: Apporapriate data for DMP algorithm
#Input Path: "data_gathering_leves_data.csv"
#Output Path: "DMP_Data/"
#Position Graph Path: "individual_Plot_Time/position/"
#Velocity Graph Path: "individual_Plot_Time/velocity/"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

input_data = pd.read_csv("data_gathering_levels_data.csv",delimiter=",")
all_data = pd.DataFrame()

for j in (input_data["user_ID"].unique().astype('int')):
    user_data = input_data.loc[input_data.user_ID == j]
    for i in (user_data["motion_ID"].unique().astype('int')):
        dmp_data = pd.DataFrame(columns=['user_ID','motion_ID','decision','time'])
        motion_data = user_data.loc[user_data.motion_ID == i]
        dmp_data["user_ID"] = motion_data["user_ID"]
        dmp_data["motion_ID"] = motion_data["motion_ID"]
        dmp_data["decision"] = motion_data["direction"]
        dmp_data["level"] = motion_data["level"]
        dmp_data["x_Pos"] = motion_data["x_pos"]
        #dmp_data["x_Pos"] = (motion_data["x_pos"] -motion_data["x_pos"].iloc[0]) / (motion_data["x_pos"].iloc[-1] -motion_data["x_pos"].iloc[0])
        dmp_data["time"] = np.linspace(0,len(dmp_data["x_Pos"])*10-10,len(dmp_data["x_Pos"]))
        dmp_data["xd"] = dmp_data["x_Pos"].diff() / (dmp_data["time"].diff()/1000)
        dmp_data["xdd"] = dmp_data["xd"].diff() / (dmp_data["time"].diff()/1000)
        dmp_data["y_Pos"] = motion_data["y_pos"]
        #dmp_data["y_Pos"] = (motion_data["y_pos"] -motion_data["y_pos"].iloc[0]) / (motion_data["y_pos"].iloc[-1] -motion_data["y_pos"].iloc[0])
        dmp_data["yd"] = dmp_data["y_Pos"].diff() / (dmp_data["time"].diff()/1000)
        dmp_data["ydd"] = dmp_data["yd"].diff() /(dmp_data["time"].diff()/1000)
        dmp_data.fillna(value=0, inplace=True) # This fills all the null values in the columns with 0)
        filename = "DMP_Data/User_"+str(j) +"_move_"+str(i)+".csv"
        dmp_data.to_csv(filename)
        all_data = all_data.append(dmp_data)

enable_individual_plots = True
def plotFigures(myData,axisName):
    for k in (myData["user_ID"].unique().astype('int')):
        velocities = []
        accelerations = []
        time = []
        decision =[]
        user_data = myData.loc[myData.user_ID == k]
        plt.figure(figsize=(20,10))
        for i in (user_data["motion_ID"].unique().astype('int')):
            x_values =[]
            y_values=[]
            motion_data = user_data.loc[user_data.motion_ID == i]
            pvr_value = -200.0
            for j in range (len(motion_data)):
                if pvr_value != motion_data[axisName].iloc[j]:
                    x_values.append(motion_data["time"].iloc[j])
                    y_values.append(motion_data[axisName].iloc[j])
            velocity = pd.Series(y_values).diff()/ (pd.Series(x_values).diff())
            acceleration = pd.Series(velocity).diff()/ pd.Series(x_values).diff()
            velocities.append(velocity)
            accelerations.append(acceleration)
            time.append(x_values)
            if(motion_data.loc[motion_data.first_valid_index(),'decision'] == True):
                plt.plot(x_values, y_values, c='blue', label="Right")
                decision.append("Right")
            else:
                plt.plot(x_values, y_values, c='red', label="Left")
                decision.append("Left")
        plt.xlabel('time')
        plt.ylabel(axisName)
        plt.savefig("individual_Plot_Time/position/UserNo"+str(k)+"_"+axisName)
        plt.clf()
        plt.figure(figsize=(20,10))
        for i in range (len(velocities)):
            if(decision[i] == "Right"):
                plt.plot(time[i], velocities[i], c='blue', label="Right")
            else:
                plt.plot(time[i], velocities[i], c='red', label="Left")
        plt.savefig("individual_Plot_Time/velocity/UserNo"+str(k)+"_" +axisName)
        plt.clf()

plotFigures(all_data,"x_Pos")
plotFigures(all_data,"y_Pos")

print("Ugur")
