import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# Add the measurements directory to the path
MEASUREMENTS_PATH = r"C:\Users\rotem\OneDrive - Technion\school - new\waves lab\waves_lab\ocilators\harmonic_ocilator\measurments"

## here we will collect the data from the harmonic oscillator
# we will get the data at the lab
## meanwhile we will use ficticious data to test the code

#5.1 simple movement of harmonic oscillator

# real data
G = 9.795 # m/s^2
L = 97.95 # mm
deltaMassK1 = 42.68 # g
deltaMassK2 = 43.26 # g
K1 = deltaMassK1 * G / L # N/m
K2 = deltaMassK2 * G / L # N/m
total_K = K1 + K2 # N/m
trailar_mass = 0.2123 # Kg
total_points_distance = 125 # mm
total_points_distance_error = 0.1 # mm
total_points_distance_number = 239
distance_between_points = total_points_distance / total_points_distance_number # mm
distance_between_points_error = total_points_distance_error / total_points_distance_number # mm
total_time = 10 # s
# Import data from CSV files
# No friction cases
small_amp_no_friction = pd.read_csv(os.path.join(MEASUREMENTS_PATH, 'small_amp_no_friction.csv'), header=None, names=['index', 'time', 'point'])
mid_amp_no_friction = pd.read_csv(os.path.join(MEASUREMENTS_PATH, 'mid_amp_no_frictoion.csv'), header=None, names=['index', 'time', 'point'])
big_amp_no_friction = pd.read_csv(os.path.join(MEASUREMENTS_PATH, 'big_amp_no_friction.csv'), header=None, names=['index', 'time', 'point'])

# Friction cases
big_amp_low_friction = pd.read_csv(os.path.join(MEASUREMENTS_PATH, 'big_amp_low_friction.csv'), header=None, names=['index', 'time', 'point'])
big_amp_mid_friction = pd.read_csv(os.path.join(MEASUREMENTS_PATH, 'big_amp_mid_friction.csv'), header=None, names=['index', 'time', 'point'])
big_amp_high_friction = pd.read_csv(os.path.join(MEASUREMENTS_PATH, 'bid_amp_high_friction.csv'), header=None, names=['index', 'time', 'point'])

# Extract time and position data for each case
# No friction cases
time_small_amp = small_amp_no_friction['time'].values
point_small_amp = small_amp_no_friction['point'].values
position_small_amp = point_small_amp * distance_between_points  

time_mid_amp = mid_amp_no_friction['time'].values
point_mid_amp = mid_amp_no_friction['point'].values
position_mid_amp = point_mid_amp * distance_between_points

time_big_amp = big_amp_no_friction['time'].values
point_big_amp = big_amp_no_friction['point'].values
position_big_amp = point_big_amp * distance_between_points

# Friction cases
time_low_friction = big_amp_low_friction['time'].values
point_low_friction = big_amp_low_friction['point'].values
position_low_friction = point_low_friction * distance_between_points

time_mid_friction = big_amp_mid_friction['time'].values
point_mid_friction = big_amp_mid_friction['point'].values
position_mid_friction = point_mid_friction * distance_between_points

time_high_friction = big_amp_high_friction['time'].values
point_high_friction = big_amp_high_friction['point'].values
position_high_friction = point_high_friction * distance_between_points

#useful functions
def find_frequency_and_damping(point_amp,time_amp):
    """
    This function finds the frequency of the oscillation
    should be at least 2 pics to find the frequency
    """
    pics_amp = 0
    new_pic = 0
    first_pic = 0
    last_pic = 0
    for i in range(len(time_amp) - 1):
        if point_amp[i] >= point_amp[i-1] and point_amp[i] >= point_amp[i+1] and new_pic == 0:
            if first_pic == 0:
                first_pic = i
            last_pic = i
            pics_amp += 1
            new_pic = 1
        if point_amp[i] < 0:
            new_pic = 0
    total_time = time_amp[last_pic] - time_amp[first_pic]
    log_time_distance = np.log(time_amp[last_pic]) - np.log(time_amp[first_pic])
    frequency_amp = (pics_amp - 1) / total_time
    damping_amp = (point_amp[last_pic] - point_amp[first_pic]) / log_time_distance
    return frequency_amp,damping_amp

def find_amplitude(point_amp):
    """
    This function finds the amplitude of the oscillation
    """
    amplitude_amp = np.max(point_amp) - np.min(point_amp)
    return amplitude_amp


