import time
import random
import os
import getpass
import threading
import datetime
import sys
from google import genai
from google.genai import types

# 10 Farklı API Anahtarı - Tam Kapasite (200 Limit)
API_KEYS_POOL = [
    "AQ.Ab8RN6JJrDJNHJ5cjDIt6FawWmyLNnf7GY7dNUIIQ-6HjZIUGA",
    "AQ.Ab8RN6LOxcfrob8rhLse9cH2xd5_m577F6fvWhuz51K3N95P_Q",
    "AQ.Ab8RN6LV-UQbwIzCvvIwSaTkfvmbfQEeUIJdy3-MRaw1d0hY_w",
    "AQ.Ab8RN6LbcJNkhqe2kLoX6uVdw6TE1gZmZaeZYbRfmNxGqoBK9Q",
    "AQ.Ab8RN6IvOP4C8jOATC0g7dkRqj0LThxPqfkrOw2PYvskLfJYWg",
    "AQ.Ab8RN6L_YMJUo5c5A6zS3G8a6-mXSnT3k-xTqxN_1WYGTVVEoA",
    "AQ.Ab8RN6JpcRDVlMiQFNq1YLCj9-F3O5WT6XvGJuHDR_jbgI_ZUQ",
    "AQ.Ab8RN6Kj_r0TJPyJRvN43-xl3xeEBq2cbGi94sPa3B1xmP6dkA",
    "AQ.Ab8RN6JX8-sY-NOXJ5o8V98NSrJhkjGEY0Na_PhRN5BXJ4TXLQ",
    "AQ.Ab8RN6LNtWhAsm7JquBxEdY5IeIjqI3j6jO-jHGsSVdRp7SVIA"
]

TR_TZ = datetime.timezone(datetime.timedelta(hours=3))
KURUCU_SIFRESI = "KAPLAN_REIS_74"
DOSYA_ADI = "aslan_parcasi_hafiza.txt"

def hafizaya_yaz(kim, mesaj):
    with open(DOSYA_ADI, "a", encoding="utf-8") as f:
        f.write(f"{kim}: {mesaj}\n")

def hafizayi_oku():
    if os.path.exists(DOSYA_ADI):
        with open(DOSYA_ADI, "r", encoding="utf-8") as f:
            return f.read()[-2000:]
    return ""

def get_tr_zaman():
    return datetime.datetime.now(TR_TZ).strftime('%Y-%m-%d %H:%M:%S')

def aktif_ajani_calistir(mesaj):
    cevap = aslan_parcasi_ai_cevap(f"Sistemden gelen otomatik mesaj: {mesaj}", "Ayaz Reis", dis_tetikleyici=True)
    sys.stdout.write(f"\n\n🤖 Aslan Parçası (Aktif): {cevap}\nSiz: ")
    sys.stdout.flush()

def hatirlatici_kur(saniye, mesaj):
    def gorev():
        time.sleep(saniye)
        aktif_ajani_calistir(mesaj)
    threading.Thread(target=gorev, daemon=True).start()

def aslan_parcasi_ai_cevap(kullanici_mesaji, kullanici_turu, dis_tetikleyici=False):
    mesaj_temiz = kullanici_mesaji.lower().replace(" ", "")

    if not dis_tetikleyici and mesaj_temiz.startswith("!hatırlat"):
        try:
            komut = mesaj_temiz.replace("!hatırlat", "")
            birim = next((c for c in komut if c.isalpha()), 's')
            miktar = int(''.join(filter(str.isdigit, komut)))
            saniye = miktar if birim == 's' else (miktar * 60 if birim == 'm' else miktar * 3600)
            hatirlatici_kur(saniye, f"{miktar}{birim} süre doldu, hatırlatmamı istemiştin.")
            return "Emrin başım üstüne, zamanı gelince seni bilgilendireceğim."
        except:
            return "Format: !Hatırlats5, !Hatırlatm10"

    gecmis = hafizayi_oku()
    anlik_zaman = get_tr_zaman()
    client = genai.Client(api_key=random.choice(API_KEYS_POOL))
    config = types.GenerateContentConfig(
        system_instruction=f"Şu an: {anlik_zaman}. Geçmiş sohbet:\n{gecmis}\n\nReis'e delikanlıca cevap ver ve gerekirse hatırlatıcıları yönet.",
        temperature=0.7
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"[TR Saat: {anlik_zaman}] {kullanici_mesaji}",
        config=config
    )
    cevap = response.text.strip()

    # Hafızaya kaydet
    if not dis_tetikleyici:
        hafizaya_yaz("Siz", kullanici_mesaji)
        hafizaya_yaz("Aslan Parçası", cevap)

    return cevap

def sistemi_baslat():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("ASLAN PARÇASI V8.9 (HAFIZA MODU AKTİF - 200 LİMİT)")
    secim = input("\nSeçim (1: Kurucu, 2: Misafir): ")
    aktif_kullanici = "Ayaz Reis" if (secim == "1" and getpass.getpass("🔑 Şifre: ") == KURUCU_SIFRESI) else "Misafir"

    print(f"\n--- Sistem Hazır | Mod: {aktif_kullanici} | Hafıza Yüklendi ---")
    while True:
        mesaj = input("\nSiz: ").strip()
        if mesaj.lower() == "çıkış": break
        if not mesaj: continue
        cevap = aslan_parcasi_ai_cevap(mesaj, aktif_kullanici)
        print(f"\n🤖 Aslan Parçası: {cevap}")

if __name__ == "__main__":
    sistemi_baslat()
