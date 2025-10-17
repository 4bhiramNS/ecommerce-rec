"""
A simple content-aware recommender:
- Builds a TF-IDF matrix over product descriptions+tags.
- For a given user, aggregates vectors of products they interacted with (weighted by event type).
- Ranks candidate products by cosine similarity to the user profile vector.
This is intentionally simple and easily replaceable with collaborative or hybrid models.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .models import Product
from sqlalchemy.orm import Session

def build_product_corpus(products):
    docs = []
    ids = []
    for p in products:
        text = " ".join(filter(None, [p.title or "", p.description or "", p.tags or ""]))
        docs.append(text)
        ids.append(p.id)
    return docs, ids

class SimpleRecommender:
    def __init__(self, db: Session):
        self.db = db
        self._fit()

    def _fit(self):
        products = self.db.query(Product).all()
        self.products = products
        docs, ids = build_product_corpus(products)
        if len(docs) == 0:
            self.vectorizer = None
            self.tfidf = None
            self.id_index = []
            return
        self.vectorizer = TfidfVectorizer(max_features=2000)
        self.tfidf = self.vectorizer.fit_transform(docs)
        self.id_index = ids

    def recommend_for_user(self, user_profile_vector, limit=10, exclude_ids=None):
        if self.tfidf is None:
            return []
        sims = cosine_similarity(user_profile_vector, self.tfidf).flatten()
        ranked_idx = np.argsort(-sims)
        results = []
        for idx in ranked_idx:
            pid = self.id_index[idx]
            if exclude_ids and pid in exclude_ids:
                continue
            prod = next((p for p in self.products if p.id == pid), None)
            if prod:
                results.append((prod, float(sims[idx])))
            if len(results) >= limit:
                break
        return results

    def user_vector_from_events(self, events, weight_map=None):
        if weight_map is None:
            weight_map = {"view": 1.0, "add_to_cart": 2.0, "purchase": 4.0}
        docs_by_pid = {p.id: " ".join(filter(None, [p.title or "", p.description or "", p.tags or ""])) for p in self.products}
        vecs = []
        weights = []
        for ev in events:
            pid = ev.product_id
            doc = docs_by_pid.get(pid)
            if doc and self.vectorizer:
                vec = self.vectorizer.transform([doc])
                vecs.append(vec.toarray().ravel())
                weights.append(weight_map.get(ev.event_type, 1.0))
        if len(vecs) == 0:
            # fallback: average of all products
            if self.tfidf is None:
                return np.zeros((1, 1))
            return np.mean(self.tfidf.toarray(), axis=0).reshape(1, -1)
        arr = np.vstack(vecs)
        w = np.array(weights).reshape(-1,1)
        profile = (arr * w).sum(axis=0) / (w.sum() + 1e-9)
        return profile.reshape(1, -1)
