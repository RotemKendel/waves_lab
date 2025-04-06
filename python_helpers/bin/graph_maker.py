import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def make_graph(csv_file, x_column, y_columns, caption, error_columns=None):
    """
    Creates a scientific graph from CSV data according to strict requirements:
    1. Font size: 11pt
    2. Proper axis scaling
    3. White background
    4. Discrete points for measurements
    5. Axis values outside graph
    6. Legend only if multiple series
    7. Caption below graph
    8. Axis labels with units
    9. Error bars if provided
    10. No title
    
    Args:
        csv_file: Path to the CSV file containing the data
        x_column: Name of the column to use for x-axis
        y_columns: List of column names to plot on y-axis
        caption: Caption text to appear below the graph
        error_columns: List of column names for error bars (optional)
    """
    # Read data from CSV
    df = pd.read_csv(csv_file)
    
    # Set fixed font size to 11pt
    plt.rcParams.update({'font.size': 11})
    
    # Create figure with white background
    fig, ax = plt.subplots(facecolor='white')
    
    # Ensure y_columns is a list
    if not isinstance(y_columns, list):
        y_columns = [y_columns]
    if error_columns is not None and not isinstance(error_columns, list):
        error_columns = [error_columns]
    
    # Plot each y column
    for i, y_col in enumerate(y_columns):
        if error_columns and error_columns[i] is not None:
            ax.errorbar(df[x_column], df[y_col], yerr=df[error_columns[i]], 
                      fmt='o', capsize=3, label=y_col)
        else:
            ax.plot(df[x_column], df[y_col], 'o', label=y_col)
    
    # Set labels with units (using column names)
    ax.set_xlabel(x_column)
    if len(y_columns) == 1:
        ax.set_ylabel(y_columns[0])
    
    # Remove gray background
    ax.set_facecolor('white')
    
    # Set axis values outside the graph
    ax.tick_params(direction='out')
    
    # Add legend if there are multiple series
    if len(y_columns) > 1:
        ax.legend()
    
    # Auto-scale axes to fit data
    ax.autoscale(enable=True, axis='both', tight=True)
    
    # Add caption below graph
    plt.figtext(0.5, 0.01, caption, ha='center', fontsize=11)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    return fig, ax
