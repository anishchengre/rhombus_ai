
import pandas as pd
import numpy as np

def load_data(file_path: str) -> pd.DataFrame:
    """
    Loads data from a CSV or Excel file into a DataFrame.
    """
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("File format not supported. Please provide a CSV or Excel file.")
    return df


def infer_and_convert_data_types(df: pd.DataFrame, unique_ratio_threshold: float = 0.5) -> pd.DataFrame:
    """
    Infers and converts data types of each column in a DataFrame.
    Columns with object types are checked and converted to the most appropriate types.
    """
    for col in df.columns:
        original_dtype = df[col].dtype
        
        # Attempt to convert column to numeric if not already numeric
        if pd.api.types.is_object_dtype(df[col]):
            try:
                converted_numeric = pd.to_numeric(df[col], errors='coerce')
                # Only apply conversion if some non-NaN numeric values were found
                if converted_numeric.notna().sum() > 0:
                    df[col] = converted_numeric
                    continue
            except Exception:
                pass  # Skip if not convertible to numeric

        # Attempt to convert to datetime if column is still object and not numeric
        if pd.api.types.is_object_dtype(df[col]):
            try:
                converted_datetime = pd.to_datetime(df[col], errors='coerce', format='%d/%m/%Y')
                if converted_datetime.notna().sum() > 0:
                    df[col] = converted_datetime
                    continue
            except Exception:
                pass  # Skip if not convertible to datetime

        # Convert to Categorical if unique ratio is below threshold and column is still object
        if pd.api.types.is_object_dtype(df[col]):
            unique_ratio = len(df[col].unique()) / len(df[col])
            if unique_ratio < unique_ratio_threshold:
                df[col] = pd.Categorical(df[col])
            else:
                # Ensure non-numeric, non-date object columns remain as strings
                df[col] = df[col].astype(str)

    # Downcast numeric columns for memory optimization
    for col in df.select_dtypes(include=['int64', 'float64']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer' if pd.api.types.is_integer_dtype(df[col]) else 'float')

    return df



def main(file_path: str):
    """
    Main function to load data, infer data types, and display results.
    """
    # Load the data
    df = load_data(file_path)
    print("Data types before inference:")
    print(df.dtypes)

    # Infer and convert data types
    df = infer_and_convert_data_types(df)

    print("\nData types after inference:")
    print(df.dtypes)
    print("\nSample DataFrame:")
    print(df.head())

# Example usage
if __name__ == "__main__":
    file_path = "/home/anishdchengre/Desktop/rhombus_ai/api/sample_data.csv"  # Replace with your file path
    main(file_path)



