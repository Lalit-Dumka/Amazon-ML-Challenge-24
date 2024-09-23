import pandas as pd

# Load the CSV files into DataFrames
f1 = 'output/final_output_v13.csv'
f2 = 'output/final_output_v14.csv'
file1 = pd.read_csv(f1)
file2 = pd.read_csv(f2)

# Merge the two files on the 'index' column
merged_df = pd.merge(file2, file1[['index', 'prediction']], on='index', how='left', suffixes=('_file2', '_file1'))

# Identify rows where prediction_file2 is NaN but prediction_file1 has a value
filled_rows = merged_df[merged_df['prediction_file2'].isna() & merged_df['prediction_file1'].notna()]

# Fill empty 'prediction' values in file2 using values from file1
merged_df['prediction_file2'].fillna(merged_df['prediction_file1'], inplace=True)

# Rename the column back to 'prediction' and drop the extra 'prediction_file1' column
merged_df = merged_df.rename(columns={'prediction_file2': 'prediction'})
merged_df = merged_df.drop(columns=['prediction_file1'])

# Save the updated file2 back to CSV
merged_df.to_csv('final_output_v14.csv', index=False)

# Save the filled rows to a separate CSV
filled_rows.to_csv(f"filled_rows{f2.split('.')[0][-1]}-{f1.split('.')[0][-1]}.csv", index=False)

# Print the count of rows that were filled
filled_count = len(filled_rows)
print(f"Number of rows filled: {filled_count}")
