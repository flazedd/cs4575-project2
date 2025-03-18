from mlc_llm import MLCEngine
from mlc_llm.serve.config import EngineConfig

model = "HF://mlc-ai/Qwen2.5-1.5B-Instruct-q4f16_1-MLC"

# Create engine
engine = MLCEngine(
    model=model,
    device="cuda",
    engine_config=EngineConfig(
        max_single_sequence_length=16384,  # Decrease context window by 50% (from 32768 default)
        prefill_chunk_size=1024), # Decrease chunk size by 50% (from 2048 defaul to 1024)
)

# Test prompt
prompt = """
You are interested in studying a rare type of breast cancer in a mouse model. 
Your research up until now has shown that the cancer cells show low expression of a key tumor suppressor gene. 
Which of these is the most suitable course of action to study the cause of gene silencing?
"""

# Run chat completion in OpenAI API.
for response in engine.chat.completions.create(
    messages=[{"role": "user", "content": f"{prompt}"}],
    model=model,
    stream=True,
    max_tokens=2048, # Amount of max output tokens
    temperature = 0.0,
):
    for choice in response.choices:
        print(choice.delta.content, end="", flush=True)
print("\n")
print(engine.metrics())