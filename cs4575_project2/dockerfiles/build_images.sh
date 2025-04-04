docker build -t tensorrt -f tensorrt.Dockerfile .
docker build -t ollama -f ollama.Dockerfile .
docker build -t mlc -f mlc.Dockerfile .
docker build -t vllm -f vllm.Dockerfile .