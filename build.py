# KolayAdım site üreticisi: python build.py  ->  docs/ klasörünü oluşturur
import os, shutil, html

SITE = "https://avcimzeyyen.github.io/kolayadim"  # alan adı alırsan burayı değiştir
BASE = "/kolayadim"  # alan adı kullanırsan "" yap
OUT = "docs"

CATS = {
 "is-ve-kariyer": ("💼 İş ve Kariyer", "CV, başvuru, staj ve mülakat için adım adım rehberler.", True),
 "egitim": ("🎓 Eğitim", "Burs, sınav ve yeni beceri öğrenme rehberleri.", False),
 "gunluk-yasam": ("🏡 Günlük Yaşam", "Taşınma, gezi ve günlük işleri düzenleme rehberleri.", False),
}

# (slug, kategori, başlık, açıklama, belgeler, adımlar[(başlık, açıklama)], ipucu)
G = [
("cv-hazirlama","is-ve-kariyer","CV Nasıl Hazırlanır?","Hedefe uygun, tek sayfalık etkili bir CV’yi adım adım hazırla.",
 ["Eğitim bilgilerin","Staj/iş geçmişin","Projelerin ve GitHub bağlantın"],
 [("Hedef pozisyonu belirle","Başvuracağın işin ilanlarını incele ve ortak istenen becerileri not al."),
  ("İletişim bilgilerini yaz","Ad, e-posta, telefon, LinkedIn ve GitHub bağlantısı yeterli. Fotoğraf zorunlu değil."),
  ("Eğitimini ekle","Okul, bölüm ve mezuniyet yılını en yeniden eskiye doğru sırala."),
  ("Projelerini öne çıkar","Her proje için kullandığın teknolojileri ve ortaya çıkan sonucu tek cümleyle yaz."),
  ("Becerileri ilana göre düzenle","İlandaki anahtar kelimelerle CV’deki beceriler örtüşmeli."),
  ("Kontrol et ve PDF al","Yazım hatalarına bak, tek sayfada tut, dosyayı “Ad-Soyad-CV.pdf” olarak kaydet.")],
 "Deneyimin azsa projelerini deneyim gibi anlat: ne yaptın, hangi araçlarla, sonucu ne oldu?"),
("is-basvurusu-takibi","is-ve-kariyer","İş Başvurularını Nasıl Takip Ederim?","Başvurularını düzenli tut, geri dönüşleri kaçırma.",
 ["Güncel CV","Ön yazı taslağı"],
 [("Takip tablosu oluştur","Şirket, pozisyon, başvuru tarihi, bağlantı ve durum sütunları yeterli."),
  ("Ön yazıyı özelleştir","Her başvuru için şirkete ve pozisyona özel birkaç cümle ekle."),
  ("Başvuruyu gönder ve kaydet","Gönderim tarihini ve ilan bağlantısını tabloya yaz."),
  ("Bir hafta sonra nazikçe takip et","Kısa bir e-postayla başvurunun durumunu sor."),
  ("Sonucu kaydet","Ret de olsa geri bildirimi not et, sonraki başvurularda kullan.")],
 "Haftada belirli bir sayıda başvuru hedefi koymak motivasyonu korur."),
("staj-basvurusu","is-ve-kariyer","Staj Başvurusu Nasıl Yapılır?","Öğrenciler için staj bulma ve başvuru rehberi.",
 ["CV","Öğrenci belgesi","Staj başvuru formu (okulundan)"],
 [("Okulunun staj kurallarını öğren","Süre, dönem ve gerekli belgeleri bölümünden ya da meslek yüksekokulu ofisinden doğrula."),
  ("Hedef şirket listesi yap","Yerel şirketler, kamu kurumları ve yazılım firmalarını listele."),
  ("CV ve ön yazı hazırla","Bölümünü, kullandığın teknolojileri ve staj dönemini yaz."),
  ("Başvur ve takip et","İlanlara başvur, ilan yoksa şirketlere doğrudan e-posta gönder."),
  ("Belgeleri tamamla","Kabul yazısı ve staj formunu okula zamanında teslim et.")],
 "Kesin tarih, süre ve belge şartları okuldan okula değişir; her zaman kendi okulunun duyurusuna bak."),
("mulakat-hazirligi","is-ve-kariyer","Mülakata Nasıl Hazırlanılır?","Mülakat öncesi kontrol listesi ve hazırlık planı.",
 ["CV çıktısı","Hazırladığın sorular"],
 [("Şirketi araştır","Ürünleri, hizmetleri ve son haberleri oku."),
  ("Sık sorulan soruları çalış","“Kendinden bahset” gibi soruları sesli prova et."),
  ("Örnek hikâyeler hazırla","Zorlandığın ve başardığın üç durumu kısa anlatmaya hazırlan."),
  ("Teknik temelleri tekrar et","Pozisyonun istediği konulardan kendini test et."),
  ("Sorular hazırla","İşverene sorabileceğin en az iki soru yaz."),
  ("Gün öncesi kontrol et","Saat, adres veya bağlantıyı ve gerekli belgeleri hazırla.")],
 "Cevaplarını ezberleme, ana noktaları bil ve doğal anlat."),
("linkedin-profili","is-ve-kariyer","LinkedIn Profili Nasıl Hazırlanır?","İşverenlerin bulabileceği güçlü bir profil oluştur.",
 ["Güncel CV","Net bir profil fotoğrafı"],
 [("Başlığını yaz","Sadece “öğrenci” yerine ne yaptığını yaz: “.NET ve Angular ile web geliştiren bilgisayar programcılığı öğrencisi” gibi."),
  ("Hakkında bölümünü doldur","Kim olduğunu, ne öğrendiğini ve ne aradığını 3–4 cümleyle anlat."),
  ("Proje ve deneyim ekle","Projelerini ve GitHub bağlantını ekle."),
  ("Becerileri işaretle","Gerçekten bildiğin teknolojileri ekle."),
  ("Bağlantı kur","Okul, hoca ve sektör çalışanlarıyla bağlantı kur.")],
 "Profil adresini özelleştir ve CV’ne ekle."),
("burs-basvurusu","egitim","Burs Başvurusu Nasıl Yapılır?","Uygun bursu bulma ve başvuru adımları.",
 ["Öğrenci belgesi","Transkript","Niyet mektubu"],
 [("Burs seçeneklerini listele","Kurum, vakıf ve üniversite burslarını araştır."),
  ("Şartları karşılaştır","Not ortalaması ve son başvuru tarihlerini not al."),
  ("Belgeleri topla","Eksik belgeleri hemen talep et."),
  ("Niyet mektubunu yaz","Hedeflerini net anlat."),
  ("Başvuruyu tamamla","Onay ekranını kaydet.")],
 "Şartlar ve tarihler değişir; her zaman resmî duyuruyu kontrol et."),
("sinav-calisma-plani","egitim","Sınav Çalışma Planı","Sınava kadar gerçekçi bir plan yap.",
 ["Konu listesi","Deneme sınavları"],
 [("Tarihi ve konuları yaz","Kapsamı konu konu çıkar."),
  ("Seviyeni ölç","Bir deneme çöz, zayıf konuları belirle."),
  ("Haftalık plan yap","Her güne küçük ve net hedefler koy."),
  ("Tekrar günü ayır","Haftada bir gün tekrar yap."),
  ("Deneme çöz ve analiz et","Yanlışlarının nedenini bul.")],
 "Planı küçük tut; uygulanabilir plan, mükemmel plandan iyidir."),
("tasinma-hazirligi","gunluk-yasam","Taşınma Hazırlığı","Taşınmayı stressiz planla.",
 ["Kira sözleşmesi","Adres değişikliği belgeleri"],
 [("Tarih belirle","Nakliye ve izinleri planla."),
  ("Eşyaları ayır","Taşınacak, bağışlanacak ve atılacakları ayır."),
  ("Kutula ve etiketle","Kutuları odalara göre işaretle."),
  ("Abonelikleri taşı","Elektrik, su ve internet işlemlerini yap."),
  ("Adresi güncelle","Banka ve resmî kurumlara bildir.")],
 "Sayaç değerlerinin ve hasarların fotoğrafını çek."),
("gezi-planlama","gunluk-yasam","Gezi Planlama","Gideceğin yeri adım adım planla.",
 ["Kimlik/pasaport","Rezervasyon onayları"],
 [("Bütçe ve tarih belirle","Harcama sınırını yaz."),
  ("Ulaşım ve konaklamayı ayarla","Rezervasyonları sakla."),
  ("Gezilecek yerleri listele","Günlere dağıt, boşluk bırak."),
  ("Belgeleri kontrol et","Kimlik ve gerekiyorsa vize."),
  ("Bavulunu hazırla","Hava durumuna göre liste yap.")],
 "Gitmeden önce resmî seyahat koşullarını kontrol et."),
]

