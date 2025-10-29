
# generate_symbols_font.py
import os
from PIL import Image, ImageFont, ImageFilter, ImageOps, ImageDraw, ImageChops
import random
import numpy as np


OUT_DIR = "data_symbols_font"
FONT_PATH = os.path.join(os.path.dirname(__file__), "Bravura.otf")
IMG_SIZE = (128, 128)
N_PER_CLASS = 200

# Kody SMuFL dla symboli muzycznych
SYMBOLS = {
    "klucz_wiolinowy": "\uE050",
    "klucz_basowy": "\uE062",
    "nuta": "\uE1D5",
    "półnuta": "\uE1D3",
    "ćwierćnuta": "\uE1D2",
    "usemka": "\uE1D7",
    "pauza_cwierc": "\uE4E5",
    "pauza_usemka": "\uE4E6",
    "pauza_pólnuta": "\uE4E4",
    "pauza_nuta": "\uE4E3",
}

def generate_symbol(symbol_name, code, idx, font):
    # Tworzymy pusty obrazek grayscale (czarny symbol na białym tle)
    img = Image.new("L", IMG_SIZE, 255)
    draw = ImageDraw.Draw(img)

    # Obliczamy wielkość symbolu
    bbox = draw.textbbox((0, 0), code, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # Wyśrodkowanie symbolu
    x = (IMG_SIZE[0] - w) / 2
    y = (IMG_SIZE[1] - h) / 2

    # Rysujemy symbol
    draw.text((x, y), code, font=font, fill=0)

    # Zapisujemy obrazek
    out_path = os.path.join(OUT_DIR, symbol_name, f"{symbol_name}_{idx}.png")
    img.save(out_path)






if __name__ == "__main__":
    # Sprawdzamy, czy czcionka istnieje
    print("🔎 Szukam czcionki pod ścieżką:", FONT_PATH)
    print("Istnieje?", os.path.exists(FONT_PATH))

    if not os.path.exists(FONT_PATH):
        raise FileNotFoundError(f"❌ Nie znaleziono czcionki {FONT_PATH}. Umieść ją w tym samym folderze co skrypt.")

    # Ładujemy font
    font = ImageFont.truetype(FONT_PATH, 100)

    # Tworzymy katalogi
    os.makedirs(OUT_DIR, exist_ok=True)
    for sym in SYMBOLS:
        os.makedirs(os.path.join(OUT_DIR, sym), exist_ok=True)
        for i in range(N_PER_CLASS):
            generate_symbol(sym, SYMBOLS[sym], i, font)

    print("✅ Wygenerowano symbole muzyczne w katalogu:", OUT_DIR)
