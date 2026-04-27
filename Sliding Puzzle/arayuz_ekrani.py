import tkinter as tk
from tkinter import messagebox
import time
from sistem_motoru import OyunMekanigi

# Arayüz renk paleti (koyu tema)
RENK_ARKA = "#121212"   # Ana arka plan rengi
RENK_PANEL = "#1f1f1f"  # Üst panel ve bilgi çubuğu arka planı
RENK_KUTU = "#bb86fc"   # Dolu kare butonlarının rengi
RENK_YAZI = "#ffffff"   # Genel yazı rengi
RENK_BOS = "#2c2c2c"    # Boş kare ve zorluk butonlarının rengi
RENK_HATA = "#cf6679"   # Geçersiz hamle animasyonu için hata rengi

class BulmacaArayuzu:
    def __init__(self, pencere):
        # Ana pencere referansını sakla
        self.ekran = pencere
        # Oyun mantığını yöneten motoru başlat
        self.oyun = OyunMekanigi()
        self.ekran.title("Zeka Bulmacası Pro v1.1")
        self.ekran.configure(bg=RENK_ARKA)
        # Zamanlayıcı görevinin referansı (iptal edebilmek için)
        self.zaman_tutucu = None
        # Oyunun başladığı anın Unix zaman damgası
        self.baslangic_an_verisi = 0
        # Oyunun aktif olup olmadığını kontrol eden bayrak
        self.aktif_mi = False
        # Tüm arayüz bileşenlerini oluştur
        self._arayuz_parcalarini_kur()
        # İlk oyunu başlat
        self.oyunu_baslat()

    def _arayuz_parcalarini_kur(self):
        # --- Üst Panel: Zorluk Seçimi ---
        ust_panel = tk.Frame(self.ekran, bg=RENK_PANEL, pady=5)
        ust_panel.pack(fill="x")
        
        # Her zorluk seviyesi için ayrı buton oluştur
        for sev in ["Kolay", "Orta", "Zor"]:
            btn = tk.Button(ust_panel, text=sev, bg=RENK_BOS, fg=RENK_YAZI,
                            command=lambda s=sev: self.zorluk_degistir(s))
            btn.pack(side="left", padx=5)

        # --- Bilgi Çubuğu: Adım Sayacı ve Süre ---
        bilgi_cubugu = tk.Frame(self.ekran, bg=RENK_PANEL, pady=10)
        bilgi_cubugu.pack(fill="x")
        # Adım sayısını gösteren etiket
        self.lbl_adim = tk.Label(bilgi_cubugu, text="ADIM: 0", bg=RENK_PANEL,
                                  fg=RENK_KUTU, font=("Arial", 11, "bold"))
        self.lbl_adim.pack(side="left", padx=20)
        # Geçen süreyi gösteren etiket
        self.lbl_sure = tk.Label(bilgi_cubugu, text="SÜRE: 00:00", bg=RENK_PANEL, fg=RENK_YAZI)
        self.lbl_sure.pack(side="right", padx=20)

        # --- Oyun Tahtası: 3x3 Buton Izgara ---
        self.cerceve = tk.Frame(self.ekran, bg=RENK_ARKA, pady=10)
        self.cerceve.pack()
        # 3x3 buton referanslarını tutan matris
        self.butonlar = [[None for _ in range(3)] for _ in range(3)]
        for r in range(3):
            for c in range(3):
                # Her kare için tıklanabilir buton oluştur
                b = tk.Button(self.cerceve, width=5, height=2, font=("Verdana", 20, "bold"),
                              relief="flat", command=lambda x=r, y=c: self.tiklama_olayi(x, y))
                b.grid(row=r, column=c, padx=3, pady=3)
                self.butonlar[r][c] = b

        # --- Alt Panel: Yeniden Oyna Butonu ---
        self.btn_tekrar = tk.Button(self.ekran, text="YENİDEN OYNA", bg=RENK_KUTU,
                                    fg="black", command=self.oyunu_baslat,
                                    font=("Arial", 10, "bold"))
        self.btn_tekrar.pack(pady=10)

    def zorluk_degistir(self, s):
        # Seçilen zorluk seviyesini oyun motoruna ilet ve oyunu sıfırla
        self.oyun.zorluk_ayarla(s)
        self.oyunu_baslat()

    def hata_goster(self, r, c):
        # Geçersiz hamle için butonu kısa süreliğine hata rengiyle renklendir
        eski_renk = self.butonlar[r][c].cget("bg")
        self.butonlar[r][c].config(bg=RENK_HATA)
        # 150 ms sonra orijinal rengine geri döndür
        self.ekran.after(150, lambda: self.butonlar[r][c].config(bg=eski_renk))

    def tiklama_olayi(self, r, c):
        # Oyun aktif değilse tıklamaları yoksay
        if not self.aktif_mi:
            return
        # Oyun motoruna hamleyi ilet; geçerli mi değil mi kontrol et
        hareket, _ = self.oyun.koordinat_dogrula(r, c)
        if hareket:
            # Geçerli hamle: ekranı güncelle ve kazanma koşulunu kontrol et
            self.ekrani_guncelle()
            if self.oyun.bitis_kontrolu():
                self.kazanma_durumu()
        else:
            # Geçersiz hamle: hata animasyonu göster
            self.hata_goster(r, c)

    def ekrani_guncelle(self):
        # Her kareyi oyunun mevcut dizilimine göre yeniden çiz
        for r in range(3):
            for c in range(3):
                deger = self.oyun.mevcut_dizilim[r][c]
                btn = self.butonlar[r][c]
                if deger == 0:
                    # Boş kare: metin yok, devre dışı bırakılmış görünüm
                    btn.config(text="", bg=RENK_BOS, state="disabled")
                else:
                    # Dolu kare: sayıyı göster ve aktif hale getir
                    btn.config(text=str(deger), bg=RENK_KUTU, fg="black", state="normal")
        # Adım sayacı etiketini güncelle
        self.lbl_adim.config(text=f"ADIM: {self.oyun.toplam_adim}")

    def oyunu_baslat(self):
        # Önceki zamanlayıcı görevi varsa iptal et
        if self.zaman_tutucu:
            self.ekran.after_cancel(self.zaman_tutucu)
        # Tahtayı yeniden karıştır
        self.oyun.tahtayi_karistir()
        # Başlangıç zamanını kaydet
        self.baslangic_an_verisi = time.time()
        # Oyunu aktif duruma getir
        self.aktif_mi = True
        # Ekranı güncel durumla yenile
        self.ekrani_guncelle()
        # Süre sayacını başlat
        self._sayaci_guncelle()

    def _sayaci_guncelle(self):
        # Oyun aktifse her saniye süre etiketini güncelle
        if self.aktif_mi:
            gecen = int(time.time() - self.baslangic_an_verisi)
            # Geçen süreyi dakika ve saniyeye böl
            min, sec = divmod(gecen, 60)
            self.lbl_sure.config(text=f"SÜRE: {min:02d}:{sec:02d}")
            # 1 saniye sonra kendini tekrar çağır
            self.zaman_tutucu = self.ekran.after(1000, self._sayaci_guncelle)

    def kazanma_durumu(self):
        # Oyunu durdur
        self.aktif_mi = False
        # Oyuncuya tebrik mesajı ve adım sayısını göster
        messagebox.showinfo("Tebrikler!", f"Oyun {self.oyun.toplam_adim} adımda bitti.")

if __name__ == "__main__":
    # Ana pencereyi oluştur ve arayüzü başlat
    root = tk.Tk()
    BulmacaArayuzu(root)
    root.mainloop()