import os
import random
from PIL import Image, ImageDraw
import numpy as np

# -------------------------
# 🔧 Ustawienia
# -------------------------
SYMBOLS_DIR = "data_symbols_font"  # folder z klasami nut (tak jak przy treningu)
OUTPUT_DIR = "generated_sheets"
IMG_HEIGHT = 200
IMG_WIDTH = 800
NUM_SYMBOLS = 10  # ile symboli na obrazku
STAFF_LINE_SPACING = 15  # odstęp między liniami pięciolinii
STAFF_TOP = 60  # pozycja pierwszej linii od góry

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------
# 🎼 Funkcja: rysowanie pięciolinii
# -------------------------
def draw_staff(draw, top, width):
    for i in range(5):
        y = top + i * STAFF_LINE_SPACING
        draw.line((20, y, width - 20, y), fill=0, width=2)

# -------------------------
# 🎵 Funkcja: generowanie jednej losowej pięciolinii
# -------------------------
def generate_random_sheet(filename="random_sheet.png"):
    # Pusta biała kartka
    sheet = Image.new("L", (IMG_WIDTH, IMG_HEIGHT), color=255)
    draw = ImageDraw.Draw(sheet)
    draw_staff(draw, STAFF_TOP, IMG_WIDTH)

    # Pobranie wszystkich możliwych klas symboli
    classes = [d for d in os.listdir(SYMBOLS_DIR) if os.path.isdir(os.path.join(SYMBOLS_DIR, d))]
    print("Dostępne klasy:", classes)

    # Losowe rozmieszczenie symboli
    x_pos = 40
    for _ in range(NUM_SYMBOLS):
        cls = random.choice(classes)
        cls_dir = os.path.join(SYMBOLS_DIR, cls)
        symbol_file = random.choice(os.listdir(cls_dir))
        symbol_path = os.path.join(cls_dir, symbol_file)

        # Wczytanie symbolu
        symbol = Image.open(symbol_path).convert("L")
        symbol = symbol.resize((random.randint(30, 60), random.randint(30, 60)))

        # Losowa wysokość (z pewnym ograniczeniem, żeby było w obrębie pięciolinii)
        y_offset = STAFF_TOP - random.randint(10, 30)
        sheet.paste(symbol, (x_pos, y_offset), symbol if symbol.mode == 'RGBA' else None)
        x_pos += random.randint(60, 100)

        if x_pos > IMG_WIDTH - 60:
            break

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
