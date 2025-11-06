from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserCreate(BaseModel):
    fullname: str
    email: EmailStr
    phone: str
    address: str
    password: str

class UserResponse(BaseModel):
    id: int
    fullname: str
    email: str
    phone: Optional[str]
    address: Optional[str]
    points: int
    total_donations: int
    total_co2_savings: float
    rating: float
    badges: int
    membership_level: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Item schemas
class ItemCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    item_type: str
    condition: str
    location: str
    center_id: int
    image_url: Optional[str] = None

class ItemResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    category: str
    item_type: str
    condition: Optional[str]
    location: Optional[str]
    image_url: Optional[str]
    points_value: int
    co2_savings: float
    status: str
    user_id: int
    center_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Donation schemas
class DonationResponse(BaseModel):
    id: int
    item_id: int
    user_id: int
    center_id: int
    status: str
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Points History schemas
class PointsHistoryResponse(BaseModel):
    id: int
    user_id: int
    points: int
    description: Optional[str]
    item_id: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Coupon schemas
class CouponResponse(BaseModel):
    id: int
    user_id: int
    business_id: str
    product_name: str
    points_used: int
    status: str
    created_at: datetime
    used_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Message schemas
class MessageResponse(BaseModel):
    id: int
    user_id: int
    sender: str
    title: str
    content: str
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Youth Center schemas
class YouthCenterResponse(BaseModel):
    id: int
    name: str
    city: str
    address: Optional[str]
    phone: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    capacity: int
    active_items: int
    status: str
    
    class Config:
        from_attributes = True

# CO2 Savings schemas
class CO2SavingsResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    item_id: Optional[int]
    description: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

