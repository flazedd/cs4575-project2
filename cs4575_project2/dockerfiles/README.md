# Docker building & experiment setup

This directory contains the Dockerfiles and related scripts for building and running the Docker containers used in the project.

## Docker Images
The following Docker images are included in this directory:
- **vLLM**
- **TensorRT**
- **MLC**
- **Ollama**

## Volume Mapping
- The `volume` directory within this folder should be mounted to the Docker container's `/app` working directory when running the experiment.
- Inside the volume directory, you will find the different Python library files required for the experiment.
- All LLM directories must also be placed in this folder.

## Building docker images
- The `build_images.sh` script is provided to build all Docker containers automatically.
- Simply run the script from a terminal to initiate the build process.
- The images have to be built first before running the experiment.

## Downloading the models
For our experiment, the following quantized versions of the Qwen2.5-Coder-14B-Instruct models were used:

- **vLLM and TensorRT:**  
  [Qwen2.5-Coder-14B-Instruct-AWQ](https://huggingface.co/Qwen/Qwen2.5-Coder-14B-Instruct-AWQ)
- **Ollama:**  
  [Qwen2.5-Coder-14B-Instruct-Q4_K_L.gguf](https://huggingface.co/bartowski/Qwen2.5-Coder-14B-Instruct-GGUF/blob/main/Qwen2.5-Coder-14B-Instruct-Q4_K_L.gguf)
- **MLC:**  
  [Qwen2.5-Coder-14B-Instruct-q4f16_1-MLC](https://huggingface.co/mlc-ai/Qwen2.5-Coder-14B-Instruct-q4f16_1-MLC)

For **MLC** and **TensorRT**, note that during the first iteration the engines will be built, compiled and saved into their respective directories. 

TensorRT does not support converting to checkpoint models natively, the `convert_checkpoint.py` file has to be placed inside the `volume` directory when running the experiment, the current `convert_checkpoint.py` file is **only for models based on the Qwen 2 architecture**. For more information and different model architectures see the [TensorRT documentation](https://github.com/NVIDIA/TensorRT-LLM/tree/main/examples/qwen#int4-awq).

## Hardware and Memory Considerations in MLC models
- If your GPU or hardware has memory constraints, you may need to adjust the `prefill_chunk_size` variable in the `mlc-chat-config.json` config file, which you can find in the MLC LLM folder when downloaded.
- The default value is set to `8192`; consider lowering it to `1024` if necessary.

## Configuration Files
- **Constants File:**  
  Contains experimental parameters and paths for results and datasets. For Linux users, it also includes the path to the EnergyBridge kernel (which must be updated to measure energy consumption).
- **Inference Library Python Files:**  
  Each Python file may require changes when switching the model used.
- **Modelfile (for Ollama):**  
  Used for Ollama's LLM creation. This file sets parameters and specifies the path to the GGUF model.
---
# Ensure that all configurations and paths are correctly set before running your experiments.
