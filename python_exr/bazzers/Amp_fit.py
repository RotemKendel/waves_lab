import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Get the absolute path to the CSV file
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
csv_path = os.path.join("C:/Users/rotem/OneDrive - Technion/school - new/waves lab/waves_lab/python_exr/bazzers", "bazzers_data.csv")

# Read the CSV file
df = pd.read_csv(csv_path)

# Extract vectors with meaningful names
x_1 = df['x_1 (cm)'].values # x_1 (cm)
Amplitude = df['Amplitude'].values # Amplitude
L = df['L (cm)'].values # L (cm)
f = df['f (Hz)'].values # f (Hz)

# Define the amplitude function
def amplitude_function(x, a, lam, phi):
    in_cos = (np.pi/lam) * (2*x - L) + phi/2
    return np.abs(2*a * np.cos(in_cos))

# Fit the data to the amplitude function
bounds = (0, np.inf)
p0 = [1, 1, 0]
params, cov = curve_fit(amplitude_function, x_1, Amplitude, p0=p0, bounds=bounds)


# Print the fit parameters
print(f"a = {popt[0]:.4f}, lam = {popt[1]:.4f}, phi = {popt[2]:.4f}")
