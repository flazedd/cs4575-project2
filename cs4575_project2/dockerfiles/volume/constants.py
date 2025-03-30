TASKS = 23 # Amount of tasks to run (23 in total for swe-bench_lite_oracle)
RESULT_FOLDER = 'results_Alex_2' # Results folder, change to ur specific custom one

# Parameters for LLM
MAX_OUTPUT_TOKENS = 4096 # The max amount of output tokens generated
MAX_CONTEXT_WINDOW = 32768 # The total length of the context window (input + output)
TEMPERATURE = 0.0 # Temperature for most deterministic results (default)
REPETITION_PENALTY = 1.05 # Sets how strongly to penalize repetitions. (default)
TOP_K = 20 # Reduces the probability of generating nonsense. (default)
TOP_P = 0.8 # Works together with top-k. (default)
SEED = 0 # Random seed for most deterministic results as possible