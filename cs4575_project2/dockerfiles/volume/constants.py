TASKS = 80 # Amount of tasks to run (23 in total for SWE-bench_Lite_oracle, 300 in total for SWE-bench_Lite_Big)
DATASET_PATH = "datasets/SWE-bench_Lite_Big.csv" # Path to dataset to be used for experiment
RESULT_FOLDER = 'results_greenserver' # Results folder, change to ur specific custom one
ENERGIBRIDGE_PATH = "/home/enrique/EnergiBridge/target/release/energibridge" # Path to energibridge file

# Parameters for LLM
MAX_OUTPUT_TOKENS = 4096 # The max amount of output tokens generated
MAX_CONTEXT_WINDOW = 32768 # The total length of the context window (input + output)
TEMPERATURE = 0.0 # Temperature for most deterministic results (default)
REPETITION_PENALTY = 1.05 # Sets how strongly to penalize repetitions. (default)
TOP_K = 20 # Reduces the probability of generating nonsense. (default)
TOP_P = 0.8 # Works together with top-k. (default)
SEED = 0 # Random seed for most deterministic results as possible