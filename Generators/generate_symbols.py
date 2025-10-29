import os
import random
import math
from PIL import Image, ImageDraw, ImageOps, ImageFilter

# Katalog wyjściowy
OUTPUT_DIR = "data_symbols"

# Kategorie symboli
CATEGORIES = [
    "klucz_wiolinowy",
    "klucz_basowy",
    "nuta_cwierc",
    "nuta_pol",
    "nuta_cala",
    "nuta_cwierc_odwrotna",
    "nuta_usemka",
    "nuta_usemka_odwrotna",
    "pauza_cwierc",
    "pauza_pol",
    "pauza_cala",
    "pauza_usemka"
]

IMG_SIZE = 128
IMAGES_PER_CLASS = 500

def create_dirs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for c in CATEGORIES:
        os.makedirs(os.path.join(OUTPUT_DIR, c), exist_ok=True)

def random_offset(value, delta=10):
    return value + random.randint(-delta, delta)

def draw_note(draw, inverted=False, with_flag=False, hollow=False):
    # Pozycja nuty
    x = random.randint(30, 90)
    y = random.randint(30, 90)
    # Główka nuty
    fill = 255 if hollow else 0
    outline = 0
    draw.ellipse((x, y, x+20, y+14), outline=outline, fill=fill)
    # Laseczka
    if inverted:
        draw.line((x+5, y, x+5, y-35), fill=0, width=3)
        if with_flag:
            draw.arc((x-10, y-50, x+20, y-20), 0, 180, fill=0, width=2)
    else:
        draw.line((x+20, y+14, x+20, y+50), fill=0, width=3)
        if with_flag:
            draw.arc((x+10, y+40, x+40, y+70), 180, 360, fill=0, width=2)

def draw_pause(draw, style):
    x = 40
    y = 50
    if style == "cwierc":
        draw.rectangle((x, y, x+10, y+20), fill=0)
    elif style == "pol":
        draw.rectangle((x, y, x+20, y+5), fill=0)
    elif style == "cala":
        draw.rectangle((x, y+10, x+20, y+5), fill=0)
    elif style == "usemka":
        draw.arc((x, y, x+30, y+30), 0, 180, fill=0, width=2)

def draw_clef(draw, clef_type):
    if clef_type == "wiolinowy":
        # spiralna kreska
        cx, cy = 64, 64
        for t in range(0, 720, 10):
            angle = math.radians(t)
            r = t / 20
            x = cx + int(r * math.cos(angle))
            y = cy + int(r * math.sin(angle))
            draw.ellipse((x, y, x+2, y+2), fill=0)
    elif clef_type == "basowy":
        # dwie kropki i półkole
        draw.arc((40, 40, 100, 100), 200, 340, fill=0, width=3)
        draw.ellipse((95, 55, 100, 60), fill=0)
        draw.ellipse((95, 70, 100, 75), fill=0)

def generate_image(category):
    img = Image.new("L", (IMG_SIZE, IMG_SIZE), 255)
    draw = ImageDraw.Draw(img)

    if "nuta" in category:
        inverted = "odwrotna" in category
        hollow = "pol" in category or "cala" in category
        with_flag = "usemka" in category
        draw_note(draw, inverted=inverted, with_flag=with_flag, hollow=hollow)
    elif "pauza" in category:
        if "cwierc" in category: draw_pause(draw, "cwierc")
        elif "pol" in category: draw_pause(draw, "pol")
        elif "cala" in category: draw_pause(draw, "cala")
        elif "usemka" in category: draw_pause(draw, "usemka")
    elif "klucz_wiolinowy" in category:
        draw_clef(draw, "wiolinowy")
    elif "klucz_basowy" in category:
        draw_clef(draw, "basowy")

    # Losowa rotacja i szum
    img = img.rotate(random.randint(-15, 15), fillcolor=255)
    img = ImageOps.autocontrast(img)
    img = img.filter(ImageFilter.GaussianBlur(random.uniform(0, 0.8)))

    return img

def main():
    create_dirs()
    for c in CATEGORIES:
        print(f"Generuję {IMAGES_PER_CLASS} obrazków dla {c}...")
        for i in range(IMAGES_PER_CLASS):
            img = generate_image(c)
            filename = os.path.join(OUTPUT_DIR, c, f"{c}_{i:04d}.png")
            img.save(filename)

if __name__ == "__main__":
    main()
