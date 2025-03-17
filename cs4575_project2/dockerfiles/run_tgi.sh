export MSYS_NO_PATHCONV=1
model=Qwen/Qwen2.5-1.5B-Instruct
volume=$PWD/data # share a volume with the Docker container to avoid downloading weights every run

docker run --gpus all --shm-size 1g -p 8080:80 ghcr.io/huggingface/text-generation-inference:3.2.0 --model-id $model --quantize bitsandbytes-fp4