import pandas as pd
import matplotlib.pyplot as plt

# Load your CSV file
csv_file_path = r'D:\My Success Key\Projects\Complete Projects\GNIT 6 SEM Major Project\Original\Experiment - Copy\Django_face_recognition_and_cheating_detection\final.csv'
df = pd.read_csv(csv_file_path, encoding='utf-8')

# Assuming your CSV has a column 'Name' for person names
def plot_individual_performance_data(df, names=None):
    if names:
        # Filter the dataframe to include only the specified names
        df = df[df['Name'].isin(names)]
    
    categories = ['Cheating Incident Count (Yes)', 'Head Position', 'Left Eye', 'Right Eye', 'Head Movement', 'SoundDetection']
    counts = {category: df[category].value_counts() for category in categories}

    # Plotting the data
    fig, axs = plt.subplots(len(counts) // 2, 2, figsize=(18, 10))

    for ax, (category, count) in zip(axs.flatten(), counts.items()):
        if category == 'Cheating Incident Count (Yes)':
            count.plot(kind='bar', ax=ax, color='skyblue')
            ax.set_title(f'{category} Distribution')
            ax.set_xlabel(category)
            ax.set_ylabel('Count')
        else:
            count.plot(kind='pie', ax=ax, autopct='%1.1f%%')
            ax.set_title(f'{category} Distribution')
            ax.set_ylabel('')

    plt.tight_layout()
    plt.show()

# Example usage: plot performance data for specific persons
plot_individual_performance_data(df, names=['pradipta here'])
