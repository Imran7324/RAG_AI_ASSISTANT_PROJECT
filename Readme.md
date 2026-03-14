# RAG-Based AI Teaching Assistant for ML Course

A local, privacy-first **Retrieval-Augmented Generation (RAG)** system built to help students navigate through 12+ hours of Machine Learning course videos using semantic search and timestamps.

## Key Features
- **Video-to-Knowledge Pipeline:** Converts raw video lectures into searchable JSON transcripts.
- **Local LLM Integration:** Uses **Ollama (Llama 3.2:1b)** for answering queries without any paid APIs.
- **Semantic Search:** Implemented **Cosine Similarity** using `nomic-embed-text` embeddings.
- **Timestamp-Based Retrieval:** AI points to the exact minutes/seconds where a topic is taught.
- **Optimized for Low-Specs:** Successfully runs on an **8GB RAM machine** with Integrated Graphics.

## Tech Stack
- **Models:** OpenAI Whisper (Transcription), Llama 3.2 (LLM), Nomic-Embed-Text (Embeddings).
- **Libraries:** Pandas, NumPy, Scikit-learn, Requests, Joblib.
- **Tools:** FFmpeg (Audio extraction), Ollama (Local AI server).

## Project Workflow
1. **Ingestion:** Extracted audio from MP4 files using FFmpeg.
2. **Transcription:** Generated raw JSON segments with timestamps using Whisper.
3. **Chunk Merging:** Combined 5-segment windows to increase semantic context (Paragraph-level RAG).
4. **Vectorization:** Created a local vector store in a Pandas DataFrame.
5. **Inference:** Queried the vector store to find relevant chunks and passed them to Llama 3.2 for final response.

## How to Run
1. `pip install -r requirements.txt`
2. `ollama pull llama3.2:1b` & `ollama pull nomic-embed-text`
3. Run `scripts/process_incoming.py` to ask questions.
