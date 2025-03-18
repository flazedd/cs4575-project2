from vllm import LLM

llm = LLM(
    model="Qwen/Qwen2.5-1.5B-Instruct-AWQ",
    device="cuda",                         # use NVIDIA GPU
    quantization="awq",  # Uses AWQ marlin 4-bit quantitization
    max_model_len = 16384, # Decrease context window (activation memory) by 50% (from 32768 default)
)

prompt = """
What is 1 + 1? 
"""

sampling_params = llm.get_default_sampling_params()
sampling_params.temperature = 0.5
sampling_params.max_tokens = 2048 # Amount of max output tokens

outputs = llm.generate(prompt, sampling_params)
response_text = outputs[0].outputs[0].text
print(response_text)