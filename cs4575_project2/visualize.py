import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import utils
from cs4575_project2.dockerfiles.volume.constants import RESULT_FOLDER
import os
from collections import defaultdict

save_directory = RESULT_FOLDER

images = ['mlc', 'ollama', 'vllm', 'tensorrt']
llm_path = f"./dockerfiles/volume/{save_directory}"

utils.sync_common_files(llm_path, save_directory, images=images)


def extract_columns_as_series(csv_file_path, columns):
    """
    Extract specified columns from a CSV file and return them as a list of Pandas Series.
    If the lengths of the columns differ, raise a ValueError.

    :param csv_file_path: Path to the CSV file.
    :param columns: A list of column names to extract.
    :return: A list of Pandas Series corresponding to each column.
    :raises: ValueError if any of the specified columns are missing or the lengths of the columns differ.
    """
    # Read the CSV file using pandas
    try:
        df = pd.read_csv(csv_file_path)
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")

    # Check if all specified columns exist in the CSV file
    missing_columns = [col for col in columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing columns in CSV file: {', '.join(missing_columns)}")

    # Extract the specified columns as Pandas Series
    series = [df[col] for col in columns]

    # Check if all columns have the same length
    lengths = [len(s) for s in series]
    if len(set(lengths)) > 1:
        raise ValueError("The lengths of the columns differ. All columns must have the same length.")

    return series

def calculate_energy(delta, power):
    """
    Calculate the energy in Joules consumed.
    Energy (J) = Power (mW) * Time (s) / 1000
    """
    return (delta * power) / 1000  # Convert mW to W

def calculate_total_tokens(tokens_per_sec, seconds):
    """
    Calculate the total tokens generated.
    """
    return (tokens_per_sec * seconds).sum()


def calculate_weighted_tokens_per_sec(tokens_per_sec, seconds):
    """
    Calculate the weighted average of tokens per second.

    :param tokens_per_sec: A Pandas Series representing tokens per second.
    :param seconds: A Pandas Series representing the time in seconds.
    :return: The weighted average tokens per second.
    """
    total_time = seconds.sum()
    if total_time == 0:
        raise ValueError("Total time cannot be zero.")

    return (tokens_per_sec * seconds).sum() / total_time


def plot_box_violin(statistics, title, y_label, filename, save_dir):
    """
    Generate a combined box and violin plot from a dictionary of statistics.
    :param statistics: Dict mapping labels to lists of data.
    :param title: Title of the plot.
    :param y_label: Label for the y-axis.
    :param filename: Name of the file to save the plot.
    :param save_dir: Directory to save the plot.
    """
    labels, data = zip(*statistics.items())  # Extract labels and corresponding data arrays

    plt.figure(figsize=(10, 6))
    positions = np.arange(len(labels))

    # Violin plot
    sns.violinplot(data=data, inner=None, linewidth=1, width=0.6, cut=0)

    # Box plot
    plt.boxplot(data, positions=positions, widths=0.2, patch_artist=True,
                boxprops=dict(facecolor="lightblue", alpha=0.6),
                medianprops=dict(color="red", linewidth=1.5),
                flierprops=dict(marker='o', color='red', markersize=6))

    plt.xticks(ticks=positions, labels=labels)
    plt.title(title, fontsize=14)
    plt.xlabel('Inference library', fontsize=12)
    plt.ylabel(y_label, fontsize=12)

    plt.grid(linestyle="--", linewidth=0.5, alpha=0.7)
    plt.tight_layout()

    save_path = os.path.join(save_dir, filename)
    plt.savefig(save_path, dpi=300)
    plt.show()


import numpy as np

def remove_outliers(statistics):
    """
    Removes outliers from a dictionary of statistical data.

    Parameters:
        statistics (dict): Dict mapping labels to lists of data.

    Returns: None
    """

    def remove_outlier(statistic):
        """
        Removes outliers from a list of data.

        Outliers are removed if they deviate from the mean by more than 2.9 std.

        Parameters:
            statistic (list): A list of numerical data.

        Returns:
            list: A new list with outliers removed.
        """
        data_ = np.array(statistic)
        mean = np.mean(data_)
        std_dev = np.std(data_)
        diff = np.abs(data_ - mean)
        # Remove all data points that deviate from the mean more than 2.9 standard deviations
        mask = diff <= (2.9 * std_dev)
        # Return the data without the outliers
        return data_[mask].tolist()

    for key in statistics.keys():
        statistics[key] = remove_outlier(statistics[key])



# Example usage:
# csv_path = 'dockerfiles/volume/results/vllm/vllm_0.csv'  # Replace with your actual CSV file path
# columns = ['tokens_per_sec', 'seconds']  # Replace with your desired columns
#
# try:
#     series_list = extract_columns_as_series(csv_path, columns)
#     for col, series in zip(columns, series_list):
#         print(f"Column '{col}' as Pandas Series:\n{series}\n")
# except ValueError as e:
#     print(f"Error: {e}")

energy_per_token_stats = defaultdict(list)
tokens_per_sec_stats = defaultdict(list)

for image in images:
    image_dir = os.path.join(save_directory, image)
    image_llm_dir = os.path.join(llm_path, image)

    if not os.path.exists(image_dir) or not os.path.isdir(image_dir):
        print(f"Skipping {image_dir}, directory does not exist.")
        continue

    files = sorted([f for f in os.listdir(image_dir) if f.endswith('.csv')])

    for i, filename in enumerate(files):
        save_file_path = os.path.join(image_dir, filename)
        llm_file_path = os.path.join(image_llm_dir, filename)

        if not os.path.exists(llm_file_path):
            print(f"Skipping {filename}, corresponding file in {image_llm_dir} does not exist.")
            continue

        delta, power = extract_columns_as_series(save_file_path, ["Delta", "GPU0_POWER (mWatts)"])
        energy = calculate_energy(delta, power).sum()
        tokens_per_sec, seconds = extract_columns_as_series(llm_file_path, ["tokens_per_sec", "seconds"])
        total_tokens = calculate_total_tokens(tokens_per_sec, seconds)

        energy_per_token = energy / total_tokens
        energy_per_token_stats[image].append(energy_per_token)

        total_token_s = calculate_weighted_tokens_per_sec(tokens_per_sec, seconds)
        tokens_per_sec_stats[image].append(total_token_s)

remove_outliers(energy_per_token_stats)
remove_outliers(tokens_per_sec_stats)

plot_box_violin(statistics=energy_per_token_stats,
                title="Energy per token",
                y_label="Energy (J)",
                filename="./energy_per_token.png",
                save_dir=save_directory)

plot_box_violin(statistics=tokens_per_sec_stats,
                title="Tokens per second",
                y_label="Tokens / s",
                filename="./tokens_per_second.png",
                save_dir=save_directory)

