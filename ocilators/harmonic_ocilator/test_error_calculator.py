import numpy as np
import sympy as sp
from python_helpers.bin.error_calculator import drag_error_calculator

# Test case 1: Simple linear equation f = x + y
print("Test case 1: Simple linear equation f = x + y")
data_names = ['x', 'y']
data_values = [2, 3]
equation = 'x + y'
error = [0.1, 0.2]
result = drag_error_calculator(data_names, data_values, equation, error)
print(f"Test 1 - Linear equation (x + y):")
print(f"Expected error: {np.sqrt(0.1**2 + 0.2**2)}")
print(f"Calculated error: {result}\n")
# Test case 2: Quadratic equation f = x^2
print("Test case 2: Quadratic equation f = x^2")
data_names = ['x']
data_values = [2]
equation = 'x**2'
error = [0.1]
result = drag_error_calculator(data_names, data_values, equation, error)
print(f"Test 2 - Quadratic equation (x^2):")
print(f"Expected error at x={data_values[0]}: {2*data_values[0]*error[0]}")
print(f"Calculated error: {result}\n")
# Test case 3: Product of variables f = x*y
print("Test case 3: Product of variables f = x*y")
data_names = ['x', 'y']
data_values = [2, 3]
equation = 'x*y'
error = [0.1, 0.2]
result = drag_error_calculator(data_names, data_values, equation, error)
print(f"Test 3 - Product equation (x*y):")
print(f"Expected error at x={data_values[0]}, y={data_values[1]}: {np.sqrt((data_values[1]*error[0])**2 + (data_values[0]*error[1])**2)}")
print(f"Calculated error: {result}\n")

# Test case 4: Three variables with mixed operations f = x*y + z
print("Test case 4: Three variables with mixed operations f = x*y + z")
data_names = ['x', 'y', 'z']
data_values = [2, 3, 4]
equation = 'x*y + z'
error = [0.1, 0.2, 0.3]
result = drag_error_calculator(data_names, data_values, equation, error)
print(f"Test 4 - Mixed operations (x*y + z):")
print(f"Expected error at x={data_values[0]}, y={data_values[1]}, z={data_values[2]}: {np.sqrt((data_values[1]*error[0])**2 + (data_values[0]*error[1])**2 + error[2]**2)}")
print(f"Calculated error: {result}\n")

# Test case 5: Four variables with complex equation f = x*y*z + w^2
print("Test case 5: Four variables with complex equation f = x*y*z + w^2")
data_names = ['x', 'y', 'z', 'w']
data_values = [2, 3, 4, 5]
equation = 'x*y*z + w**2'
error = [0.1, 0.2, 0.3, 0.4]
result = drag_error_calculator(data_names, data_values, equation, error)
print(f"Test 5 - Complex equation (x*y*z + w^2):")
print(f"Expected error at x={data_values[0]}, y={data_values[1]}, z={data_values[2]}, w={data_values[3]}: {np.sqrt((data_values[1]*data_values[2]*error[0])**2 + (data_values[0]*data_values[2]*error[1])**2 + (data_values[0]*data_values[1]*error[2])**2 + (2*data_values[3]*error[3])**2)}")
print(f"Calculated error: {result}\n")

# Test case 6: Real-world pendulum frequency f = 1/(2π) * √(g/L)
print("Test case 6: Pendulum frequency f = 1/(2π) * √(g/L)")
data_names = ['g', 'L']
data_values = [9.81, 1.0]  # g in m/s², L in meters
equation = '1/(2*pi) * sqrt(g/L)'
error = [0.01, 0.005]  # error in g and L measurements
result = drag_error_calculator(data_names, data_values, equation, error)
print(f"Test 6 - Pendulum frequency:")
print(f"Expected error at g={data_values[0]} m/s², L={data_values[1]} m:")
expected_error = (1/(2*np.pi)) * np.sqrt((error[0]/(2*np.sqrt(data_values[0]*data_values[1])))**2 + 
                                        (np.sqrt(data_values[0])*error[1]/(2*data_values[1]**(3/2)))**2)
print(f"Expected error: {expected_error}")
print(f"Calculated error: {result}")