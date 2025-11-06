from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Points calculation based on category and item type
def calculate_points(category: str, item_type: str) -> int:
    # Base points by category
    category_points = {
        "mobilya": 50,
        "beyaz-esyalar": 100,
        "egitim-araclari": 30,
        "mutfak-gerecleri": 25
    }
    
    base_points = category_points.get(category, 30)
    
    # Item type multipliers
    item_multipliers = {
        "Kanepe": 1.5,
        "Masa": 1.2,
        "Sandalye": 1.0,
        "Dolap": 1.8,
        "Raf": 0.8,
        "Buzdolabı": 2.0,
        "Çamaşır Makinesi": 1.8,
        "Bulaşık Makinesi": 1.7,
        "Fırın": 1.5,
        "Mikrodalga": 1.2,
        "Kitap": 0.5,
        "Defter": 0.3,
        "Kalem": 0.2,
        "Hesap Makinesi": 0.8,
        "Sıra": 1.5,
        "Tencere": 0.8,
        "Tava": 0.6,
        "Tabak": 0.4,
        "Bardak": 0.3,
        "Çatal Bıçak": 0.5
    }
    
    multiplier = item_multipliers.get(item_type, 1.0)
    return int(base_points * multiplier)

# CO2 savings calculation based on item type
def calculate_co2_savings(item_type: str) -> float:
    co2_values = {
        "Kanepe": 45.0,
        "Masa": 35.0,
        "Sandalye": 25.0,
        "Dolap": 60.0,
        "Raf": 20.0,
        "Buzdolabı": 80.0,
        "Çamaşır Makinesi": 70.0,
        "Bulaşık Makinesi": 65.0,
        "Fırın": 55.0,
        "Mikrodalga": 30.0,
        "Kitap": 5.0,
        "Defter": 2.0,
        "Kalem": 1.0,
        "Hesap Makinesi": 15.0,
        "Sıra": 40.0,
        "Tencere": 12.0,
        "Tava": 8.0,
        "Tabak": 3.0,
        "Bardak": 2.0,
        "Çatal Bıçak": 5.0
    }
    
    return co2_values.get(item_type, 10.0)

