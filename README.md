🧩 3x3 Sliding Puzzle
Klasik 8-puzzle (Kayan Bulmaca) oyununun Python ile geliştirilmiş masaüstü versiyonu. Tkinter tabanlı modern koyu tema arayüzü ve akıllı çözülebilirlik kontrolü ile donatılmıştır.

📁 Proje Yapısı
Slidinn Puzzle/
├── sistem_motoru.py   # Oyun mantığı ve algoritmaları
├── arayuz.py          # Tkinter tabanlı görsel arayüz
└── README.md

🔧 sistem_motoru.py — Oyun Motoru
Oyunun tüm mantığını barındıran çekirdek modül.
OyunMekanigi Sınıfı
__init__(matris_boyutu)Tahtayı başlatır, hedef matrisi üretir ve karıştırır
zorluk_ayarla(seviye)Kolay / Orta / Zor seviyelerine göre karıştırma miktarını ayarlar
_hedef_matris_uret()[1,2,3 / 4,5,6 / 7,8,0] formatında kazanma matrisini üretir
tahtayi_karistir()Yalnızca çözülebilir ve başlangıç ≠ hedef olan dizilişleri kabul eder
_analiz_et(dizi)Ters düzen (inversion) algoritması ile çözülebilirliği doğrular
koordinat_dogrula(satir, sutun)Manhattan mesafesi ile geçerli hamleyi kontrol eder, taşı hareket ettirir
bitis_kontrolu()Mevcut dizilimin hedef matrisle eşleşip eşleşmediğini kontrol eder

Önemli Özellikler

Çözülebilirlik Garantisi: Her karıştırma işlemi sonrası ters düzen sayısı çift mi diye kontrol edilir. Tek ters düzenli (çözümsüz) dizilimler otomatik olarak reddedilir.
Zorluk Seviyeleri: Kolay (10), Orta (50), Zor (150) hamlelik karıştırma.
Dinamik Boyut: matris_boyutu parametresiyle 3x3 dışında farklı boyutlar da desteklenir.

🖥️ arayuz.py — Görsel Arayüz
Tkinter ile oluşturulmuş koyu temalı masaüstü arayüzü.
BulmacaArayuzu Sınıfı
_arayuz_parcalarini_kur()Tüm widget'ları (panel, buton, etiket) oluşturur ve yerleştirir
zorluk_degistir(s)Zorluk butonuna basıldığında motoru günceller ve oyunu sıfırlar
tiklama_olayi(r, c)Kare tıklamalarını yakalar, motora iletir ve sonucu işler
hata_goster(r, c)Geçersiz hamlelerde 150 ms kırmızı yanıp sönme animasyonu uygular
ekrani_guncelle()Tüm butonları motor durumuna göre yeniden çizer
oyunu_baslat()Tahtayı sıfırlar, zamanlayıcıyı yeniden başlatır
_sayaci_guncelle()Her saniye kendini çağıran özyinelemeli zamanlayıcı
kazanma_durumu()Oyunu durdurur ve tebrik mesajı gösterir

🎮 Nasıl Oynanır?

Boş kareye komşu (yukarı, aşağı, sol, sağ) olan bir kareye tıkla.
Tıklanan kare boş kareyle yer değiştirir.
Tüm sayıları sırayla 1-2-3 / 4-5-6 / 7-8-[boş] dizilimine getirince oyunu kazanırsın.
Üst panelden zorluk seviyesini değiştirebilir, YENİDEN OYNA butonuyla istediğin zaman sıfırlayabilirsin.


📐 Algoritma Notları
Ters Düzen (Inversion) Kontrolü
Bir permütasyon, önceki indekste yer alan elemanın sonraki indeksteki elemandan büyük olduğu her çift için bir "ters düzen" içerir. 3x3 tabloda çift sayıda ters düzen içeren dizilimler çözülebilirdir.
Manhattan Mesafesi
Hamle geçerliliği |satır_farkı| + |sütun_farkı| == 1 koşuluyla kontrol edilir; yani yalnızca yatay ve dikey komşular geçerli hamledir.
