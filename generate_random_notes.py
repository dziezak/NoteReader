import os
import random
from PIL import Image, ImageDraw

# -------------------------
# 🔧 Ustawienia
# -------------------------
SYMBOLS_DIR = "data_symbols_font"
OUTPUT_DIR = "generated_sheets"
IMG_HEIGHT = 200
IMG_WIDTH = 800
NUM_SYMBOLS = 10
STAFF_LINE_SPACING = 15
STAFF_TOP = 60

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------
# 🎼 Funkcja: rysowanie pięciolinii
# -------------------------
def draw_staff(draw, top, width):
    for i in range(5):
        y = top + i * STAFF_LINE_SPACING
        draw.line((20, y, width - 20, y), fill=0, width=2)

# -------------------------
# 🎵 Generowanie jednej nutowej kartki
# -------------------------
def generate_random_sheet(filename="random_sheet.png"):
    # Biała kartka
    sheet = Image.new("L", (IMG_WIDTH, IMG_HEIGHT), color=255)
    draw = ImageDraw.Draw(sheet)

    # 1️⃣ Rysujemy pięciolinię
    draw_staff(draw, STAFF_TOP, IMG_WIDTH)

    # Pobieramy klasy symboli
    classes = [d for d in os.listdir(SYMBOLS_DIR) if os.path.isdir(os.path.join(SYMBOLS_DIR, d))]
    print("Dostępne klasy:", classes)

    x_pos = 40

    # 2️⃣ Wklejamy symbole
    for _ in range(NUM_SYMBOLS):
        cls = random.choice(classes)
        cls_dir = os.path.join(SYMBOLS_DIR, cls)
        symbol_file = random.choice(os.listdir(cls_dir))
        symbol_path = os.path.join(cls_dir, symbol_file)

        symbol = Image.open(symbol_path).convert("L")
        symbol = symbol.resize((random.randint(30, 60), random.randint(30, 60)))

        y_offset = STAFF_TOP - random.randint(10, 30)

        # Wklejamy z białym tłem — NIE PRZEJMUJEMY SIĘ TYM
        sheet.paste(symbol, (x_pos, y_offset))

        x_pos += random.randint(60, 100)
        if x_pos > IMG_WIDTH - 60:
            break

    # 3️⃣ Rysujemy pięciolinię JESZCZE RAZ (co zakryje przerwy)
    draw = ImageDraw.Draw(sheet)
    draw_staff(draw, STAFF_TOP, IMG_WIDTH)

    # Zapis
    output_path = os.path.join(OUTPUT_DIR, filename)
    sheet.save(output_path)
    print(f"✅ Zapisano: {output_path}")

# -------------------------
# 🔄 Główna pętla
# -------------------------
if __name__ == "__main__":
    for i in range(5):
        generate_random_sheet(f"sheet_{i+1}.png")

