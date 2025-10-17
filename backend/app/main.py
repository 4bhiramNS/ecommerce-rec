from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, recommender, schemas
from .database import engine, SessionLocal, Base
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
load_dotenv()

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print("DB create:", e)

app = FastAPI(title="E-commerce Recommender")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def llm_explain(product, user_id, reason_text):
    """Return an explanation string. If OPENAI_API_KEY is set, attempt to call OpenAI;
    otherwise return a generated template."""
    import os
    key = os.getenv("OPENAI_API_KEY")
    if key:
        try:
            import openai
            openai.api_key = key
            prompt = f"Explain in 1-2 short sentences why the product titled '{product.title}' (id={product.id}) is a good recommendation for user {user_id}. Use the reason: {reason_text}"
            resp = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role":"user", "content": prompt}],
                max_tokens=60,
                temperature=0.7
            )
            text = resp["choices"][0]["message"]["content"].strip()
            return text
        except Exception as e:
            return f"Recommended because: {reason_text} (LLM call failed: {e})"
    else:
        return f"Recommended because: {reason_text}"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/recommend/{user_id}", response_model=list[schemas.Recommendation])
def recommend(user_id: int, limit: int = 10, db: Session = Depends(get_db)):
    # load user events
    events = db.query(models.UserEvent).filter(models.UserEvent.user_id==user_id).all()
    # exclude already purchased items from results
    purchased = [e.product_id for e in events if e.event_type == "purchase"]
    # build recommender
    r = recommender.SimpleRecommender(db)
    user_vec = r.user_vector_from_events(events)
    results = r.recommend_for_user(user_vec, limit=limit, exclude_ids=purchased)
    out = []
    for prod, score in results:
        reason_text = f"User interacted with similar items (score={score:.3f})"
        explanation = llm_explain(prod, user_id, reason_text)
        out.append({"product": prod, "score": score, "explanation": explanation})
    return out
