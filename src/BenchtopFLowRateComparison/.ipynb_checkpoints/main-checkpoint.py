# Entry point of the application
import pandas as pd
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display


# Plot configs
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 14

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
    data['Time'] = (data['Time'] - data['Time'].min()).dt.total_seconds()
    return data

# Import both data sets
file_path_w_air = r'C:\Users\anoon\OneDrive - Vanderbilt\Masters Research\Data\Clean Oil\Flowmeter Calibration 11_23 w Shower Head\Aerated 2 to 3 GPM.txt'
file_path_wo_air= r'C:\Users\anoon\OneDrive - Vanderbilt\Masters Research\Data\Clean Oil\Flowmeter Calibration 11_23 w Shower Head\No Aerator 2 to 3 GPM.txt'

aerated_data = read_data(file_path_w_air)
aerated_data = normalize_time(aerated_data)

normal_data = read_data(file_path_wo_air)
normal_data = normalize_time(normal_data)

# Plotting the first dataset
plt.figure(figsize=(10, 6))
plt.plot(aerated_data['Time']/60, aerated_data['Flow Rate'], marker='o', linestyle='none', markersize=5, label='Aerated Flow')

# Plotting the second dataset
# Replace 'Time2' and 'Flow Rate2' with actual column names of the second dataset
plt.plot(normal_data['Time']/60, normal_data['Flow Rate'], marker='^', linestyle='none', markersize=5, label='No aeration')

# Adding title and labels
plt.title('Flow Rate vs Time')
plt.xlabel('Time (min)')
plt.ylabel('Flow Rate (gpm)')

# Adding a grid
plt.grid(True)

# Adding a legend
plt.legend()
