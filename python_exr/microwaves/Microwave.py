import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Get the absolute path to the CSV file
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
csv_path = os.path.join("C:/Users/rotem/OneDrive - Technion/school - new/waves lab/waves_lab/python_exr/microwaves", "microwave_waveguide_data.csv")

# Read the CSV file
df = pd.read_csv(csv_path)

# Extract vectors with meaningful names
theta = df['theta(deg)'].values  # Angles in degrees
intensity1 = df['power_1'].values    # Power measurements from first detector (x-axis)
intensity2 = df['power_2'].values    # Power measurements from second detector (y-axis)
mean_intensity2 = np.mean(intensity2)

# Convert angles to radians for potential calculations
theta_rad = np.radians(theta)
mean_intensity2_vector = np.full_like(theta_rad, mean_intensity2)

# Define the sine function
def sine_function(x, A, B, C, D):
    return A * np.sin(B * x + C) + D

# Fit sine function to linear polarization data
popt, _ = curve_fit(sine_function, theta_rad, intensity1)
sine_fit = sine_function(theta_rad, *popt)

# Create figure with specific size
plt.figure(figsize=(10, 6))

# Plot the data
plt.plot(theta_rad, mean_intensity2_vector, 'g--', label='mean intensity')
plt.plot(theta_rad, intensity1, 'o', label='linear polarization')
plt.plot(theta_rad, intensity2, 'go', label='circular polarization')
plt.plot(theta_rad, sine_fit, 'r-', label='sine fit', alpha=1)

plt.xlabel('Angle (radians)')
plt.ylabel('Intensity')
plt.title('Intensity vs Angle(radians)')

# Add caption with adjusted position
plt.figtext(0.5, 0.01, 'The plot shows two measurements of the intensity of a microwave signal as a function of the angle of the polarization of the signal base of the galbo distance.', 
            ha='center', fontsize=10, wrap=True)

# Adjust layout to prevent overlap
plt.tight_layout()

plt.legend()
plt.show()

# Print the sine function parameters
print(f"Sine function: y = {popt[0]:.4f} * sin({popt[1]:.4f}x + {popt[2]:.4f}) + {popt[3]:.4f}")

# The vectors can now be used for further analysis
# theta: contains the angle measurements in degrees
# theta_rad: contains the angle measurements in radians
# power_1: contains the power measurements from the first detector (x-axis)
# power_2: contains the power measurements from the second detector (y-axis)
# intensity: contains the total wave intensity
