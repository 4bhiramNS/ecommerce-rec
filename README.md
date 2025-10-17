# E-commerce Product Recommender

This repository contains a simple, full-stack example of an **E-commerce Product Recommender**
with LLM-powered explanations for why a product was recommended.

It was generated based on your uploaded project brief. For reference: the uploaded spec is included in the repo and summarized in the README. fileciteturn0file0

## Contents
- `backend/` — FastAPI backend providing recommendation API and a lightweight SQLite database.
- `frontend/` — Static HTML + JS dashboard to fetch and display recommendations.
- `requirements.txt` — Python dependencies.
- `.env.example` — Example environment variables (add your OPENAI_API_KEY to enable LLM explanations).
- `Dockerfile` — Containerize the backend (optional).

## Quick start (local)
1. Create a Python venv and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # mac/linux
   venv\Scripts\activate    # windows
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Seed the database with demo data:
   ```bash
   python backend/app/seed.py
   ```
4. Run the backend:
   ```bash
   uvicorn backend.app.main:app --reload --port 8000
   ```
5. Open `frontend/index.html` in your browser (or serve it from any static host) and try the demo.

## API
- `GET /recommend/{user_id}?limit=10` — returns recommended products and a short LLM-generated explanation.

## Notes
- LLM explanations are powered by the OpenAI API if `OPENAI_API_KEY` is set in environment variables. Otherwise a local template explanation is returned.
- The recommender is a simple item-based/content-aware recommender designed for demo purposes. Replace with a production model as needed.


