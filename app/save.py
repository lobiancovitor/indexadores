import pandas as pd
import os

data_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

def save_indicator_data(data_dict: dict) -> None:
    """
    Save each economic indicator data as a CSV file in the 'data' directory.

    Args:
    data_dict (dict): Dictionary where keys are indicator names and values are DataFrames with the data.
    """
    # Create 'data' directory if it doesn't exist
    os.makedirs(data_folder_path, exist_ok=True)
    
    # Get the current date for the filenames
    current_date = pd.Timestamp.now().strftime("%Y%m%d")

    # Save each DataFrame to CSV
    for indicator, df in data_dict.items():
        # Generate filename with current date
        filename = os.path.join(data_folder_path, f"{indicator.lower()}_{current_date}.csv")
        
        # Save DataFrame to CSV
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")