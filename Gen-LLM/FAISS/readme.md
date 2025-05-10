# Gen‑LLM • FAISS Index Construction

The **FAISS/FAISS.ipynb** notebook reveals how we transform 252 O‑RAN and 14 560 3GPP specifications into a high‑speed vector store that underpins Gen‑LLM’s retrieval‑augmented generation (RAG) engine.

1. **Chunking & Embedding** – Each spec is segmented into semantically coherent slices; we embed every slice with **BGE‑Large‑en‑v1.5** (1024‑D) to capture fine‑grained telecom semantics.  
2. **Indexing** – 573 M words are ingested into a FAISS index, enabling fasr nearest‑neighbor search across the entire corpus.  
3. **Packaging** –  
   * **docs.zip** → raw text chunks (will be available on a public HuggingFace repo).  
   * **AI5GTest_FAISS** → the compiled index (will also be hosted on HuggingFace) for instant reuse.
