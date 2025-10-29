
# generate_symbols_font.py
import os
from PIL import Image, ImageFont

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
    from PIL import Image

    img = Image.new("L", IMG_SIZE, 255)

    # Pobierz maskę symbolu z fontu
    mask_raw = font.getmask(code)

    # Konwertuj ImagingCore → obraz PIL
    mask = Image.frombuffer("L", mask_raw.size, bytes(mask_raw), "raw", "L", 0, 1)

    # Wycentruj
    x = (IMG_SIZE[0] - mask.size[0]) // 2
    y = (IMG_SIZE[1] - mask.size[1]) // 2
    box = (x, y, x + mask.size[0], y + mask.size[1])

    # Wklej symbol jako czarny
    img.paste(0, box, mask)

    # Zapisz do pliku
    img.save(os.path.join(OUT_DIR, symbol_name, f"{symbol_name}_{idx}.png"))





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