CSS = """:root{--bg:#faf8f4;--card:#fff;--ink:#1f2a24;--mut:#5c6862;--acc:#2f7d5b;--acc2:#e3f2ea;--line:#e4e0d8}
@media(prefers-color-scheme:dark){:root{--bg:#151a17;--card:#1e2521;--ink:#eef2ef;--mut:#9aa8a0;--acc:#5fc59a;--acc2:#23372d;--line:#2d3731}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif}
.w{max-width:820px;margin:0 auto;padding:16px}a{color:var(--acc)}
nav{display:flex;gap:14px;flex-wrap:wrap;align-items:center;padding:12px 0;border-bottom:1px solid var(--line);margin-bottom:20px}nav b{margin-right:auto;font-size:20px}nav a{text-decoration:none}
h1{font-size:28px;line-height:1.25}.mut{color:var(--mut)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px;margin:16px 0}
.card{display:block;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px;text-decoration:none;color:var(--ink)}.card:hover{border-color:var(--acc)}
.card h3{margin:0 0 4px;font-size:17px}.card p{margin:0;color:var(--mut);font-size:14px}
.bar{height:8px;background:var(--acc2);border-radius:6px;overflow:hidden;margin:10px 0 4px}.bar i{display:block;height:100%;width:0;background:var(--acc);transition:width .3s}
.docs,.tip{background:var(--acc2);border-radius:12px;padding:12px 16px;margin:16px 0}
.step{display:flex;gap:12px;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px;margin:8px 0;cursor:pointer}
.step input{width:22px;height:22px;flex:none;margin-top:3px;accent-color:var(--acc)}.step.done b{text-decoration:line-through;color:var(--mut)}.step b{display:block}.step span{color:var(--mut);font-size:15px}
.ad{min-height:0}footer{margin:40px 0 20px;padding-top:16px;border-top:1px solid var(--line);color:var(--mut);font-size:14px}"""

