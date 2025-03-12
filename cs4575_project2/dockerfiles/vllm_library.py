from vllm import LLM, SamplingParams

llm = LLM(
    model="Qwen/Qwen2.5-1.5B-Instruct-AWQ",
    quantization="awq_marlin",
    generation_config="auto"
)

prompt = """
You are interested in studying a rare type of breast cancer in a mouse model. 
Your research up until now has shown that the cancer cells show low expression of a key tumor suppressor gene. 
Which of these is the most suitable course of action to study the cause of gene silencing?
"""

sampling_params = llm.get_default_sampling_params()
sampling_params.temperature = 0.5
sampling_params.max_tokens = 2048

outputs = llm.generate(
    prompt=prompt,
    sampling_params=sampling_params,
)

response_text = outputs[0].outputs[0].text
print(response_text)