import os
import subprocess
import whisper
from pathlib import Path

# === AYARLAR ===
kaynak_klasor = r"C:\Users\tunah\OneDrive\Masaüstü\ses dosyaları"
parca_suresi_dk = 30  # Dakika
model_adi = "small"   # "tiny", "base", "small", "medium", "large"

# === MODELİ YÜKLE ===a
model = whisper.load_model(model_adi)

# === SES DOSYALARINI LİSTELE ===
ses_uzantilari = [".mp3", ".wav", ".mp4", ".m4a"]
ses_dosyalari = [f for f in os.listdir(kaynak_klasor) if Path(f).suffix in ses_uzantilari]

for dosya in ses_dosyalari:
    tam_yol = os.path.join(kaynak_klasor, dosya)
    dosya_adi = Path(dosya).stem
    cikti_klasor = os.path.join(kaynak_klasor, dosya_adi + "_parcalar")
    os.makedirs(cikti_klasor, exist_ok=True)

    # === 30 DAKİKALIK PARÇALARA BÖL ===
    bolme_komutu = f'ffmpeg -i "{tam_yol}" -f segment -segment_time {parca_suresi_dk*60} -c copy "{cikti_klasor}\\{dosya_adi}_parca_%03d.mp3"'
    subprocess.run(bolme_komutu, shell=True)

    # === HER PARÇAYI TRANSKRİBE ET ===
    parcali_dosyalar = sorted([f for f in os.listdir(cikti_klasor) if f.endswith(".mp3")])
    for parca in parcali_dosyalar:
        parca_yolu = os.path.join(cikti_klasor, parca)
        print(f"İşleniyor: {parca_yolu}")
        sonuc = model.transcribe(parca_yolu, language="tr")

        txt_yol = os.path.splitext(parca_yolu)[0] + ".txt"
        with open(txt_yol, "w", encoding="utf-8") as f:
            f.write(sonuc["text"])

print("\n✅ Tamamlandı! Tüm metin dosyaları klasörlerde.")
