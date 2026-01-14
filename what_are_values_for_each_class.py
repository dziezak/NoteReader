import os
import random
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt

# -------------------------
MODEL_PATH = "models/best_light_cnn.keras"
IMG_SIZE = (128, 128)
DATA_DIR = "data_symbols_font"

# -------------------------
# Wczytanie modelu
model = load_model(MODEL_PATH)
print("✅ Model wczytany")

# -------------------------
# Lista klas
class_names = sorted([d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))])
print("Klasy:", class_names)

# -------------------------
# Predykcja dla przykładowego obrazka z każdej klasy
for cls in class_names:
    cls_path = os.path.join(DATA_DIR, cls)
    files = [f for f in os.listdir(cls_path) if f.lower().endswith(".png")]
    
    if not files:
        continue

    # Losowy obrazek z klasy
    img_file = random.choice(files)
    img_path = os.path.join(cls_path, img_file)
    
    # Wczytanie i przygotowanie
    img = image.load_img(img_path, color_mode="grayscale", target_size=IMG_SIZE)
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predykcja
    pred = model.predict(img_array)
    pred_idx = np.argmax(pred)
    pred_label = class_names[pred_idx]

    print(f"\nKlasa: {cls}")
    print(f"Plik: {img_file}")
    print(f"Predykcja: {pred_label}")
    print(f"Softmax: {np.round(pred[0], 3)}")

    # Wizualizacja
    plt.imshow(img_array[0].squeeze(), cmap="gray")
    plt.title(f"Rzeczywista: {cls} | Predykcja: {pred_label}")
    plt.axis("off")
    plt.show()
