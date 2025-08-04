import pandas as pd
import os

def load_excel_data(filepath, sheet_name=None):
    """
    Load data from an Excel file.
    
    Args:
        filepath (str): Path to the Excel file
        sheet_name (str or None): Sheet name or None to read all sheets

    Returns:
        pd.DataFrame or dict: Loaded data
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    try:
        if sheet_name:
            df = pd.read_excel(filepath, sheet_name=sheet_name)
        else:
            df = pd.read_excel(filepath, sheet_name=None)  # all sheets
        return df
    except Exception as e:
        raise Exception(f"Error loading Excel file: {e}")
