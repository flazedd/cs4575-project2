from datasets import load_dataset
import pandas as pd
import random
import math

stem_categories = [
    'abstract_algebra', 'anatomy', 'astronomy', 'college_biology', 
    'college_chemistry', 'college_computer_science', 'college_mathematics',
    'college_physics', 'computer_security', 'conceptual_physics',
    'econometrics', 'electrical_engineering',
    'high_school_biology', 'high_school_chemistry', 'high_school_computer_science',
    'high_school_mathematics', 'high_school_physics', 'high_school_statistics',
    'machine_learning', 'medical_genetics', 'virology'
]

mmlu_dataset = load_dataset("cais/mmlu", "all")
print("Dataset loaded successfully")

category_examples = {category: [] for category in stem_categories}

for example in mmlu_dataset['test']:
    if example['subject'] in stem_categories:
        category_examples[example['subject']].append(example)

available_categories = [cat for cat in stem_categories if len(category_examples[cat]) > 0]
examples_per_category = math.floor(100 / len(available_categories))
remainder = 100 % len(available_categories)

balanced_sample = []
for i, category in enumerate(available_categories):
    category_sample_size = examples_per_category + (1 if i < remainder else 0)
    actual_sample_size = min(category_sample_size, len(category_examples[category]))
    
    category_samples = random.sample(category_examples[category], actual_sample_size)
    balanced_sample.extend(category_samples)

print(f"Total samples collected: {len(balanced_sample)}")

balanced_df = pd.DataFrame(balanced_sample)

def get_text_answer(row):
    """Convert the numeric answer (0,1,2,3) to the actual text choice"""
    if 'choices' in row and len(row['choices']) > 0:
        answer_idx = row['answer']
        if 0 <= answer_idx < len(row['choices']):
            return row['choices'][answer_idx]
    return "Answer unavailable"

balanced_df['text_answer'] = balanced_df.apply(get_text_answer, axis=1)

print(f"Total samples collected: {len(balanced_df)}")
category_distribution = balanced_df['subject'].value_counts()
print("\nCategory distribution in sample:")
for category, count in category_distribution.items():
    print(f"{category}: {count} examples")

output_file = "cs4575_project2/Datasets/mmlu_stem_subset.csv"
balanced_df.to_csv(output_file, index=False)
print(f"\nData saved to {output_file}")