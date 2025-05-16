import matplotlib.pyplot as plt
import matplotlib
import pandas as pd 
import seaborn as sns; sns.set()
import time
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

# _____________________________________________________________________________________ # 
# 
#                                 USER INTERFACE
# Change the CSV file destinations to where you need them to be
# _____________________________________________________________________________________ #


hswapsurf = 'bemco_hs.csv' # hotswap
surfdata = 'bemco_surfs.csv' # surfs
turfiodata = 'turf_bemco.csv' # turfios/turf

window_size = 100  # Adjust do what you want 

# Colors for the  graph
colors = [ "#C76D6D", "#9C4A6F", "#A067A5", "#8357A4", "#6D5792", "#46688D", "#5F9EA0", 
          "#4E7E7B", "#688E4E", "#3C665A", "#7F885C", "#9C8566", "#5C6A82", "#318C8C" ]



# _____________________________________________________________________________________ # 
# 
#                                 DAQ ORDER
# This shows the different orders of the SURFs/TURFIOs in the crates
# _____________________________________________________________________________________ #

# Hotswap order
hs_HDAQ_order = [ '7HS_3', '6HS_3', '5HS_3', '4HS_3', '3HS_3', '2HS_3', '1HS_3', '1HS_2', '2HS_2', '3HS_2', '4HS_2', '5HS_2', '6HS_2', '7HS_2' ]
hs_VDAQ_order = [ '6HS_1', '5HS_1', '4HS_1', '3HS_1', '2HS_1', '1HS_1', '1HS_0', '2HS_0', '3HS_0', '4HS_0', '5HS_0', '6HS_0']

# All the SURFs in the DAQ
HDAQ_order = [ 10, 20, 29, 13, 25, 32, 23, 12, 21, 31, 26, 7, 5, 28 ]
VDAQ_order = [ 15, 16, 14, 22, 27, 19, 9, 8, 30, 11, 33, 24 ]


# Save the strings as written in CSV (I didn't set this)
for iter in range(len(hs_HDAQ_order)): 
    hs_HDAQ_order[iter] = 'T_SURF' + str(hs_HDAQ_order[iter])
for iter in range(len(hs_VDAQ_order)): 
    hs_VDAQ_order[iter] = 'T_SURF' + str(hs_VDAQ_order[iter])


apu_HDAQ_order, apu_VDAQ_order = [], []
for iter in range(len(HDAQ_order)): 
    apu_HDAQ_order.append('T_APU_SURF_' + str(HDAQ_order[iter]))
for iter in range(len(VDAQ_order)): 
    apu_VDAQ_order.append('T_APU_SURF_' + str(VDAQ_order[iter]))


# _____________________________________________________________________________________ # 
# 
#                             VARIABLES
# This takes all the data points and saves them under a dictionary with each SURF being
# a label
# 
# _____________________________________________________________________________________ #

# Dictionaries 
hotswapsurf = {}
apusurf = {}
turfios = {}


#_______________________________________________________________________________________# 
#
#                             FUNCTIONS 
#
#_______________________________________________________________________________________#

# Sort by times
def sortvals(df): 
    df['time'] = pd.to_datetime(df['time'], format = '%I:%M:%S %p')
    return df.sort_values(by='time')  

# Creates nested dictionaries
def grouping(df, dictval): 
    for sensor, group in df.groupby('sensor'):
        dictval[sensor] = dict(zip(group['time'], group['temperature'])) 
    return dictval

# RMS Smoothing the data
def smoothing(order, dictval): 
    crate = {}
    error = []
    filtered_times = []
    for key in order:
        if key in dictval:  
            sensor_data = dictval[key]  
            df = pd.DataFrame(sensor_data.items(), columns=['time', 'temperature'])
            df['time'] = pd.to_datetime(df['time'], format = '%I:%M:%S %p')
            start = pd.to_datetime('1900-01-01 15:20:03')
            end = pd.to_datetime('1900-01-01 18:39:46')
            df_filter = df[(df['time'] >= start) & (df['time'] <= end)]
            df['rms_smooth'] = df['temperature'].rolling(window=window_size).apply(lambda x: np.sqrt(np.mean(x**2)), raw=True)
            error.append(df_filter['temperature'].std())
            filtered_times.append(df_filter['time'])
            crate[key] = dict(zip(df['time'], df['rms_smooth']))
    return crate, error, filtered_times


