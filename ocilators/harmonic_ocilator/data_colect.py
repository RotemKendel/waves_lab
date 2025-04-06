import numpy as np
import matplotlib.pyplot as plt




## here we will collect the data from the harmonic oscillator
# we will get the data at the lab
## meanwhile we will use ficticious data to test the code

#5.1 simple movement of harmonic oscillator

# fake data
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

