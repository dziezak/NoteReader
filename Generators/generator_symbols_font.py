# generate_symbols_font.py
import os
import random
from PIL import Image, ImageDraw, ImageFont
import sys

# --- Ustawienia ---
OUT_DIR = "data_symbols_font"
FONT_PATH = os.path.join(os.path.dirname(__file__), "Bravura.otf")
IMG_SIZE = (128, 128)
N_PER_CLASS = 200

# Symbole muzyczne (SMuFL – Bravura)
SYMBOLS = {
    "klucz_wiolinowy": "\uE050",
    "klucz_basowy":    "\uE062",
    "nuta":            "\uE1D5",
    "półnuta":         "\uE1D3",
    "ćwierćnuta":      "\uE1D2",
    "usemka":          "\uE1D7",
    "pauza_cwierc":    "\uE4E5",
    "pauza_usemka":    "\uE4E6",
    "pauza_pólnuta":   "\uE4E4",
    "pauza_nuta":      "\uE4E3",
}

MARGIN = 6
SHIFT_RANGE = 10  # maksymalne przesunięcie w pikselach


def find_max_font_size(code, font_path, img_size, margin):
    """Dobiera największy rozmiar czcionki, który zmieści symbol w obrazku."""
    max_try = 300
    min_try = 6
    w_img, h_img = img_size

    size = min(max_try, int(min(w_img, h_img) * 1.2))
    while size >= min_try:
        font = ImageFont.truetype(font_path, size)
        im = Image.new("L", (1, 1), 255)
        draw = ImageDraw.Draw(im)
        bbox = draw.textbbox((0, 0), code, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        if w + 2 * margin <= w_img and h + 2 * margin <= h_img:
            return size
        size -= 2
    return min_try


def render_symbol_image(code, font, shift=True):
    """Renderuje symbol na środku obrazka z ewentualnym lekkim przesunięciem."""
    img = Image.new("L", IMG_SIZE, 255)
    draw = ImageDraw.Draw(img)

    bbox = draw.textbbox((0, 0), code, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    x = (IMG_SIZE[0] - w) / 2 - bbox[0]
    y = (IMG_SIZE[1] - h) / 2 - bbox[1]

    if shift:
        x += random.randint(-SHIFT_RANGE, SHIFT_RANGE)
        y += random.randint(-SHIFT_RANGE, SHIFT_RANGE)

    draw.text((x, y), code, font=font, fill=0)
    return img


def main():
    print("🔎 Szukam czcionki pod ścieżką:", FONT_PATH)
    if not os.path.exists(FONT_PATH):
        print(f"❌ Nie znaleziono czcionki: {FONT_PATH}")
        print("Umieść plik Bravura.otf w tym samym katalogu co skrypt.")
        sys.exit(1)

    os.makedirs(OUT_DIR, exist_ok=True)

    for name, code in SYMBOLS.items():
        target_dir = os.path.join(OUT_DIR, name)
        os.makedirs(target_dir, exist_ok=True)

        font_size = find_max_font_size(code, FONT_PATH, IMG_SIZE, MARGIN)
        font = ImageFont.truetype(FONT_PATH, font_size)
        print(f"🖋 Generuję {N_PER_CLASS} obrazków dla '{name}' (font size={font_size})...")

        for i in range(N_PER_CLASS):
            img = render_symbol_image(code, font, shift=True)
            filename = os.path.join(target_dir, f"{name}_{i:04d}.png")
            img.save(filename)

    print("✅ Gotowe — wygenerowano symbole w katalogu:", OUT_DIR)


if __name__ == "__main__":
    main()
