import pandas as pd
from cs4575_project2.dockerfiles.volume.prompt import Prompt

# Load the dataset
df = pd.read_csv('SWE-bench_Lite_Big.csv')
print(df.info)
# Define a function to count words in a single row
def count_words(row):
    # Convert the row to a dictionary
    instance = row.to_dict()
    # Create a Prompt object using the row's data
    prompt_obj = Prompt(instance)
    # Construct the prompt string
    prompt_str = prompt_obj.construct_prompt()
    # Count the words in the constructed prompt
    return len(prompt_str.split())

# Apply the function to each row and store results in a new column
df['total_word_count'] = df.apply(count_words, axis=1)

# Sort by total_word_count in descending order
sorted_df = df.sort_values(by='total_word_count', ascending=False)

# Get top 10 rows with the highest word counts
top_10_rows = sorted_df.head(10)

# Display the top 10 rows along with their total word counts
print(top_10_rows[['total_word_count']])