JS = """(function(){
var P=location.pathname.replace(/\\/$/,'');
function get(k){try{return JSON.parse(localStorage.getItem(k)||'[]')}catch(e){return[]}}
function set(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
var steps=document.querySelectorAll('.step input');
if(steps.length){
  var key='ka:'+P,d=get(key),bar=document.getElementById('bar'),lab=document.getElementById('lab');
  function upd(){var n=0;steps.forEach(function(c,i){c.checked=!!d[i];c.parentNode.classList.toggle('done',!!d[i]);if(d[i])n++});
    var p=Math.round(n*100/steps.length);bar.style.width=p+'%';lab.textContent='%'+p+' tamamlandı'}
  steps.forEach(function(c,i){c.onchange=function(){d[i]=c.checked;set(key,d);upd()}});upd();
}
document.querySelectorAll('[data-g]').forEach(function(a){
  var d=get('ka:'+a.getAttribute('data-g')),t=+a.getAttribute('data-n'),n=0;
  for(var i=0;i<t;i++)if(d[i])n++;
  var p=Math.round(n*100/t),e=a.querySelector('i'),l=a.querySelector('.pl');
  if(e)e.style.width=p+'%';if(l)l.textContent='%'+p+' tamamlandı';
});
})();"""

def page(title, desc, path, body):
    e = html.escape
    nav = f'<nav><b><a href="{BASE}/">KolayAdım 🌱</a></b>' + "".join(
        f'<a href="{BASE}/{s}/">{c[0]}</a>' for s, c in CATS.items()) + "</nav>"
    foot = (f'<footer>© KolayAdım · <a href="{BASE}/hakkinda/">Hakkında</a> · '
            f'<a href="{BASE}/gizlilik/">Gizlilik</a><br>Bu sitedeki bilgiler genel rehberlik içindir; '
            'resmî şartlar ve tarihler için ilgili kurumun güncel duyurusunu kontrol edin.</footer>')
    return (f'<!DOCTYPE html><html lang="tr"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{e(title)} | KolayAdım</title><meta name="description" content="{e(desc)}">'
            f'<link rel="canonical" href="{SITE}{path}"><link rel="stylesheet" href="{BASE}/style.css"></head>'
            f'<body><div class="w">{nav}{body}{foot}</div><script src="{BASE}/app.js"></script></body></html>')

