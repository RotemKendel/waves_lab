import numpy as np
import matplotlib.pyplot as plt
import pandas as pd




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
small_amp_no_friction = pd.read_csv('measurments/small_amp_no_friction.csv', header=None, names=['index', 'time', 'point'])
mid_amp_no_friction = pd.read_csv('measurments/mid_amp_no_frictoion.csv', header=None, names=['index', 'time', 'point'])
big_amp_no_friction = pd.read_csv('measurments/big_amp_no_friction.csv', header=None, names=['index', 'time', 'point'])

# Friction cases
big_amp_low_friction = pd.read_csv('measurments/big_amp_low_friction.csv', header=None, names=['index', 'time', 'point'])
big_amp_mid_friction = pd.read_csv('measurments/big_amp_mid_friction.csv', header=None, names=['index', 'time', 'point'])
big_amp_high_friction = pd.read_csv('measurments/bid_amp_high_friction.csv', header=None, names=['index', 'time', 'point'])

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

# no friction case - calclations
def find_pics(point_amp,time_amp):
    pics_amp = 0
    new_pic = 0
    first_pic = 0
    last_pic = 0
    for i in range(len(time_small_amp)):
        if point_amp[i] >= point_amp[i-1] and point_amp[i] >= point_amp[i+1] and new_pic == 0:
            if first_pic == 0:
                first_pic = time_amp[i]
            pics_amp += 1
            new_pic = 1
        if point_amp[i] < 0:
            new_pic = 0
    frequency_amp = pics_amp / total_time
    return frequency_amp

time = np.linspace(0, 10, 1000)
x = np.sin(time)
position_error = np.ones_like(x) * 0.1  # Create error array for position data
# calclations
Amplitude = np.max(x)
Frequency = np.mean(x)
phase = np.mean(x)
sample_error_Amplitude = 0.1 # TODO: get the error from the lab
sample_error_Frequency = 0.1 # TODO: get the error from the lab
sample_error_phase = 0.1 # TODO: get the error from the lab
#plot the data for sanity check
plt.figure(figsize=(12, 8))

# Plot the position data
plt.subplot(2, 1, 1)
plt.plot(time, x, label="Position")
plt.axhline(y=Amplitude, color='r', linestyle='--', label=f'Amplitude = {Amplitude:.2f}')
plt.axhline(y=Frequency, color='g', linestyle='--', label=f'Frequency = {Frequency:.2f}')
plt.axhline(y=phase, color='b', linestyle='--', label=f'Phase = {phase:.2f}')
plt.title("Harmonic Oscillator Position and Parameters")
plt.xlabel("Time")
plt.ylabel("Position")
plt.legend()

# Plot with error bars
plt.subplot(2, 1, 2)
plt.errorbar(time, x, yerr=position_error, label="Position")
plt.axhline(y=Amplitude, color='r', linestyle='--', label=f'Amplitude = {Amplitude:.2f} ± {sample_error_Amplitude:.2f}')
plt.axhline(y=Frequency, color='g', linestyle='--', label=f'Frequency = {Frequency:.2f} ± {sample_error_Frequency:.2f}')
plt.axhline(y=phase, color='b', linestyle='--', label=f'Phase = {phase:.2f} ± {sample_error_phase:.2f}')
plt.title("Harmonic Oscillator with Error Bars")
plt.xlabel("Time")
plt.ylabel("Position")
plt.legend()

plt.tight_layout()
plt.show()

#5.2 find K for two springs

# fake data
first_spring_weight = 10
second_spring_weight = 20
first_spring_extension = 0.05
second_spring_extension = 0.1
oscillator_weight = 10

weight_error = 0.1
extension_error = 0.01

# calclations
k_first_spring = first_spring_weight / first_spring_extension
k_second_spring = second_spring_weight / second_spring_extension
k_first_spring_error = weight_error / first_spring_extension
k_second_spring_error = weight_error / second_spring_extension


#5.3

#5.4 - bound states

