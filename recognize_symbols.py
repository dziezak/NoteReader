import os
import cv2
import csv
import numpy as np
from tensorflow.keras.models import load_model

# -------------------------
# 🔧 Ustawienia
# -------------------------
IMG_SIZE = (128, 128)
MODEL_PATH = "models/best_light_cnn.keras"
INPUT_FOLDER = "to_check"
RESIZED_FOLDER = "resized_after_staff_removed"
OUTPUT_CSV = "recognized_symbols.csv"

os.makedirs(RESIZED_FOLDER, exist_ok=True)

class_names = [
    "klucz_basowy",
    "klucz_wiolinowy",
    "nuta",
    "pauza_cwierc",
    "pauza_nuta",
    "pauza_pólnuta",
    "pauza_usemka",
    "półnuta",
    "usemka",
    "ćwierćnuta"
]

# -------------------------
# 🧩 Resize + padding
# -------------------------
def resize_with_padding(img, target_size=(128,128), bg_color=255):
    h, w = img.shape[:2]
    th, tw = target_size

    scale = min(tw / w, th / h)
    new_w = int(w * scale)
    new_h = int(h * scale)

    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    canvas = np.ones((th, tw), dtype=np.uint8) * bg_color
    x_offset = (tw - new_w) // 2
    y_offset = (th - new_h) // 2
    canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized

    return canvas

# -------------------------
# 🧠 Model
# -------------------------
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ Nie znaleziono modelu: {MODEL_PATH}")

model = load_model(MODEL_PATH)
print("✅ Model wczytany.\n")

# -------------------------
# 📄 CSV
# -------------------------
with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["filename", "prediction", "confidence"])

    files = [
        f for f in os.listdir(INPUT_FOLDER)
        if f.lower().endswith(".png") and "_sym_" in f
    ]

    if not files:
        print("⚠️ Brak plików *_sym_*.png w folderze to_check/")
        exit()

    print(f"📦 Znaleziono {len(files)} symboli:\n")

    for file in sorted(files):
        path = os.path.join(INPUT_FOLDER, file)

        # -------------------------
        # 🧩 Wczytaj ROI
        # -------------------------
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print("❌ Nie można wczytać:", file)
            continue

        resized = resize_with_padding(img, IMG_SIZE)

        # -------------------------
        # 💾 ZAPISZ PRZETWORZONY OBRAZ
        # -------------------------
        cv2.imwrite(os.path.join(RESIZED_FOLDER, file), resized)

        # -------------------------
        # 🔮 Predykcja
        # -------------------------
        img_array = resized.astype("float32") / 255.0
        img_array = np.expand_dims(img_array, axis=(0, -1))

        preds = model.predict(img_array, verbose=0)
        index = int(np.argmax(preds))
        label = class_names[index]
        confidence = float(preds[0][index])

        writer.writerow([file, label, confidence])
        print(f"📄 {file:<18} → {label:<15} ({confidence:.2f})")

print(f"\n📑 Wyniki zapisano do: {OUTPUT_CSV}")
print(f"🖼️ Obrazy zapisano do: {RESIZED_FOLDER}/")
print("🎉 Gotowe.")

