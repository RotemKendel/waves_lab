import pandas as pd
import matplotlib.pyplot as plt
from sympy import var, sqrt, exp, sin, cos, I
import numpy as np

n_g = 1.518
d = var('d')
E_0 = var('E_0')
k_0 = var('k_0')
theta = var('theta')
cos_alpha = sqrt(1 - n_g**2*sin(theta)**2)
r_s = (cos_alpha - n_g*cos(theta))/(cos_alpha + n_g*cos(theta))
t_sg = 2*n_g*cos(theta)/(cos_alpha + n_g*cos(theta))
t_sa = 2*cos_alpha/(n_g*cos(theta) + cos_alpha)
betta = k_0*(n_g**2*sin(theta)**2 - 1)**0.5

intensity = (t_sa*t_sg*E_0*exp(-betta*d))/(1-r_s**2*exp(-2*betta*d))

# Calculate critical angle
critical_angle = np.arcsin(1/n_g)


# Create angles between critical angle and 90 degrees
angles = np.linspace(critical_angle, np.pi/2 - 0.1, 5)  # stopping at 89.9 degrees to avoid division by zero

# Create distance array
d_values = np.linspace(0, 1000, 1000)  # distance in nm

# Set constants
E_0_val = 1
k_0_val = 2*np.pi/500  # wavelength of 500nm

# Create the plot
plt.figure(figsize=(10, 6))

for angle in angles:
    # Convert symbolic expression to numerical function
    intensity_func = intensity.subs({
        'E_0': E_0_val,
        'k_0': k_0_val,
        'theta': angle
    })
    
    # Calculate intensity values and take absolute value
    intensity_values = [abs(complex(intensity_func.subs('d', d_val))) for d_val in d_values]
    
    # Plot
    plt.plot(d_values, intensity_values, label=f'θ = {np.degrees(angle):.1f}°')

plt.xlabel('Distance (nm)')
plt.ylabel('Intensity')
plt.title('Intensity vs Distance for Different Angles Above Critical Angle')
plt.legend()
plt.grid(True)
plt.show()

