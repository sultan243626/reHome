# 🔧 Sorun Giderme Rehberi

## Problem: init_db.py Hatası

### Hata Mesajı:
```
(trapped) error reading bcrypt version
AttributeError: module 'bcrypt' has no attribute '__about__'
Error initializing database: password cannot be longer than 72 bytes
```

### Çözüm:

1. **Docker container'ları durdurun:**
   ```bash
   docker-compose down
   ```

2. **Backend image'ını yeniden oluşturun:**
   ```bash
   docker-compose build --no-cache backend
   ```

3. **Servisleri tekrar başlatın:**
   ```bash
   docker-compose up -d
   ```

4. **init_db.py'yi tekrar çalıştırın:**
   ```bash
   docker-compose exec backend python init_db.py
   ```

## Problem: API'ye Erişilemiyor (http://localhost:8000/api)

### Kontrol Adımları:

1. **Container'ların çalıştığını kontrol edin:**
   ```bash
   docker-compose ps
   ```
   Her iki servis de "Up" durumunda olmalı.

2. **Backend loglarını kontrol edin:**
   ```bash
   docker-compose logs backend
   ```
   Hata mesajı var mı bakın.

3. **Backend'in çalıştığını test edin:**
   Tarayıcıda şu adreslere gidin:
   - http://localhost:8000
   - http://localhost:8000/api/health
   - http://localhost:8000/docs

4. **Port'un kullanılabilir olduğunu kontrol edin:**
   ```bash
   netstat -ano | findstr :8000
   ```
   Eğer başka bir uygulama 8000 portunu kullanıyorsa, `docker-compose.yml` dosyasında portu değiştirin.

### Çözüm:

Eğer backend çalışmıyorsa:

1. **Backend'i yeniden başlatın:**
   ```bash
   docker-compose restart backend
   ```

2. **Tüm servisleri yeniden başlatın:**
   ```bash
   docker-compose down
   docker-compose up -d
   ```

3. **Backend loglarını izleyin:**
   ```bash
   docker-compose logs -f backend
   ```
   Hata mesajlarını kontrol edin.

## Problem: CORS Hatası (Frontend'den API'ye erişilemiyor)

### Hata Mesajı:
```
Access to fetch at 'http://localhost:8000/api/...' from origin 'file://' has been blocked by CORS policy
```

### Çözüm:

1. **Frontend'i bir web sunucusu üzerinden çalıştırın:**
   - HTML dosyalarını doğrudan açmak yerine, bir web sunucusu kullanın
   - Python ile: `python -m http.server 3000` (frontend klasöründe)
   - Node.js ile: `npx serve` veya `npx http-server`
   - VS Code Live Server extension kullanın

2. **CORS ayarlarını kontrol edin:**
   `backend/main.py` dosyasında CORS ayarları zaten tüm origin'lere açık:
   ```python
   allow_origins=["*"]
   ```

## Problem: Frontend'den API'ye İstek Atılamıyor

### Kontrol Listesi:

1. ✅ Backend çalışıyor mu? (http://localhost:8000/docs)
2. ✅ Frontend bir web sunucusu üzerinden mi çalışıyor?
3. ✅ API URL doğru mu? (`http://localhost:8000/api`)
4. ✅ CORS ayarları doğru mu?

### Test Komutları:

**PowerShell'de backend'i test edin:**
```powershell
# Backend'in çalıştığını kontrol et
Invoke-WebRequest -Uri "http://localhost:8000/api/health"

# Veya curl ile
curl http://localhost:8000/api/health
```

## Problem: Veritabanı Bağlantı Hatası

### Hata Mesajı:
```
sqlalchemy.exc.OperationalError: could not connect to server
```

### Çözüm:

1. **PostgreSQL'in çalıştığını kontrol edin:**
   ```bash
   docker-compose ps postgres
   ```

2. **PostgreSQL loglarını kontrol edin:**
   ```bash
   docker-compose logs postgres
   ```

3. **PostgreSQL'i yeniden başlatın:**
   ```bash
   docker-compose restart postgres
   ```

4. **Tüm servisleri yeniden başlatın:**
   ```bash
   docker-compose down
   docker-compose up -d
   ```

## Hızlı Çözüm: Her Şeyi Sıfırlama

Eğer hiçbir şey çalışmıyorsa:

```bash
# 1. Tüm container'ları durdur ve sil
docker-compose down -v

# 2. Image'ları yeniden oluştur
docker-compose build --no-cache

# 3. Servisleri başlat
docker-compose up -d

# 4. Veritabanını başlat
docker-compose exec backend python init_db.py

# 5. Logları kontrol et
docker-compose logs -f
```

## Yardımcı Komutlar

```bash
# Container durumunu kontrol et
docker-compose ps

# Tüm logları görüntüle
docker-compose logs

# Sadece backend logları
docker-compose logs backend

# Backend'e bağlan
docker-compose exec backend bash

# PostgreSQL'e bağlan
docker-compose exec postgres psql -U rehome_user -d rehome_db

# Container'ları yeniden başlat
docker-compose restart

# Belirli bir servisi yeniden başlat
docker-compose restart backend
```

## Test Endpoint'leri

Backend'in çalıştığını test etmek için:

1. **Ana sayfa:** http://localhost:8000
2. **Health check:** http://localhost:8000/api/health
3. **API docs:** http://localhost:8000/docs
4. **ReDoc:** http://localhost:8000/redoc

## Frontend Test

Frontend'den API'yi test etmek için:

1. Frontend'i bir web sunucusu üzerinden çalıştırın
2. Tarayıcı konsolunu açın (F12)
3. Network sekmesine gidin
4. Frontend'den bir işlem yapın (örneğin bağış yap)
5. İsteklerin gönderildiğini ve yanıtların alındığını kontrol edin

