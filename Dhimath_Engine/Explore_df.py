import pandas as pd

# Function to get column names, data types, min and max values
def summarize_csv(file_path):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    # Get column names
    column_names = df.columns
    
    # Data summary
    summary = []
    
    # Iterate over each column
    for col in column_names:
        data_type = df[col].dtype  # Get the data type of the column
        
        if pd.api.types.is_numeric_dtype(df[col]):
            min_value = df[col].min()  # Get min value if numeric
            max_value = df[col].max()  # Get max value if numeric
        else:
            min_value = None
            max_value = None
            
        summary.append({
            'Column Name': col,
            'Data Type': data_type,
            'Min Value': min_value,
            'Max Value': max_value
        })
    
    # Convert to DataFrame for better readability
    summary_df = pd.DataFrame(summary)
    
    return summary_df

    # Example usage
 # Replace with your actual file path
file_path = f"G:\\XLS Data\\Battery Analytics Data\\diagnostic_capacity_data.csv"
summary = summarize_csv(file_path)
print(summary)
print(type(summary))