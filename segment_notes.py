import cv2
import os
import numpy as np

INPUT_FOLDER = "staff_removed"   # ⬅️ WAŻNE
OUTPUT_FOLDER = "to_check"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

MIN_WIDTH = 8
MIN_HEIGHT = 8

def sort_contours_left_to_right(contours):
    boxes = [cv2.boundingRect(c) for c in contours]
    idxs = sorted(range(len(boxes)), key=lambda i: boxes[i][0])
    return [contours[i] for i in idxs], [boxes[i] for i in idxs]

for fname in os.listdir(INPUT_FOLDER):
    if not fname.lower().endswith(".png"):
        continue

    path = os.path.join(INPUT_FOLDER, fname)
    print(f"\n📄 Segmentacja: {fname}")

    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        continue

    # Binaryzacja
    thresh = cv2.adaptiveThreshold(
        img, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        35, 10
    )

    # Morfologia
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)

    contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours, boxes = sort_contours_left_to_right(contours)

    img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    saved = 0

    for cnt, (x,y,w,h) in zip(contours, boxes):
        if w < MIN_WIDTH or h < MIN_HEIGHT:
            continue

        pad = 4
        x0, y0 = max(0,x-pad), max(0,y-pad)
        x1, y1 = min(img.shape[1], x+w+pad), min(img.shape[0], y+h+pad)

        roi = img[y0:y1, x0:x1]
        out_name = f"{os.path.splitext(fname)[0]}_sym_{saved}.png"
        cv2.imwrite(os.path.join(OUTPUT_FOLDER, out_name), roi)

        cv2.rectangle(img_color, (x0,y0), (x1,y1), (0,255,0), 1)
        saved += 1

    cv2.imwrite(os.path.join(OUTPUT_FOLDER, f"debug_boxes_{fname}"), img_color)
    print(f"✅ Wycięto symboli: {saved}")

print("\n🎉 Segmentacja zakończona.")
