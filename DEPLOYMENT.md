# Deployment Guide

This document provides step-by-step instructions for setting up and running the DATLLMARCH project on your local machine using Visual Studio Code or any Python IDE.

## Prerequisites

- **Python 3.10+** installed.
- **Git** installed for cloning the repository.
- **Virtual environment tool** such as `venv`.
- **Visual Studio Code** (or any IDE) with the Python extension. The instructions are similar for other editors.

## Setup Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/Reedickulos/DATLLMARCH.git
   cd DATLLMARCH
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`
   ```

3. **Install dependencies**

   Install the base dependencies listed in `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

   *Optional:* For an advanced setup with retrieval-augmented generation and model fine-tuning you may need additional libraries such as `beautifulsoup4`, `faiss-cpu`, `sentence-transformers`, `torch`, `transformers` and `llama-cpp-python`. Install them as needed:

   ```bash
   pip install beautifulsoup4 faiss-cpu sentence-transformers torch transformers llama-cpp-python openai
   ```

4. **Configure the system**

   Edit `config.json` to adjust the number of discovery cycles, the path to the database file, or to enable the retrieval-augmented knowledge base (`"rag_enabled": true`).

5. **Run the pipeline**

   From the project root run:

   ```bash
   python -m pipeline.pipeline
   ```

   The script will iterate through candidate architectures, evaluate them using your local LLaMA 3 model via an Ollama server if available (see below), compute composite scores and output a summary. Results are stored in the path specified by `database_path`.

## Using LLaMA 3

The architecture evaluator is designed to call a local LLaMA 3 via [Ollama](https://ollama.com). Install and run Ollama on your machine, then pull the LLaMA 3 model:

```bash
brew install ollama  # or see the Ollama docs for other platforms
ollama pull llama3
ollama serve
```

The evaluator will automatically send prompts to `http://localhost:11434/api/generate`. If this endpoint is unavailable, random scores are used as a fallback.

## Retrieval-Augmented Generation (RAG)

To enable retrieval‑augmented reasoning, set `"rag_enabled": true` in `config.json` and populate the `cognition_base/rag_service.py` with a corpus of domain knowledge. For a production deployment you can replace the stub with a vector database such as FAISS or Pinecone, and integrate scraping functions to ingest papers from the web.

## Opening in Visual Studio Code

1. Launch **VS Code** and open the cloned `DATLLMARCH` folder.
2. When prompted, select the Python interpreter from your virtual environment (`venv` folder).
3. Install the Python extension if not already installed.
4. Use the integrated terminal to run the setup commands above.
5. You can set breakpoints and debug `pipeline/pipeline.py` to trace the discovery loop.

## Notes

- This project is a minimal skeleton to illustrate how ASI-Arch’s multi‑agent architecture discovery can be integrated with a lightweight local agent. Extending it to a fully fledged research system requires implementing the `database` and `cognition_base` backends, adding real scoring metrics, and integrating a state-of-the-art LLM.
- Ensure your machine has sufficient resources to run LLaMA 3. The model can be memory intensive; adjust the model size in `config.json` if using a smaller version.
