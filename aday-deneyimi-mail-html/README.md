# Aday Deneyimi Projesi — Mail İçerikleri (HTML)

Bu klasör, `Aday_Deneyim_Projesi__Mail_I_c_erikleri.pdf` dosyasındaki 19 sayfanın
Türk Telekom marka diline (lacivert zemin, turkuaz vurgu) sadık, **düzenlenebilir
HTML e‑posta** karşılıklarını içerir.

## İçerik

| # | Dosya | İçerik |
|---|-------|--------|
| 01 | `01-sourcing-inmail.html` | Adaya ilk temas / InMail |
| 02 | `02-online-mulakat-daveti.html` | Online (Zoom) mülakat daveti |
| 03 | `03-yuzyuze-mulakat-daveti.html` | Yüz yüze mülakat daveti |
| 04 | `04-mulakat-sonrasi-bilgilendirme.html` | Mülakat sonrası teşekkür / süreç devam ediyor |
| 05 | `05-adaya-ulasamadik.html` | Adaya ulaşılamadı, geri dönüş talebi |
| 06 | `06-yoneticiye-online-mulakat.html` | Yöneticiye online mülakat bilgilendirmesi |
| 07 | `07-yoneticiye-yuzyuze-mulakat.html` | Yöneticiye yüz yüze mülakat bilgilendirmesi |
| 08 | `08-olumsuz-sonuc.html` | Olumsuz sonuç / red maili |
| 09 | `09-vaka-calismasi.html` | Vaka çalışması daveti |
| 10 | `10-referans-kontrolu.html` | Referans bilgisi talebi (2 referans formu) |
| 11 | `11-is-teklifi.html` | İş teklifi bildirimi |
| 12 | `12-sozlesme-elden-teslim.html` | Sözleşme — elden teslim (3 lokasyon adresi) |
| 13 | `13-sozlesme-kargo.html` | Sözleşme — kargo ile gönderim |
| 14 | `14-ise-baslangic-evrak-takvimi.html` | İşe başlangıç tarihleri + evrak notları |
| 15 | `15-evrak-teslim-ankara-elden.html` | Evrak teslimi — Ankara, elden (17. kat) |
| 16 | `16-evrak-teslim-ankara-kargo.html` | Evrak teslimi — Ankara, muhaberat |
| 17 | `17-evrak-teslim-istanbul-elden.html` | Evrak teslimi — İstanbul, elden (10. kat) |
| 18 | `18-evrak-teslim-istanbul-kargo.html` | Evrak teslimi — İstanbul, muhaberat |
| 19 | `19-adaya-ulasamadik-variant.html` | 05 ile aynı içeriğin PDF'teki ikinci varyasyonu |

`index.html` dosyası tüm şablonları tek bir listede gösterir (tarayıcıda önizleme içindir,
e‑posta olarak gönderilmez).

## Nasıl kullanılır

1. İlgili `.html` dosyasını tarayıcıda açıp önizleyin.
2. **Sarı vurgulu alanlar** (`X Bey/Hanım`, tarih/saat, pozisyon adı, XXX vb.) her
   gönderimde doldurulması/değiştirilmesi gereken yer tutuculardır — kaynak `.html`
   dosyasını bir metin editörüyle açıp bu alanları güncelleyin.
3. Dosyanın tamamını (Ctrl+A) seçip doğrudan Outlook/Gmail gibi bir e‑posta
   istemcisinin HTML gövdesine yapıştırabilir, ya da dosyayı bir e‑posta gönderim
   aracına (ESP) HTML şablon olarak yükleyebilirsiniz.
4. **Önemli:** Bazı e‑posta istemcileri (özellikle masaüstü Outlook) `<style>`
   bloğundaki CSS'i tam desteklemez. Üretim ortamında göndermeden önce şablonu bir
   "CSS inliner" (örn. Premailer, ya da kullandığınız ESP'nin otomatik inline
   özelliği) üzerinden geçirmeniz, görünümün tüm istemcilerde tutarlı olmasını
   sağlar. Modern istemcilerde (Gmail web/mobil, Apple Mail, Outlook web) mevcut
   haliyle sorunsuz görüntülenir.
5. Marka logosu burada basit bir metin/CSS rozeti olarak temsil edilmiştir; gerçek
   Türk Telekom logo görselini eklemek isterseniz `.logo-cell` bloğunu bir
   `<img>` etiketiyle değiştirebilirsiniz.

## Yeniden üretmek isterseniz

İçerik `generate.py` içinde veri olarak tanımlıdır (her sayfa için başlık, paragraf,
kutu, tablo vb. bloklar). Metni güncelleyip

```bash
python3 generate.py
```

çalıştırarak tüm HTML dosyalarını yeniden üretebilirsiniz.

---
Kaynak: `Aday_Deneyim_Projesi__Mail_I_c_erikleri.pdf` (19 sayfa).
