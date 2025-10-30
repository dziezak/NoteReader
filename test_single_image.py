import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt
import os

# -------------------------
# 🔧 Ustawienia
# -------------------------
IMG_SIZE = (128, 128)
MODEL_PATH = "models/best_light_cnn.keras"  # ścieżka do zapisanego modelu
TEST_IMAGE_PATH = "test_półnuta.png"                     # ścieżka do obrazka do przetestowania

# -------------------------
# 🧠 Wczytanie modelu
# -------------------------
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ Nie znaleziono modelu pod ścieżką: {MODEL_PATH}")

model = load_model(MODEL_PATH)
print("✅ Model wczytany pomyślnie.")

# Jeśli chcesz znać nazwy klas – upewnij się, że są takie same jak w treningu:
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
# 🧩 Wczytanie i przygotowanie obrazka
# -------------------------
if not os.path.exists(TEST_IMAGE_PATH):
    raise FileNotFoundError(f"❌ Nie znaleziono pliku obrazu: {TEST_IMAGE_PATH}")

print(f"\n🧩 Testuję pojedynczy obrazek: {TEST_IMAGE_PATH}")

img = image.load_img(TEST_IMAGE_PATH, color_mode="grayscale", target_size=IMG_SIZE)
img_array = image.img_to_array(img)

print("Przed normalizacją:", np.min(img_array), np.max(img_array), img_array.shape)

# Normalizacja i przygotowanie batcha
img_array = img_array / 255.0
img_array = np.expand_dims(img_array, axis=0)

print("Po normalizacji i batch:", np.min(img_array), np.max(img_array), img_array.shape, img_array.dtype)

# -------------------------
# 🔮 Predykcja
# -------------------------
predictions = model.predict(img_array)
predicted_index = np.argmax(predictions)
predicted_label = class_names[predicted_index]

print(f"\n➡️ Obrazek '{os.path.basename(TEST_IMAGE_PATH)}' został sklasyfikowany jako: {predicted_label}")
print("🔢 Wyniki predykcji (softmax):", np.round(predictions[0], 3))

# -------------------------
# 🖼️ Wizualizacja
# -------------------------
plt.imshow(img_array[0].squeeze(), cmap="gray")
plt.title(f"Predykcja: {predicted_label}")
plt.axis('off')
plt.show()
