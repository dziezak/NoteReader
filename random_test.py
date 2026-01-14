import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt
import os
import random

# -------------------------
# 🔧 Ustawienia
# -------------------------
IMG_SIZE = (128, 128)
MODEL_PATH = "models/light_cnn_notes_final.keras"  # albo best_light_cnn.keras
NORMAL_FOLDER = "data_symbols_font"
BLURRY_FOLDER = "data_symbols_font_blury"

# -------------------------
# 🧠 Wczytanie modelu
# -------------------------
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Nie znaleziono modelu pod ścieżką: {MODEL_PATH}")

model = load_model(MODEL_PATH)
print("✅ Model wczytany pomyślnie.")

# Kolejność klas musi być identyczna jak przy treningu
class_names = [
    "klucz_basowy",
    "klucz_wiolinowy",
    "nuta",
    "pauza_cwierc",
    "pauza_nuta",
    "pauza_polnuta",
    "pauza_usemka",
    "polnuta",
    "usemka",
    "cwiercnuta"
]

# -------------------------
# 🔄 Wybór danych do testu
# -------------------------
choice = input("Testować z normalnych danych (n) czy blurry (b)? [n/b]: ").strip().lower()
if choice == "b":
    DATA_FOLDER = BLURRY_FOLDER
else:
    DATA_FOLDER = NORMAL_FOLDER

# -------------------------
# 🎲 Losowanie pliku
# -------------------------
# Zbierz wszystkie pliki w folderach klas
all_files = []
for root, dirs, files in os.walk(DATA_FOLDER):
    for f in files:
        if f.lower().endswith(".png"):
            all_files.append(os.path.join(root, f))

if not all_files:
    raise FileNotFoundError(f"Brak plików .png w folderze {DATA_FOLDER}")

random_file = random.choice(all_files)
print(f"\n🧩 Testowany obrazek: {random_file}")

# -------------------------
# 🖼️ Wczytanie i przygotowanie obrazka
# -------------------------
img = image.load_img(random_file, color_mode="grayscale", target_size=IMG_SIZE)
img_array = image.img_to_array(img)
img_array = img_array / 255.0
img_array = np.expand_dims(img_array, axis=0)  # batch size = 1

# -------------------------
# 🔮 Predykcja
# -------------------------
predictions = model.predict(img_array)
predicted_index = np.argmax(predictions)
predicted_label = class_names[predicted_index]

print(f"\nObrazek '{os.path.basename(random_file)}' został sklasyfikowany jako: {predicted_label}")
print("🔢 Wyniki predykcji (softmax):", np.round(predictions[0], 3))

# -------------------------
# 🖼️ Wizualizacja
# -------------------------
plt.imshow(img_array[0].squeeze(), cmap="gray")
plt.title(f"Predykcja: {predicted_label}")
plt.axis('off')
plt.show()