def write(path, content):
    full = os.path.join(OUT, path.strip("/"), "index.html") if not path.endswith((".css", ".js", ".xml", ".txt")) else os.path.join(OUT, path.strip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)

def card(g):
    return (f'<a class="card" href="{BASE}/{g[1]}/{g[0]}/" data-g="/{g[1]}/{g[0]}" data-n="{len(g[5])}">'
            f'<h3>{html.escape(g[2])}</h3><p>{html.escape(g[3])}</p><div class="bar"><i></i></div><div class="small mut pl"></div></a>')

shutil.rmtree(OUT, ignore_errors=True)
write("/style.css", CSS); write("/app.js", JS)
write("/robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
urls = ["/"]

# Ana sayfa
body = ('<h1>Yapmak istediğin işi seç, adım adım ilerle</h1>'
        '<p class="mut">KolayAdım; iş, eğitim ve günlük hayat için kontrol listeleri ve yol haritaları sunar. İlerlemen tarayıcında saklanır.</p><div class="grid">')
for s, (t, d, live) in CATS.items():
    body += f'<a class="card" href="{BASE}/{s}/"><h3>{t}</h3><p>{d}</p></a>'
body += '</div><h2>Öne çıkan rehberler</h2><div class="grid">' + "".join(card(g) for g in G if g[1] == "is-ve-kariyer") + "</div>"
write("/", page("Adım adım yol haritaları", "İş, eğitim ve günlük yaşam için adım adım rehberler ve kontrol listeleri.", "/", body))

# Kategori sayfaları
for s, (t, d, live) in CATS.items():
    urls.append(f"/{s}/")
    body = f'<h1>{t}</h1><p class="mut">{d}</p><div class="grid">' + "".join(card(g) for g in G if g[1] == s) + "</div>"
    if not live:
        body += '<p class="mut">Bu kategoriye yeni rehberler eklenecek.</p>'
    write(f"/{s}/", page(t, d, f"/{s}/", body))

# Rehber sayfaları
for slug, cat, title, desc, docs, steps, tip in G:
    p = f"/{cat}/{slug}/"; urls.append(p)
    e = html.escape
    body = (f'<p><a href="{BASE}/{cat}/">← {CATS[cat][0]}</a></p><h1>{e(title)}</h1><p class="mut">{e(desc)}</p>'
            f'<div class="bar"><i id="bar"></i></div><div class="mut" id="lab"></div>'
            f'<div class="docs"><b>Hazırlaman gereken belgeler</b><ul>' + "".join(f"<li>{e(x)}</li>" for x in docs) + "</ul></div>")
    for i, (a, b) in enumerate(steps):
        body += f'<label class="step"><input type="checkbox"><div><b>{i+1}. {e(a)}</b><span>{e(b)}</span></div></label>'
    body += f'<div class="tip"><b>İpucu:</b> {e(tip)}</div>'
    write(p, page(title, desc, p, body))

# Statik sayfalar
write("/hakkinda/", page("Hakkında", "KolayAdım hakkında", "/hakkinda/",
  "<h1>Hakkında</h1><p>KolayAdım, insanların yapmak istedikleri işleri daha kolay tamamlayabilmesi için hazırlanan bir rehber sitesidir. "
  "Bilgisayar Programcılığı öğrencisi Müzeyyen Avcı tarafından geliştirilmektedir.</p>"
  '<p><a href="https://github.com/avcimzeyyen">GitHub</a></p>')); urls.append("/hakkinda/")
write("/gizlilik/", page("Gizlilik Politikası", "KolayAdım gizlilik politikası", "/gizlilik/",
  "<h1>Gizlilik Politikası</h1><p>KolayAdım hesap istemez ve kişisel veri toplamaz. Tamamladığın adımlar yalnızca tarayıcında (LocalStorage) saklanır. "
  "İleride reklam veya analiz hizmeti eklenirse bu sayfa güncellenecektir.</p><p>İletişim: buraya e-posta adresini yaz.</p>")); urls.append("/gizlilik/")

sm = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{SITE}{u}</loc></url>" for u in urls) + "</urlset>"
write("/sitemap.xml", sm)
print(len(urls), "sayfa üretildi ->", OUT)
