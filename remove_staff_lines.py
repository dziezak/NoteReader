import cv2
import os
import numpy as np

# ----------------------------
# 📁 Foldery
# ----------------------------
INPUT_FOLDER = "generated_sheets"
OUTPUT_FOLDER = "staff_removed"
DEBUG_FOLDER = "debug_staff"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(DEBUG_FOLDER, exist_ok=True)

# ----------------------------
# ⚙️ Parametry
# ----------------------------
THRESHOLD = 200
HORIZONTAL_KERNEL_WIDTH = 40   # długość wykrywanej linii
LINE_THICKNESS = 3             # grubość linii do usunięcia

# ----------------------------
# 🔁 Przetwarzanie plików
# ----------------------------
for file in os.listdir(INPUT_FOLDER):
    if not file.lower().endswith(".png"):
        continue

    path = os.path.join(INPUT_FOLDER, file)
    print(f"\n📄 Przetwarzanie: {file}")

    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("❌ Nie udało się wczytać")
        continue

    # ----------------------------
    # 1️⃣ Binaryzacja
    # ----------------------------
    _, thresh = cv2.threshold(img, THRESHOLD, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite(f"{DEBUG_FOLDER}/debug_thresh_{file}", thresh)

    # ----------------------------
    # 2️⃣ Wykrycie poziomych linii
    # ----------------------------
    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT, (HORIZONTAL_KERNEL_WIDTH, 1)
    )

    detected_lines = cv2.morphologyEx(
        thresh, cv2.MORPH_OPEN, kernel, iterations=1
    )

    cv2.imwrite(f"{DEBUG_FOLDER}/debug_detected_lines_{file}", detected_lines)

    # ----------------------------
    # 3️⃣ Poszerzenie linii (maski)
    # ----------------------------
    kernel_thick = cv2.getStructuringElement(
        cv2.MORPH_RECT, (1, LINE_THICKNESS)
    )

    lines_mask = cv2.dilate(detected_lines, kernel_thick, iterations=1)
    cv2.imwrite(f"{DEBUG_FOLDER}/debug_lines_mask_{file}", lines_mask)

    # ----------------------------
    # 4️⃣ Usunięcie linii (inpainting)
    # ----------------------------
    img_no_lines = cv2.inpaint(
        img, lines_mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA
    )

    # ----------------------------
    # 5️⃣ Zapis
    # ----------------------------
    out_path = os.path.join(OUTPUT_FOLDER, file)
    cv2.imwrite(out_path, img_no_lines)

    print("✅ Usunięto pięciolinię")

print("\n🎉 Wszystkie obrazy przetworzone.")
