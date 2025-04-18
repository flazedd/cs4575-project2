# CS4575 Project 2: Energy Efficiency in LLM Inference: Comparing Inference Libraries in a Unified Docker Framework - Instructions

### Step 1: Install Python 3.11.8

1. Download Python 3.11.8 from the official website:
   - Visit [Python 3.11.8 Downloads](https://www.python.org/downloads/release/python-3118/)
   - Select the appropriate installer for your system (Windows, macOS, Linux)

2. Verify Python Installation
```bash
py --version
```
Output:
```
Python 3.11.8
```

### Step 2: Install Poetry
Open Powershell in administrator mode and run
```bash
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```
Verify installation
```
poetry --version
```
Output:
```
Poetry (version 1.8.3) 
```

### Step 3: Clone this repo

First, clone the repository using Git. Open a terminal and run:

```bash
git clone https://github.com/flazedd/cs4575-project2
cd cs4575_project2
```

### Step 4: Install all dependencies

```bash
poetry install
```

Verify dependencies got installed
```bash
poetry show
```


### Step 5: Install service for EnergiBridge

**IMPORTANT**: To make energibridge work for Windows you have to change the ```cs4575_project2\energi_custom.py``` file and change the ```sleep``` command to ```timeout``` on line 35.


Open CMD in Administrator mode on Windows

REPLACE with your own path!
```powershell
sc create rapl type=kernel binPath="C:\Users\reini\Documents\github_repos\cs4575-project2\cs4575_project2\energibridge_things\LibreHardwareMonitor.sys"
```
Output:
```
[SC] CreateService SUCCESS
```


Then this command needs to be run everytime you reboot your pc...
```powershell
sc start rapl
```
Output:
```powershell
SERVICE_NAME: rapl
        TYPE               : 1  KERNEL_DRIVER
        STATE              : 4  RUNNING
                                (STOPPABLE, NOT_PAUSABLE, IGNORES_SHUTDOWN)
        WIN32_EXIT_CODE    : 0  (0x0)
        SERVICE_EXIT_CODE  : 0  (0x0)
        CHECKPOINT         : 0x0
        WAIT_HINT          : 0x0
        PID                : 0
        FLAGS              :
```

For Linux installation instructions head to ```cs4575_project2\energibridge_things\README.md```, the current project is setup for a Linux device. 

### Step 6: Building the docker containers & experiment setup
To run the experiments for inference library energy comparison, you have to follow multiple steps to make it work. Un the ```cs4575_project2\dockerfiles``` folder, you will be able to find the documentation on how to do all this in the [```README.MD```](https://github.com/flazedd/cs4575-project2/blob/master/cs4575_project2/dockerfiles/README.md) file.

### Step 7: Run the project
Make sure to launch your IDE/terminal in Administrator mode! 

```bash
poetry run python .\cs4575_project2\main.py
```
or
```bash
cd cs4575_project2
poetry run python .\main.py
```


