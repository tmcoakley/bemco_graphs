import matplotlib.dates
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd 
import matplotlib.colors as mcolors
import seaborn as sns; sns.set()
from matplotlib import animation
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
import matplotlib.image as mpimg
from random import randrange
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
from matplotlib.animation import PillowWriter
import time
from matplotlib.colors import LinearSegmentedColormap
import numpy as np



window_size = 50  # Adjust based on desired smoothness

# Order with hotswaps 
hs_HDAQ_order = [ '7HS_3', '6HS_3', '5HS_3', '4HS_3', '3HS_3', '2HS_3', '1HS_3', '1HS_2', '2HS_2', '3HS_2', '4HS_2', '5HS_2', '6HS_2', '7HS_2' ]
hs_VDAQ_order = [ '6HS_1', '5HS_1', '4HS_1', '3HS_1', '2HS_1', '1HS_1', '1HS_0', '2HS_0', '3HS_0', '4HS_0', '5HS_0', '6HS_0']

# _____________________________________________________________________________________ # 
# 
# This takes all the data points and saves them under a dictionary with each SURF being
# a label
# 
# _____________________________________________________________________________________ #


# All the different CSV files 
hswapsurf = 'C:/Users/coakley.64/Downloads/bemco_hs.csv' # hotswap
surfdata = 'C:/Users/coakley.64/Downloads/bemco_surfs.csv' # surfs
turfiodata = 'C:/Users/coakley.64/Downloads/turf_bemco.csv' # turfios/turf


# Read in all the CSV files 
dfhssrf = pd.read_csv(hswapsurf) # hotswap
dftfio = pd.read_csv(turfiodata) # turfio/turf
dfsrf = pd.read_csv(surfdata)    # surf 


def sortvals(df): 
    df['time'] = pd.to_datetime(df['time'])
    return df.sort_values(by='time')  

board = [ dfhssrf, dfsrf, dftfio]

for iter in range(len(board)): 
    board[iter] = sortvals(board[iter])

hssurf = {}
hhssurfs = {}
vhssurfs = {}

def grouping(df, dictval): 
    for sensor, group in df.groupby('sensor'):  # Group data by sensor
        dictval[sensor] = dict(zip(group['time'], group['temperature'])) 
    return dictval


def smoothing(order, dictval, crate): 
    for key in order:
        if key in dictval:  # Ensure key exists in surfs before updating
            sensor_data = dictval[key]  # Retrieve dictionary of timestamps & temperature
            df = pd.DataFrame(sensor_data.items(), columns=['time', 'temperature'])
            df['time'] = pd.to_datetime(df['time'])  # Ensure timestamps are in datetime format
            df = df.sort_values(by='time')  # Sorting to maintain correct order
            df['rms_smooth'] = df['temperature'].rolling(window=window_size).apply(lambda x: np.sqrt(np.mean(x**2)), raw=True)
            crate[key] = dict(zip(df['time'], df['rms_smooth']))
    return crate

hssurf = grouping(dfhssrf, hssurf)

for iter in range(len(hs_HDAQ_order)): 
    hs_HDAQ_order[iter] = 'T_SURF' + str(hs_HDAQ_order[iter])
for iter in range(len(hs_VDAQ_order)): 
    hs_VDAQ_order[iter] = 'T_SURF' + str(hs_VDAQ_order[iter])

hhssurfs = smoothing(hs_HDAQ_order, hssurf, hhssurfs)

"""
# Populate hsurfs in the correct order
for key in hs_HDAQ_order:
    if key in hssurf:  # Ensure key exists in surfs before updating
        sensor_data = hssurf[key]  # Retrieve dictionary of timestamps & temperature

        # Convert dictionary to DataFrame for smoothing
        df = pd.DataFrame(sensor_data.items(), columns=['time', 'temperature'])
        df['time'] = pd.to_datetime(df['time'])  # Ensure timestamps are in datetime format
        df = df.sort_values(by='time')  # Sorting to maintain correct order

        # Apply rolling RMS smoothing
        df['rms_smooth'] = df['temperature'].rolling(window=window_size).apply(lambda x: np.sqrt(np.mean(x**2)), raw=True)

        # Convert back to dictionary and store in `hhssurfs`
        hhssurfs[key] = dict(zip(df['time'], df['rms_smooth']))
        # hhssurfs[key] = hssurf[key]
        # hhssurfs[key].values().rolling(window=window_size).apply(lambda x: np.sqrt(np.mean(x**2)), raw=True)
       
"""
# Populate vsurfs in the correct order
for key in hs_VDAQ_order:
    if key in hssurf:  # Ensure key exists in surfs before updating
        sensor_data = hssurf[key]  # Retrieve dictionary of timestamps & temperature

        # Convert dictionary to DataFrame for smoothing
        df = pd.DataFrame(sensor_data.items(), columns=['time', 'temperature'])
        df['time'] = pd.to_datetime(df['time'])  # Ensure timestamps are in datetime format
        df = df.sort_values(by='time')  # Sorting to maintain correct order

        # Apply rolling RMS smoothing
        df['rms_smooth'] = df['temperature'].rolling(window=window_size).apply(lambda x: np.sqrt(np.mean(x**2)), raw=True)

        # Convert back to dictionary and store in `hhssurfs`
        vhssurfs[key] = dict(zip(df['time'], df['rms_smooth']))

