# 🚀 ReHome Backend Kurulum Rehberi

Bu rehber, ReHome backend servisini Docker kullanarak adım adım kurmanızı sağlar.

## 📋 Gereksinimler

- **Docker Desktop** yüklü olmalı (Windows için: https://www.docker.com/products/docker-desktop/)
- **Docker Compose** (Docker Desktop ile birlikte gelir)
- En az 2GB boş disk alanı

## 🔧 Adım Adım Kurulum

### Adım 1: Docker Desktop'ı Başlatın

1. Docker Desktop uygulamasını açın
2. Sistem tepsisinde Docker ikonunun yeşil olduğundan emin olun
3. Docker'ın çalıştığını kontrol etmek için terminalde şu komutu çalıştırın:
   ```bash
   docker --version
   ```

### Adım 2: Proje Klasörüne Gidin

Terminal (PowerShell veya Command Prompt) açın ve proje klasörüne gidin:

```bash
cd C:\Users\topsu\OneDrive\Masaüstü\kodluyoruzz
```

### Adım 3: Docker Compose ile Servisleri Başlatın

Aşağıdaki komutu çalıştırın:

```bash
docker-compose up -d
```

Bu komut:
- ✅ PostgreSQL veritabanını başlatır (port 5432)
- ✅ FastAPI backend servisini başlatır (port 8000)
- ✅ Servisler arası bağlantıyı yapılandırır

**Not:** İlk çalıştırmada Docker image'ları indirileceği için 2-5 dakika sürebilir.

### Adım 4: Servislerin Durumunu Kontrol Edin

Servislerin çalıştığını kontrol etmek için:

```bash
docker-compose ps
```

Her iki servis de (postgres ve backend) "Up" durumunda olmalı.

### Adım 5: Veritabanını Başlatın

Veritabanı tablolarını oluşturmak ve örnek veriler eklemek için:

```bash
docker-compose exec backend python init_db.py
```

Bu komut:
- ✅ Tüm veritabanı tablolarını oluşturur
- ✅ Örnek gençlik merkezleri ekler
- ✅ Örnek kullanıcı ekler

### Adım 6: Backend'in Çalıştığını Test Edin

Tarayıcınızda şu adreslere gidin:

- **API Ana Sayfa**: http://localhost:8000
- **API Dokümantasyonu (Swagger)**: http://localhost:8000/docs
- **Alternatif Dokümantasyon (ReDoc)**: http://localhost:8000/redoc

Eğer sayfalar açılıyorsa, backend başarıyla çalışıyor demektir! 🎉

## 🧪 API'yi Test Etme

### 1. API Dokümantasyonu ile Test

1. http://localhost:8000/docs adresine gidin
2. **POST /api/auth/register** endpoint'ini bulun ve "Try it out" butonuna tıklayın
3. Örnek veri girin:
   ```json
   {
     "fullname": "Test Kullanıcı",
     "email": "test@example.com",
     "phone": "0555 123 45 67",
     "address": "Test Adres",
     "password": "test123"
   }
   ```
4. "Execute" butonuna tıklayın
5. Başarılı olursa 200 yanıtı alacaksınız

### 2. Giriş Yapma

1. **POST /api/auth/login** endpoint'ine gidin
2. "Try it out" butonuna tıklayın
3. Form verilerini girin:
   - username: `test@example.com`
   - password: `test123`
4. "Execute" butonuna tıklayın
5. Dönen `access_token`'ı kopyalayın

### 3. Token ile Korumalı Endpoint'e Erişim

1. Sayfanın üst kısmındaki **"Authorize"** butonuna tıklayın
2. Kopyaladığınız token'ı yapıştırın
3. "Authorize" butonuna tıklayın
4. Artık korumalı endpoint'leri kullanabilirsiniz

## 📱 Frontend'i Backend'e Bağlama

Frontend dosyalarınızda API URL'ini güncellemeniz gerekiyor. Örneğin `3Bagis.html` dosyasında:

```javascript
const API_URL = 'http://localhost:8000/api';
```

Bu şekilde frontend'iniz backend API'nize bağlanacaktır.

## 🔍 Logları Görüntüleme

### Tüm servislerin logları:
```bash
docker-compose logs -f
```

### Sadece backend logları:
```bash
docker-compose logs -f backend
```

### Sadece postgres logları:
```bash
docker-compose logs -f postgres
```

## ⏹️ Servisleri Durdurma

### Servisleri durdurmak (veriler korunur):
```bash
docker-compose down
```

### Servisleri durdurmak ve verileri silmek:
```bash
docker-compose down -v
```

## 🔄 Servisleri Yeniden Başlatma

```bash
docker-compose restart
```

## 🗄️ Veritabanına Doğrudan Bağlanma

Veritabanına doğrudan bağlanmak için:

```bash
docker-compose exec postgres psql -U rehome_user -d rehome_db
```

SQL komutlarını çalıştırabilirsiniz:
```sql
-- Kullanıcıları listele
SELECT * FROM users;

-- Eşyaları listele
SELECT * FROM items;

-- Çıkış
\q
```

## 🐛 Sorun Giderme

### Problem: Port zaten kullanılıyor

**Çözüm:** `docker-compose.yml` dosyasındaki port numaralarını değiştirin:
```yaml
ports:
  - "8001:8000"  # Backend için farklı port
  - "5433:5432"  # PostgreSQL için farklı port
```

### Problem: Backend başlamıyor

**Çözüm:**
1. Logları kontrol edin: `docker-compose logs backend`
2. Container'ı yeniden başlatın: `docker-compose restart backend`
3. Container'ı sıfırlayın: `docker-compose down && docker-compose up -d`

### Problem: Veritabanı bağlantı hatası

**Çözüm:**
1. PostgreSQL'in çalıştığını kontrol edin: `docker-compose ps`
2. PostgreSQL loglarını kontrol edin: `docker-compose logs postgres`
3. Servisleri yeniden başlatın: `docker-compose restart`

### Problem: init_db.py çalışmıyor

**Çözüm:**
1. Backend container'ının çalıştığından emin olun: `docker-compose ps`
2. Manuel olarak çalıştırın: `docker-compose exec backend python init_db.py`
3. Hata mesajlarını kontrol edin

## 📊 Veritabanı Şeması

Backend aşağıdaki tabloları içerir:

- **users**: Kullanıcı bilgileri
- **items**: Bağışlanan eşyalar
- **youth_centers**: Gençlik merkezleri
- **donations**: Bağış kayıtları
- **received_items**: Alınan eşyalar
- **points_history**: Puan geçmişi
- **coupons**: Kuponlar
- **messages**: Mesajlar
- **co2_savings**: CO2 tasarrufu kayıtları

## 🔐 Güvenlik Notları

⚠️ **Önemli:** Production ortamında:

1. `docker-compose.yml` dosyasındaki `SECRET_KEY`'i değiştirin
2. Veritabanı şifrelerini güçlendirin
3. CORS ayarlarını frontend URL'inize göre sınırlandırın
4. HTTPS kullanın

## 📞 Yardım

Sorun yaşarsanız:

1. Logları kontrol edin: `docker-compose logs`
2. Container durumunu kontrol edin: `docker-compose ps`
3. Docker Desktop'ta container'ların çalıştığını kontrol edin

## ✅ Başarı Kontrol Listesi

Kurulumun başarılı olduğunu kontrol etmek için:

- [ ] Docker Desktop çalışıyor
- [ ] `docker-compose ps` komutu 2 servis gösteriyor (postgres ve backend)
- [ ] http://localhost:8000/docs sayfası açılıyor
- [ ] `init_db.py` hatasız çalıştı
- [ ] API dokümantasyonunda endpoint'ler görünüyor
- [ ] Kayıt ve giriş işlemleri çalışıyor

Tüm maddeleri işaretlediyseniz, backend'iniz hazır! 🎉

