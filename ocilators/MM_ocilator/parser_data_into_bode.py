import os
import numpy as np
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from python_helpers.bin.bode_sample_calc import bode_sample_calc
from python_helpers.bin.fit_nonlinear import fit_nonlinear_multiple
# Get list of data files starting with 'oc'
data_dir = os.path.join(os.path.dirname(__file__), 'Data')
data_files = [f for f in os.listdir(data_dir) if f.startswith('oc') and f.endswith('.txt')]

# Initialize lists to store results
omegas_list = []
transfer_functions_list = []
delta_phases_list = []

k1 = 6.3 #N/m
k2 = 6.7 #N/m
m = 0.219 #Kg
omega_0_calc = np.sqrt(k1 + k2 / m)

# Process each file
for data_file in data_files:
    # Calculate bode plot parameters
    full_path = os.path.join(data_dir, data_file)
    transfer, phase, _, _, _, _, _, omega = bode_sample_calc(full_path, omega_0_calc)
    
    # Append results to lists
    omegas_list.append(omega)
    transfer_functions_list.append(transfer) 
    delta_phases_list.append(phase)

# Convert lists to numpy arrays
omegas = np.array(omegas_list)
transfer_functions = np.array(transfer_functions_list)
delta_phases = np.array(delta_phases_list)

# Get sorting indices based on omega values
sort_idx = np.argsort(omegas)

# Sort all arrays using the same index order
omegas = omegas[sort_idx]
transfer_functions = transfer_functions[sort_idx]
delta_phases = delta_phases[sort_idx]

for i, phase in enumerate(delta_phases):
    if phase > np.pi + 0.1:
        delta_phases[i] = phase / 2


# Now you can use omegas, transfer_functions, and delta_phases as needed
import matplotlib.pyplot as plt

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 9))

# Define the transfer function model for magnitude
def magnitude_func(omega, A, omega_0, zeta):
    return A / np.sqrt((omega_0**2 - omega**2)**2 + (2*zeta*omega_0*omega)**2)

# Define the phase function model 
def phase_func(omega, omega_0, zeta):
    return -np.arctan2(2*zeta*omega_0*omega, (omega_0**2 - omega**2))

# Define parameter ranges for magnitude fitting
magnitude_param_ranges = [
    (0, np.max(transfer_functions) * 2),  # A
    (0.5 * omega_0_calc, 2 * omega_0_calc),  # omega_0
    (0, 2)  # zeta
]

# Define parameter ranges for phase fitting
phase_param_ranges = [
    (0.5 * omega_0_calc, 2 * omega_0_calc),  # omega_0
    (0, 2)  # zeta
]

# Perform multiple fits for magnitude
mag_popt, mag_pcov, mag_residual, mag_results = fit_nonlinear_multiple(
    omegas, transfer_functions, magnitude_func,
    n_iterations=100,
    param_ranges=magnitude_param_ranges
)

# Perform multiple fits for phase
phase_popt, phase_pcov, phase_residual, phase_results = fit_nonlinear_multiple(
    omegas, delta_phases, phase_func,
    n_iterations=5,
    param_ranges=phase_param_ranges
)

# Generate smooth curves for plotting
omega_smooth = np.linspace(min(omegas), max(omegas), 1000)
magnitude_fit = magnitude_func(omega_smooth, *mag_popt)
phase_fit = phase_func(omega_smooth, *phase_popt)


# Plot amplitude response
ax1.plot(omegas, transfer_functions, 'b.', label='Data')
ax1.plot(omega_smooth, magnitude_fit, 'b-', label='Fit')
ax1.axvline(x=omega_0_calc, color='k', linestyle='--', label='ω₀')
ax1.set_xlabel('Angular Frequency ω (rad/s)')
ax1.set_ylabel('Magnitude [a.u.]')
ax1.set_title('Frequency Response - Magnitude')
ax1.grid(True)
ax1.set_xlim(4, omegas.max()*1.01)
ax1.set_ylim(transfer_functions.min()/0.9, transfer_functions.max()*1.1)
ax1.legend()

# Plot phase response 
ax2.plot(omegas, delta_phases, 'r.', label='Data')
ax2.plot(omega_smooth, phase_fit, 'r-', label='Fit')
ax2.axvline(x=omega_0_calc, color='k', linestyle='--', label='ω₀')
ax2.axhline(y=np.pi/2, color='k', linestyle=':', label='π/2')
ax2.set_xlabel('Angular Frequency ω (rad/s)')
ax2.set_ylabel('Phase [rad]')
ax2.set_title('Frequency Response - Phase')
ax2.grid(True)
ax2.set_xlim(4, omegas.max()*1.01)
ax2.set_ylim(delta_phases.min()/0.9, delta_phases.max()*1.1)
ax2.legend()

# Adjust spacing between subplots
plt.subplots_adjust(hspace=1)  # Increase vertical spacing between subplots
plt.tight_layout()

# Show the plot
plt.show()
