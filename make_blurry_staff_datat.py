import os
import cv2
import numpy as np
from pathlib import Path

INPUT_DIR = Path("data_symbols_font")
OUTPUT_DIR = Path("data_symbols_font_blury")

THRESHOLD = 200
HORIZONTAL_KERNEL_WIDTH = 30
LINE_THICKNESS = 3

os.makedirs(OUTPUT_DIR, exist_ok=True)


def apply_staff_removal_artifact(img):
    h, w = img.shape
    work = img.copy()

    # 0. Dodanie losowej cienkiej linii
    y = np.random.randint(int(h * 0.2), int(h * 0.8))
    cv2.line(work, (0, y), (w, y), color=0, thickness=1)

    # 1. Binaryzacja
    _, thresh = cv2.threshold(work, THRESHOLD, 255, cv2.THRESH_BINARY_INV)

    # 2. Wykrycie poziomych linii
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (HORIZONTAL_KERNEL_WIDTH, 1))
    detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

    # 3. Poszerzenie maski
    kernel_thick = cv2.getStructuringElement(cv2.MORPH_RECT, (1, LINE_THICKNESS))
    lines_mask = cv2.dilate(detected_lines, kernel_thick, iterations=1)

    # 4. Inpainting
    result = cv2.inpaint(work, lines_mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
    return result


print("🔄 Generowanie danych...\n")

for class_dir in INPUT_DIR.iterdir():
    if not class_dir.is_dir():
        continue

    out_class = OUTPUT_DIR / class_dir.name
    out_class.mkdir(parents=True, exist_ok=True)

    print(f"📂 Klasa: {class_dir.name}")

    # tylko pliki PNG w tym folderze — żadnych podfolderów
    for img_path in class_dir.glob("*.png"):

        img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)

        if img is None:
            print(f"⚠️ Nie mogę wczytać: {img_path}")
            continue

        aug = apply_staff_removal_artifact(img)

        out_path = out_class / img_path.name
        cv2.imwrite(str(out_path), aug)

print("\n✅ Dataset utworzony:", OUTPUT_DIR)
