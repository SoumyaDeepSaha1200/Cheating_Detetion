import pandas as pd
import numpy as np

# Specify the paths to your CSV files
output_file_path = r'D:\My Success Key\Projects\On Going College Project\Experiment\Experiment - Copy\Django_face_recognition_and_cheating_detection\output.csv'
user_data_file_path = r'D:\My Success Key\Projects\On Going College Project\Experiment\Experiment - Copy\Django_face_recognition_and_cheating_detection\user_data.csv'
filtered_output_file_path = r'D:\My Success Key\Projects\On Going College Project\Experiment\Experiment - Copy\Django_face_recognition_and_cheating_detection\filtered_data.csv'

# Load the CSV files
output_df = pd.read_csv(output_file_path, encoding='utf-8')
user_data_df = pd.read_csv(user_data_file_path, encoding='utf-8')

# Normalize the "Name" columns to lowercase for case-insensitive matching
output_df['Name'] = output_df['Name'].str.lower()
user_data_df['Name'] = user_data_df['Name'].str.lower()

# Count data by name in the output DataFrame
name_counts = output_df['Name'].value_counts()

# Filter data where 'Cheating Incident' is 'yes'
cheating_yes_counts = output_df[output_df['Cheating Incident'].str.lower() == 'yes']['Name'].value_counts()

# Filter data where 'Cheating Incident' is 'no'
cheating_no_counts = output_df[output_df['Cheating Incident'].str.lower() == 'no']['Name'].value_counts()

# Create a new DataFrame for the counts
final_df = pd.DataFrame({'Name': name_counts.index, 'Attendance Count': name_counts.values})

# Merge 'Cheating Incident (Yes)' count with the final DataFrame
final_df['Cheating Incident Count (Yes)'] = final_df['Name'].map(cheating_yes_counts).fillna(0).astype(int)

# Merge 'Cheating Incident (No)' count with the final DataFrame
final_df['Cheating Incident Count (No)'] = final_df['Name'].map(cheating_no_counts).fillna(0).astype(int)

# Merge the dataframes based on 'Name'
merged_df = pd.merge(final_df, user_data_df, on='Name', how='outer')

# Replace NaN values with 'Null'
merged_df.fillna('Null', inplace=True)

# Add movement and time data
output_data = pd.read_csv(output_file_path, encoding='utf-8')
merged_df = pd.merge(merged_df, output_data[['Name', 'Head Movement', 'Left Eye','Right Eye','Head Position','Date','Time']], on='Name', how='left')

# Append additional columns with example and default values
merged_df['Subject Exam'] = np.random.choice(['Aptitude', 'English'], size=len(merged_df))  # Randomly choose difficulty
merged_df['Difficulty'] = np.random.choice(['Easy', 'Medium', 'Hard'], size=len(merged_df))  # Randomly choose difficulty
merged_df['Score Marks'] = np.random.choice(['10', '21', '15','24','5','25','30','5','14','12','23','17','19','29','1','0','2','7'], size=len(merged_df))  # default value, should be populated with actual data
merged_df['Out of Marks'] = 30  # example total marks


# Save the merged DataFrame to a new CSV file
# merged_df.to_csv(final_output_file_path, index=False)

# Categorize performance
def categorize_performance(count):
    if count > 30:
        return 'Many Cheater'
    elif count >= 21:
        return 'Average'
    elif count >= 11:
        return 'Good'
    elif count >= 0:
        return 'Very Good'
    else:
        return 'Invalid'

# Apply the categorization function
merged_df['Performance'] = merged_df['Cheating Incident Count (Yes)'].apply(categorize_performance)

# Save the merged DataFrame with performance data
# merged_df.to_csv(performance_output_file_path, index=False)

# Filter and save the filtered data
filtered_data = pd.DataFrame()
unique_names = merged_df['Name'].unique()
for name in unique_names:
    specific_rows = merged_df[merged_df['Name'] == name].iloc[1:3]
    filtered_data = filtered_data.append(specific_rows)

filtered_data.to_csv(filtered_output_file_path, index=False)
