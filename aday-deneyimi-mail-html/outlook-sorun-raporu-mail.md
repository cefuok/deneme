# Gönderime hazır mail metni

**Konu:** Aday Deneyimi mail şablonları — Outlook gönderiminde yaşanan sorunlar ve çözüm önerileri

---

Merhaba,

Aday Deneyimi Projesi kapsamında hazırladığımız 19 mail şablonunu, özellikle **Outlook
üzerinden gönderim** tarafında yaşadığımız sorunlar açısından baştan sona inceledim.
Aşağıda hem sorunun teknik nedenini hem de önümüzdeki üç çözüm seçeneğini ve önerimi
paylaşıyorum.

## 1. Sorunun kaynağı

Windows masaüstü Outlook, HTML maili tarayıcı motoruyla değil **Word'ün render
motoruyla** çiziyor. Word motoru modern CSS'in büyük bölümünü (gradient, yuvarlak köşe,
`max-width`, medya sorguları, div üzerindeki arka plan/dolgu) ya yok sayıyor ya da farklı
yorumluyor. Şablonlarımız ise tasarımı tek bir `<style>` bloğuna ve `<div>` yapısına
dayandırıyor. Bunun iki sonucu var:

- Maili Outlook'un yazma penceresine **kopyala-yapıştır** yaptığımızda `<style>` bloğu
  korunmuyor; tasarımın tamamı gidiyor, mail düz beyaz zemin + siyah metne dönüyor.
- Korunduğu durumlarda bile lacivert zemin paragraf boşluklarının arkasına basılmıyor;
  paragraf aralarında **beyaz şeritler** çıkıyor. Hâlihazırda gördüğümüz sorun tam olarak bu.

Şu an 22 şablon dosyasından yalnızca **3'ü** Outlook'a uygun yapıda:
`07-yoneticiye-yuzyuze-mulakat-outlook.html`, `10-referans-kontrolu-tasarim.html` ve
`14-ise-baslangic-evrak-takvimi-tasarim.html`. Kalan **19 dosya** eski yapıda ve Outlook'ta
bozuk görünecek.

## 2. Tespit edilen sorunlar

**Outlook render sorunları (19 dosyanın tamamında)**

1. **Inline stil yok, her şey `<style>` bloğunda.** Yapıştırma ile gönderimde tasarım sıfırlanıyor.
2. **Arka plan `<div>` üzerinde.** Word motoru div arka planını paragraf marjlarının arkasına
   basmadığı için paragraf aralarında beyaz şeritler oluşuyor.
3. **`linear-gradient` zemin, düz renk yedeği olmadan.** Outlook gradient'i desteklemiyor;
   altında `background-color` olmadığı için zemin komple beyaz kalıyor.
4. **`max-width:640px`.** Outlook bunu uygulamıyor; geniş ekranda mail tüm pencere genişliğine
   yayılıyor. Outlook'a özel (mso koşullu) 640 px'lik sabit tablo gerekiyor.
5. **`border-radius` (dosya başına ~6 kullanım).** Turkuaz çerçeveli kutular ve beyaz tarih
   "pill"leri köşeli çıkıyor.
6. **9 adımlı "İşe Alım Süreçleri" şeridi.** 17 hücreli, yüzde genişlikli bir tablo; Outlook
   yüzde genişlikleri ve `@media` kurallarını yok sayıyor, adım yazıları üst üste biniyor ve
   okunmaz hâle geliyor. Tasarım sürümlerinde bu şerit tek bir görsele (`mail-2-surec.png`)
   çevrildi — doğru çözüm bu.
7. **Emoji'ler doğrudan karakter olarak gömülü** (11 dosyada 3–7 adet: 📅 🕑 📍 ✉ ☎ …).
   Outlook'ta kullanılan fonta göre siyah-beyaz glif ya da boş kutu olarak çıkıyor. HTML
   entity + `Segoe UI Emoji` font zinciri gerekiyor.
8. **Oransal satır yüksekliği (`line-height:1.65`).** Word motoru farklı yorumluyor, satırlar
   sıkışıyor. Sabit px + `mso-line-height-rule:exactly` gerekiyor.
9. **Outlook karanlık mod.** Koyu lacivert zemin + beyaz metin kombinasyonunda Outlook renkleri
   zorla ters çevirebiliyor; okunamaz kontrast riski var, test edilmesi gerekiyor.

**Görsel ve içerik riskleri**

10. **Dış görsel bağımlılığı.** Tasarım sürümleri 5 görseli
    `https://turktelekomkariyer.com.tr/assets/mailing/20260929/` altından çağırıyor. (a) Bu
    dosyaların gerçekten o yola yüklenmesi gerekiyor, aksi hâlde kırık görsel çıkar. (b) Outlook
    dış görselleri varsayılan olarak indirmiyor; alıcı "görselleri indir" demeden süreç diyagramı
    ve logo boş görünüyor. Görselleri maile gömmek (CID) bu sorunu tamamen ortadan kaldırır.
