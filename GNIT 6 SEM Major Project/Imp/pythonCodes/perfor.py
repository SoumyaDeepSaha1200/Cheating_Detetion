import pandas as pd

# Specify the correct path to your CSV file
csv_file_path = r'D:\My Success Key\Projects\On Going College Project\Experiment\Experiment - Copy\Django_face_recognition_and_cheating_detection\output.csv'

# Load the CSV file with specified encoding if needed
df = pd.read_csv(csv_file_path, encoding='utf-8')

# Count data by name
name_counts = df['Name'].value_counts()

# Filter data where 'Cheating Incident' is 'yes'
cheating_yes_counts = df[df['Cheating Incident'].str.lower() == 'yes']['Name'].value_counts()

# Filter data where 'Cheating Incident' is 'no'
cheating_no_counts = df[df['Cheating Incident'].str.lower() == 'no']['Name'].value_counts()

# Create a new DataFrame for the counts
final_df = pd.DataFrame({'Name': name_counts.index, 'Attendance Count': name_counts.values})

# Merge 'Cheating Incident (Yes)' count with the final DataFrame
final_df['Cheating Incident Count (Yes)'] = final_df['Name'].map(cheating_yes_counts).fillna(0).astype(int)

# Merge 'Cheating Incident (No)' count with the final DataFrame
final_df['Cheating Incident Count (No)'] = final_df['Name'].map(cheating_no_counts).fillna(0).astype(int)

# Save the final DataFrame to a new CSV file
final_output_file_path = r'D:\My Success Key\Projects\On Going College Project\Experiment\Experiment - Copy\Django_face_recognition_and_cheating_detection\final_counts.csv'
final_df.to_csv(final_output_file_path, index=False)

# Print the count of 'no' occurrences in 'Cheating Incident'
print("Cheating Incident (No) Counts:")
print(cheating_no_counts)
