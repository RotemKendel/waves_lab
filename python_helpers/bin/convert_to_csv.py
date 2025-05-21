import pandas as pd
import os

def convert_to_csv(input_file, column_names, output_file=None):
    """
    Convert a measurement file to CSV format.
    
    Args:
        input_file (str): Path to the input file
        column_names (list): List of column names to use
        output_file (str, optional): Path to the output CSV file. If None, will use input filename with .csv extension
        
    Returns:
        str: Path to the converted CSV file
    """
    # Read the file, skipping the header line
    df = pd.read_csv(input_file, sep='\t', skiprows=1)
    
    # Drop empty columns
    df = df.dropna(axis=1, how='all')
    
    # Rename columns using 'idx' for first column and provided names for the rest
    columns = ['idx'] + column_names
    if len(columns) != len(df.columns):
        raise ValueError(f"Number of column names ({len(columns)}) does not match number of data columns ({len(df.columns)})")
    df.columns = columns
    
    # If output_file is not specified, create one from input filename
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + '.csv'
    
    # Save as CSV
    df.to_csv(output_file, index=False)
    print(f"File converted successfully: {output_file}")
    return output_file