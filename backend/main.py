from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

from database import SessionLocal, engine, Base
from models import User, Item, YouthCenter, Donation, ReceivedItem, PointsHistory, Coupon, Message, CO2Savings
from schemas import (
    UserCreate, UserResponse, UserLogin, ItemCreate, ItemResponse,
    DonationResponse, PointsHistoryResponse, CouponResponse, MessageResponse,
    YouthCenterResponse, CO2SavingsResponse
)
from utils import calculate_points, calculate_co2_savings, get_password_hash, verify_password

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ReHome API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

# Routes

@app.get("/")
def read_root():
    return {"message": "ReHome API is running", "status": "ok"}

@app.get("/api")
def api_root():
    return {"message": "ReHome API", "version": "1.0.0", "endpoints": {
        "auth": "/api/auth",
        "items": "/api/items",
        "users": "/api/users",
        "youth-centers": "/api/youth-centers",
        "coupons": "/api/coupons",
        "health": "/api/health"
    }}

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "message": "API is running"}

# Auth routes
@app.post("/api/auth/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        fullname=user.fullname,
        email=user.email,
        phone=user.phone,
        address=user.address,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "user": UserResponse.model_validate(user)}

@app.get("/api/auth/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

# Items routes
@app.post("/api/items", response_model=ItemResponse)
def create_item(item: ItemCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Calculate points and CO2 savings
    points_value = calculate_points(item.category, item.item_type)
    co2_savings = calculate_co2_savings(item.item_type)
    
    db_item = Item(
        title=item.title,
        description=item.description,
        category=item.category,
        item_type=item.item_type,
        condition=item.condition,
        location=item.location,
        center_id=item.center_id,
        user_id=current_user.id,
        points_value=points_value,
        co2_savings=co2_savings,
        image_url=item.image_url
    )
    db.add(db_item)
    
    # Create donation record
    donation = Donation(
        item_id=db_item.id,
        user_id=current_user.id,
        center_id=item.center_id,
        status="pending"
    )
    db.add(donation)
    
    # Add points to user
    current_user.points += points_value
    current_user.total_donations += 1
    current_user.total_co2_savings += co2_savings
    
    # Create points history
    points_history = PointsHistory(
        user_id=current_user.id,
        points=points_value,
        description=f"Bağış: {item.title}",
        item_id=db_item.id
    )
    db.add(points_history)
    
    # Create CO2 savings record
    co2_record = CO2Savings(
        user_id=current_user.id,
        amount=co2_savings,
        item_id=db_item.id,
        description=f"Bağış: {item.title}"
    )
    db.add(co2_record)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/api/items", response_model=List[ItemResponse])
def get_items(
    center_id: Optional[int] = None,
    category: Optional[str] = None,
    item_type: Optional[str] = None,
    city: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Item)
    
    if center_id:
        query = query.filter(Item.center_id == center_id)
    if category:
        query = query.filter(Item.category == category)
    if item_type:
        query = query.filter(Item.item_type == item_type)
    if city:
        # Filter by city through youth center
        query = query.join(YouthCenter).filter(YouthCenter.city == city)
    
    items = query.all()
    return items

@app.get("/api/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# User profile routes
@app.get("/api/users/{user_id}/donations", response_model=List[DonationResponse])
def get_user_donations(user_id: int, db: Session = Depends(get_db)):
    donations = db.query(Donation).filter(Donation.user_id == user_id).all()
    return donations

@app.get("/api/users/{user_id}/received", response_model=List[ItemResponse])
def get_user_received_items(user_id: int, db: Session = Depends(get_db)):
    received_items = db.query(ReceivedItem).filter(ReceivedItem.user_id == user_id).all()
    items = [db.query(Item).filter(Item.id == ri.item_id).first() for ri in received_items]
    return [item for item in items if item]

@app.get("/api/users/{user_id}/points-history", response_model=List[PointsHistoryResponse])
def get_user_points_history(user_id: int, db: Session = Depends(get_db)):
    history = db.query(PointsHistory).filter(PointsHistory.user_id == user_id).order_by(PointsHistory.created_at.desc()).all()
    return history

@app.get("/api/users/{user_id}/stats")
def get_user_stats(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "total_donations": user.total_donations,
        "total_co2_savings": user.total_co2_savings,
        "points": user.points,
        "rating": user.rating,
        "badges": user.badges
    }

# Youth Centers routes
@app.get("/api/youth-centers", response_model=List[YouthCenterResponse])
def get_youth_centers(city: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(YouthCenter)
    if city:
        query = query.filter(YouthCenter.city == city)
    centers = query.all()
    return centers

@app.get("/api/youth-centers/{center_id}", response_model=YouthCenterResponse)
def get_youth_center(center_id: int, db: Session = Depends(get_db)):
    center = db.query(YouthCenter).filter(YouthCenter.id == center_id).first()
    if not center:
        raise HTTPException(status_code=404, detail="Youth center not found")
    return center

# Coupons routes
@app.get("/api/coupons/businesses")
def get_businesses():
    businesses = [
        {
            "id": "beltur",
            "name": "Beltur",
            "icon": "☕",
            "min_points": 200,
            "products": [
                {"name": "Kahve (1 adet)", "points": 200, "value": "40 TL"},
                {"name": "Kahve + Pasta", "points": 350, "value": "70 TL"}
            ]
        },
        {
            "id": "halkekmek",
            "name": "Halk Ekmek",
            "icon": "🍞",
            "min_points": 150,
            "products": [
                {"name": "Ekmek Paketi", "points": 150, "value": "30 TL"},
                {"name": "Unlu Mamul Seti", "points": 300, "value": "60 TL"}
            ]
        },
        {
            "id": "sosyaltesisler",
            "name": "Sosyal Tesisler",
            "icon": "🏛️",
            "min_points": 250,
            "products": [
                {"name": "Yemek Kuponu", "points": 250, "value": "50 TL"},
                {"name": "Aktivite Kuponu", "points": 400, "value": "80 TL"}
            ]
        },
        {
            "id": "cinemaximum",
            "name": "Cinemaximum",
            "icon": "🎬",
            "min_points": 300,
            "products": [
                {"name": "Sinema Bileti (1 kişi)", "points": 300, "value": "60 TL"},
                {"name": "Sinema Bileti (2 kişi)", "points": 500, "value": "100 TL"}
            ]
        },
        {
            "id": "teknosa",
            "name": "Teknosa",
            "icon": "💻",
            "min_points": 500,
            "products": [
                {"name": "Kulaklık", "points": 500, "value": "100 TL"},
                {"name": "Telefon Aksesuar Seti", "points": 700, "value": "140 TL"}
            ]
        },
        {
            "id": "kirtasiye",
            "name": "Yerel Kırtasiye",
            "icon": "📝",
            "min_points": 200,
            "products": [
                {"name": "Kırtasiye Seti", "points": 200, "value": "40 TL"},
                {"name": "Defter ve Kalem Paketi", "points": 350, "value": "70 TL"}
            ]
        }
    ]
    return businesses

@app.post("/api/coupons/exchange", response_model=CouponResponse)
def exchange_coupon(
    business_id: str,
    product_name: str,
    points_required: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.points < points_required:
        raise HTTPException(status_code=400, detail="Insufficient points")
    
    # Deduct points
    current_user.points -= points_required
    
    # Create coupon
    coupon = Coupon(
        user_id=current_user.id,
        business_id=business_id,
        product_name=product_name,
        points_used=points_required,
        status="active"
    )
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon

@app.get("/api/users/{user_id}/coupons", response_model=List[CouponResponse])
def get_user_coupons(user_id: int, db: Session = Depends(get_db)):
    coupons = db.query(Coupon).filter(Coupon.user_id == user_id).order_by(Coupon.created_at.desc()).all()
    return coupons

# Messages routes
@app.get("/api/users/{user_id}/messages", response_model=List[MessageResponse])
def get_user_messages(user_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.user_id == user_id).order_by(Message.created_at.desc()).all()
    return messages

# CO2 Savings routes
@app.get("/api/users/{user_id}/co2-savings", response_model=List[CO2SavingsResponse])
def get_user_co2_savings(user_id: int, db: Session = Depends(get_db)):
    savings = db.query(CO2Savings).filter(CO2Savings.user_id == user_id).order_by(CO2Savings.created_at.desc()).all()
    return savings

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

