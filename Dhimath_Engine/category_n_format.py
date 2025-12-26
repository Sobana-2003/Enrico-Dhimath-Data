# %%
import pandas as pd
import random
from datetime import datetime
import matplotlib.pyplot as plt
import re
import validators

# %%
# List of possible date formats
DMY_FAMILY = [
    "%d-%m-%Y", "%d/%m/%Y", "%d.%m.%Y", "%d %b %Y", "%d %B %Y",
    "%d-%m-%y", "%d/%b/%Y", "%d%m%Y", "%d-%b-%Y", "%d-%b-%y",
    "%d-%B-%y", "%d/%m/%y"
]

MDY_FAMILY = [
    "%m-%d-%Y", "%m/%d/%Y", "%b %d, %Y", "%B %d, %Y",
    "%m-%d-%y", "%b-%d-%Y", "%m/%d/%y", "%m%d%Y"
]

MY_FAMILY = ["%b-%Y", "%B-%Y", "%B %Y", "%b %Y"]

YMD_FAMILY = [
    "%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d",
    "%Y%m%d", "%y-%m-%d", "%Y/%b/%d"
]

Y_FAMILY = ["%Y"] #"%y", 

FAMILY_MAP = {
    'DMY': DMY_FAMILY,
    'MDY': MDY_FAMILY,
    'MY': MY_FAMILY,
    'YMD': YMD_FAMILY,
    'Y': Y_FAMILY
}

# %%
def is_valid_date(value, date_format):
    try:
        datetime.strptime(str(value), date_format)
        return True
    except ValueError:
        return False

# %%
def detect_date_format(column_data):
    scores = {}
    family_scores = {}

    fraction = 0.10
    sample_size = min(int(fraction * len(column_data)), len(column_data))
    sequential_sample = column_data.iloc[:sample_size]
    remaining_data = column_data.iloc[sample_size:]
    random_sample = remaining_data.sample(frac=fraction, replace=False, random_state=42)

    combined_sample = pd.concat([sequential_sample, random_sample])
    total_samples = len(combined_sample)

    for fmt_family, fmt_list in FAMILY_MAP.items():
        for fmt in fmt_list:
            scores[fmt] = 0

    for val in combined_sample:
        matched_formats = []
        for fmt_family, fmt_list in FAMILY_MAP.items():
            for fmt in fmt_list:
                if is_valid_date(val, fmt):
                    matched_formats.append(fmt)
        for matched_fmt in matched_formats:
            scores[matched_fmt] += 1

    for fmt_family, fmt_list in FAMILY_MAP.items():
        family_scores[fmt_family] = sum(scores[fmt] for fmt in fmt_list)

    best_family = max(family_scores, key=family_scores.get)
    if family_scores[best_family] >= 0.85 * total_samples:
        sub_category = best_family
    else:
        sub_category = 'Unknown'

    return scores, family_scores, sub_category

# %%
def plot_family_scores(family_scores, column_name):
    plt.figure(figsize=(8,6))
    plt.bar(family_scores.keys(), family_scores.values(), color='skyblue')
    plt.title(f"Date Format Family Scores for Column '{column_name}'")
    plt.xlabel('Date Format Family')
    plt.ylabel('Matching Scores')
    plt.tight_layout()
    plt.show()

# %%
def plot_winner_format_scores(format_scores, winner_family, column_name):
    winner_formats = FAMILY_MAP[winner_family]
    winner_format_scores = {fmt: format_scores.get(fmt, 0) for fmt in winner_formats}

    plt.figure(figsize=(12,6))
    bars = plt.bar(winner_format_scores.keys(), winner_format_scores.values(), color='lightgreen')
    plt.title(f"Winner Family ('{winner_family}') Format Scores for Column '{column_name}'")
    plt.xticks(rotation=90)
    plt.xlabel('Date Formats')
    plt.ylabel('Matching Scores')

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.5, int(yval), ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    plt.show()

# %%
def is_date_column_by_first_rows(column_data, threshold=0.7):
    non_null_data = column_data.dropna().astype(str)
    first_entries = non_null_data.head(10)
    
    valid_dates = 0
    for val in first_entries:
        for fmt_list in FAMILY_MAP.values():
            if any(is_valid_date(val, fmt) for fmt in fmt_list):
                valid_dates += 1
                break  # Stop checking other formats once one matches
    
    return valid_dates >= len(first_entries) * threshold


