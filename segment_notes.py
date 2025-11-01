import cv2
import os

# ----------------------------
# 📁 Konfiguracja folderów
# ----------------------------
INPUT_FOLDER = "generated_sheets"
OUTPUT_FOLDER = "to_check"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ----------------------------
# ⚙️ Parametry segmentacji
# ----------------------------
MIN_WIDTH = 5       # minimalna szerokość konturu
MIN_HEIGHT = 5      # minimalna wysokość konturu
THRESHOLD_VALUE = 200  # próg binarnego progowania (0–255)

# ----------------------------
# 🧩 Przetwarzanie każdego obrazu
# ----------------------------
for file in os.listdir(INPUT_FOLDER):
    if not file.lower().endswith(".png"):
        continue

    path = os.path.join(INPUT_FOLDER, file)
    print(f"\n📄 Przetwarzanie: {path}")
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"❌ Nie udało się wczytać obrazu: {path}")
        continue

    # ----------------------------
    # 🔲 Progowanie (inwersja)
    # ----------------------------
    _, thresh = cv2.threshold(img, THRESHOLD_VALUE, 255, cv2.THRESH_BINARY_INV)
    debug_thresh_path = os.path.join(OUTPUT_FOLDER, f"debug_thresh_{file}")
    cv2.imwrite(debug_thresh_path, thresh)
    print(f"💾 Zapisano obraz progowany: {debug_thresh_path}")

    # ----------------------------
    # 🔍 Znajdź kontury
    # ----------------------------
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"🔍 Znaleziono konturów: {len(contours)}")

    # Kopia oryginalnego obrazu do wizualizacji
    img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    count = 0

    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        print(f"➡️ Kontur {i}: x={x}, y={y}, w={w}, h={h}")

        # ----------------------------
        # ✂️ Wycinanie nut
        # ----------------------------
        if w > MIN_WIDTH and h > MIN_HEIGHT:
            roi = img[y:y+h, x:x+w]
            out_name = f"{os.path.splitext(file)[0]}_{count}.png"
            out_path = os.path.join(OUTPUT_FOLDER, out_name)
            cv2.imwrite(out_path, roi)
            cv2.rectangle(img_color, (x, y), (x + w, y + h), (0, 255, 0), 1)
            count += 1

    # ----------------------------
    # 💾 Zapisz obraz z ramkami
    # ----------------------------
    debug_boxes_path = os.path.join(OUTPUT_FOLDER, f"debug_boxes_{file}")
    cv2.imwrite(debug_boxes_path, img_color)
    print(f"💾 Zapisano obraz z ramkami: {debug_boxes_path}")

    print(f"✅ Gotowe — wycięto {count} symboli.")

print("\n🎉 Zakończono segmentację wszystkich obrazów.")
