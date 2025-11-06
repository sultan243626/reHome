# 🚀 Backend Başlatma Rehberi

## ❌ Sorun: "localhost refused to connect" Hatası

Bu hata, backend sunucusunun çalışmadığını gösterir. Aşağıdaki adımları takip ederek backend'i başlatın.

## ✅ Çözüm Adımları

### Adım 1: Docker Desktop'ın Çalıştığını Kontrol Edin

1. **Docker Desktop** uygulamasını açın
2. Sistem tepsisinde (tray) Docker ikonunun **yeşil** olduğundan emin olun
3. Eğer Docker çalışmıyorsa, Docker Desktop'ı başlatın

### Adım 2: Terminal (PowerShell) Açın

1. Windows tuşuna basın
2. "PowerShell" yazın ve Enter'a basın
3. Veya proje klasöründe sağ tıklayıp "Open in Terminal" seçin

### Adım 3: Proje Klasörüne Gidin

PowerShell'de şu komutu çalıştırın:

```powershell
cd C:\Users\topsu\OneDrive\Masaüstü\kodluyoruzz
```

### Adım 4: Mevcut Container'ları Kontrol Edin

Önce mevcut durumu kontrol edin:

```powershell
docker-compose ps
```

Eğer hiçbir container çalışmıyorsa veya durmuşsa, devam edin.

### Adım 5: Backend'i Başlatın

Aşağıdaki komutu çalıştırın:

```powershell
docker-compose up -d
```

**Ne olur?**
- PostgreSQL veritabanı başlar (port 5432)
- FastAPI backend başlar (port 8000)
- Servisler arka planda çalışır (`-d` flag'i sayesinde)

**İlk çalıştırmada:** Docker image'ları indirileceği için 2-5 dakika sürebilir.

### Adım 6: Container'ların Çalıştığını Doğrulayın

```powershell
docker-compose ps
```

Şunu görmelisiniz:
```
NAME                STATUS
rehome_postgres     Up
rehome_backend      Up
```

### Adım 7: Backend Loglarını Kontrol Edin

Eğer bir sorun varsa, logları kontrol edin:

```powershell
docker-compose logs backend
```

### Adım 8: Veritabanını Başlatın (İlk Kurulum İçin)

Eğer ilk kez çalıştırıyorsanız, veritabanını başlatın:

```powershell
docker-compose exec backend python init_db.py
```

### Adım 9: Backend'in Çalıştığını Test Edin

Tarayıcınızda şu adresleri açın:

1. **API Health Check**: http://localhost:8000/api/health
   - Şunu görmelisiniz: `{"status": "healthy", "message": "API is running"}`

2. **API Dokümantasyonu**: http://localhost:8000/docs
   - Swagger UI açılmalı

3. **API Root**: http://localhost:8000/api
   - API bilgilerini görmelisiniz

## 🔧 Sorun Giderme

### Sorun 1: Port 8000 Zaten Kullanılıyor

**Hata:** `port 8000 is already allocated`

**Çözüm:**
```powershell
# Port'u kullanan process'i bulun
netstat -ano | findstr :8000

# Process'i sonlandırın (PID'yi yukarıdaki komuttan alın)
taskkill /PID <PID_NUMARASI> /F

# Tekrar başlatın
docker-compose up -d
```

### Sorun 2: Docker Compose Bulunamadı

**Hata:** `docker-compose: command not found`

**Çözüm:**
```powershell
# Docker Compose V2 kullanın
docker compose up -d
```

### Sorun 3: Container Başlamıyor

**Çözüm:**
```powershell
# Container'ları durdurun
docker-compose down

# Volume'ları temizleyin (dikkatli: veriler silinir)
docker-compose down -v

# Tekrar başlatın
docker-compose up -d

# Logları kontrol edin
docker-compose logs backend
```

### Sorun 4: Backend Başlıyor Ama Hata Veriyor

**Logları kontrol edin:**
```powershell
docker-compose logs -f backend
```

**Yaygın hatalar:**
- Veritabanı bağlantı hatası → PostgreSQL'in başladığından emin olun
- Port hatası → Port 8000'in boş olduğundan emin olun
- Python modül hatası → `docker-compose build` çalıştırın

### Sorun 5: Veritabanı Bağlantı Hatası

**Çözüm:**
```powershell
# PostgreSQL'in hazır olduğunu kontrol edin
docker-compose ps postgres

# PostgreSQL loglarını kontrol edin
docker-compose logs postgres

# Backend'i yeniden başlatın
docker-compose restart backend
```

## 📝 Hızlı Komutlar

```powershell
# Backend'i başlat
docker-compose up -d

# Backend'i durdur
docker-compose down

# Backend'i yeniden başlat
docker-compose restart backend

# Logları görüntüle
docker-compose logs -f backend

# Container durumunu kontrol et
docker-compose ps

# Backend shell'ine gir
docker-compose exec backend bash
```

## ✅ Başarı Kontrolü

Backend başarıyla çalışıyorsa:

1. ✅ http://localhost:8000/api/health → `{"status": "healthy"}`
2. ✅ http://localhost:8000/docs → Swagger UI açılır
3. ✅ Frontend'den kayıt olma çalışır
4. ✅ Frontend'den giriş yapma çalışır

## 🆘 Hala Çalışmıyor mu?

1. Docker Desktop'ın çalıştığından emin olun
2. Windows Defender veya antivirüsün port 8000'i engellemediğinden emin olun
3. Firewall ayarlarını kontrol edin
4. `docker-compose logs backend` ile hata mesajlarını kontrol edin

