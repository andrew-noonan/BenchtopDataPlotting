# Andrew Noonan 11/13
# Messing around with python to import and clean Benchtop 

# This code will plot the two runs against each other and compare 
# avg and std deviation values during different parts of the experiment

#%% 
# Import libraries
import pandas as pd
import matplotlib.pyplot as plt

#%% 
# Plot configs
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 14

#%% 
# Helper functions
# Read the CSV file
def read_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Convert epoch time to seconds and normalize
def normalize_time(data):
     # Add '20' to the beginning of the 'Time' string to make the year four digits
    data['Time'] = '20' + data['Time'].astype(str)
    # Now convert to datetime
    data['Time'] = pd.to_datetime(data['Time'], format='%Y%m%d%H%M%S.%f')
    # Normalizing time to start from zero
    data['Time'] = (data['Time'] - data['Time'].min()).dt.total_seconds()/60
    return data

# Function to identify the time window for each row
def get_time_window(time, windows_list):
    for start, end in windows_list:
        if start <= time < end:
            return f"{start}-{end}"
    return "Other"

def remove_others_sorted(data):
    return data[data['Time_Window'] != 'Other'].sort_values(by='mean')

#%% 
# Import both data sets
file_path_w_air = r'C:\Users\anoon\OneDrive - Vanderbilt\Masters Research\Data\Clean Oil\Flowmeter Calibration 11_23 w Shower Head\Aerated 2 to 3 GPM.txt'
file_path_wo_air= r'C:\Users\anoon\OneDrive - Vanderbilt\Masters Research\Data\Clean Oil\Flowmeter Calibration 11_23 w Shower Head\No Aerator 2 to 3 GPM.txt'

aerated_data = read_data(file_path_w_air)
aerated_data = normalize_time(aerated_data)

normal_data = read_data(file_path_wo_air)
normal_data = normalize_time(normal_data)

#%% 
# Plotting the first dataset
plt.figure(figsize=(10, 6))
plt.plot(aerated_data['Time'], aerated_data['Flow Rate'], marker='o', linestyle='none', markersize=5, label='Aerated Flow')

# Plotting the second dataset
plt.plot(normal_data['Time'], normal_data['Flow Rate'], marker='^', linestyle='none', markersize=5, label='No aeration')
# Adding title and labels
plt.title('Flow Rate vs Time')
plt.xlabel('Time (min)')
plt.ylabel('Flow Rate (gpm)')
# Adding a grid
plt.grid(True)
# Adding a legend
plt.legend()

#%%
# Define time windows for each dataset, calculate avg flow rates + std deviation
aerated_windows = [(0,7), (10,17), (20,28)]
normal_windows = [(0, 10), (11, 20), (22, 30)]

aerated_data['Time_Window'] = aerated_data['Time'].apply(lambda x: get_time_window(x, aerated_windows))
normal_data['Time_Window'] = normal_data['Time'].apply(lambda x: get_time_window(x, normal_windows))

aerated_stats = aerated_data.groupby('Time_Window')['Flow Rate'].agg(['mean', 'std']).reset_index()
aerated_stats = remove_others_sorted(aerated_stats)


normal_stats = normal_data.groupby('Time_Window')['Flow Rate'].agg(['mean', 'std']).reset_index()
normal_stats = remove_others_sorted(normal_stats)

print(aerated_stats)
print(normal_stats)