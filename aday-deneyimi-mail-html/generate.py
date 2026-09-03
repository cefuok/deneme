#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Turk Telekom Aday Deneyimi - Mail Icerikleri
PDF -> Editable HTML e-mail templates generator
"""
import os, re, html

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------- helpers ----------

def ph(text):
    """Turn [[...]] markers into editable-placeholder spans, escape the rest."""
    parts = re.split(r'(\[\[.*?\]\])', text)
    out = []
    for part in parts:
        m = re.match(r'^\[\[(.*)\]\]$', part)
        if m:
            out.append(f'<span class="ph">{html.escape(m.group(1))}</span>')
        else:
            # allow **bold** via **text**, and \n as a manual line break
            seg = html.escape(part)
            seg = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', seg)
            seg = seg.replace('\n', '<br>')
            out.append(seg)
    return ''.join(out)

def plain(text):
    """Strip [[ ]] and ** markers, for use in <title> / index listings."""
    text = re.sub(r'\[\[(.*?)\]\]', r'\1', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    return text

def para(text):
    return f'<p class="p">{ph(text)}</p>'

def block_greeting(text):
    return f'<p class="greeting">{ph(text)}</p>'

def block_detail_box(items, title=None):
    rows = []
    for icon, label, value in items:
        rows.append(
            f'<tr><td class="detail-icon">{icon}</td>'
            f'<td class="detail-text"><strong>{html.escape(label)}:</strong> {ph(value)}</td></tr>'
        )
    title_html = f'<p class="box-title">{html.escape(title)}</p>' if title else ''
    return (
        '<div class="box">' + title_html +
        '<table role="presentation" class="detail-table" cellpadding="0" cellspacing="0">' +
        ''.join(rows) + '</table></div>'
    )

def block_notes_box(items, title):
    lis = ''.join(f'<li>{ph(i)}</li>' for i in items)
    return (
        f'<div class="box"><p class="box-title">📝 {html.escape(title)}</p>'
        f'<ul class="notes">{lis}</ul></div>'
    )

def block_table_box(header, rows, title=None):
    title_html = f'<p class="box-title">{html.escape(title)}</p>' if title else ''
    head = f'<tr><th>{html.escape(header[0])}</th><th></th><th>{html.escape(header[1])}</th></tr>'
    body = ''.join(
        f'<tr><td class="pill">{ph(a)}</td><td class="sep">┊</td><td class="pill">{ph(b)}</td></tr>'
        for a, b in rows
    )
    return (
        f'<div class="box">{title_html}'
        f'<table role="presentation" class="date-table" cellpadding="0" cellspacing="0">{head}{body}</table></div>'
    )

def block_address_list(items):
    blocks = []
    for it in items:
        blocks.append(
            '<div class="addr">'
            f'<p class="addr-title">📍 <strong>{html.escape(it["title"])}</strong></p>'
            f'<p class="addr-lines">{"<br>".join(html.escape(l) for l in it["lines"])}</p>'
            '</div>'
        )
    return '<div class="box">' + ''.join(blocks) + '</div>'

def block_contact_box(name, phone, email, address_lines):
    contact_line = f'☎ {html.escape(phone)} &nbsp;·&nbsp; ✉ <a class="a-link" href="mailto:{email}">{html.escape(email)}</a>' if (phone or email) else ''
    return (
        '<div class="box">'
        f'<p class="p"><strong>👤 {html.escape(name)}</strong>'
        + (f'<br>{contact_line}' if contact_line else '') + '</p>'
        f'<p class="p">📍 {"<br>".join(html.escape(l) for l in address_lines)}</p>'
        '</div>'
    )

def block_referee_pairs(n=2):
    one = (
        '<table role="presentation" class="ref-table" cellpadding="0" cellspacing="0">'
        '<colgroup><col style="width:46%"><col style="width:54%"></colgroup>'
        '<tr><td class="ref-label">Referans Veren Kişinin Adı Soyadı</td>'
        '<td class="ref-input">&nbsp;</td></tr>'
        '<tr><td class="ref-label">Şirketi ve Pozisyonu</td>'
        '<td class="ref-input">&nbsp;</td></tr>'
        '<tr><td class="ref-label">Telefon Numarası</td>'
        '<td class="ref-input">&nbsp;</td></tr>'
        '</table>'
    )
    return '<div class="box">' + (one + '<div class="ref-gap"></div>') * n + '</div>'

def block_link_button(url, label=None):
    label = label or url
    return f'<p class="cta-wrap"><a class="cta" href="{html.escape(url)}">{html.escape(label)}</a></p>'

PROCESS_STEPS = [
    "Genel Yetenek ve İngilizce Testi",
    "Kişilik Envanteri",
    "İnsan Kaynakları Mülakatı",
    "İş Birimi Mülakatı",
    "Vaka Çalışması*",
    "Referans Kontrolü",
    "İş Teklifi Hazırlıkları",
    "İş Teklifi",
    "İşe Başlama Hazırlıkları",
]

def block_process_bar():
    items = ''.join(
        f'<td class="step"><div class="step-num">{i+1}</div>'
        f'<div class="step-label">{html.escape(s)}</div></td>'
        + ('<td class="step-arrow">&#8594;</td>' if i < len(PROCESS_STEPS) - 1 else '')
        for i, s in enumerate(PROCESS_STEPS)
    )
    return (
        '<div class="process">'
        '<p class="box-title">İşe Alım Süreçleri</p>'
        '<table role="presentation" class="process-table" cellpadding="0" cellspacing="0"><tr>'
        + items + '</tr></table>'
        '<p class="footnote">*İşe alım sürecimizde, stratejik öncelik durumuna göre bazı adımlar '
        'eş zamanlı yürütülebilir veya adımların sırası değiştirilebilir.</p>'
        '</div>'
    )

def block_signature(lines):
    return '<p class="sig">' + '<br>'.join(html.escape(l) for l in lines) + '</p>'

def block_social():
    return (
        '<div class="social">'
        '<p class="p">Türk Telekom’u daha yakından tanımak için sosyal medya hesaplarımızdan bizi takip edebilirsiniz.</p>'
        '<p class="p">'
        '🔗 <a class="a-link" href="https://www.linkedin.com/company/turktelekom">/turktelekom</a><br>'
        '📷 <a class="a-link" href="https://www.instagram.com/turktelekomkariyer">/turktelekomkariyer</a><br>'
        '🌐 <a class="a-link" href="https://turktelekomkariyer.com.tr">turktelekomkariyer.com.tr</a>'
        '</p></div>'
    )

def block_logo_header():
    return (
        '<table role="presentation" class="header" cellpadding="0" cellspacing="0" width="100%">'
        '<tr><td class="logo-cell">'
        '<span class="logo-mark">&#9654;&#9654;</span>'
        '<span class="logo-text">Türk Telekom</span>'
        '<div class="logo-tag">Değerli Hissettirir</div>'
        '</td></tr></table>'
    )

CSS = """
    body{margin:0;padding:0;background:#060733;font-family:'Segoe UI',Arial,Helvetica,sans-serif;}
    .wrapper{max-width:640px;margin:0 auto;background:linear-gradient(160deg,#0a0c4d 0%,#141877 100%);padding:36px 28px 28px;}
    .header{margin-bottom:22px;}
    .logo-cell{text-align:right;color:#ffffff;}
    .logo-mark{color:#ff5a3c;font-size:14px;letter-spacing:-2px;margin-right:6px;}
    .logo-text{font-size:20px;font-weight:700;color:#ffffff;}
    .logo-tag{font-size:10px;color:#bfc3f0;letter-spacing:.5px;margin-top:-2px;}
    .box{border:2px solid #2ce0cf;border-radius:22px;padding:22px 26px;margin:0 0 20px 0;}
    .greeting{color:#ffffff;font-size:18px;font-weight:700;margin:0 0 14px;}
    .p{color:#dfe1fb;font-size:14.5px;line-height:1.65;margin:0 0 14px;}
    .box-title{color:#2ce0cf;font-size:16px;font-weight:700;margin:0 0 14px;}
    .detail-table{width:100%;}
    .detail-icon{width:30px;color:#2ce0cf;font-size:16px;vertical-align:top;padding:4px 8px 4px 0;}
    .detail-text{color:#eef0ff;font-size:14.5px;line-height:1.6;padding:4px 0;}
    .detail-text strong{color:#2ce0cf;}
    .notes{margin:0;padding-left:18px;color:#dfe1fb;font-size:14px;line-height:1.7;}
    .notes li{margin-bottom:8px;}
    .date-table{width:100%;border-collapse:separate;border-spacing:0 10px;}
    .date-table th{color:#9ea3e8;font-size:12px;text-transform:uppercase;letter-spacing:.4px;text-align:center;padding-bottom:6px;}
    .pill{background:#ffffff;color:#101266;text-align:center;font-weight:700;font-size:14px;border-radius:20px;padding:10px 14px;}
    .sep{color:#2ce0cf;text-align:center;width:20px;}
    .addr{margin-bottom:16px;}
    .addr:last-child{margin-bottom:0;}
    .addr-title{color:#2ce0cf;font-size:14.5px;margin:0 0 4px;}
    .addr-lines{color:#dfe1fb;font-size:14px;line-height:1.5;margin:0;}
    .ref-table{width:100%;margin-bottom:4px;table-layout:fixed;}
    .ref-label{color:#9ea3e8;font-size:13px;padding:0 10px 14px 0;vertical-align:bottom;}
    .ref-input{border-bottom:1px solid #2ce0cf;padding:0 0 14px;}
    .ref-gap{height:18px;}
    .cta-wrap{margin:4px 0 18px;}
    .cta{display:inline-block;border:2px solid #2ce0cf;border-radius:30px;color:#eafffb;
         font-size:14px;font-weight:600;padding:14px 22px;text-decoration:none;word-break:break-all;}
    .process{border-top:1px solid #2a2d80;padding-top:20px;margin-top:6px;}
    .process-table{width:100%;}
    .step{text-align:center;vertical-align:top;padding:0 4px;width:11%;}
    .step-num{width:30px;height:30px;line-height:30px;border-radius:50%;background:#101266;
               border:2px solid #2ce0cf;color:#2ce0cf;font-weight:700;font-size:12px;margin:0 auto 6px;}
    .step-label{color:#c7c9f5;font-size:10.5px;line-height:1.25;}
    .step-arrow{color:#2ce0cf;text-align:center;vertical-align:middle;width:2%;}
    .footnote{color:#7d81c2;font-size:11px;margin:14px 0 0;font-style:italic;}
    .sig{color:#ffffff;font-size:14.5px;line-height:1.6;margin:6px 0 18px;}
    .social{border-top:1px solid #2a2d80;padding-top:16px;margin-top:4px;}
    .a-link{color:#2ce0cf;text-decoration:none;}
    .ph{background:#ffe98a;color:#3a2e00;padding:1px 5px;border-radius:4px;font-weight:600;}
    .footer-bottom{text-align:right;color:#7d81c2;font-size:11px;margin-top:24px;}
    .subject-tag{display:inline-block;background:#12145f;color:#8ee8de;border:1px dashed #2ce0cf;
                  border-radius:8px;padding:6px 12px;font-size:12px;margin-bottom:18px;font-family:Consolas,monospace;}
    @media only screen and (max-width:480px){
      .wrapper{padding:22px 14px;}
      .box{padding:16px 16px;}
      .step{width:33%;display:inline-block;margin-bottom:14px;}
      .step-arrow{display:none;}
      .process-table, .process-table tr, .process-table td{display:block;width:100%;}
    }
"""

def render(page_no, subject, blocks, has_process=False, has_social=False):
    body = block_logo_header()
    body += f'<p class="subject-tag">Konu / Subject: {ph(subject)}</p>'
    for b in blocks:
        body += b
    if has_process:
        body += block_process_bar()
    if has_social:
        body += block_social()
    body += f'<p class="footer-bottom">Sayfa {page_no}/19 · Aday Deneyimi Projesi — Mail İçerikleri</p>'

    return f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(plain(subject))}</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrapper">
{body}
</div>
</body>
</html>
"""

# ---------- content per page ----------

PAGES = []

# Page 1
PAGES.append(dict(
    no=1, file="01-sourcing-inmail.html",
    subject="[[XXX]] Pozisyonu için Sizinle İletişime Geçmek İstiyoruz",
    blocks=[
        block_greeting("Merhaba [[X Bey/Hanım]],"),
        para("Türk Telekom İşe Alım Ekibi’nden size ulaşıyorum. Halihazırda [[XXX]] şirketinde [[XXX]] "
             "pozisyonunda çalıştığınızı görüyorum. Deneyimlerinize uygun olduğunu düşündüğümüz [[XXX]] "
             "pozisyonumuz için sizinle iletişime geçtim."),
        para("İlanımızı incelemek isterseniz, aşağıdaki link üzerinden detaylara ulaşabilirsiniz. "
             "Pozisyonla ilgilenmeniz durumunda özgeçmişinizi tarafımıza iletmenizi rica ederiz."),
        block_link_button("https://www.turktelekomkariyer.com.tr/turk-telekomda-yasam/degerlerimiz/"),
        para("Teşekkür ederiz."),
        para("Görüşmek dileğiyle."),
    ],
))

# Page 2
PAGES.append(dict(
    no=2, file="02-online-mulakat-daveti.html",
    subject="Mülakat Davetiniz — [[XX Pozisyonu]]",
    blocks=[
        block_greeting("Merhaba [[X Bey/Hanım]],"),
        para("Türkiye’nin dijital dönüşüm yolculuğunda bize katılabilmenizin ilk adımı olarak, [[XX]] pozisyonu "
             "için şirketimizle yapacağınız görüşmeye “Join Zoom Meeting / Zoom Toplantısına Katıl” "
             "linkine tıklayarak bağlanabilirsiniz."),
        para("Mülakat öncesinde, teknik bir sorun yaşamamak ve verimli bir mülakat süreci geçirmek için "
             "kullanacağınız cihazın ses ve görüntü kontrollerini yaptığınızdan, internet bağlantınızda "
             "herhangi bir sorun olmadığından emin olunuz."),
        para("Mülakatınıza dair tüm bilgiler aşağıda yer almaktadır. Herhangi bir sorun yaşamanız halinde, "
             "mülakat öncesinde bizimle iletişime geçmenizi rica ederiz."),
        para("Başarılı ve keyifli bir mülakat süreci geçirmenizi dileriz."),
        block_detail_box([
            ("📅", "Mülakat Tarihi", "[[01.01.2026 - Perşembe]]"),
            ("🕑", "Mülakat Saati", "[[10.00]]"),
            ("👤", "Mülakatınızı Gerçekleştirecek Kişi", "[[XX (Unvan)]]"),
        ]),
        block_notes_box([
            "Mülakata katılım sağlamadan önce Türk Telekom kariyer sayfamızdan profil oluşturmanız ve "
            "özgeçmişinizi detaylı bir şekilde doldurmanız gerekmektedir.",
            "https://turktelekomkariyer.com.tr/ linki ile kariyer sayfamıza ulaşabilirsiniz.",
            "Mülakata katılım sağlamadan önce FlowQ üzerinden sizlere iletilen test ve envanterleri "
            "tamamlamanız önem arz etmektedir.",
        ], "Mülakat Öncesinde Hatırlatmalar"),
        block_signature(["Saygılarımızla,", "Türk Telekom İnsan Kaynakları"]),
    ],
    has_process=True, has_social=True,
))

# Page 3
PAGES.append(dict(
    no=3, file="03-yuzyuze-mulakat-daveti.html",
    subject="Yüz Yüze Mülakat Davetiniz — [[XXX Pozisyonu]]",
    blocks=[
        block_greeting("Merhaba [[X Bey/Hanım]],"),
        para("Şirketimize gösterdiğiniz ilgiye teşekkür ederiz. Türkiye’nin dijital dönüşüm yolculuğunda bize "
             "katılabilmenizin bir adımı olarak, [[XXX]] pozisyonu için yüz yüze gerçekleşecek mülakatınızın "
             "detaylarını aşağıda paylaşmak isteriz."),
        block_detail_box([
            ("📅", "Mülakat Tarihi", "[[01.01.2026 - Perşembe]]"),
            ("🕑", "Mülakat Saati", "[[10.00]]"),
            ("👤", "Mülakatınızı Gerçekleştirecek Kişi", "[[Adem Öztürk (İşe Alım Müdürü)]]"),
            ("📍", "Mülakat Adresi", "Türk Telekom Genel Müdürlük - Makam Binası, Gayrettepe Mahallesi, "
                                       "Yıldız Posta Caddesi No:40 Beşiktaş, İstanbul"),
        ]),
        para("Danışmaya geldiğinizde, görüşme yapacağınız kişi bilgisini paylaşmanız halinde, gerekli "
             "yönlendirme yapılacaktır."),
        para("Başarılı ve keyifli bir mülakat süreci geçirmenizi dileriz."),
        block_signature(["Saygılarımızla,", "Türk Telekom İnsan Kaynakları"]),
    ],
    has_process=True, has_social=True,
))

# Page 4
PAGES.append(dict(
    no=4, file="04-mulakat-sonrasi-bilgilendirme.html",
    subject="Mülakatınız için Teşekkür Ederiz",
    blocks=[
        block_greeting("Merhaba [[X Bey/Hanım]],"),
        para("Mülakata katılıp bize vakit ayırdığınız için teşekkür ederiz, sizinle tanışmaktan ve "
             "deneyimlerinizi dinlemekten büyük memnuniyet duyduk."),
        para("Aday değerlendirme sürecimiz devam etmekte olup sonraki aşamalarla ilgili bilgilendirme "
             "en kısa sürede tarafınıza iletilecektir."),
        para("Süreç hakkında herhangi bir sorunuz olursa bizimle her zaman iletişime geçebilirsiniz."),
        para("Teşekkür ederiz."),
        block_signature(["Saygılarımızla,", "Türk Telekom İnsan Kaynakları"]),
    ],
))

# Page 5
PAGES.append(dict(
    no=5, file="05-adaya-ulasamadik.html",
    subject="Sizinle İletişime Geçmek İstiyoruz",
    blocks=[
        block_greeting("Merhaba [[X Bey/Hanım]],"),
        para("Ben Türk Telekom İşe Alım Ekibi’nden [[XXXX]]."),
        para("Şirketimizde ilgilendiğiniz kariyer fırsatı kapsamında sizinle iletişime geçtim; ancak "
             "ulaşamadım. Detayları aktarabilmek ve görüşmeyi planlayabilmek adına, uygun olduğunuz "
             "bir zaman aralığını paylaşabilirseniz, sizinle yeniden iletişime geçmek isterim."),
        para("Teşekkür ederim."),
    ],
))

# Page 6
PAGES.append(dict(
    no=6, file="06-yoneticiye-online-mulakat.html",
    subject="Aday Görüşme Daveti — [[Pozisyon Adı]]",
    blocks=[
        block_greeting("Değerli Yöneticimiz,"),
        para("[[(Pozisyon Adı)]] pozisyonu için adayımız [[(Aday Adı)]] ile gerçekleştireceğiniz "
             "görüşmenizin detaylarını sizinle paylaşmak isteriz."),
        para("Adayımıza ait güncel özgeçmiş ekte yer almaktadır."),
        para("Görüşmeye katılmak için aşağıdaki bağlantıyı kullanabilirsiniz."),
        block_detail_box([
            ("📅", "Mülakat Tarihi", "[[01.01.2026 – Perşembe]]"),
            ("🕑", "Mülakat Saati", "[[10.00]]"),
            ("🌐", "Mülakata Katılım Linki", "[[https://support.zoom.com/hc/tr/article?id=zm_kb&sysparm]]"),
        ]),
        para("Görüşme sonrasında adayla ilgili değerlendirmenizi iletmenizi rica ederiz."),
        para("Teşekkür eder, iyi çalışmalar dileriz."),
    ],
))

# Page 7
PAGES.append(dict(
    no=7, file="07-yoneticiye-yuzyuze-mulakat.html",
    subject="Aday Görüşme Daveti — [[Pozisyon Adı]]",
    blocks=[
        block_greeting("Değerli Yöneticimiz,"),
        para("[[(Pozisyon Adı)]] pozisyonu için adayımız [[(Aday Adı)]] ile gerçekleştireceğiniz "
             "görüşmenizin detaylarını sizinle paylaşmak isteriz."),
        para("Adayımıza ait güncel özgeçmiş ekte yer almaktadır."),
        block_detail_box([
            ("📅", "Mülakat Tarihi", "[[01.01.2026 - Perşembe]]"),
            ("🕑", "Mülakat Saati", "[[10.00]]"),
            ("📍", "Mülakata Katılım Adresi", "Türk Telekom Genel Müdürlük / Kule Bina Kat: 9, "
                                                 "Gayrettepe Mah. Yıldız Posta Caddesi No:40 Beşiktaş, İstanbul"),
        ]),
        para("Görüşme sonrasında adayla ilgili değerlendirmenizi iletmenizi rica ederiz."),
        para("Teşekkür eder, iyi çalışmalar dileriz."),
    ],
))

# Page 8
PAGES.append(dict(
    no=8, file="08-olumsuz-sonuc.html",
    subject="Başvurunuz Hakkında Bilgilendirme",
    blocks=[
        block_greeting("Merhaba [[X Bey/Hanım]],"),
        para("Şirketimize göstermiş olduğunuz ilgi için teşekkür ederiz. Sizinle tanışmaktan ve "
             "deneyimlerinizi dinlemekten memnuniyet duyduk."),
        para("Yapılan değerlendirmeler sonucunda, görüşme yaptığımız pozisyon için size olumlu bir "
             "dönüş yapamadığımızı bildirmek isteriz."),
        para("İleride doğabilecek uygun pozisyonlarda değerlendirmek üzere başvurunuz 6698 sayılı "
             "Kişisel Verilerin Korunması Kanunu hükümlerine uygun şekilde saklı tutulacak olup, "
             "niteliklerinize uygun pozisyon olması durumunda sizinle iletişime geçilecektir."),
        para("Türk Telekom’u tercih ettiğiniz için teşekkür eder, kariyer hayatınızda başarılar dileriz."),
        block_signature(["Saygılarımızla,", "Türk Telekom İnsan Kaynakları"]),
    ],
    has_social=True,
))

# Page 9
PAGES.append(dict(
    no=9, file="09-vaka-calismasi.html",
    subject="Vaka Çalışması Davetiniz",
    blocks=[
        block_greeting("Merhaba [[X Bey/Hanım]],"),
        para("İşe alım sürecimizin bir sonraki aşamasında ekteki vaka çalışmasını tamamlamanız "
             "gerekmektedir. Vaka çalışmamız, değerlendirme sürecimiz için bize önemli içgörüler "
             "sağlamaktadır. Bu sebeple, düşüncelerinizi yapıcı, analitik ve mümkün olduğunca somut "
             "temellere dayandırarak, belirlediğimiz tarihte sunmanız beklenmektedir."),
        block_detail_box([
            ("📅", "Sunum Tarihi", "[[01.01.2026 – Perşembe]]"),
            ("🕑", "Sunum Saati", "[[10.00]]"),
            ("📝", "Konu", "[[Vaka Çalışması konusu]]"),
            ("🗣", "Sunum Dili", "[[İngilizce/Türkçe]]"),
            ("📄", "Sunum Formatı", "[[PDF, Word, PowerPoint vb.]]"),
        ], title="Vaka Çalışması Detayları"),
        para("Vaka çalışmanızı önden inceleyebilmek adına, belirlenen sunum günü saat [[08:00]]’e kadar "
             "dosyanızı bizimle mail üzerinden paylaşmanızı rica ederiz."),
        para("Herhangi bir sorunuz olursa, bu e-posta üzerinden bizimle iletişime geçebilirsiniz."),
        para("Başarılar dileriz!"),
        block_signature(["Saygılarımızla,", "Türk Telekom İnsan Kaynakları"]),
    ],
    has_process=True,
))

# Page 10
PAGES.append(dict(
    no=10, file="10-referans-kontrolu.html",
    subject="Referans Bilgilerinizi Paylaşır mısınız?",
    blocks=[
        block_greeting("Merhaba [[X Bey/Hanım]],"),
        para("İşe alım sürecimizde referans kontrolü aşamasına gelmiş bulunmaktayız."),
        para("Sizinle ilgili görüşlerine başvurmak üzere iş, proje veya staj deneyimlerinizde daha önce "
             "birlikte çalıştığınız iki yöneticinizin iletişim bilgilerini bu mail üzerinden paylaşmanızı "
             "rica ederiz."),
        para("Teşekkür ederiz."),
        block_referee_pairs(2),
        block_signature(["Saygılarımızla,", "Türk Telekom İnsan Kaynakları"]),
    ],
    has_process=True,
))

# Page 11
PAGES.append(dict(
    no=11, file="11-is-teklifi.html",
    subject="Sizi Aramızda Görmekten Mutluluk Duyarız — İş Teklifi",
    blocks=[
        block_greeting("Merhaba [[X Bey/Hanım]],"),
        para("Türkiye’nin dijital dönüşüm yolculuğuna katılmaya yönelik tüm adımları başarıyla "
             "tamamladınız, tebrik ederiz."),
        para("Sizin için hazırladığımız iş teklifi mektubunu ekte bilgilerinize sunarız."),
        para("Teklifi kabul etmeniz durumunda, işe başlangıç öncesinde hazırlamanız gereken evraklar ve "
             "süreç detayları size ayrıca iletilecektir."),
        para("Bu yolculukta birlikte keşfetmeyi, potansiyelimizi dönüştürmeyi ve üreteceğimiz değerle "
             "ilham vermeyi heyecanla bekliyoruz."),
        block_signature(["Saygılarımızla,", "Türk Telekom İnsan Kaynakları"]),
    ],
))

# Page 12
PAGES.append(dict(
    no=12, file="12-sozlesme-elden-teslim.html",
    subject="İş Sözleşmeniz ve Evrak Süreciniz Hakkında",
    blocks=[
        block_greeting("Merhaba [[X Bey/Hanım]],"),
        para("Yeni bir yolculuğa başlamanızın heyecanını sizinle paylaşıyoruz."),
        para("Evrak sürecinizi tamamlamak adına; ekte ilettiğimiz iş sözleşmenizin iki nüsha çıktısını "
             "aldıktan sonra, her sayfanın sol alt kısmına ve son sayfada bulunan isminizin altına imza "
             "atmanız gerekmektedir."),
        para("İki nüsha halinde hazırlayarak imzaladığınız sözleşmenizi kapalı zarf içinde ilk iş "
             "gününüzde aşağıda belirtilen adreste bulunan işe alım ekibine teslim etmenizi rica ederiz."),
        para("Sözleşmeler için işveren imzaları da tamamlandıktan sonra, bir nüshayı size ulaştıracağız."),
        para("Konuyla ilgili göstereceğiniz hassasiyet için teşekkür ederiz."),
        block_address_list([
            dict(title="Türk Telekom Gayrettepe Genel Müdürlük (Kule Bina Kat: 9)",
                 lines=["Gayrettepe Mahallesi, Yıldız Posta Caddesi, No:40,", "Beşiktaş / İstanbul"]),
            dict(title="Türk Telekom Acıbadem Genel Müdürlük (Kule Bina Kat: 4)",
                 lines=["Acıbadem Mahallesi, Acıbadem Caddesi, No: 150,", "Üsküdar / İstanbul"]),
            dict(title="Türk Telekom Aydınlıkevler Genel Müdürlük (Kule Bina Kat: 17)",
                 lines=["Turgut Özal 2 Bulvarı, Samsun Yolu Kavşağı, No:4", "Altındağ / Ankara"]),
        ]),
        block_signature(["Saygılarımızla,", "Türk Telekom İnsan Kaynakları"]),
    ],
))

# Page 13
PAGES.append(dict(
    no=13, file="13-sozlesme-kargo.html",
    subject="İş Sözleşmeniz ve Evrak Süreciniz Hakkında",
    blocks=[
        block_greeting("Merhaba [[X Bey/Hanım]],"),
        para("Yeni bir yolculuğa başlamanızın heyecanını sizinle paylaşıyoruz."),
        para("Evrak sürecinizi tamamlamak adına; ekte ilettiğimiz iş sözleşmenizin iki nüsha çıktısını "
             "aldıktan sonra, her sayfanın sol alt kısmına ve son sayfada bulunan isminizin altına imza "
             "atmanız gerekmektedir."),
        para("İki nüsha halinde hazırlayarak imzaladığınız sözleşmenizi kapalı zarf içinde aşağıdaki "
             "adres ve alıcı bilgisi ile ilk iş gününüzde şirketimizin iç muhaberatından kargolamanızı "
             "rica ederiz."),
        para("Sözleşmeler için işveren imzaları da tamamlandıktan sonra, bir nüshayı size ulaştıracağız."),
        para("Konuyla ilgili göstereceğiniz hassasiyet için teşekkür ederiz."),
        block_contact_box(
            "Alıcı: İşe Alım Grup Müdürlüğü’nden Feyzanur Akbaba", "", "",
            ["Türk Telekom Genel Müdürlük / Kule Bina Kat: 9, Gayrettepe Mahallesi,",
             "Yıldız Posta Caddesi No:40 Beşiktaş, İstanbul"],
        ),
        block_signature(["Saygılarımızla,", "Türk Telekom İnsan Kaynakları"]),
    ],
))

# Page 14
PAGES.append(dict(
    no=14, file="14-ise-baslangic-evrak-takvimi.html",
    subject="Aramıza Hoş Geldiniz — İşe Başlangıç ve Evrak Süreciniz",
    blocks=[
        block_greeting("Merhaba [[X Bey/Hanım]],"),
        para("Aramıza hoş geldiniz."),
        para("Merakınızla keşfedeceğiniz, gücünüzle dönüşüm yaratacağınız ve vizyonunuzla ilham "
             "vereceğiniz yolculuğumuzda sizi aramızda görmekten çok mutluyuz."),
        para("Aşağıdaki tabloda işe başlangıç yapabileceğiniz tarihler ve buna bağlı olarak "
             "evraklarınızı teslim edebileceğiniz son tarih seçenekleri yer almaktadır. Bu tarihler "
             "dışında kalan tarihler için evraklarınızı işe başlama tarihinizden en geç 7 iş günü "
             "öncesine kadar eksiksiz bir şekilde iletmeniz gerekmektedir. Aksi durumda, işe "
             "başlangıcınızın daha ileri bir tarihe alınacağını bildirmek isteriz."),
        para("Size uygun olan tarihi seçerek tarafımıza bildirmenizi, buna yönelik evrak teslim "
             "tarihini baz alarak işe giriş evraklarınızı eksiksiz olarak hazırlamanızı rica ederiz."),
        block_table_box(
            ("İşe Başlangıç Yapabileceğiniz Tarihler", "Evrak Teslimi için Son Tarih"),
            [("[[7 Nisan 2025]]", "[[19 Mart 2025]]"),
             ("[[14 Nisan 2025]]", "[[26 Mart 2025]]"),
             ("[[21 Nisan 2025]]", "[[9 Nisan 2025]]")],
        ),
        para("Aşağıdaki notlar kısmını dikkate alarak, sizlere ilettiğimiz evrakları imzaladıktan "
             "sonra taratarak PDF formatında e-posta yoluyla göndermenizi rica ederiz. Belgelerin "
             "asıllarını daha sonra tarafımıza teslim edeceğiniz için muhafaza etmenizi rica ederiz."),
        para("Evraklarınızın eksik ya da istenilen formatta olmaması halinde, sizinle iletişime "
             "geçilecektir."),
        block_notes_box([
            "Ekteki tüm evrakların çıktılarını aldıktan sonra, ilgili evrakların hepsine imza atmanız "
            "gerekmektedir. “Hizmet”, “Tahsil”, “Ücret İstisnası”, “Terhis” ve “Acil Durum İrtibat "
            "Kişisi” formlarını ilk aşamada excel formatında iletmeniz yeterlidir. Evrak asıllarının "
            "teslimatı öncesinde bu formların çıktılarını alıp imzalayarak diğer evraklar arasına "
            "eklemeniz beklenmektedir.",
            "“1-1”, “2-1”, “3-1”, “5-1”, “TTBYS broşürü”, “Aydınlatma Metni” ve 10 numaralı PDF’ler "
            "bilgilendirme amaçlıdır, tarafımıza iletmeniz gerekmemektedir.",
            "“KVKK Gizlilik sözleşmesi” ve “BT Kullanımı Taahhütnamesi” evraklarında tüm sayfaların "
            "altına paraf atılması gerekmektedir.",
            "Maile dönüşünüzü, “Reply All / Tümünü Yanıtla” yaparak, evrak ekleriniz ile birlikte "
            "“.zip” formatında iletmeniz beklenmektedir.",
            "İlk iş gününüzde ihtiyacınız olacak bilgileri içeren mail, işe başlangıç tarihiniz "
            "öncesinde İnsan Kaynakları İş Ortağınız ([[İK İş Ortağı Ad Soyad]]) tarafından iletilecektir.",
            "Formlardaki “sicil numarası” kısımlarını boş bırakmanız ve “……” olarak belirtilen "
            "alanlar işe başlangıç tarihiniz olacak şekilde doldurulmalıdır.",
            "Formlardaki “unvan” kısmının işe başlayacağınız pozisyon ismi ile doldurulması "
            "gerekmektedir.",
            "Diplomanızın mutlaka noter onaylı kopyası iletilmelidir. Herhangi bir noter aracılığıyla "
            "işlem gerçekleştirilebilir.",
            "İkametiniz görev alacağınız ilde (İstanbul/Ankara) olmalıdır.",
            "E-Devlet formlarınızın çıktıları barkodlu olmalıdır.",
        ], "Notlar"),
        para("Evrak listenizle ilgili diğer sorularınız için **Vural Çakırlar** ile iletişime "
             "geçebilirsiniz.\nE-mail: vural.cakirlar@partner.turktelekom.com.tr\nTelefon: 0553 970 21 48"),
        para("Evrak hazırlık sürecinizi kolaylıkla geçirmenizi diliyor, en kısa sürede aramıza "
             "katılmanızı temenni ediyoruz."),
        block_signature(["Saygılarımızla,", "Türk Telekom İnsan Kaynakları"]),
    ],
))

DOC_LIST_ITEMS = [
    "5 Adet vesikalık,",
    "Islak imzalı evrak asılları, (Çalışma Esasları Tutanağı, İş Etiği Kodu Bildirim Formu, İnsan "
    "Hakları Politikası Bilgilendirme Formu, Bilgi Teknolojileri Kullanımı Taahhütnamesi, Sosyal "
    "Medya Kullanım Taahhütnamesi, Muvafakat-Taahhütname, Kümülatif Gelir Vergisi Matrah Sorgulama "
    "Formu, Adli Sicil Kaydı Beyanı ve Dava Soruşturma Taahhütnamesi, Meslek Odası Kaydı "
    "Taahhütname, Sürekli-Hibrit-Uzaktan Çalışma Ek Protokol, Yan Hak Formu, KVKK Bilgilendirme ve "
    "Gizlilik Taahhütnamesi, Ücret İstisnası İşçi Sorumluluk ve Taahhüt Formu, Hizmet Bilgi Formu, "
    "Tahsil Bilgi Formu, Terhis Formu, Acil Durum İrtibat Kişisi)",
    "Noter onaylı diploma fotokopisinin ıslak imzalı hali,",
    "Tüm E-Devlet belgeleri ve imza alanı olmayan belgeler (Adli Sicil Kaydı, Terhis Belgesi, Banka "
    "Hesap Cüzdanı, E Devlet Mezuniyet Belgesi, SGK Hizmet Dökümü, İkametgah, Bordro, Nüfus Cüzdanı "
    "Fotokopisi, Nüfus Kayıt Örneği).",
]

def doc_delivery_page(no, file, subject, intro, contact_name, contact_phone, contact_email, addr_lines):
    return dict(
        no=no, file=file, subject=subject,
        blocks=[
            block_greeting("Merhaba [[X Bey/Hanım]],"),
            para(intro),
            block_notes_box(DOC_LIST_ITEMS, "Teslim Edilecek Evraklar"),
            block_contact_box(contact_name, contact_phone, contact_email, addr_lines),
            para("Not: Sağlık Raporu ve Tetkikler işe giriş muayenesi sırasında sağlık ekibine teslim "
                 "edilecektir. Sağlık ekibi muayene için sizinle iletişime geçecektir."),
            block_signature(["Saygılarımızla,", "Türk Telekom İnsan Kaynakları"]),
        ],
    )

# Page 15
PAGES.append(doc_delivery_page(
    15, "15-evrak-teslim-ankara-elden.html",
    "İşe Giriş Evraklarınızın Teslimi — Ankara",
    "İşe girişiniz için hazırlamış ve imzalamış olduğunuz evraklardan Sağlık Raporu, Tetkikler ve "
    "Hat Evrakları hariç, listelenen dokümanların asıllarını işe başladığınız hafta 17. katta "
    "bulunan İnsan Kaynakları Özlük Ekibi’ne teslim edebilirsiniz.",
    "Evren Göksel Duman", "(554) 554 27 44", "evrengoksel.duman@turktelekom.com.tr",
    ["Türk Telekom Genel Müdürlüğü Kule Bina 17.Kat",
     "Turgut Özal Bulvarı, Samsun Yolu Kavşağı, Aydınlıkevler - Altındağ / Ankara"],
))

# Page 16
PAGES.append(doc_delivery_page(
    16, "16-evrak-teslim-ankara-kargo.html",
    "İşe Giriş Evraklarınızın Teslimi — Ankara",
    "İşe girişiniz için hazırlamış ve imzalamış olduğunuz evraklardan Sağlık Raporu, Tetkikler ve "
    "Hat Evrakları hariç, listelenen dokümanların asıllarını işe başladığınız hafta aşağıda "
    "belirtilen kişi adına muhaberata teslim etmenizi rica ederiz.",
    "Evren Göksel Duman", "(554) 554 27 44", "evrengoksel.duman@turktelekom.com.tr",
    ["Türk Telekom Genel Müdürlüğü Kule Bina 17.Kat",
     "Turgut Özal Bulvarı, Samsun Yolu Kavşağı, Aydınlıkevler - Altındağ / Ankara"],
))

# Page 17
PAGES.append(doc_delivery_page(
    17, "17-evrak-teslim-istanbul-elden.html",
    "İşe Giriş Evraklarınızın Teslimi — İstanbul",
    "İşe girişiniz için hazırlamış ve imzalamış olduğunuz evraklardan Sağlık Raporu, Tetkikler ve "
    "Hat Evrakları hariç, listelenen dokümanların asıllarını işe başladığınız hafta 10. katta "
    "bulunan İnsan Kaynakları Özlük Ekibi’ne teslim edebilirsiniz.",
    "Selda Gökçe", "(553) 968 48 56", "selda.gokce@turktelekom.com.tr",
    ["Türk Telekom Genel Müdürlüğü Kule Bina 10.Kat",
     "Gayrettepe Mah. Yıldız Posta Cad. No:40 Beşiktaş/İstanbul"],
))

# Page 18
PAGES.append(doc_delivery_page(
    18, "18-evrak-teslim-istanbul-kargo.html",
    "İşe Giriş Evraklarınızın Teslimi — İstanbul",
    "İşe girişiniz için hazırlamış ve imzalamış olduğunuz evraklardan Sağlık Raporu, Tetkikler ve "
    "Hat Evrakları hariç, listelenen dokümanların asıllarını işe başladığınız hafta aşağıda "
    "belirtilen kişi adına muhaberata teslim etmenizi rica ederiz.",
    "Selda Gökçe", "(553) 968 48 56", "selda.gokce@turktelekom.com.tr",
    ["Türk Telekom Genel Müdürlüğü Kule Bina 10.Kat",
     "Gayrettepe Mah. Yıldız Posta Cad. No:40 Beşiktaş/İstanbul"],
))

# Page 19 (variant/duplicate of page 5)
PAGES.append(dict(
    no=19, file="19-adaya-ulasamadik-variant.html",
    subject="Sizinle İletişime Geçmek İstiyoruz",
    blocks=[
        block_greeting("Merhaba [[X Bey/Hanım]],"),
        para("Ben Türk Telekom İşe Alım Ekibi’nden [[XXXX]]."),
        para("Şirketimizde ilgilendiğiniz kariyer fırsatı kapsamında sizinle iletişime geçtim; ancak "
             "ulaşamadım. Detayları aktarabilmek ve görüşmeyi planlayabilmek adına, uygun olduğunuz "
             "bir zaman aralığını paylaşabilirseniz, sizinle yeniden iletişime geçmek isterim."),
        para("Teşekkür ederim."),
    ],
))

# ---------- generate files ----------

TITLES = {}
for pg in PAGES:
    html_out = render(pg["no"], pg["subject"], pg["blocks"],
                       has_process=pg.get("has_process", False),
                       has_social=pg.get("has_social", False))
    path = os.path.join(OUT_DIR, pg["file"])
    with open(path, "w", encoding="utf-8") as f:
        f.write(html_out)
    TITLES[pg["file"]] = (pg["no"], pg["subject"])
    print("wrote", pg["file"])

# ---------- index ----------
rows = ''.join(
    f'<tr><td class="idx-no">{no:02d}</td>'
    f'<td><a class="idx-link" href="{fn}">{html.escape(plain(subj))}</a></td></tr>'
    for fn, (no, subj) in sorted(TITLES.items(), key=lambda kv: kv[1][0])
)
index_html = f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Aday Deneyimi — Mail İçerikleri (HTML)</title>
<style>
body{{margin:0;background:#060733;font-family:'Segoe UI',Arial,Helvetica,sans-serif;color:#fff;}}
.wrap{{max-width:720px;margin:0 auto;padding:40px 24px;}}
h1{{font-size:22px;margin-bottom:6px;}}
p.lead{{color:#c7c9f5;font-size:14px;margin-top:0;}}
table{{width:100%;border-collapse:collapse;margin-top:20px;}}
td{{border-bottom:1px solid #23256e;padding:12px 10px;font-size:14px;}}
.idx-no{{color:#2ce0cf;font-weight:700;width:36px;}}
.idx-link{{color:#eef0ff;text-decoration:none;}}
.idx-link:hover{{color:#2ce0cf;}}
</style>
</head>
<body>
<div class="wrap">
<h1>Aday Deneyimi Projesi — Mail İçerikleri</h1>
<p class="lead">PDF’teki 19 sayfanın editlenebilir HTML e-posta versiyonları. Sarı vurgulu alanlar
([[ ]] ile işaretli örnekler) her gönderimde güncellenmesi gereken yer tutuculardır.</p>
<table>{rows}</table>
</div>
</body>
</html>
"""
with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)
print("wrote index.html")