# All the SURFs and TURFIOs in the DAQ
HDAQ_order = [ 10, 20, 29, 13, 25, 32, 23, 12, 21, 31, 26, 7, 5, 28 ]
VDAQ_order = [ 15, 16, 14, 22, 27, 19, 9, 8, 30, 11, 33, 24 ]


surfs = {}
turfios = {}  # Dictionary for sensor data

for sensor, group in dftfio.groupby('sensor'):  # Group data by sensor
    turfios[sensor] = dict(zip(group['time'], group['temperature'])) 

for sensor, group in dfsrf.groupby('sensor'):  # Group data by sensor
    surfs[sensor] = dict(zip(group['time'], group['temperature'])) 

for iter in range(len(HDAQ_order)): 
    HDAQ_order[iter] = 'T_APU_SURF_' + str(HDAQ_order[iter])
for iter in range(len(VDAQ_order)): 
    VDAQ_order[iter] = 'T_APU_SURF_' + str(VDAQ_order[iter])


hsurfs = {}
vsurfs = {}

"""
for key in HDAQ_order:
    if key in surfs:
        hsurfs[key] = dict(sorted(surfs[key].items())) """


# Populate hsurfs in the correct order
for key in HDAQ_order:
    if key in surfs:  # Ensure key exists in surfs before updating
        sensor_data = surfs[key]  # Retrieve dictionary of timestamps & temperature

        # Convert dictionary to DataFrame for smoothing
        df = pd.DataFrame(sensor_data.items(), columns=['time', 'temperature'])
        df['time'] = pd.to_datetime(df['time'])  # Ensure timestamps are in datetime format
        df = df.sort_values(by='time')  # Sorting to maintain correct order

        # Apply rolling RMS smoothing
        df['rms_smooth'] = df['temperature'].rolling(window=window_size).apply(lambda x: np.sqrt(np.mean(x**2)), raw=True)

        # Convert back to dictionary and store in `hhssurfs`
        hsurfs[key] = dict(zip(df['time'], df['rms_smooth']))


# Populate vsurfs in the correct order
for key in VDAQ_order:
    if key in surfs:  # Ensure key exists in surfs before updating
        sensor_data = surfs[key]  # Retrieve dictionary of timestamps & temperature

        # Convert dictionary to DataFrame for smoothing
        df = pd.DataFrame(sensor_data.items(), columns=['time', 'temperature'])
        df['time'] = pd.to_datetime(df['time'])  # Ensure timestamps are in datetime format
        df = df.sort_values(by='time')  # Sorting to maintain correct order

        # Apply rolling RMS smoothing
        df['rms_smooth'] = df['temperature'].rolling(window=window_size).apply(lambda x: np.sqrt(np.mean(x**2)), raw=True)

        # Convert back to dictionary and store in `hhssurfs`
        vsurfs[key] = dict(zip(df['time'], df['rms_smooth']))

"""
for key in surfs: 
    for iter in range(len(HDAQ_order)): 
        if key == HDAQ_order[iter]: 
            hsurfs.update({key:{}})
            hsurfs[key].update(surfs[key])
    
    for iter in range(len(VDAQ_order)): 
        if key == VDAQ_order[iter]: 
            vsurfs.update({key:{}})
            vsurfs[key].update(surfs[key])"""


# All the SURFs and TURFIOs in the DAQ
HDAQ_order = [ 10, 20, 29, 13, 25, 32, 23, 12, 21, 31, 26, 7, 5, 28 ]
VDAQ_order = [ 15, 16, 14, 22, 27, 19, 9, 8, 30, 11, 33, 24 ]
















fig, ax = plt.subplots()


# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
colors = ['darkgreen', 'cornflowerblue', 'paleturquoise', 'orchid', 'palegreen', 'lavender', 'firebrick', 'dodgerblue', 'darkseagreen', 'mediumslateblue', 'cadetblue', 'rebeccapurple', 'thistle', 'mediumaquamarine']
colors = [
    "#C76D6D",  # Muted Cranberry (Red)
    "#9C4A6F",  # Dusty Rose (Red-Violet)
    "#A067A5",  # Dusky Mauve (Violet)
    "#8357A4",  # Soft Purple (Purple)
    "#6D5792",  # Muted Indigo (Blue-Violet)
    "#46688D",  # Muted Navy (Blue)
    "#5F9EA0",  # Cadet Blue (Cool Blue)
    "#4E7E7B",  # Faded Teal (Blue-Green)
    "#688E4E",  # Sage Green (Green)
    "#3C665A",  # Deep Evergreen (Green)
    "#7F885C",  # Olive Gray (Green-Yellow)
    "#9C8566",  # Muted Gold (Soft Yellow)
    "#5C6A82",  # Dusty Blue-Gray (Muted Cool Tone)
    "#318C8C",  # Muted Aqua (Blue-Green)
]

