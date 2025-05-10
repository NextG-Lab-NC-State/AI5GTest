# Gen‑LLM • Procedural‑Flow Generation Pipeline

**Inference.ipynb** demonstrates our complete RAG workflow for synthesizing standards‑compliant procedural flows:

1. **Retrieval** – Queries produced by the Test‑Case Formatter fetch the top‑k spec chunks from the pre‑built FAISS index. (Refer to the _FAISS_ directory for more details).  
2. **Reranking** – The **BGE‑M3 reranker** filters noise; only the 15 most relevant chunks feed the LLM, dramatically reducing hallucinations and significantly improving the Gemma‑Score and generation fidelity versus GPT‑4o/Gemini.  
3. **Generation** – A Mistral‑7B‑Instruct endpoint (called via `transformers` on HuggingFace Inference) crafts the required test case procedure.  

An **exemplar run** for the *Initial UE Access* test case shows the pipeline and the resultant procedural flow.

> **API credentials**  
> Export `HUGGINGFACEHUB_API_TOKEN` (or set it in a `.env`) before execution so the notebook can call the LLM endpoint.