# no friction case - calclations
assert np.array_equal(time_big_amp, time_mid_amp) and np.array_equal(time_mid_amp, time_small_amp)
time = time_big_amp

frequency_small_amp,damping_small_amp = find_frequency_and_damping(point_small_amp,time_small_amp)
amplitude_small_amp = find_amplitude(point_small_amp)
frequency_mid_amp,damping_mid_amp = find_frequency_and_damping(point_mid_amp,time_mid_amp)
amplitude_mid_amp = find_amplitude(point_mid_amp)
frequency_big_amp,damping_big_amp = find_frequency_and_damping(point_big_amp,time_big_amp)
amplitude_big_amp = find_amplitude(point_big_amp)
amplitude_error = 2*distance_between_points_error

frequency_error = 0 #TODO: find the error
damping_error = 0 #TODO: find the error

plt.figure(figsize=(12, 8))
plt.title("Harmonic Oscillator Position for different amplitudes with no friction", y=1.1)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
# Remove tick labels and marks from main figure
plt.gca().set_xticklabels([])
plt.gca().set_yticklabels([])
plt.gca().set_xticks([])
plt.gca().set_yticks([])
#plot position
plt.subplot(2, 2, 1)
plt.plot(time, position_small_amp, '--g')
plt.title("fig1 - small amplitude")
plt.xlabel("Time[s]")
plt.ylabel("Position[mm]")
plt.gca().tick_params(direction='in', which='both', pad=-20)
plt.gca().tick_params(axis='x', pad=-15)  # Additional padding for x-axis
plt.gca().tick_params(axis='y', pad=-30)  # Additional padding for y-axis
plt.gca().ticklabel_format(style='plain', useOffset=False)
plt.legend()
plt.subplot(2, 2, 2)
plt.plot(time, position_mid_amp, '--g')
plt.title("fig2 - mid amplitude")
plt.xlabel("Time[s]")
plt.ylabel("Position[mm]")
plt.gca().tick_params(direction='in', which='both', pad=-20)
plt.gca().tick_params(axis='x', pad=-15)  # Additional padding for x-axis
plt.gca().tick_params(axis='y', pad=-30)  # Additional padding for y-axis
plt.gca().ticklabel_format(style='plain', useOffset=False)
plt.legend()
plt.subplot(2, 2, 3)
plt.plot(time, position_big_amp, '--g')
plt.title("fig3 - big amplitude")
plt.xlabel("Time[s]")
plt.ylabel("Position[mm]")
plt.gca().tick_params(direction='in', which='both', pad=-20)
plt.gca().tick_params(axis='x', pad=-15)  # Additional padding for x-axis
plt.gca().tick_params(axis='y', pad=-30)  # Additional padding for y-axis
plt.gca().ticklabel_format(style='plain', useOffset=False)
plt.legend()
plt.subplot(2, 2, 4)
plt.title("captions")
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
# Remove tick labels and marks from main figure
plt.gca().set_xticklabels([])
plt.gca().set_yticklabels([])
plt.gca().set_xticks([])
plt.gca().set_yticks([])
plt.text(0.2, 0.9, f"fig1 - amplitude = {amplitude_small_amp:.2f} ± {amplitude_error:.2f} \n frequency = {frequency_small_amp:.2f} ± {frequency_error:.2f} \n damping = {damping_small_amp:.2f} ± {damping_error:.2f}",
         transform=plt.gca().transAxes, verticalalignment='top', horizontalalignment='left')
plt.text(0.9, 0.9, f"fig2 - amplitude = {amplitude_mid_amp:.2f} ± {amplitude_error:.2f} \n frequency = {frequency_mid_amp:.2f} ± {frequency_error:.2f} \n damping = {damping_mid_amp:.2f} ± {damping_error:.2f}",
         transform=plt.gca().transAxes, verticalalignment='top', horizontalalignment='right')
plt.text(0.2, 0.2, f"fig3 - amplitude = {amplitude_big_amp:.2f} ± {amplitude_error:.2f} \n frequency = {frequency_big_amp:.2f} ± {frequency_error:.2f} \n damping = {damping_big_amp:.2f} ± {damping_error:.2f}",
         transform=plt.gca().transAxes, verticalalignment='bottom', horizontalalignment='left')

plt.subplots_adjust(wspace=0.4, hspace=0.4)  # Increase horizontal and vertical spacing
plt.tight_layout()  # This ensures the subplots don't overlap
plt.show()  # This will display the plot




