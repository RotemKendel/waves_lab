import numpy as np
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from python_helpers.bin.convert_to_csv import convert_to_csv
from python_helpers.bin.fit_nonlinear import fit_nonlinear_multiple

def bode_sample_calc(data, omega_0):
    """
    Calculate Bode plot parameters from measurement data.
    
    Args:
        data (str): Path to the input data file (.txt)
        
    Returns:
        tuple: (transfer_function, delta_phase, time, force, position, force_fit, position_fit, omega_force)
    """
    assert data.endswith('.txt'), "Input file must be a .txt file"
    csv_path = convert_to_csv(data, ['time(s)', 'count B', 'count C'])
    if csv_path is None:
        raise ValueError("Failed to convert input file to CSV")

    # Read data from CSV
    df = pd.read_csv(csv_path)
    
    # Extract vectors from dataframe
    time = df['time(s)'].values
    force = df['count B'].values  
    position = df['count C'].values

    distance_between_points = 125 / 239
    position = position * distance_between_points #mm
    force = force * distance_between_points #mm

    # Define the cosine function for fitting
    def cos_func(t, A, omega, phase):
        return A * np.cos(omega * t + phase)
    
    # Define parameter ranges for fitting
    # Force fitting parameters
    force_param_ranges = [
        (0, np.max(np.abs(force)) * 2),  # A
        (0.1 * omega_0, 10 * omega_0),   # omega 
        (-np.pi, np.pi)                   # phase
    ]
    
    # Position fitting parameters
    pos_param_ranges = [
        (0, np.max(np.abs(position)) * 2),  # A
        (0.1 * omega_0, 10 * omega_0),      # omega
        (-np.pi, np.pi)                      # phase
    ]
    omega_force = 4
    omega_pos = 0
    count = 0
    while abs(omega_force - omega_pos) > 0.3 and count < 100:
        # Perform multiple fits to find best parameters for force
        force_popt, force_pcov, force_residual, force_results = fit_nonlinear_multiple(
            time, force, cos_func, 
            n_iterations=20,
            param_ranges=force_param_ranges
        )
    
        # Perform multiple fits to find best parameters for position
        pos_popt, pos_pcov, pos_residual, pos_results = fit_nonlinear_multiple(
            time, position, cos_func,
            n_iterations=20,
            param_ranges=pos_param_ranges
        )
        # Extract best fit parameters
        A_force, omega_force, phase_force = force_popt
        A_pos, omega_pos, phase_pos = pos_popt
        count += 1
    if count == 100:
        print("Failed to converge - bad sample")
        return 0,0,time,force,position,0,0,0
    
    
    # Generate fitted curves
    force_fit = cos_func(time, A_force, omega_force, phase_force)
    position_fit = cos_func(time, A_pos, omega_pos, phase_pos)

    delta_phase = ( phase_force - phase_pos)%(np.pi)
    if omega_force < omega_0 and delta_phase > 2.5:
        delta_phase = delta_phase - np.pi
    elif omega_force > omega_0 and delta_phase < 1:
        delta_phase = delta_phase + np.pi
    print(delta_phase)
    transfer_function = abs(A_pos / A_force)
    print(transfer_function)

    return transfer_function, delta_phase, time, force, position, force_fit, position_fit, omega_force