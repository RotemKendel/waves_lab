import pandas as pd
import os

def convert_to_csv(input_file, output_file=None):
    """
    Convert a measurement file to CSV format.
    
    Args:
        input_file (str): Path to the input file
        output_file (str, optional): Path to the output CSV file. If None, will use input filename with .csv extension
    """
    # Read the file, skipping the header line
    df = pd.read_csv(input_file, sep='\t', skiprows=1)
    
    # Drop empty columns
    df = df.dropna(axis=1, how='all')
    
    # If output_file is not specified, create one from input filename
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + '.csv'
    
    # Save as CSV
    df.to_csv(output_file, index=False)
    print(f"File converted successfully: {output_file}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python convert_to_csv.py <input_file> [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    convert_to_csv(input_file, output_file) 