from tensorrt_llm import LLM, SamplingParams
import logging
import time

logger = logging.getLogger(__name__)
logging.basicConfig(filename='tensorrt.log',
                    encoding='utf-8',
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S')

def main():

    prompts = [
        "Hello, my name is",
        "The president of the United States is",
        "The capital of France is",
        "The future of AI is",
    ]
    sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

    llm = LLM(model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

    outputs = llm.generate(prompts, sampling_params)

    # Print the outputs.
    for output in outputs:
        prompt = output.prompt
        generated_text = output.outputs[0].text
        print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")
        logger.info(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")

    for idx, prompt in enumerate(prompts):
        # Start timing
        start_time = time.time()

        outputs = llm.generate([prompt], sampling_params)

        # Calculate duration
        duration = time.time() - start_time

        # Get generated text and token count
        generated_text = outputs[0].outputs[0].text
        token_count = len(llm.tokenizer.encode(generated_text))

        # Calculate tokens per second (avoid division by zero)
        tokens_per_sec = token_count / duration if duration > 0 else 0

        # Format output with metrics
        log_message = (
            f"Prompt [{idx + 1}/{len(prompts)}]: {prompt!r}\n"
            f"Generated: {generated_text!r}\n"
            f"Duration: {duration:.2f}s | Tokens: {token_count} | "
            f"Tokens/s: {tokens_per_sec:.2f}\n"
            f"{'-' * 50}"
        )

        print(log_message)
        logger.info(log_message)


# The entry point of the program need to be protected for spawning processes.
if __name__ == '__main__':
    main()