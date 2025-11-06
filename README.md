# ReHome Backend - FastAPI + PostgreSQL + Docker

Bu proje, ReHome frontend uygulaması için FastAPI ve PostgreSQL kullanılarak geliştirilmiş bir backend servisidir.

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler

- Docker ve Docker Compose yüklü olmalıdır
- Windows, macOS veya Linux işletim sistemi

### Adım Adım Kurulum

#### 1. Projeyi İndirin ve Klasöre Gidin

```bash
cd kodluyoruzz
```

#### 2. Docker Compose ile Servisleri Başlatın

```bash
docker-compose up -d
```

Bu komut:
- PostgreSQL veritabanını başlatır (port 5432)
- FastAPI backend servisini başlatır (port 8000)
- Veritabanı bağlantısını otomatik olarak yapılandırır

#### 3. Veritabanını Başlatın (İlk Kurulum)

```bash
docker-compose exec backend python init_db.py
```

Bu komut veritabanı tablolarını oluşturur ve örnek veriler ekler.

#### 4. Servislerin Çalıştığını Kontrol Edin

- **Backend API**: http://localhost:8000
- **API Dokümantasyonu**: http://localhost:8000/docs
- **Alternatif Dokümantasyon**: http://localhost:8000/redoc

#### 5. Servisleri Durdurma

```bash
docker-compose down
```

Verileri de silmek için:

```bash
docker-compose down -v
```

## 📁 Proje Yapısı

```
backend/
├── main.py              # FastAPI uygulaması ve route'lar
├── database.py          # Veritabanı bağlantı ayarları
├── models.py            # SQLAlchemy modelleri
├── schemas.py           # Pydantic şemaları
├── utils.py             # Yardımcı fonksiyonlar
├── init_db.py           # Veritabanı başlatma scripti
├── requirements.txt     # Python bağımlılıkları
└── Dockerfile           # Docker image tanımı

docker-compose.yml       # Docker Compose konfigürasyonu
README.md                # Bu dosya
```

## 🔌 API Endpoints

### Authentication

- `POST /api/auth/register` - Kullanıcı kaydı
- `POST /api/auth/login` - Kullanıcı girişi
- `GET /api/auth/me` - Mevcut kullanıcı bilgileri

### Items (Eşyalar)

- `POST /api/items` - Yeni eşya/bağış oluştur
- `GET /api/items` - Eşyaları listele (filtreleme: center_id, category, item_type, city)
- `GET /api/items/{item_id}` - Belirli bir eşya detayı

### User Profile

- `GET /api/users/{user_id}/donations` - Kullanıcının bağışları
- `GET /api/users/{user_id}/received` - Kullanıcının aldığı eşyalar
- `GET /api/users/{user_id}/points-history` - Puan geçmişi
- `GET /api/users/{user_id}/stats` - Kullanıcı istatistikleri

### Youth Centers (Gençlik Merkezleri)

- `GET /api/youth-centers` - Gençlik merkezlerini listele
- `GET /api/youth-centers/{center_id}` - Belirli bir merkez detayı

### Coupons (Kuponlar)

- `GET /api/coupons/businesses` - İşletmeleri ve ürünleri listele
- `POST /api/coupons/exchange` - Puanları kuponla değiştir
- `GET /api/users/{user_id}/coupons` - Kullanıcının kuponları

### Messages (Mesajlar)

- `GET /api/users/{user_id}/messages` - Kullanıcının mesajları

### CO2 Savings

- `GET /api/users/{user_id}/co2-savings` - Kullanıcının CO2 tasarrufu geçmişi

## 🔐 Authentication

API'yi kullanmak için önce kayıt olup giriş yapmanız gerekir:

1. **Kayıt Ol**: `POST /api/auth/register`
```json
{
  "fullname": "Ahmet Yılmaz",
  "email": "ahmet@example.com",
  "phone": "0555 123 45 67",
  "address": "Konya, Türkiye",
  "password": "password123"
}
```

2. **Giriş Yap**: `POST /api/auth/login`
```
Form data:
- username: ahmet@example.com
- password: password123
```

3. **Token Kullan**: Giriş yaptıktan sonra dönen `access_token`'ı kullanarak korumalı endpoint'lere erişebilirsiniz:
```
Authorization: Bearer <access_token>
```

## 🗄️ Veritabanı

PostgreSQL veritabanı Docker container'ında çalışmaktadır. Bağlantı bilgileri:

- **Host**: localhost (dışarıdan) veya postgres (container içinden)
- **Port**: 5432
- **Database**: rehome_db
- **User**: rehome_user
- **Password**: rehome_password

### Veritabanına Doğrudan Bağlanma

```bash
docker-compose exec postgres psql -U rehome_user -d rehome_db
```

## 🧪 Test Etme

### API Dokümantasyonu ile Test

1. http://localhost:8000/docs adresine gidin
2. "Authorize" butonuna tıklayın
3. Login endpoint'ini kullanarak token alın
4. Token'ı "Authorize" kısmına yapıştırın
5. Diğer endpoint'leri test edebilirsiniz

### cURL ile Test

```bash
# Kayıt ol
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "fullname": "Test User",
    "email": "test@example.com",
    "phone": "0555 123 45 67",
    "address": "Test Address",
    "password": "test123"
  }'

# Giriş yap
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=test123"

# Token ile korumalı endpoint'e eriş
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer <your_token_here>"
```

## 🔧 Geliştirme

### Backend Kodunu Değiştirme

Backend klasöründeki dosyaları düzenleyebilirsiniz. Docker Compose `--reload` modunda çalıştığı için değişiklikler otomatik olarak yansır.

### Logları Görüntüleme

```bash
# Tüm servislerin logları
docker-compose logs -f

# Sadece backend logları
docker-compose logs -f backend

# Sadece postgres logları
docker-compose logs -f postgres
```

### Veritabanını Sıfırlama

```bash
# Container'ları durdur ve verileri sil
docker-compose down -v

# Tekrar başlat
docker-compose up -d

# Veritabanını yeniden başlat
docker-compose exec backend python init_db.py
```

## 📝 Notlar

- Production ortamında `SECRET_KEY`'i değiştirmeyi unutmayın
- CORS ayarları şu anda tüm origin'lere açık (`allow_origins=["*"]`). Production'da frontend URL'inizi belirtin.
- Veritabanı şifreleri production'da daha güvenli olmalıdır.

## 🐛 Sorun Giderme

### Port Zaten Kullanılıyor

Eğer 8000 veya 5432 portları kullanılıyorsa, `docker-compose.yml` dosyasındaki port numaralarını değiştirebilirsiniz.

### Veritabanı Bağlantı Hatası

```bash
# PostgreSQL'in hazır olduğunu kontrol edin
docker-compose ps

# PostgreSQL loglarını kontrol edin
docker-compose logs postgres
```

### Backend Başlamıyor

```bash
# Backend loglarını kontrol edin
docker-compose logs backend

# Container'ı yeniden başlatın
docker-compose restart backend
```

## 📞 Destek

Sorun yaşarsanız:
1. Logları kontrol edin: `docker-compose logs`
2. Container'ların çalıştığını kontrol edin: `docker-compose ps`
3. Veritabanı bağlantısını test edin

