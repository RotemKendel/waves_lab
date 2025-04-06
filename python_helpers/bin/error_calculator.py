import numpy as np
import sympy as sp

#data_names is a vector of data names
#data_values is a vector of data values
#equation is a string of the equation to be calculated
#error is a vector of data errors by number
#return_format is a string of the format to return the error in
def drag_error_calculator(data_names, data_values, equation, error, return_format = "lab_conventional"):
    assert len(data_names) == len(error)
    try:
        equation = sp.sympify(equation)
    except Exception as e:
        raise ValueError(f"Invalid equation: {e}, please use sympy syntax https://docs.sympy.org/latest/tutorial/index.html")
    power_total_error = 0.0
    print("delta(",equation, ") = ", end="")
    for i in range(len(data_names)):
        local_diff = equation.diff(data_names[i])
        print(local_diff, "*delta(", data_names[i], ") + ", end="")
        local_diff_value = local_diff.subs(data_names[i], data_values[i])
        local_error = (local_diff_value * error[i])**2
        power_total_error += local_error
    # Evaluate the final expression with all substitutions
    evaluated_error = power_total_error.subs(dict(zip(data_names, data_values)))
    evaluated_error = float(np.sqrt(float(evaluated_error)))
    print(" = ",evaluated_error)
    if return_format == "float":
        return evaluated_error
    elif return_format == "sympy":
        return evaluated_error
    elif return_format == "lab_conventional":
        equation_result = equation.subs(dict(zip(data_names, data_values)))
        # Convert to float for formatting
        result_value = float(equation_result)
        error_value = float(evaluated_error)
        
        # Find the position of the first non-zero digit in the error
        error_str = f"{error_value:.10f}"
        first_non_zero = next((i for i, c in enumerate(error_str) if c != '0' and c != '.'), len(error_str))
        
        # Format the result to match the error's precision
        if first_non_zero < len(error_str):
            # Calculate how many decimal places we need based on the error
            if error_value < 1:
                # If error is in tenths place (0.x), we need 1 decimal place
                if first_non_zero == 2:  # Error is in tenths place (0.x)
                    decimal_places = 1
                else:
                    decimal_places = first_non_zero - 1  # -1 to include the digit after the error position
                # Ensure we have enough decimal places, adding zeros if needed
                formatted_result = f"{result_value:.{decimal_places}f}"
            else:
                # For errors >= 1, no decimal places needed
                formatted_result = f"{int(round(result_value))}"
            
            # Get the first significant digit of the error
            error_digit = int(error_str[first_non_zero])
            result = f"{formatted_result}({error_digit})"
        else:
            # Only use 1 if we truly can't find any non-zero digits
            result = f"{result_value}(1)"
        
        return result
    else:
        raise ValueError(f"Invalid return format: {return_format}, please use 'float' or 'sympy'")