11. **İç referans alt notu.** 20 dosyanın hepsinde "Sayfa X/19 · Aday Deneyimi Projesi — Mail
    İçerikleri" satırı duruyor. Gerçek gönderim öncesi mutlaka kaldırılmalı.
12. **Referans formu alanları.** `10-referans-kontrolu` içindeki alt çizgili boşluklar mail
    içinde doldurulamıyor; adayın doldurabileceği bir form linki daha doğru olur.
13. **Yer tutucu doldurma süreci.** Sarı vurgulu alanlar ("X Bey/Hanım", "01.01.2026",
    "XXX Pozisyonu") HTML kaynağından elle değiştiriliyor. Yapıştırma sonrası sarı vurgu da
    kaybolduğu için doldurulmamış bir alanın adaya gitme riski yüksek.
14. **Düz metin alternatifi yok.** Kopyala-yapıştır yöntemiyle üretilmesi de mümkün değil;
    spam skoru ve erişilebilirlik açısından eksik kalıyor.

## 3. Çözüm seçenekleri

### Seçenek A — Hazır Outlook şablonu / .eml dosyaları
Her mail için Outlook'ta çift tıklayarak açılan hazır bir şablon dosyası (`.oft` veya `.eml`)
üretiriz. Mail gövdesi Outlook'un yazma penceresine yapıştırılmadığı, doğrudan içeri alındığı
için tasarım bozulmaz; görseller dosyanın içine gömülü geldiği için "görselleri indir" sorunu
da ortadan kalkar.
*Artısı:* hızlı, entegrasyon/IT onayı gerektirmez, ekip alışık olduğu Outlook akışında kalır.
*Eksisi:* yer tutucular yine elle dolduruluyor; 19 dosyanın sürüm yönetimi gerekiyor.

### Seçenek B — 19 şablonu Outlook uyumlu yapıya çevirmek
`07-yoneticiye-yuzyuze-mulakat-outlook.html` dosyasında uyguladığımız deseni (tüm stiller
inline, arka plan tablo hücrelerinde, marj yerine hücre dolgusu, sabit satır yüksekliği, mso
koşullu 640 px sarmalayıcı, entity emoji) kalan 19 şablona da uygularız.
*Artısı:* hangi yöntemle gönderilirse gönderilsin tasarım korunur.
*Not:* bu, A ve C seçeneklerinin de önkoşulu — her hâlükârda yapılması gereken temel iş.

### Seçenek C — HTML şablon + otomatik gönderim sistemi
Şablonlar tek yerde dururken yer tutucular değişken hâline gelir (aday adı, pozisyon, tarih,
saat, link) ve gönderim SMTP ya da Microsoft Graph üzerinden otomatik yapılır; tek tek veya
listeden toplu.
*Artısı:* Outlook'un yazma penceresi hiç devreye girmediği için tasarım %100 korunur, yer
tutucu hatası sıfıra iner, görseller gömülü gider, düz metin alternatifi otomatik üretilir,
gönderim kaydı tutulur.
*Eksisi:* IT ve Bilgi Güvenliği onayı, gönderim yetkisi (SMTP hesabı ya da Graph `Mail.Send`
izni), KVKK tarafında aday verisinin işlenmesi başlıkları ve küçük bir geliştirme/bakım eforu.

## 4. Önerim

1. **Hemen:** B — 19 şablonu Outlook uyumlu yapıya çevirmek. Deseni zaten doğruladık, tekrar
   eden bir iş; ayrıca "Sayfa X/19" alt notunu ve dış görsel bağımlılığını da bu turda temizleriz.
2. **Kısa vade:** A — ekibe hazır şablon paketi (.oft/.eml) vererek sahada hemen kullanıma
   açmak. Mevcut akışı değiştirmediği için adaptasyon maliyeti yok.
3. **Orta vade:** C — otomatik gönderim. Yer tutucu hatası ve render riskini kalıcı olarak
   bitiren tek seçenek bu; onay süreçleri paralelde başlatılabilir.

## 5. Netleştirmemiz gerekenler

- Ekipte kullanılan Outlook sürümü hangisi: **klasik Windows Outlook**, **yeni Outlook**,
  **Outlook Web (OWA)** veya **Mac Outlook**? Render davranışları birbirinden farklı; yeni
  Outlook ve OWA modern CSS'i büyük ölçüde destekliyor, asıl kısıt klasik masaüstü sürümünde.
- Mail görselleri hangi adresten yayınlanacak (onaylı bir URL/CDN) — yoksa görselleri maile
  gömerek ilerleyelim mi?
- Seçenek C için gönderim yetkisi (SMTP hesabı / Graph izni) talebini kiminle başlatmamız gerekiyor?

Görüşlerinizi ve hangi seçenekle ilerlemek istediğinizi paylaşırsanız, B maddesini hemen
başlatabilirim.

Teşekkürler,
