import pandas as pd

# Specify the paths to your CSV files
output_file_path = r'D:\My Success Key\Projects\On Going College Project\Experiment\Experiment - Copy\Django_face_recognition_and_cheating_detection\output.csv'
user_data_file_path = r'D:\My Success Key\Projects\On Going College Project\Experiment\Experiment - Copy\Django_face_recognition_and_cheating_detection\user_data.csv'
final_output_file_path = r'D:\My Success Key\Projects\On Going College Project\Experiment\Experiment - Copy\Django_face_recognition_and_cheating_detection\final_counts.csv'

# Load the CSV files
output_df = pd.read_csv(output_file_path, encoding='utf-8')
user_data_df = pd.read_csv(user_data_file_path, encoding='utf-8')

# Convert the "Name" columns to lowercase for case-insensitive matching
output_df['Name'] = output_df['Name'].str.lower()
user_data_df['Name'] = user_data_df['Name'].str.lower()

# Count data by name in the output DataFrame
name_counts = output_df['Name'].value_counts()

# Filter data where 'Cheating Incident' is 'yes' in the output DataFrame
cheating_yes_counts = output_df[output_df['Cheating Incident'].str.lower() == 'yes']['Name'].value_counts()

# Filter data where 'Cheating Incident' is 'no' in the output DataFrame
cheating_no_counts = output_df[output_df['Cheating Incident'].str.lower() == 'no']['Name'].value_counts()

# Create a new DataFrame for the counts
final_df = pd.DataFrame({'Name': name_counts.index, 'Attendance Count': name_counts.values})

# Merge 'Cheating Incident (Yes)' count with the final DataFrame
final_df['Cheating Incident Count (Yes)'] = final_df['Name'].map(cheating_yes_counts).fillna(0).astype(int)

# Merge 'Cheating Incident (No)' count with the final DataFrame
final_df['Cheating Incident Count (No)'] = final_df['Name'].map(cheating_no_counts).fillna(0).astype(int)

# Merge the dataframes based on the common field 'Name' (converted to lowercase)
merged_df = pd.merge(final_df, user_data_df, on='Name', how='outer')

# Replace NaN values with 'Null'
merged_df = merged_df.fillna('Null')

# Add data from the 'output.csv' file including eye movement, head movement, and date time
output_data = pd.read_csv(output_file_path, encoding='utf-8')
merged_df = pd.merge(merged_df, output_data[['Name', 'Head Movement', 'Left Eye','Right Eye','Head Position','Date','Time']], on='Name', how='left')

# Save the merged DataFrame to a new CSV file
merged_df.to_csv(final_output_file_path, index=False)

print("Merged data saved to 'final_counts.csv' successfully with 'Null' values for empty parts.")
