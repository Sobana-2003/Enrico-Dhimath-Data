import pandas as pd

def get_category(data_type: str) -> str:
    data_type = data_type.lower()
    if any(x in data_type for x in ["int", "decimal", "numeric", "float", "double", "real"]):
        return "Numeric"
    elif any(x in data_type for x in ["date", "time", "timestamp"]):
        return "Datetime"
    elif any(x in data_type for x in ["char", "text", "varchar", "string"]):
        return "Categorical"
    elif "url" in data_type or "link" in data_type:
        return "Link"
    elif "image" in data_type or "blob" in data_type:
        return "Image"
    return "Categorical"

def summarise_df(df):
    column_names = df.columns
    summary = []
    for col in column_names:
        data_type = df[col].dtype
        if pd.api.types.is_numeric_dtype(df[col]):
            min_value = df[col].min()
            max_value = df[col].max()
        else:
            min_len = 0
            max_len = 0
            min_value = f"Len : {min_len}"
            max_value = f"Len : {max_len}"
        summary.append({
            'Column_Name': col,
            'Data_Type': data_type,
            'Min_Value': min_value,
            'Max_Value': max_value
        })
    summary_df = pd.DataFrame(summary)
    num_rows = len(df)
    num_cols = len(df.columns)
    return summary_df, num_rows, num_cols