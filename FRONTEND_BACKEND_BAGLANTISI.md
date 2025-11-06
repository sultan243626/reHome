# ✅ Frontend ve Backend Bağlantısı Tamamlandı!

## 🎉 Yapılan Değişiklikler

### Backend
1. ✅ `/api` endpoint'i eklendi - artık http://localhost:8000/api çalışıyor
2. ✅ Tüm API endpoint'leri hazır ve çalışıyor

### Frontend
1. ✅ **1iindex.html** - Kayıt ve giriş fonksiyonları backend'e bağlandı
2. ✅ **3Bagis.html** - Bağış yapma fonksiyonu backend'e bağlandı
3. ✅ API URL'leri güncellendi: `http://localhost:8000/api`
4. ✅ Token yönetimi eklendi (localStorage)
5. ✅ Gençlik merkezleri backend'den dinamik olarak yükleniyor

## 🚀 Nasıl Kullanılır?

### 1. Backend'in Çalıştığını Kontrol Edin

Tarayıcıda şu adreslere gidin:
- http://localhost:8000/api ✅ (Artık çalışıyor!)
- http://localhost:8000/docs ✅

### 2. Frontend'i Bir Web Sunucusu Üzerinden Çalıştırın

**Önemli:** HTML dosyalarını doğrudan açmak yerine bir web sunucusu kullanın!

**Seçenek 1: Python ile (Önerilen)**
```powershell
cd frontend
python -m http.server 3000
```
Sonra tarayıcıda: http://localhost:3000

**Seçenek 2: VS Code Live Server**
- VS Code'da frontend klasörünü açın
- Live Server extension'ını yükleyin
- HTML dosyasına sağ tıklayıp "Open with Live Server" seçin

**Seçenek 3: Node.js ile**
```powershell
cd frontend
npx serve
```

### 3. Test Edin

1. **Ana Sayfa (1iindex.html)**:
   - "Kayıt Ol" butonuna tıklayın
   - Formu doldurup kayıt olun
   - "Giriş Yap" butonuna tıklayın
   - Email ve şifre ile giriş yapın
   - Başarılı girişte profil sayfasına yönlendirileceksiniz

2. **Bağış Sayfası (3Bagis.html)**:
   - Giriş yaptıktan sonra "Bağış Yap" sayfasına gidin
   - Formu doldurun
   - "Bağışı Tamamla" butonuna tıklayın
   - Bağış başarıyla kaydedilecek ve puan kazanacaksınız!

## 📋 API Endpoint'leri

### Authentication
- `POST /api/auth/register` - Kullanıcı kaydı
- `POST /api/auth/login` - Kullanıcı girişi
- `GET /api/auth/me` - Mevcut kullanıcı bilgileri

### Items
- `POST /api/items` - Yeni eşya/bağış oluştur (Token gerekli)
- `GET /api/items` - Eşyaları listele

### Youth Centers
- `GET /api/youth-centers` - Gençlik merkezlerini listele
- `GET /api/youth-centers?city=Konya` - Şehre göre filtrele

## 🔐 Authentication Akışı

1. Kullanıcı kayıt olur → `POST /api/auth/register`
2. Kullanıcı giriş yapar → `POST /api/auth/login`
3. Backend token döner → Token `localStorage`'a kaydedilir
4. Sonraki isteklerde token header'da gönderilir:
   ```
   Authorization: Bearer <token>
   ```

## ⚠️ Önemli Notlar

1. **CORS:** Backend CORS ayarları tüm origin'lere açık. Production'da frontend URL'inizi belirtin.

2. **Token:** Token localStorage'da saklanıyor. Tarayıcıyı kapatıp açtığınızda token hala orada olacak.

3. **Gençlik Merkezleri:** Bağış formu açıldığında gençlik merkezleri backend'den otomatik yüklenir.

4. **Hata Yönetimi:** Tüm API çağrılarında hata mesajları kullanıcıya gösterilir.

## 🧪 Test Kullanıcısı

Veritabanında örnek bir kullanıcı var:
- **Email:** ahmet@example.com
- **Şifre:** password123

Bu kullanıcı ile giriş yapabilirsiniz.

## 📝 Sonraki Adımlar

Frontend ve backend artık birleştirildi! Şimdi yapabilecekleriniz:

1. ✅ Kayıt olma ve giriş yapma
2. ✅ Bağış yapma
3. ⏳ Profil sayfasını backend'e bağlama (5profilim.html)
4. ⏳ Eşya arama sayfasını backend'e bağlama (4esyaara.html)
5. ⏳ Gençlik merkezleri haritasını backend'e bağlama (2Genclik.html)

## 🐛 Sorun Giderme

### Problem: "CORS hatası" alıyorum
**Çözüm:** Frontend'i bir web sunucusu üzerinden çalıştırın (doğrudan HTML açmayın)

### Problem: "Token bulunamadı" hatası
**Çözüm:** Önce giriş yapmanız gerekiyor. Ana sayfadan giriş yapın.

### Problem: "Backend çalışıyor mu?" hatası
**Çözüm:** 
1. Backend'in çalıştığını kontrol edin: http://localhost:8000/docs
2. Docker container'ların çalıştığını kontrol edin: `docker-compose ps`

### Problem: Gençlik merkezleri yüklenmiyor
**Çözüm:** 
1. Backend'in çalıştığını kontrol edin
2. Tarayıcı konsolunu açın (F12) ve hataları kontrol edin
3. Network sekmesinde API isteğinin başarılı olup olmadığını kontrol edin

## ✅ Başarı Kontrol Listesi

- [x] Backend çalışıyor (http://localhost:8000/docs)
- [x] `/api` endpoint'i çalışıyor
- [x] Frontend kayıt olma backend'e bağlı
- [x] Frontend giriş yapma backend'e bağlı
- [x] Frontend bağış yapma backend'e bağlı
- [x] Token yönetimi çalışıyor
- [x] Gençlik merkezleri dinamik yükleniyor

**Tebrikler! Frontend ve backend başarıyla birleştirildi! 🎉**

