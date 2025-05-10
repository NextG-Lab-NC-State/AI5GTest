# AI5GTest • Validation

The **Validation.ipynb** notebook is a walkthrough of our test‑case validation pipeline that comprises of two main LLM based methods build on the 70‑B _LLaMA‑3.1_ model:

* **Val‑LLM** performs a strictly chronological scan of signaling logs with the 70‑B LLaMA‑3.1 model, classifying each step in the expected procedural flow and delivering a binary *Pass/Fail* verdict with 100 % accuracy across 15 diverse O‑RAN test cases.  
* **Debug‑LLM** re‑processes the same log from every index to pinpoint missing or out‑of‑order messages, returning *Partial Pass* diagnostics that explain root causes—crucial when Val‑LLM flags a failure.

**Each forward pass** for the _LLaMA_ returns a structured natural‑language response, which we automatically parse into three fields:  
    1. **Label** – *Yes* / *No* for the current step.  
    2. **Explanation** – a detailed explaination for the prediction.  
    3. **Confidence** – the model’s self‑reported certainty.  

The notebook showcases the **UE Initial Access over E1 and F1** test case and the resultant visualisation is—saved as **`sequence_diagram.svg`** and is available in this directory.

> **Before you run**  
> Set an environment variable named `NVIDIA_API_KEY`.  
> The notebook calls `langchain‑nvidia‑ai‑endpoints` to access the LLaMA model used by Val‑LLM and Debug‑LLM.
