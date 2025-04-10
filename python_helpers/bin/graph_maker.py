import matplotlib.pyplot as plt
import pandas as pd

def make_graph(csv_file, caption):
    """
    Creates a scientific graph from CSV data according to requirements:
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
        caption: Caption text to appear below the graph
    """
    # Read data from CSV
    df = pd.read_csv(csv_file)
    assert len(df.columns) > 1, "CSV file must have at least two columns"
    
    # Set fixed font size to 11pt
    plt.rcParams.update({'font.size': 11})
    
    # Create figure with white background
    fig, ax = plt.subplots(facecolor='white')
    
    # Get column names
    columns = df.columns.tolist()
    
    # First column is x-axis
    x_column = columns[0]
    assert x_column.lower().startswith("x"), "First column must be x-axis"
    assert "[" in x_column and "]" in x_column, "X-axis column must include units in parentheses"
    x_name = x_column[1:].strip()  # Remove first letter only
    
    # Process y-columns and their errors
    y_columns = []
    error_columns = []
    y_names = []
    
    # Each y-column must have a corresponding error column
    for i in range(1, len(columns), 2):
        y_col = columns[i]
        error_col = columns[i + 1] if i + 1 < len(columns) else None
        
        # Validate y-column
        assert y_col.lower().startswith("y"), f"Column {y_col} must be a y-axis column"
        assert "[" in y_col and "]" in y_col, f"Column {y_col} must include units in parentheses"
        
        # Validate error column
        assert error_col is not None, f"Missing error column for {y_col}"
        assert error_col.lower().startswith("error"), f"Column {error_col} must be an error column"
        assert "[" in error_col and "]" in error_col, f"Column {error_col} must include units in parentheses"
        
        # Extract names (without prefix)
        y_name = y_col[1:].split("[")[0].strip()
        error_name = error_col[5:].split("[")[0].strip()
        assert y_name == error_name, f"Y-column {y_col} and error column {error_col} must match"
        
        y_columns.append(y_col)
        error_columns.append(error_col)
        y_names.append(y_name)
    
    # Plot each y column with its error
    for y_col, error_col in zip(y_columns, error_columns):
        ax.errorbar(df[x_column], df[y_col], yerr=df[error_col], 
                  fmt='o', capsize=3, label=y_col)
    
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
