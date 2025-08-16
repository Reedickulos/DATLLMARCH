# DATLLM × ASI‑Arch Integration

This repository provides a **minimal working skeleton** that combines the
[DAT LLM](https://github.com/Reedickulos/DATLLM) local AI agent with the
autonomous research framework described in [ASI‑Arch](https://github.com/GAIR-NLP/ASI-Arch).
The goal of this project is to demonstrate how a *multi‑agent architecture
discovery loop* can be integrated into a lightweight local agent while
leveraging **LLaMA 3** as the underlying language model.

### What This Repository Contains

- **`pipeline/`** – a simplified implementation of the ASI‑Arch
  architecture discovery pipeline. It orchestrates a cycle of **sampling
  candidate architectures**, **evolving** them to propose new designs,
  **evaluating** their performance using a local LLM and simple metrics,
  and **analysing** the results to guide subsequent iterations.  Each
  component is modular, making it easy to extend or replace.

- **`database/`** – a stubbed database interface that demonstrates how a
  MongoDB‑like API might be exposed.  In a full implementation this
  module would manage experimental results and candidate sets, but here
  it simply persists JSON files to disk for demonstration purposes.

- **`cognition_base/`** – a placeholder for a retrieval‑augmented
  knowledge base.  In this skeleton it contains a dummy RAG service
  callable via an internal API.  In future work you can populate this
  module with a corpus of scientific papers and implement vector search
  using an appropriate library (e.g. FAISS or OpenSearch).

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
> installed.  See the [DAT LLM README](https://github.com/Reedickulos/DATLLM)
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

### Current Limitations

This repository is **not** a full reimplementation of ASI‑Arch.  It is a
minimal skeleton to illustrate how such a system might be integrated
into DAT LLM.  The evolve/eval/analyse steps operate on dummy
architectures represented as simple Python dictionaries; real
architecture descriptions and training loops would require far more
complex code and substantial compute.  Nevertheless, the modular
structure adopted here should make it straightforward to extend each
component incrementally.
