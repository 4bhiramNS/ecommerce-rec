"""
Seed script to populate demo products, users and events into the SQLite DB.
Run: python backend/app/seed.py
"""
from sqlalchemy.orm import Session
from backend.app.database import engine, SessionLocal, Base
from backend.app.models import Product, User, UserEvent
import os

Base.metadata.create_all(bind=engine)
db: Session = SessionLocal()

# Clear (for dev/demo)
db.query(UserEvent).delete()
db.query(Product).delete()
db.query(User).delete()
db.commit()

# Sample products
products = [
    {"title":"Wireless Noise-Cancelling Headphones", "description":"Over-ear headphones with active noise cancellation and 30h battery.", "price":99.99, "tags":"audio,headphones,wireless"},
    {"title":"Portable Bluetooth Speaker", "description":"Compact speaker with powerful sound and IPX6 water resistance.", "price":45.00, "tags":"audio,speaker,portable"},
    {"title":"Stainless Steel Water Bottle 1L", "description":"Keeps liquids hot or cold for hours. BPA-free.", "price":19.99, "tags":"kitchen,hydration,travel"},
    {"title":"Ergonomic Office Chair", "description":"Adjustable lumbar support and breathable mesh.", "price":199.0, "tags":"furniture,office,chair"},
    {"title":"Gaming Mechanical Keyboard", "description":"RGB backlit, tactile switches, programmable macros.", "price":79.0, "tags":"gaming,keyboard,pc"},
    {"title":"Running Shoes - Lightweight", "description":"Cushioned running shoes for daily training.", "price":59.0, "tags":"sports,shoes,fitness"},
    {"title":"Smart LED Light Bulb", "description":"Wi-Fi enabled tunable white and color lighting.", "price":15.0, "tags":"home,smart,lighting"},
    {"title":"Instant Pot - 6 Quart", "description":"Multicooker: pressure cooker, slow cooker, rice cooker.", "price":89.0, "tags":"kitchen,appliances,cooking"},
    {"title":"Noise-Isolating Earbuds", "description":"In-ear earbuds with secure fit and clear sound.", "price":29.0, "tags":"audio,earbuds,portable"},
    {"title":"4K Action Camera", "description":"Waterproof camera with image stabilization and mounts.", "price":129.0, "tags":"camera,action,outdoors"},
]

for p in products:
    prod = Product(**p)
    db.add(prod)
db.commit()

# Sample users
u1 = User(name="Alice")
u2 = User(name="Bob")
db.add_all([u1, u2])
db.commit()

# Sample events: user 1 viewed audio products and purchased earbuds
events = [
    UserEvent(user_id=u1.id, product_id=1, event_type="view"),
    UserEvent(user_id=u1.id, product_id=2, event_type="view"),
    UserEvent(user_id=u1.id, product_id=9, event_type="purchase"),
    UserEvent(user_id=u2.id, product_id=4, event_type="view"),
    UserEvent(user_id=u2.id, product_id=5, event_type="add_to_cart"),
]
db.add_all(events)
db.commit()
print("Seeding complete. DB path:", os.getenv("DATABASE_URL", "sqlite:///./recommender.db"))
