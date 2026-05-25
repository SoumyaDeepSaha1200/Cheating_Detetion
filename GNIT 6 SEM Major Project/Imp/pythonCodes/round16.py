import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

# Specify the paths to your CSV files
output_file_path = r'D:\My Success Key\Projects\On Going College Project\Last Edited Noise detection - Copy\Experiment - Copy\Django_face_recognition_and_cheating_detection\output.csv'
user_data_file_path = r'D:\My Success Key\Projects\On Going College Project\Last Edited Noise detection - Copy\Experiment - Copy\Django_face_recognition_and_cheating_detection\user_data.csv'
filtered_output_file_path = r'D:\My Success Key\Projects\On Going College Project\Last Edited Noise detection - Copy\Experiment - Copy\Django_face_recognition_and_cheating_detection\final.csv'
performance_output_file_path = r'D:\My Success Key\Projects\On Going College Project\Last Edited Noise detection - Copy\Experiment - Copy\Django_face_recognition_and_cheating_detection\performance.csv'

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

# Merge 'Cheating Incident (No)' count with the final_df
final_df['Cheating Incident Count (No)'] = final_df['Name'].map(cheating_no_counts).fillna(0).astype(int)

# Merge the dataframes based on the common field 'Name' (converted to lowercase)
merged_df = pd.merge(final_df, user_data_df, on='Name', how='outer')

# Replace NaN values with 'Null'
merged_df = merged_df.fillna('Null')

# Add data from the 'output.csv' file including eye movement, head movement, and date time
output_data = pd.read_csv(output_file_path, encoding='utf-8')
merged_df = pd.merge(merged_df, output_data[['Name', 'Head Movement', 'Left Eye', 'Right Eye', 'Head Position', 'Date', 'Time', 'SessionID', 'StudentID', 'SoundDetection', 'BackgroundNoiseLevel']], on='Name', how='left')

# Replace 'Null' values with 0 for numeric fields
numeric_fields = ['Cheating Incident Count (Yes)', 'Cheating Incident Count (No)']
for field in numeric_fields:
    merged_df[field] = merged_df[field].replace('Null', 0).astype(int)

# Categorize performance based on multiple cheating-related criteria
def categorize_performance(row):
    attendance_count = row['Attendance Count']
    cheating_yes_count = row['Cheating Incident Count (Yes)']
    cheating_no_count = row['Cheating Incident Count (No)']
    head_position = row['Head Position']
    left_eye = row['Left Eye']
    right_eye = row['Right Eye']
    head_movement = row['Head Movement']
    sound_detection = row['SoundDetection']
    
    # Define a function to safely convert to float or return a default value
    def safe_float(value, default=0):
        try:
            return float(value)
        except ValueError:
            return default
    
    # Convert relevant columns to numeric type or use default value if conversion fails
    left_eye = safe_float(left_eye)
    right_eye = safe_float(right_eye)
    head_movement = safe_float(head_movement)
    
    # Define conditions based on multiple criteria
    if (cheating_yes_count > 60 and (cheating_no_count < 20 or cheating_no_count < 30)) \
            or (head_position == 'Tilted Down' and (left_eye < 0.5 or right_eye < 0.5)) \
            or (head_movement > 90) \
            or (sound_detection == 'Talking' and (left_eye < 0.5 or right_eye < 0.5)):
        return 'Many Cheater'
    elif (cheating_yes_count >= 21) \
            or (head_position == 'Tilted Up' and (left_eye >= 0.5 and right_eye >= 0.5)) \
            or (head_movement <= 90 and head_movement > 60) \
            or (sound_detection == 'Silent' and (left_eye >= 0.5 and right_eye >= 0.5)):
        return 'Average'
    elif (cheating_yes_count >= 11) \
            or (head_position == 'Tilted Right' and (left_eye >= 0.5 and right_eye >= 0.5)) \
            or (head_movement <= 60 and head_movement > 30) \
            or (sound_detection == 'Silent' and (left_eye >= 0.5 and right_eye >= 0.5)):
        return 'Good'
    elif cheating_yes_count >= 0 \
            or (head_position == 'Tilted Left' and (left_eye >= 0.5 and right_eye >= 0.5)) \
            or (head_movement <= 30) \
            or (sound_detection == 'Silent' and (left_eye >= 0.5 and right_eye >= 0.5)):
        return 'Very Good'
    else:
        return 'Invalid'

# Apply the categorization function to create the 'Performance' column
merged_df['Performance'] = merged_df.apply(categorize_performance, axis=1)

# Apply the categorization function to create the 'Performance' column
merged_df['Performance'] = merged_df.apply(categorize_performance, axis=1)

# Add extra columns 'Marks', 'Difficulty', and 'Subject' with placeholder values
merged_df['Marks'] = [random.randint(0, 30) for _ in range(len(merged_df))]
merged_df['Difficulty'] = [random.choice(['Easy', 'Medium', 'Hard']) for _ in range(len(merged_df))]
merged_df['Subject'] = [random.choice(['Aptitude', 'Subject', 'English']) for _ in range(len(merged_df))]

# Define function to determine overall performance
def overall_performance(row):
    if row['Marks'] >= 25 and row['Difficulty'] == 'Hard':
        return 'Excellent'
    elif row['Marks'] >= 20:
        return 'Very Good'
    elif row['Marks'] >= 15:
        return 'Good'
    elif row['Marks'] >= 10:
        return 'Average'
    else:
        return 'Poor'

# Apply the function to create the 'Overall Performance' column
merged_df['Overall Performance'] = merged_df.apply(overall_performance, axis=1)

# Filter the data and save the filtered data to a new CSV file
filtered_data = pd.DataFrame()
unique_names = merged_df['Name'].unique()
for name in unique_names:
    specific_rows = merged_df[merged_df['Name'] == name].iloc[1:3]
    filtered_data = pd.concat([filtered_data, specific_rows])

filtered_data.to_csv(filtered_output_file_path, index=False)

# Save the performance and overall performance columns to a new CSV for review
performance_data = merged_df[['Name', 'Performance', 'Overall Performance']]
performance_data.to_csv(performance_output_file_path, index=False)

# Analyze and visualize the performance data
def plot_performance_data(df):
    categories = ['Cheating Incident Count (Yes)', 'Head Position', 'Left Eye', 'Right Eye', 'Head Movement', 'SoundDetection']
    counts = {category: df[category].value_counts() for category in categories}

    # Plotting the data
    fig, axs = plt.subplots(2, 3, figsize=(18, 10))

    for ax, (category, count) in zip(axs.flatten(), counts.items()):
        if category == 'Cheating Incident Count (Yes)':
            count.plot(kind='bar', ax=ax, title=category)
        else:
            count.plot(kind='pie', ax=ax, title=category, autopct='%1.1f%%', startangle=90)

    plt.tight_layout()
    plt.show()

# Plot the performance data
plot_performance_data(merged_df)
