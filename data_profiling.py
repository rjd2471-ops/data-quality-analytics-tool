import pandas as pd
import streamlit as st

@st.cache_data

def profiling(df):
    """
    Function to perform data profiling on a given DataFrame.

    Parameters:
        df (pd.DataFrame): The input DataFrame to profile.

    Returns:
        dict: A dictionary containing profiling information.
    """

    # 1. Check whether DataFrame is empty
    if len(df) == 0:
        raise ValueError( "The DataFrame is empty. Please provide a non-empty DataFrame for profiling.")

    # 2. Calculate memory usage in MB
    memory_usage = df.memory_usage(deep=True).sum() / (1024 ** 2)#Here deep=True means that the memory usage of the DataFrame will be calculated including the memory used by the data itself, as well as any additional memory used by the DataFrame's index and other metadata. This provides a more accurate estimate of the total memory footprint of the DataFrame.

    # 3. Warn if DataFrame is large
    if memory_usage > 1000:
        print(f"Warning: The DataFrame is large "f"({memory_usage:.2f} MB). Profiling may take some time.")

    # 4. Calculate duplicate rows and percentage
    duplicate_count = df.duplicated().sum()
    duplicate_percentage = (duplicate_count / len(df)) * 100

    # 5. Calculate missing-value counts and percentage
    missing_counts = df.isnull().sum()
    missing_percentage = (missing_counts / len(df)) * 100

    # 6. Calculate summary statistics
    summary_statistics = df.describe(include="all").to_dict()#include="all" means that the summary statistics will be calculated for all columns in the DataFrame, regardless of their data type. This includes numerical, categorical, and object columns. By default, describe() only includes numerical columns, but with include="all", it provides a more comprehensive overview of the entire DataFrame.

    # 7. Create profiling dictionary
    profiling_info = {
        "num_rows": df.shape[0],
        "num_columns": df.shape[1],
        "column_names": df.columns.tolist(),
        "data_types": df.dtypes.to_dict(),

        "duplicate_rows": duplicate_count,
        "duplicate_percentage": duplicate_percentage,

        "missing_values": missing_counts.to_dict(),
        "missing_percentage": missing_percentage.to_dict(),

        "summary_statistics": summary_statistics,

        "memory_usage": memory_usage,

        "unique_values": {col: df[col].nunique() for col in df.columns}
    }

    return profiling_info
if __name__ == "__main__":
    import data_loader as dl
    df = dl.load_data(r"C:\Users\PC\Desktop\DataCleaning_Tool\student-data-v2.csv")
    profiling_info = profiling(df)
    print(profiling_info)