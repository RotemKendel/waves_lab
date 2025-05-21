import numpy as np
from scipy.optimize import curve_fit
import inspect

def fit_nonlinear(x, y, func, p0=None, bounds=(-np.inf, np.inf)):
    """
    Perform nonlinear least squares fitting of data to a given function.
    
    Parameters:
    -----------
    x : array_like
        The x-axis values
    y : array_like
        The y-axis values
    func : callable
        The function to fit. Should take x as first argument and parameters as subsequent arguments
    p0 : array_like, optional
        Initial guess for the parameters
    bounds : tuple, optional
        Lower and upper bounds on parameters. Default is no bounds.
        
    Returns:
    --------
    popt : array
        Optimal values for the parameters
    pcov : 2d array
        The estimated covariance of popt
    """
    # Convert inputs to numpy arrays
    x = np.asarray(x)
    y = np.asarray(y)
    
    # Perform the fit
    popt, pcov = curve_fit(func, x, y, p0=p0, bounds=bounds)
    
    return popt, pcov

def fit_nonlinear_multiple(x, y, func, n_iterations=10, param_ranges=None, bounds=(-np.inf, np.inf)):
    """
    Perform multiple nonlinear fits with different initial parameters to find the best fit.
    
    Parameters:
    -----------
    x : array_like
        The x-axis values
    y : array_like
        The y-axis values
    func : callable
        The function to fit
    n_iterations : int, optional
        Number of different initial parameter sets to try
    param_ranges : list of tuples, optional
        List of (min, max) tuples for each parameter to generate random initial values
    bounds : tuple, optional
        Lower and upper bounds on parameters
        
    Returns:
    --------
    best_popt : array
        Best optimal values for the parameters
    best_pcov : 2d array
        The estimated covariance of best_popt
    best_residual : float
        The residual sum of squares for the best fit
    all_results : list
        List of all results (popt, pcov, residual) for each iteration
    """
    x = np.asarray(x)
    y = np.asarray(y)
    
    best_residual = float('inf')
    best_popt = None
    best_pcov = None
    all_results = []
    
    # If param_ranges not provided, use default ranges
    if param_ranges is None:
        # Default to ±10 around 0 for each parameter
        param_ranges = [(-10, 10) for _ in range(len(inspect.signature(func).parameters) - 1)]
    
    for _ in range(n_iterations):
        # Generate random initial parameters within the specified ranges
        p0 = [np.random.uniform(min_val, max_val) for min_val, max_val in param_ranges]
        
        try:
            popt, pcov = curve_fit(func, x, y, p0=p0, bounds=bounds)
            
            # Calculate residual sum of squares
            y_fit = func(x, *popt)
            residual = np.sum((y - y_fit) ** 2)
            
            all_results.append((popt, pcov, residual))
            
            # Update best fit if this one is better
            if residual < best_residual:
                best_residual = residual
                best_popt = popt
                best_pcov = pcov
                
        except (RuntimeError, ValueError):
            # Skip this iteration if the fit fails
            continue
    
    return best_popt, best_pcov, best_residual, all_results

# Example usage:
if __name__ == "__main__":
    # Example function: y = a * exp(-b * x) + c
    def example_func(x, a, b, c):
        return a * np.exp(-b * x) + c
    
    # Generate some example data
    x = np.linspace(0, 10, 100)
    y = 2.5 * np.exp(-0.5 * x) + 1.0 + 0.1 * np.random.randn(len(x))
    
    # Define parameter ranges for the example function
    param_ranges = [
        (0, 5),    # range for parameter 'a'
        (0, 2),    # range for parameter 'b'
        (0, 2)     # range for parameter 'c'
    ]
    
    # Perform multiple fits
    best_popt, best_pcov, best_residual, all_results = fit_nonlinear_multiple(
        x, y, example_func, n_iterations=20, param_ranges=param_ranges
    )
    
    print("Best fitted parameters:", best_popt)
    print("Parameter uncertainties:", np.sqrt(np.diag(best_pcov)))
    print("Best residual sum of squares:", best_residual)
    
    # Print all results sorted by residual
    print("\nAll results sorted by residual:")
    sorted_results = sorted(all_results, key=lambda x: x[2])
    for i, (popt, pcov, residual) in enumerate(sorted_results):
        print(f"\nIteration {i+1}:")
        print(f"Parameters: {popt}")
        print(f"Residual: {residual}")