i = 0
for key in hsurfs:
    sorted_hsurfs = dict(sorted(hsurfs[key].items()))  # Ensure timestamps are ordered
    if key[-2:-1] == '_': 
        ax.plot(list(sorted_hsurfs.keys()), list(sorted_hsurfs.values()),  colors[i], label = key[-1:])
        i+=1 
    else: 
        ax.plot(list(sorted_hsurfs.keys()), list(sorted_hsurfs.values()), colors[i], label = key[-2:])
        i+=1

ax.xaxis.set_major_locator(matplotlib.dates.AutoDateLocator())  # Auto-adjust tick frequency
ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%I:%M:%S %p'))  # 12-hour format



ax.xaxis.set_label_text('Time')
ax.yaxis.set_label_text('Temperature (C)')
plt.title('HPOL Crate')
plt.legend(
    ncol=3, 
    loc='upper right', 
    fontsize=10, 
    frameon=True, 
    edgecolor='black', 
    facecolor='lightgray',
    columnspacing=1.5
)
plt.show()
fig, ax = plt.subplots()

# Shrink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
i = 0
for key in vsurfs:
    if key[-2:-1] == '_': 
        ax.plot(vsurfs[key].keys(), vsurfs[key].values(),  colors[i], label = key[-1:])
        i+=1 
    else: 
        ax.plot(vsurfs[key].keys(), vsurfs[key].values(), colors[i], label = key[-2:])
        i+=1

start, end = ax.get_xlim()
starty, endy = ax.get_ylim()

ax.xaxis.set_major_locator(matplotlib.dates.AutoDateLocator())  # Auto-adjust tick frequency
ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%I:%M:%S %p'))  # 12-hour format

ax.xaxis.set_label_text('Time')
ax.yaxis.set_label_text('Temperature (C)')
plt.title('VPOL Crate')
plt.legend(
    ncol=3, 
    loc='upper right', 
    fontsize=10, 
    frameon=True, 
    edgecolor='black', 
    facecolor='lightgray',
    columnspacing=1.5
)
plt.show()

















fig, ax = plt.subplots()


# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
colors = ['darkgreen', 'cornflowerblue', 'paleturquoise', 'orchid', 'palegreen', 'lavender', 'firebrick', 'dodgerblue', 'darkseagreen', 'mediumslateblue', 'cadetblue', 'rebeccapurple', 'thistle', 'mediumaquamarine']
colors = [
    "#C76D6D",  # Muted Cranberry (Red)
    "#9C4A6F",  # Dusty Rose (Red-Violet)
    "#A067A5",  # Dusky Mauve (Violet)
    "#8357A4",  # Soft Purple (Purple)
    "#6D5792",  # Muted Indigo (Blue-Violet)
    "#46688D",  # Muted Navy (Blue)
    "#5F9EA0",  # Cadet Blue (Cool Blue)
    "#4E7E7B",  # Faded Teal (Blue-Green)
    "#688E4E",  # Sage Green (Green)
    "#3C665A",  # Deep Evergreen (Green)
    "#7F885C",  # Olive Gray (Green-Yellow)
    "#9C8566",  # Muted Gold (Soft Yellow)
    "#5C6A82",  # Dusty Blue-Gray (Muted Cool Tone)
    "#318C8C",  # Muted Aqua (Blue-Green)
]

i = 0
for key in vhssurfs:
    sorted_vhssurfs = dict(sorted(vhssurfs[key].items()))  # Ensure timestamps are ordered
    
    ax.plot(list(sorted_vhssurfs.keys()), list(sorted_vhssurfs.values()),  colors[i], label = VDAQ_order[i])
    i+=1 


ax.xaxis.set_major_locator(matplotlib.dates.AutoDateLocator())  # Auto-adjust tick frequency
ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%I:%M:%S %p'))  # 12-hour format
ax.xaxis.set_label_text('Time')
ax.yaxis.set_label_text('Temperature (C)')

plt.title('VPOL Crate')
plt.legend(
    ncol=3, 
    loc='upper right', 
    fontsize=10, 
    frameon=True, 
    edgecolor='black', 
    facecolor='lightgray',
    columnspacing=1.5
)
plt.show()

fig.clear
fig, ax = plt.subplots()
# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

i = 0
for key in hhssurfs:
    sorted_hhssurfs = dict(sorted(hhssurfs[key].items()))  # Ensure timestamps are ordered
    ax.plot(list(sorted_hhssurfs.keys()), list(sorted_hhssurfs.values()),  colors[i], label = HDAQ_order[i])
    i+=1 
    
ax.xaxis.set_major_locator(matplotlib.dates.AutoDateLocator())  # Auto-adjust tick frequency
ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%I:%M:%S %p'))  # 12-hour format
ax.xaxis.set_label_text('Time')
ax.yaxis.set_label_text('Temperature (C)')

plt.title('HPOL Crate')
plt.legend(
    ncol=3, 
    loc='upper right', 
    fontsize=10, 
    frameon=True, 
    edgecolor='black', 
    facecolor='lightgray',
    columnspacing=1.5
)
plt.show()

