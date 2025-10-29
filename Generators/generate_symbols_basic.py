# generate_symbols_basic.py
import os
import random
from PIL import Image, ImageDraw

OUT_DIR = "data_symbols"
SYMBOLS = [
    "klucz_wiolinowy",
    "klucz_basowy",
    "nuta",
    "półnuta",
    "ćwierćnuta",
    "usemka",
    "pauza_cwierc",
    "pauza_usemka",
    "pauza_pólnuta",
    "pauza_nuta",
]

IMG_SIZE = (128, 128)
N_PER_CLASS = 200


def draw_treble_clef(draw: ImageDraw.Draw):
    w, h = IMG_SIZE
    x, y = w // 2, h // 2
    draw.line((x, y - 40, x, y + 40), fill="black", width=3)
    for i in range(4):
        bbox = (x - 10 + i * 2, y - 10 + i * 2, x + 10 - i * 2, y + 10 - i * 2)
        draw.arc(bbox, start=0, end=360, fill="black")


def draw_bass_clef(draw: ImageDraw.Draw):
    w, h = IMG_SIZE
    x, y = w // 2, h // 2
    draw.arc((x - 30, y - 30, x + 10, y + 30), start=90, end=270, fill="black", width=3)
    draw.ellipse((x + 12, y - 10, x + 18, y - 4), fill="black")
    draw.ellipse((x + 12, y + 4, x + 18, y + 10), fill="black")


def draw_note(draw: ImageDraw.Draw, filled=True, with_flag=False):
    w, h = IMG_SIZE
    x, y = w // 2, h // 2 + 10
    draw.ellipse((x - 10, y - 7, x + 10, y + 7), outline="black", fill="black" if filled else None)
    draw.line((x + 10, y, x + 10, y - 40), fill="black", width=3)
    if with_flag:
        draw.arc((x + 10, y - 50, x + 25, y - 35), start=0, end=180, fill="black", width=2)


def draw_rest(draw: ImageDraw.Draw, type_: str):
    w, h = IMG_SIZE
    if type_ == "pauza_cwierc":
        draw.rectangle((w//2 - 15, h//2 - 5, w//2 + 15, h//2 + 5), fill="black")
    elif type_ == "pauza_usemka":
        draw.arc((w//2 - 10, h//2 - 10, w//2 + 10, h//2 + 10), start=180, end=360, fill="black")
        draw.line((w//2, h//2 + 10, w//2, h//2 + 20), fill="black", width=2)
    elif type_ == "pauza_pólnuta":
        draw.rectangle((w//2 - 20, h//2 - 3, w//2 + 20, h//2), fill="black")
    elif type_ == "pauza_nuta":
        draw.rectangle((w//2 - 20, h//2, w//2 + 20, h//2 + 3), fill="black")


def generate_symbol(symbol_name: str, idx: int):
    img = Image.new("L", IMG_SIZE, 255)
    draw = ImageDraw.Draw(img)

    if symbol_name == "klucz_wiolinowy":
        draw_treble_clef(draw)
    elif symbol_name == "klucz_basowy":
        draw_bass_clef(draw)
    elif symbol_name == "nuta":
        draw_note(draw, filled=True)
    elif symbol_name == "półnuta":
        draw_note(draw, filled=False)
    elif symbol_name == "ćwierćnuta":
        draw_note(draw, filled=True)
    elif symbol_name == "usemka":
        draw_note(draw, filled=True, with_flag=True)
    elif "pauza" in symbol_name:
        draw_rest(draw, symbol_name)

    img.save(os.path.join(OUT_DIR, symbol_name, f"{symbol_name}_{idx}.png"))


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    for sym in SYMBOLS:
        os.makedirs(os.path.join(OUT_DIR, sym), exist_ok=True)
        for i in range(N_PER_CLASS):
            generate_symbol(sym, i)
    print("✅ Wygenerowano wszystkie symbole w katalogu:", OUT_DIR)