def categorize_column_type(column_data):
    if is_date_column_by_first_rows(column_data):
        return "datetime"

    num_count = 0
    alnum_count = 0
    link_count = 0
    text_count = 0

    sample = column_data.dropna().astype(str)
    sample_size = min(200, len(sample))
    sample = sample.sample(n=sample_size, random_state=42)

    for val in sample:
        val = val.strip()
        if validators.url(val):
            link_count += 1
        elif val.replace('.', '', 1).isdigit():
            num_count += 1
        elif re.match(r'^[a-zA-Z0-9\s]+$', val):
            alnum_count += 1
        else:
            text_count += 1

    if link_count >= len(sample) * 0.7:
        return "link"
    elif num_count >= len(sample) * 0.7:
        return "numerical"
    elif alnum_count >= len(sample) * 0.7:
        return "alphanumeric"
    else:
        return "text"

        

# %%
def categorize_link_type(link):
    image_exts = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp']
    doc_exts = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt']

    link = link.lower()
    if any(link.endswith(ext) for ext in image_exts):
        return "image"
    elif any(link.endswith(ext) for ext in doc_exts):
        return "document"
    elif validators.url(link):
        return "webpage"
    else:
        return "unknown"

# %%
def split_date_and_time(df, column_name, winner_family):
    if winner_family not in FAMILY_MAP:
        print(f"Skipping column '{column_name}': Unknown or unsupported date family.")
        return

    date_formats = FAMILY_MAP[winner_family]
    column_data = df[column_name].dropna().astype(str)

    day_col = []
    month_col = []
    year_col = []

    for val in column_data:
        parsed = False
        for fmt in date_formats:
            try:
                date_obj = datetime.strptime(val, fmt)
                # Set components based on format
                day_col.append(date_obj.day if any(k in fmt for k in ['%d']) else 'N/A')
                month_col.append(date_obj.month if any(k in fmt for k in ['%m', '%b', '%B']) else 'N/A')
                year_col.append(date_obj.year if any(k in fmt for k in ['%Y', '%y']) else 'N/A')
                parsed = True
                break  # Stop after the first matching format
            except:
                continue

        if not parsed:
            day_col.append(None)
            month_col.append(None)
            year_col['year'].append(None)
    
    df_copy = df.copy()
    df_copy[f"{column_name}_day"] = day_col
    df_copy[f"{column_name}_month"] = month_col
    df_copy[f"{column_name}_year"] = year_col

    
    output_file = f"{column_name}_with_date_parts.csv"
    df_copy.to_csv(output_file, index=False)
    print(f"Parsed date components saved to '{output_file}'")

# %%
def categorize_columns(csv_file, output_csv='categorized_columns.csv'):
    try:
        df = pd.read_csv(csv_file, dtype=str)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    result = []

    for col in df.columns:
        print(f"\nAnalyzing column: {col}")
        col_data = df[col].dropna()

        col_type = categorize_column_type(col_data)
        sub_category = ''

        if col_type == 'datetime':
            format_scores, family_scores, winner_family = detect_date_format(col_data)
            sub_category = winner_family

            if winner_family != 'Unknown':
                plot_family_scores(family_scores, col)
                plot_winner_format_scores(format_scores, winner_family, col)
                split_date_and_time(df, col, winner_family)

        elif col_type == 'link':
            # Use majority logic to guess link subcategory
            subcats = col_data.apply(categorize_link_type)
            sub_category = subcats.value_counts().idxmax()

        result.append({
            'column name': col,
            'category': col_type,
            'sub-category': sub_category
        })

    if result:
        result_df = pd.DataFrame(result)
        result_df.to_csv(output_csv, index=False)
        print(f"\nCategorized columns saved to '{output_csv}'")
    else:
        print("\nNo valid columns detected.")

# %%
def main(input_csv):
    categorize_columns(input_csv)

# %%
if __name__ == "__main__":
    input_csv = 'AzureUsage.csv'  # <-- Replace with your file
    main(input_csv)
