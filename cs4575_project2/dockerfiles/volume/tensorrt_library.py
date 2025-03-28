from tensorrt_llm import LLM, SamplingParams
import time


def main():
    with open('inference_results.txt', 'w', encoding='utf-8') as f:
        prompts = [
            "Hello, my name is",
            "The president of the United States is",
            "The capital of France is",
            "The future of AI is",
        ]
        sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

        # Initialize model
        llm = LLM(model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        f.write("Model loaded successfully\n")

        # Initial batch inference
        outputs = llm.generate(prompts, sampling_params)

        # Write batch results
        f.write("Batch Inference Results:\n")
        f.write("=" * 50 + "\n")
        for output in outputs:
            generated_text = output.outputs[0].text
            f.write(f"Prompt: {output.prompt!r}\nGenerated: {generated_text!r}\n\n")

        # Timed individual inferences
        f.write("\nIndividual Timing Metrics:\n")
        f.write("=" * 50 + "\n")
        for idx, prompt in enumerate(prompts):
            start_time = time.time()
            outputs = llm.generate([prompt], sampling_params)
            duration = time.time() - start_time

            generated_text = outputs[0].outputs[0].text
            token_count = len(llm.tokenizer.encode(generated_text))
            tokens_per_sec = token_count / duration if duration > 0 else 0

            f.write(
                f"Prompt [{idx + 1}/{len(prompts)}]: {prompt!r}\n"
                f"Generated: {generated_text!r}\n"
                f"Duration: {duration:.2f}s | Tokens: {token_count} | "
                f"Tokens/s: {tokens_per_sec:.2f}\n"
                f"{'-' * 50}\n"
            )


if __name__ == '__main__':
    main()
