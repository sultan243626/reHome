# 🧪 Test Adımları - ReHome Uygulaması

## ✅ Mevcut Durum

1. ✅ **Backend çalışıyor** - http://localhost:8000/api endpoint'i çalışıyor
2. ✅ **Python HTTP sunucusu çalışıyor** - Port 3000'de (bu normal, "freeze" değil!)
3. ⏳ **Veritabanı kontrol edilmeli**
4. ⏳ **Frontend test edilmeli**

## 📋 Adım Adım Test

### 1. Veritabanını Kontrol Et

**Yeni bir PowerShell penceresi açın** (mevcut Python sunucusunu kapatmayın!) ve şu komutu çalıştırın:

```powershell
cd C:\Users\topsu\OneDrive\Masaüstü\kodluyoruzz
docker-compose exec backend python init_db.py
```

**Beklenen çıktı:**
```
Database already initialized. All data exists.
```
veya
```
Database initialized successfully!
  - Added X youth centers
  - Added X users
```

### 2. Veritabanı Verilerini Kontrol Et

Backend'in veritabanına bağlanabildiğini test edin:

**Tarayıcıda şu adrese gidin:**
- http://localhost:8000/api/youth-centers

**Beklenen çıktı:** Gençlik merkezlerinin listesi (JSON formatında)

**Örnek kullanıcı ile test:**
- http://localhost:8000/api/auth/login endpoint'ini test edin (Swagger UI'dan: http://localhost:8000/docs)

### 3. Frontend'i Test Et

**Python sunucusu zaten çalışıyor!** (Port 3000'de)

**Tarayıcıda şu adrese gidin:**
- http://localhost:3000/1iindex.html
- veya http://localhost:3000 (ana sayfa)

### 4. Test Senaryoları

#### Senaryo 1: Kayıt Olma
1. http://localhost:3000/1iindex.html adresine gidin
2. "Kayıt Ol" butonuna tıklayın
3. Formu doldurun:
   - Ad Soyad: Test Kullanıcı
   - Telefon: 0555 123 45 67
   - E-mail: test@example.com
   - Adres: Test Adres
   - Şifre: test123 (en az 6 karakter)
4. "Kayıt Ol" butonuna tıklayın
5. ✅ Başarılı mesajı görmelisiniz

#### Senaryo 2: Giriş Yapma
1. Ana sayfada "Giriş Yap" butonuna tıklayın
2. Test kullanıcısı ile giriş yapın:
   - E-mail: `ahmet@example.com`
   - Şifre: `password123`
3. ✅ Başarılı girişte profil sayfasına yönlendirileceksiniz

#### Senaryo 3: Bağış Yapma
1. Giriş yaptıktan sonra "Bağış Yap" sayfasına gidin
2. "Bağış Yap" butonuna tıklayın
3. Formu doldurun:
   - Gençlik Merkezi: Bir merkez seçin
   - Eşya Kategorisi: Mobilya
   - Eşya Türü: Masa
   - Durumu: İyi
   - Konum: Konya
   - Açıklama: Test bağışı
4. "Bağışı Tamamla" butonuna tıklayın
5. ✅ Başarılı mesajı ve puan bilgisi görmelisiniz

## 🔍 Sorun Giderme

### Problem: Python sunucusu "freeze" gibi görünüyor

**Çözüm:** Bu normal! Python HTTP sunucusu çalışırken terminal "donmuş" gibi görünür. Bu, sunucunun çalıştığı anlamına gelir. 

**Kontrol etmek için:**
- Tarayıcıda http://localhost:3000 adresine gidin
- Sayfa yükleniyorsa sunucu çalışıyor demektir

**Durdurmak için:**
- Terminal'de `Ctrl + C` tuşlarına basın

### Problem: Veritabanı boş görünüyor

**Çözüm:**
```powershell
docker-compose exec backend python init_db.py
```

### Problem: Frontend'den API'ye istek atılamıyor

**Kontrol listesi:**
1. ✅ Backend çalışıyor mu? (http://localhost:8000/docs)
2. ✅ Frontend bir web sunucusu üzerinden mi çalışıyor? (http://localhost:3000)
3. ✅ Tarayıcı konsolunda (F12) hata var mı?
4. ✅ Network sekmesinde API istekleri görünüyor mu?

### Problem: CORS hatası

**Çözüm:** Frontend'i mutlaka bir web sunucusu üzerinden çalıştırın. HTML dosyasını doğrudan açmayın.

## 📊 Test Kontrol Listesi

- [ ] Backend çalışıyor (http://localhost:8000/api)
- [ ] Veritabanı başlatıldı (`init_db.py` çalıştırıldı)
- [ ] Python HTTP sunucusu çalışıyor (port 3000)
- [ ] Frontend açılıyor (http://localhost:3000)
- [ ] Kayıt olma çalışıyor
- [ ] Giriş yapma çalışıyor
- [ ] Bağış yapma çalışıyor
- [ ] Token localStorage'da saklanıyor

## 🎯 Hızlı Test

**PowerShell'de (yeni pencere):**
```powershell
# 1. Veritabanını kontrol et
cd C:\Users\topsu\OneDrive\Masaüstü\kodluyoruzz
docker-compose exec backend python init_db.py

# 2. Backend'i test et (tarayıcıda)
# http://localhost:8000/api/youth-centers

# 3. Frontend'i test et (tarayıcıda)
# http://localhost:3000/1iindex.html
```

**Tarayıcıda:**
1. http://localhost:3000/1iindex.html - Ana sayfa
2. http://localhost:8000/docs - API dokümantasyonu
3. http://localhost:8000/api/youth-centers - Gençlik merkezleri listesi

## ✅ Başarı Kriterleri

Tüm testler başarılıysa:
- ✅ Backend API'leri çalışıyor
- ✅ Veritabanı hazır ve veriler yüklü
- ✅ Frontend backend'e bağlanabiliyor
- ✅ Kayıt, giriş ve bağış işlemleri çalışıyor

**Tebrikler! Uygulamanız hazır! 🎉**

