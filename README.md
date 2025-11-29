# Bootcamp - Building, Deploying and Scaling Agentic AI Systems

This repository contains all examples discussed during the bootcamp.

## Project Structure

- `script_1.py` - Simple LangChain chat example with prompt template and langfuse tracing
- `example.env` - Template for environment variables
- `pyproject.toml` - Project dependencies and configuration

## Browser

The Chrome browser is recommended.

## Prerequisites

### Install

**Python**
- Installation steps: https://www.python.org/downloads/
- Recommended: Python 3.11 - 3.13. This version is required for optimal compatibility with LangChain.

**uv package manager**
- Installation steps: https://docs.astral.sh/uv/getting-started/installation/
- Recommended: Latest Version. Standalone Installer.

**git**
- Installation steps: https://git-scm.com/install
- Recommended: Latest Version.

**Visual Studio Code**
- Installation steps: https://code.visualstudio.com/docs/setup/setup-overview
- Recommended: Latest Version. No additional components, extensions or AI features needed.

### Set up LLM API Keys

You'll need a Google API key (Free Tier). If you don’t have a Google API key, you can sign up here:
https://aistudio.google.com/api-keys

This would later be set in .env file as:
```
GOOGLE_API_KEY="..."
```

### Setup Langfuse

Create a Langfuse account and API key here:
1. Signup here: https://us.cloud.langfuse.com/auth/sign-in?targetPath=%2F
2. Create a new organization - Bootcamp
3. Create a new project - Day1
4. Go to Settings -> Under Project Settings -> API Keys -> Create new API Keys -> Create API Keys -> Copy the .env content

This would later be set in .env file as:
```
LANGFUSE_SECRET_KEY="sk-lf-..."
LANGFUSE_PUBLIC_KEY="pk-lf-..."
LANGFUSE_BASE_URL="https://us.cloud.langfuse.com"
```

## Bootcamp Repository Setup

### Clone the repo
```bash
git clone https://github.com/nsbisht/Bootcamp_Repository.git
```

### Create .env file
```bash
cd Bootcamp_Repository
cp example.env .env
```

### Open in VS Code
1. Open VS Code
2. File -> Open Folder -> Navigate and select Bootcamp_Repository -> Open

### Add Google API key
Add in .env file:
```
GOOGLE_API_KEY="..."
```

### API key for Langfuse Tracing
Add in .env file:
```
LANGFUSE_SECRET_KEY="sk-lf-..."
LANGFUSE_PUBLIC_KEY="pk-lf-..."
LANGFUSE_BASE_URL="https://us.cloud.langfuse.com"
```


### Open Terminal in VS Code
At the top,
```bash
Terminal -> New Terminal
```

### Create virtual environment and install dependencies
```bash
uv sync
```

## Running the Scripts

### Run the basic LangChain example
```bash
uv run script_1.py
```

## Troubleshooting

### Import errors
If you encounter import errors, ensure all dependencies are installed:
```bash
uv sync
```

### API key issues
- Verify your `.env` file contains valid API keys
- Ensure there are no extra spaces around the `=` sign
- Check that the `.env` file is in the project root directory

### Langfuse tracing not working
- Verify all three Langfuse environment variables are set correctly
- Check your project settings in the Langfuse dashboard
- Ensure you're using the correct region URL (US: `https://us.cloud.langfuse.com`)

### Version issues
Check your version:
```bash
python --version
uv --version
git --version
```