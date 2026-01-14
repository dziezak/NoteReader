import os

BASE_DIR = "data_symbols_font"

OLD_NAME = "półnuta"
NEW_NAME = "polnuta"

old_dir = os.path.join(BASE_DIR, OLD_NAME)
new_dir = os.path.join(BASE_DIR, NEW_NAME)

# ----------------------------
# 1️⃣ Sprawdzenie
# ----------------------------
if not os.path.isdir(old_dir):
    raise FileNotFoundError(f"❌ Nie znaleziono folderu: {old_dir}")

if os.path.exists(new_dir):
    raise FileExistsError(f"❌ Folder docelowy już istnieje: {new_dir}")

# ----------------------------
# 2️⃣ Zmiana nazw plików
# ----------------------------
for filename in os.listdir(old_dir):
    if not filename.lower().endswith(".png"):
        continue

    old_path = os.path.join(old_dir, filename)

    if OLD_NAME not in filename:
        continue

    new_filename = filename.replace(OLD_NAME, NEW_NAME)
    new_path = os.path.join(old_dir, new_filename)

    os.rename(old_path, new_path)
    print(f"📝 {filename} → {new_filename}")

# ----------------------------
# 3️⃣ Zmiana nazwy folderu
# ----------------------------
os.rename(old_dir, new_dir)
print(f"\n📂 Folder zmieniony: {OLD_NAME} → {NEW_NAME}")

print("\n✅ Gotowe. Dane zachowane.")
