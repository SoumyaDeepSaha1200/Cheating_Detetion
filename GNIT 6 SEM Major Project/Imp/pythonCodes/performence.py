import pandas as pd

# File paths
output_file_path = r'D:\My Success Key\Projects\On Going College Project\Experiment\Experiment - Copy\Django_face_recognition_and_cheating_detection\output.csv'
user_data_file_path = r'D:\My Success Key\Projects\On Going College Project\Experiment\Experiment - Copy\Django_face_recognition_and_cheating_detection\user_data.csv'
output_merged_file_path = r'D:\My Success Key\Projects\On Going College Project\Experiment\Experiment - Copy\Django_face_recognition_and_cheating_detection\filtered_data.csv'

# Load the CSV files
output_df = pd.read_csv(output_file_path)
user_data_df = pd.read_csv(user_data_file_path)

# Convert the "Name" columns to lowercase for case-insensitive matching
output_df['Name'] = output_df['Name'].str.lower()
user_data_df['Name'] = user_data_df['Name'].str.lower()

# Merge the dataframes based on the common field (converted to lowercase)
merged_df = pd.merge(user_data_df, output_df, on='Name', how='outer', suffixes=('_user', '_output'))

# Fill missing values with 'NILL'
merged_df.fillna('NILL', inplace=True)

# Fill "Cheating Incident" column based on priority
merged_df['Cheating Incident'] = merged_df.apply(lambda row: 'Yes' if row['Cheating Incident'] == 'Yes' else 'No', axis=1)

# Filter rows based on "Cheating Incident" column
filtered_df = merged_df.loc[merged_df['Cheating Incident'].isin(['No', 'Yes'])]

# Keep only the first occurrence of each "Name" in the merged dataframe
filtered_df.drop_duplicates(subset='Name', keep='first', inplace=True)

# Count occurrences of "Yes" and "No" in the "Cheating Incident" column
cheating_counts = output_df['Cheating Incident'].value_counts()

# Create a summary DataFrame
summary_df = pd.DataFrame({'Cheating Incident': ['Yes', 'No'], 'Count': cheating_counts})

# Add the summary to the filtered DataFrame
summary_dict = summary_df.set_index('Cheating Incident')['Count'].to_dict()
filtered_df['Cheating Count'] = filtered_df['Cheating Incident'].map(summary_dict).fillna(0).astype(int)

# Save the filtered DataFrame with the summary to CSV
filtered_df.to_csv(output_merged_file_path, index=False, na_rep='NILL')

print("Filtered data with summary saved to 'filtered_data.csv' successfully!")
