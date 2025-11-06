"""
Script to initialize database with sample data
This script is idempotent - it can be run multiple times safely
"""
from database import SessionLocal, engine, Base
from models import User, YouthCenter, Item, Donation
from utils import get_password_hash
from datetime import datetime

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    centers_added = 0
    users_added = 0
    
    # Create sample youth centers (only if they don't exist)
    centers_data = [
        {
            "name": "Selçuklu Gençlik Merkezi",
            "city": "Konya",
            "address": "Selçuklu, Konya",
            "phone": "0332 123 45 67",
            "latitude": 37.8667,
            "longitude": 32.4833,
            "capacity": 150,
            "active_items": 45,
            "status": "active"
        },
        {
            "name": "Meram Gençlik Merkezi",
            "city": "Konya",
            "address": "Meram, Konya",
            "phone": "0332 234 56 78",
            "latitude": 37.8500,
            "longitude": 32.4500,
            "capacity": 120,
            "active_items": 32,
            "status": "active"
        },
        {
            "name": "Karatay Gençlik Merkezi",
            "city": "Konya",
            "address": "Karatay, Konya",
            "phone": "0332 345 67 89",
            "latitude": 37.8800,
            "longitude": 32.5200,
            "capacity": 100,
            "active_items": 28,
            "status": "busy"
        },
        {
            "name": "Merkez Gençlik Merkezi",
            "city": "Konya",
            "address": "Merkez, Konya",
            "phone": "0332 456 78 90",
            "latitude": 37.8600,
            "longitude": 32.4900,
            "capacity": 200,
            "active_items": 60,
            "status": "active"
        },
        {
            "name": "Bahçeşehir Gençlik Merkezi",
            "city": "Konya",
            "address": "Bahçeşehir, Konya",
            "phone": "0332 567 89 01",
            "latitude": 37.8700,
            "longitude": 32.5000,
            "capacity": 180,
            "active_items": 50,
            "status": "active"
        }
    ]
    
    for center_data in centers_data:
        # Check if center already exists
        existing_center = db.query(YouthCenter).filter(
            YouthCenter.name == center_data["name"]
        ).first()
        
        if not existing_center:
            center = YouthCenter(**center_data)
            db.add(center)
            centers_added += 1
        else:
            print(f"Youth center '{center_data['name']}' already exists, skipping...")
    
    # Create a sample user (only if it doesn't exist)
    existing_user = db.query(User).filter(User.email == "ahmet@example.com").first()
    
    if not existing_user:
        sample_user = User(
            fullname="Ahmet Yılmaz",
            email="ahmet@example.com",
            phone="0555 123 45 67",
            address="Konya, Türkiye",
            hashed_password=get_password_hash("password123"),
            points=2450,
            total_donations=127,
            total_co2_savings=45.2,
            rating=4.8,
            badges=12,
            membership_level="Gold"
        )
        db.add(sample_user)
        users_added += 1
    else:
        print("Sample user 'ahmet@example.com' already exists, skipping...")
    
    db.commit()
    
    if centers_added > 0 or users_added > 0:
        print(f"Database initialized successfully!")
        print(f"  - Added {centers_added} youth centers")
        print(f"  - Added {users_added} users")
    else:
        print("Database already initialized. All data exists.")
    
except Exception as e:
    print(f"Error initializing database: {e}")
    db.rollback()
    raise
finally:
    db.close()

