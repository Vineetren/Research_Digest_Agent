# 🧠 AI Research Digest Generator

An end-to-end system that automatically ingests multiple information sources (URLs or local files), extracts key claims, validates them, groups them by semantic similarity, detects conflicts, and generates a structured research digest — complete with a cluster visualization.

This project simulates a lightweight research intelligence pipeline for aggregating and synthesizing information across documents.

---

# 📌 What This Project Does

Given a topic and a set of sources, the system:

1. Loads content from URLs or local files  
2. Extracts factual, topic-relevant claims using an LLM  
3. Validates claims against source content  
4. Generates semantic embeddings for each claim  
5. Groups similar claims into themes  
6. Detects contradictions between similar claims  
7. Produces a structured Markdown research digest  
8. Generates a 2D visualization of thematic clusters  

The goal is to demonstrate multi-document reasoning, semantic grouping, and research synthesis.

---

# 🏗️ High-Level Architecture

```
Input (URLs / Folder)
        ↓
Content Ingestion
        ↓
Claim Extraction (LLM)
        ↓
Claim Validation
        ↓
Embedding Generation
        ↓
Semantic Grouping
        ↓
Conflict Detection
        ↓
Digest Generation
        ↓
Cluster Visualization (PCA)
```

---

# 📂 Project Structure

```
agent/
│
├── ingestion.py          # Load URLs or folder files
├── cleaning.py           # HTML cleaning utilities
├── claim_extraction.py   # LLM-based claim extraction
├── validation.py         # Claim validation
├── embeddings.py         # Sentence-transformer embeddings
├── grouping.py           # Semantic clustering logic
├── conflict.py           # LLM-based contradiction detection
├── digest.py             # Markdown digest generation
├── exporter.py           # Export source metadata
├── visualization.py      # PCA cluster visualization
│
config/
└── settings.py           # Similarity thresholds and configs
│
main.py                   # Entry point
```

---

# ⚙️ Installation

## 📦 Dependencies

Main libraries used:

- requests
- beautifulsoup4
- pydantic
- sentence-transformers
- scikit-learn
- openai
- python-dotenv
- pytest
- numpy
- matplotlib

Install:

```
pip install -r requirements.txt
```

---

## 🔑 Environment Setup

Create a `.env` file in the root directory:

```
OPENROUTER_API_KEY=your_openai_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
CHAT_MODEL=meta-llama/llama-3-8b-instruct
SIMILARITY_THRESHOLD=0.65
```

### Variable Explanation

- `OPENROUTER_API_KEY` → Your OpenRouter API key  
- `OPENROUTER_BASE_URL` → Base endpoint for OpenRouter API  
- `CHAT_MODEL` → Model used for claim extraction and conflict detection  
- `SIMILARITY_THRESHOLD` → Cosine similarity cutoff for grouping claims  

Make sure environment variables are loaded using `python-dotenv`.

---

# 🚀 How to Run

## Option 1 — Using URLs

Create a file with one URL per line:

```
https://example.com/article1
https://example.com/article2
```

Run:

```
python main.py --urls_file {file_path} --topic "{topic}"
```

---

## Option 2 — Using a Local Folder

Folder may contain:
- `.txt`
- `.html`

Run:

```
python main.py --folder_path {folder_path} --topic "{topic}"
```

---

## Option 3 — Both

```
python main.py \
  --urls_file {file_path} \
  --folder_path {folder_path} \
  --topic "{topic}"
```

---

# 📊 Output Files

Generated in:

```
data/outputs/
```

- `digest.md` → Structured research summary  
- `sources.json` → Metadata for traceability  
- `clusters.png` → Visualization of grouped themes  

---

# 🧠 Key Features Explained

## 1️⃣ Multi-Source Ingestion

Supports:

- Web URLs  
- Local `.txt` files  
- Local `.html` files  

HTML is cleaned safely, while plain text is preserved.

---

## 2️⃣ LLM-Based Claim Extraction

The system extracts structured, factual claims relevant to the specified topic.

---

## 3️⃣ Claim Validation

Each extracted claim is checked against the source content to ensure it is supported.

This prevents hallucinated or unsupported claims from entering the digest.

---

## 4️⃣ Semantic Grouping (Embeddings)

The system uses:

- `sentence-transformers/all-MiniLM-L6-v2`  
- Cosine similarity  

Each claim is converted into a vector representation.

Claims above a configurable similarity threshold are grouped into themes.

Example threshold:

```
SIMILARITY_THRESHOLD = 0.65
```

---

## 5️⃣ Conflict Detection

Before grouping two similar claims together, the system:

- Sends both claims to an LLM  
- Asks whether they contradict each other  
- Keeps them separate if they conflict  

This ensures:

- Similar but opposite claims are not merged  
- The digest preserves disagreement  

---

## 6️⃣ Cluster Visualization

Each theme receives an average embedding vector.

Vectors are reduced from 384 dimensions to 2D using PCA.

The result is a scatter plot where:

- Each dot = one semantic theme  
- Distance = semantic similarity  
- Closer themes are more related  

This provides a visual understanding of the research landscape.

---

# 📘 Output Format

- Test outputs are produced in the `data/outputs` folder.
- Each test result folder contains:
  - `digest.md`
  - `sources.json`
  - `clusters.png`

---

## 🧪 Test Structure and Results

- Test inputs are kept in the `test_inputs/` folder.
- Test outputs are kept in the `test_results/` folder.
- Each test result folder contains:
  - `digest.md`
  - `sources.json`
  - `clusters.png`

---

# ⚙️ Design Decisions

## Why Sentence Transformers?

Efficient and strong semantic embeddings for grouping related claims.

## Why PCA?

Fast, simple dimensionality reduction for visual explanation.

## Why Use an LLM for Conflict Detection?

Cosine similarity detects closeness — not contradiction.  
LLMs allow reasoning over logical disagreement.

---

# ⚠ Limitations

- PCA is linear and may not perfectly capture cluster structure.  
- LLM conflict detection depends on model reliability.  
- Very short input files may be filtered if aggressively cleaned.  
- Not optimized for large-scale distributed processing.  

---

# 🔮 Possible Future Improvements

- Replace PCA with UMAP for better visualization  
- Interactive dashboard (Plotly or Streamlit)  
- Caching embeddings for faster re-runs  
- Adjustable similarity threshold via CLI  
- Confidence scoring per claim  
- Duplicate-run detection  
- PDF export option  

---

# 🎯 What This Project Demonstrates

- Multi-document reasoning  
- Semantic similarity grouping  
- Conflict-aware aggregation  
- LLM-assisted validation  
- Structured research synthesis  
- High-dimensional embedding visualization  
- Clean modular pipeline design  

This system demonstrates how AI can be used to automate research digestion and theme discovery across heterogeneous sources.