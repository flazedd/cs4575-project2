# Building and Running Docker Images using PowerShell scripts

## Structure of Docker files

Each inference library has a Dockerfile and a Python file with the code that belongs to that inference library.

**Example in this folder**  
- **Dockerfile**: `<inference_library>.Dockerfile`  
- **Python Library**: `<inference_library>_library.py`  

This setup includes all the necessary instructions to build and run the Python code (`<inference_library>_library.py`) inside the Docker container defined by `<inference_library>.Dockerfile`.

---

## Building Docker Images

The `build_images.ps1` script builds all Dockerfiles in the folder.  
It searches for Dockerfiles following the naming pattern `<inference_library>.Dockerfile`, builds each Docker image, and tags them using the `<inference_library>` name.

## Running Docker Images

The `run_images.ps1` script runs all Docker images that were built.  
It executes each image, allowing you to launch the containers (with options such as GPU support, interactive terminal, or automatic container removal, depending on your configuration).

---

## Instructions

### 1. Open a PowerShell terminal with Administrator privileges

On Windows, you can right-click the PowerShell icon and select **Run as administrator**.

### 2. Navigate to the script directory

```powershell
cd path\to\scripts\dockerfiles
```

### 3. Run the Script

To build Docker images:
```powershell
.\build_images.ps1
```

To run Docker images:
```powershell
.\run_images.ps1
```

#### Adjust Execution Policy (if necessary)
If you encounter an error about the script not being digitally signed, you can either unblock the file or change the execution policy:

- **Unblock the file:**
  ```powershell
  Unblock-File -Path .\build_images.ps1
  ```
- **Or change the execution policy to bypass digital signature requirements:**
  ```powershell
  Set-ExecutionPolicy Bypass -Scope CurrentUser
  ```
  *Note: Changing the execution policy may have security implications. Only use this if you trust the source of the script.*