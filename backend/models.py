from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum

class ItemStatus(str, enum.Enum):
    available = "available"
    reserved = "reserved"
    taken = "taken"

class DonationStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    completed = "completed"
    cancelled = "cancelled"

class CouponStatus(str, enum.Enum):
    active = "active"
    used = "used"
    expired = "expired"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String)
    address = Column(Text)
    hashed_password = Column(String, nullable=False)
    points = Column(Integer, default=0)
    total_donations = Column(Integer, default=0)
    total_co2_savings = Column(Float, default=0.0)
    rating = Column(Float, default=0.0)
    badges = Column(Integer, default=0)
    membership_level = Column(String, default="Bronze")  # Bronze, Silver, Gold, Platinum
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    items = relationship("Item", back_populates="user")
    donations = relationship("Donation", back_populates="user")
    received_items = relationship("ReceivedItem", back_populates="user")
    points_history = relationship("PointsHistory", back_populates="user")
    coupons = relationship("Coupon", back_populates="user")
    messages = relationship("Message", back_populates="user")
    co2_savings = relationship("CO2Savings", back_populates="user")

class YouthCenter(Base):
    __tablename__ = "youth_centers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    address = Column(Text)
    phone = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    capacity = Column(Integer, default=0)
    active_items = Column(Integer, default=0)
    status = Column(String, default="active")  # active, busy, inactive
    
    # Relationships
    items = relationship("Item", back_populates="center")
    donations = relationship("Donation", back_populates="center")

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String, nullable=False)  # mobilya, beyaz-esyalar, egitim-araclari, mutfak-gerecleri
    item_type = Column(String, nullable=False)  # Kanepe, Masa, etc.
    condition = Column(String)  # yeni, iyi, orta, kötü
    location = Column(String)
    image_url = Column(String)
    points_value = Column(Integer, default=0)
    co2_savings = Column(Float, default=0.0)
    status = Column(String, default="available")
    user_id = Column(Integer, ForeignKey("users.id"))
    center_id = Column(Integer, ForeignKey("youth_centers.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="items")
    center = relationship("YouthCenter", back_populates="items")
    donations = relationship("Donation", back_populates="item")
    received_items = relationship("ReceivedItem", back_populates="item")
    points_history = relationship("PointsHistory", back_populates="item")
    co2_savings_records = relationship("CO2Savings", back_populates="item")

class Donation(Base):
    __tablename__ = "donations"
    
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    center_id = Column(Integer, ForeignKey("youth_centers.id"))
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    item = relationship("Item", back_populates="donations")
    user = relationship("User", back_populates="donations")
    center = relationship("YouthCenter", back_populates="donations")

class ReceivedItem(Base):
    __tablename__ = "received_items"
    
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    received_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    item = relationship("Item", back_populates="received_items")
    user = relationship("User", back_populates="received_items")

class PointsHistory(Base):
    __tablename__ = "points_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    points = Column(Integer, nullable=False)
    description = Column(String)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="points_history")
    item = relationship("Item", back_populates="points_history")

class Coupon(Base):
    __tablename__ = "coupons"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    business_id = Column(String)
    product_name = Column(String)
    points_used = Column(Integer)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    used_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="coupons")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    sender = Column(String)  # "system", "youth_center", or user email
    title = Column(String)
    content = Column(Text)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="messages")

class CO2Savings(Base):
    __tablename__ = "co2_savings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="co2_savings")
    item = relationship("Item", back_populates="co2_savings_records")

