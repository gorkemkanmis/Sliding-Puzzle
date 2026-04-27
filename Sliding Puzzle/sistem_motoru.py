import random

class OyunMekanigi:
    def __init__(self, matris_boyutu=3):
        # Oyun tahtasının boyutunu belirler (varsayılan 3x3)
        self.olcek = matris_boyutu
        # Kazanma durumunu temsil eden hedef matrisi oluşturur
        self.final_hali = self._hedef_matris_uret()
        # Oyunun anlık durumunu tutan matris
        self.mevcut_dizilim = []
        # Oyuncunun yaptığı toplam hamle sayısı
        self.toplam_adim = 0
        # Varsayılan karıştırma hamlesi sayısı
        self.karistirma_miktarı = 20
        # Oyun başladığında tahtayı karıştır
        self.tahtayi_karistir()

    def zorluk_ayarla(self, seviye):
        # Zorluk seviyesine göre karıştırma miktarını belirler
        ayarlar = {"Kolay": 10, "Orta": 50, "Zor": 150}
        # Tanımsız bir seviye girilirse varsayılan olarak 20 kullanılır
        self.karistirma_miktarı = ayarlar.get(seviye, 20)
        # Yeni zorluk seviyesiyle tahtayı yeniden karıştır
        self.tahtayi_karistir()

    def _hedef_matris_uret(self):
        # 1'den n²-1'e kadar sayılar + 0 (boş kare) ile sıralı listeyi oluşturur
        rakamlar = list(range(1, self.olcek**2)) + [0]
        # Listeyi olcek x olcek boyutunda bir matrise dönüştürür
        return [rakamlar[i:i+self.olcek] for i in range(0, len(rakamlar), self.olcek)]

    def tahtayi_karistir(self):
        veriler = list(range(self.olcek**2))
        while True:
            random.shuffle(veriler)
            # Yalnızca çözülebilir ve başlangıç ≠ hedef olan dizilişleri kabul et
            if self._analiz_et(veriler):
                yeni_yapi = [veriler[i:i+self.olcek] for i in range(0, len(veriler), self.olcek)]
                if yeni_yapi != self.final_hali:
                    self.mevcut_dizilim = yeni_yapi
                    break
        # Yeni oyunda adım sayacını sıfırla
        self.toplam_adim = 0

    def _analiz_et(self, dizi):
        # Dizinin çözülebilir olup olmadığını ters düzen (inversion) sayısıyla kontrol eder
        ters_duzen_sayisi = 0
        # Boş kareyi (0) hesaplamaya dahil etme
        sadece_sayilar = [n for n in dizi if n != 0]
        for sira_a in range(len(sadece_sayilar)):
            for sira_b in range(sira_a + 1, len(sadece_sayilar)):
                # Önceki eleman sonrakinden büyükse ters düzen var demektir
                if sadece_sayilar[sira_a] > sadece_sayilar[sira_b]:
                    ters_duzen_sayisi += 1
        # Çift sayıda ters düzen varsa dizilim çözülebilirdir
        return ters_duzen_sayisi % 2 == 0

    def koordinat_dogrula(self, satir, sutun):
        # Boş karenin (0) mevcut konumunu bul
        br, bs = -1, -1
        for i in range(self.olcek):
            for j in range(self.olcek):
                if self.mevcut_dizilim[i][j] == 0:
                    br, bs = i, j
                    break
        
        # Seçilen kare ile boş kare arasındaki Manhattan mesafesini hesapla
        mesafe = abs(satir - br) + abs(sutun - bs)
        if mesafe == 1:
            # Komşu kare ise yer değiştir ve adım sayacını artır
            self.mevcut_dizilim[br][bs] = self.mevcut_dizilim[satir][sutun]
            self.mevcut_dizilim[satir][sutun] = 0
            self.toplam_adim += 1
            # Hamle başarılı; boş karenin yeni koordinatlarını döndür
            return True, (br, bs)
        # Geçersiz hamle: seçilen kare boş kareye komşu değil
        return False, None

    def bitis_kontrolu(self):
        # Mevcut dizilim hedef matrisle eşleşiyorsa oyun tamamlanmıştır
        return self.mevcut_dizilim == self.final_hali