#_______________________________________________________________________________________# 
#
#                             EXECUTABLE  
#
#_______________________________________________________________________________________#


# Read in all the CSV files 
dfhssrf = pd.read_csv(hswapsurf) # hotswap
dftfio = pd.read_csv(turfiodata) # turfio/turf
dfsrf = pd.read_csv(surfdata)    # surf 

# Iterate over the different boards to sort over time
board = [ dfhssrf, dfsrf, dftfio]

for iter in range(len(board)): 
    board[iter] = sortvals(board[iter])

# Groups HDAQ and VDAQ 
hotswapsurf = grouping(dfhssrf, hotswapsurf)
turfios = grouping(dftfio, turfios)
apusurf = grouping(dfsrf, apusurf)

# Applies RMS smoothing because that data sure is noisy :) 
horzhotswapsurfs, horzhotswaperr, horzhotswaperrtime = smoothing(hs_HDAQ_order, hotswapsurf)
verthotswapsurfs, verthotswaperr, verthotswaperrtime = smoothing(hs_VDAQ_order, hotswapsurf)
horzapusurfs, horzapuerr, horzapuerrtime = smoothing(apu_HDAQ_order, apusurf)
vertapusurfs, vertapuerr, vertapuerrtime = smoothing(apu_VDAQ_order, apusurf)



#_______________________________________________________________________________________# 
#
#                             TIME TO GRAPH IT, YO  
#
#_______________________________________________________________________________________#

    
def graphygraph(data, order, error = False, title = False, num = False): 

    _, ax = plt.subplots()
      
    i = 0

    if error != False: 
        data_values = np.array(list(data.values()))
        errval = error[0]
        errtime = np.array(list(error[1]))
        filtered_values = [data[t] for t in errtime]

        # Plot filtered data
        ax.plot(list(data.keys()), data_values, colors[num], label = order[num] )

        # Apply the error shading
        ax.fill_between(errtime, np.array(filtered_values) - errval, 
                        np.array(filtered_values) + errval, 
                        color='gray', alpha=0.3, label='Error')
        ax.plot()

    else: 
        for key in data:
            # sorted_data = dict(sorted(data[key].items()))  # Ensure timestamps are ordered
            ax.plot(list(data[key].keys()), list(data[key].values()), colors[i], label = order[i])
            ax.plot()
            i+=1 

    ax.xaxis.set_major_locator(matplotlib.dates.AutoDateLocator())  # Auto-adjust tick frequency
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%I:%M:%S %p'))  # 12-hour format
    ax.xaxis.set_label_text('Time')
    ax.yaxis.set_label_text('Temperature (C)')

    if title != False: 
        plt.title(title)

    plt.legend( ncol = 3, loc = 'upper right', fontsize = 10, frameon = True, edgecolor = 'black', 
               facecolor = 'lightgray', columnspacing = 1.5 )

    plt.show()




graphygraph(horzapusurfs, HDAQ_order, title='HPOL APU')
graphygraph(vertapusurfs, VDAQ_order, title='VDAQ APU')
graphygraph(horzhotswapsurfs, HDAQ_order, title = 'HPOL Hotswap')
graphygraph(verthotswapsurfs, VDAQ_order, title = 'VPOL Hotswap')
"""
beep = []
for key in horzapusurfs: 
    beep.append(horzapusurfs[key])

for iter in range(len(beep)) : 
    graphygraph(beep[iter], HDAQ_order, error=[horzapuerr[iter], horzapuerrtime[iter]], title='HPOL APU', num = iter)

bop = []
for key in vertapusurfs: 
    bop.append(vertapusurfs[key])

for iter in range(len(bop)) : 
    graphygraph(bop[iter], VDAQ_order, error=[vertapuerr[iter], vertapuerrtime[iter]], title='VPOL APU', num = iter)


"""


