# Langchain Weather Agent

This repository contains a simple Python weather agent project built with LangChain.

## Overview

- `weather_agent.py`: Main application file for querying weather information.
- `langchain/`: Local Python virtual environment directory.
- `.env`: Environment file for API keys and configuration.

## Setup

1. Activate the virtual environment:
   - Windows PowerShell: `.\langchain\Scripts\Activate.ps1`
   - Windows Command Prompt: `.\langchain\Scripts\activate.bat`

2. Install dependencies if needed:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables in `.env`.

## Usage

Run the weather agent script:

```bash
python weather_agent.py
```

## Notes

- The `.gitignore` file excludes the local `langchain/` virtual environment and `__pycache__/` folders.
- Add your API keys to `.env` before running the project.
