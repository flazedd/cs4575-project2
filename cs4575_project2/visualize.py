import pandas as pd


def calculate_energy(csv_file):
    # Read CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Initialize total energy used (in Joules)
    total_energy = 0.0

    # Iterate through each row of the dataframe
    for index, row in df.iterrows():
        # Power in watts (convert mW to W by dividing by 1000)
        power_watts = row['GPU0_POWER (mWatts)'] / 1000.0

        # Time in seconds (convert ms to s by dividing by 1000)
        time_seconds = row['Delta'] / 1000.0

        # Check for negative power or time values
        if power_watts < 0:
            raise ValueError(f"Negative power value detected at row {index}: {row['GPU0_POWER (mWatts)']} mW")

        if time_seconds < 0:
            raise ValueError(f"Negative time value detected at row {index}: {row['Delta']} ms")

        # Energy used in Joules for this row
        energy = power_watts * time_seconds

        # Add to the total energy
        total_energy += energy

    return total_energy


# Example usage:
total_energy = calculate_energy('./results/mlc/mlc_0.csv')
print(f"Total energy used: {total_energy} Joules")
