import os
import random
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# 🔧 Stałe
# -------------------------
IMG_SIZE = (128, 128)

# -------------------------
# 🔘 Wybór wersji modelu
# -------------------------
print("Wybierz wersję modelu do testów:")
print("1 - CLEAN (font, bez artefaktów)")
print("2 - FINAL (font + augmentacja)")
print("3 - BLURRY (symulacja artefaktów po usuwaniu pięciolinii)")

choice = input("Twój wybór (1/2/3): ").strip()

if choice == "1":
    MODEL_PATH = "models/best_light_cnn.keras"
    DATA_DIR = "data_symbols_font"
    VERSION_NAME = "CLEAN"

elif choice == "2":
    MODEL_PATH = "models/light_cnn_notes_final.keras"
    DATA_DIR = "data_symbols_font"
    VERSION_NAME = "FINAL"

elif choice == "3":
    MODEL_PATH = "models/blurry_model.keras"
    DATA_DIR = "data_symbols_font_blury"
    VERSION_NAME = "BLURRY"

else:
    raise ValueError("❌ Niepoprawny wybór.")

# -------------------------
# 🧠 Wczytanie modelu
# -------------------------
model = load_model(MODEL_PATH)
print(f"\n✅ Model {VERSION_NAME} wczytany")

# -------------------------
# 📚 Lista klas
# -------------------------
class_names = sorted([
    d for d in os.listdir(DATA_DIR)
    if os.path.isdir(os.path.join(DATA_DIR, d))
])

num_classes = len(class_names)
print("📌 Klasy:", class_names)

# -------------------------
# 🖼️ Przygotowanie figure
# -------------------------
cols = 5
rows = int(np.ceil(num_classes / cols))

fig, axes = plt.subplots(rows, cols, figsize=(18, 7))
fig.suptitle(
    f"Test modelu CNN – wersja {VERSION_NAME}",
    fontsize=16,
    fontweight="bold"
)

axes = axes.flatten()

# -------------------------
# 🔍 Test: 1 losowy obrazek z każdej klasy
# -------------------------
for idx, cls in enumerate(class_names):
    cls_path = os.path.join(DATA_DIR, cls)
    files = [f for f in os.listdir(cls_path) if f.lower().endswith(".png")]

    img_file = random.choice(files)
    img_path = os.path.join(cls_path, img_file)

    # Wczytanie
    img = image.load_img(
        img_path,
        color_mode="grayscale",
        target_size=IMG_SIZE
    )
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predykcja
    pred = model.predict(img_array, verbose=0)
    pred_idx = np.argmax(pred)
    pred_label = class_names[pred_idx]

    # Kolor tytułu
    color = "green" if pred_label == cls else "red"

    # Rysowanie
    axes[idx].imshow(img_array[0].squeeze(), cmap="gray")
    axes[idx].set_title(
        f"GT: {cls}\nPred: {pred_label}",
        color=color,
        fontsize=10
    )
    axes[idx].axis("off")

# -------------------------
# Ukrycie pustych pól
# -------------------------
for i in range(idx + 1, len(axes)):
    axes[i].axis("off")

plt.tight_layout()
plt.show()
