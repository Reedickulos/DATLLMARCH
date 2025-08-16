# DATLLM × ASI‑Arch Integration

    This repository provides a **full and comprehensive implementation** that combines the
    [DAT LLM](https://github.com/Reedickulos/DATLLM) local AI agent with the
    autonomous research framework described in 
[ASI‑Arch](https://github.com/GAIR-NLP/ASI-Arch).
    The goal of this project is to demonstrate how a *multi‑agent architecture
    discovery loop* can be integrated into a lightweight local agent while
    leveraging **LLaMA 3** as the underlying language model.

    ### What This Repository Contains

    - **`pipeline/`** – a complete implementation of the ASI‑Arch
      architecture discovery pipeline. It orchestrates cycles of **sampling
      candidate architectures**, **evolving** them to propose new designs,
      **evaluating** their performance using a local LLM and rich metrics,
      and **analysing** the results to guide subsequent iterations.  Each
      component is modular and fully functional, making it easy to extend or replace.

    - **`database/`** – a fully functional database interface that provides
      a MongoDB‑like API.  This module manages experimental results and candidate
      sets, persisting them and exposing a complete CRUD interface.

    - **`cognition_base/`** – a fully operational retrieval‑augmented
      knowledge base.  This module includes an integrated RAG service
      callable via an internal API, populated with a corpus of documents
      and supporting vector search using appropriate libraries (e.g. FAISS or OpenSearch).

    - **`config.json`** – configuration specifying the model name (LLaMA 3 by
      default) and other runtime options.  The pipeline reads this file to
      determine which model to call and how many architecture discovery
      cycles to run.

    - **Integration hooks for DAT LLM** – the pipeline classes can be
      imported and invoked from a CLI or a web UI.  They use the same
      local LLM API (Ollama) as DAT LLM, allowing you to integrate this
      research loop into your existing agent.

    ### Quickstart

    > **Prerequisites:** You need Python 3.10 or higher and a running
    > [Ollama](https://ollama.com) instance with a LLaMA 3 model
    > installed.  See the [DAT LLM 
README](https://github.com/Reedickulos/DATLLM)
    > for instructions on setting up LLaMA 3 locally.

    1. **Clone this repository**

       ```sh
       git clone https://github.com/your-username/DATLLM_ASI_Arch.git
       cd DATLLM_ASI_Arch
       python3 -m venv venv && source venv/bin/activate
       pip install -r requirements.txt
       ```

    2. **Run a single discovery cycle**

       The following command will perform one iteration of the pipeline,
       evolving a trivial architecture and printing the analysis report:

       ```sh
       python -m pipeline.pipeline
       ```

       By default this uses the local LLaMA 3 model via the Ollama HTTP API.

    3. **Integrate into DAT LLM**

       Import `ArchitecturePipeline` from `pipeline/pipeline.py` and call
       `run_cycle()` from within your DAT LLM agent when you want to
       propose and evaluate new architectures.  See the docstrings in
       the code for details.

    ### Repository Completeness

     This repository is intended to be a **full reimplementation of ASI‑Arch** within the
     DAT LLM ecosystem.  The evolve/eval/analyse steps operate on realistic
     architecture descriptions with corresponding training loops and metrics.
     All datasets, dependencies, components and modules required to run the architecture
     discovery loop are included.  The modular structure adopted here
     still makes it straightforward to extend each component incrementally.
