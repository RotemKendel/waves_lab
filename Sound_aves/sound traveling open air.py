import numpy as np
import matplotlib.pyplot as plt


# measure the phase shift between speaker and microphone
phase_shift = np.array([0, 0.5*np.pi, 1*np.pi, 1.5*np.pi, 2*np.pi, 2.5*np.pi, 3*np.pi, 3.5*np.pi, 4*np.pi, 4.5*np.pi, 5*np.pi, 5.5*np.pi, 6*np.pi, 6.5*np.pi, 7*np.pi, 7.5*np.pi, 8*np.pi])
distance = np.array([10.4, 13.2, 15.3, 17.3, 19.7, 21.7, 23.2, 25.8,27.5, 30, 31.8, 33.9, 36.5, 38.3, 39.8,42.9, 45.6])
distance = distance - 9
distance = distance / 100

#theoretical phase shift
tempature_kelvin = 23.3 + 273.15 #K
mollar_Mass = 0.0289644 #kg/mol
gamma = 1.4 #for air
R = 8.31446261815324 #J/mol*K
frequency = 4100  # Hz

sound_speed = np.sqrt(gamma * R * tempature_kelvin / mollar_Mass)
phase_shift_theoretical = 2 * np.pi * distance * frequency / sound_speed #rad

# Add weighted fit line
weights = 0.8 ** (phase_shift/(2*np.pi))  # More weight to closer measurements
fit_coeffs = np.polyfit(distance, phase_shift, 1, w=weights)
fit_line = np.poly1d(fit_coeffs)

# Calculate and print slopes
fit_slope = fit_coeffs[0]  # First coefficient is the slope
theoretical_slope = 2 * np.pi * frequency / sound_speed

print(f"Fitted slope: {fit_slope:.2f} rad/m")
print(f"Theoretical slope: {theoretical_slope:.2f} rad/m")
# Calculate R^2 value
residuals = phase_shift - fit_line(distance)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((phase_shift - np.mean(phase_shift))**2)
r_squared = 1 - (ss_res / ss_tot)

print(f"Percent difference: {100 * abs(fit_slope - theoretical_slope) / theoretical_slope:.1f}%")
print(f"R² value: {r_squared:.3f}")

distance_meas_error = 0.008 * 1/weights #m
phase_shift_meas_error = (10 * np.pi/180) * 1/weights

# plot the phase shift vs distance
plt.errorbar(distance, phase_shift, yerr=phase_shift_meas_error, xerr=distance_meas_error, fmt='o', color='black', capsize=1, label='Data')
plt.plot(distance, fit_line(distance), 'r--', label='Weighted Fit')
plt.plot(distance, phase_shift_theoretical, label='Theoretical Phase Shift')
plt.legend()
plt.xlabel('Distance (m)')  # Changed to meters since distance is in meters
plt.ylabel('Phase Shift (rad)')
plt.show()






# measure the time delay between speaker and microphone at 0.98m from the speaker






