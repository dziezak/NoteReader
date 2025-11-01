# model_symbol.py
import tensorflow as tf
from tensorflow.keras import layers, models
import os
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

IMG_SIZE = (128, 128)
BATCH_SIZE = 32
DATA_DIR = "data_symbols_font"
EPOCHS = 50

# -------------------------
# 🔹 Augmentacja danych
# -------------------------
data_augmentation = tf.keras.Sequential([
    layers.RandomRotation(0.05),
    layers.RandomTranslation(0.1, 0.1),
    layers.RandomZoom(0.1),
    layers.RandomContrast(0.1)
])

# -------------------------
# Tworzenie datasetów
# -------------------------
train_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="training",
    seed=42,
    image_size=IMG_SIZE,
    color_mode="grayscale",
    batch_size=BATCH_SIZE
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="validation",
    seed=42,
    image_size=IMG_SIZE,
    color_mode="grayscale",
    batch_size=BATCH_SIZE
)

# Pobranie nazw klas zanim zastosujemy prefetch
class_names = train_ds.class_names
num_classes = len(class_names)
print("Klasy/znaki rozpoznawane:", class_names)

# Normalizacja pikseli do zakresu [0,1]
train_ds = train_ds.map(lambda x, y: (x / 255.0, y))
val_ds = val_ds.map(lambda x, y: (x / 255.0, y))

# Cache, shuffle, prefetch
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# -------------------------
# 🔹 Uproszczony model CNN (AlexNet-light)
# -------------------------
def build_light_cnn(input_shape=(128, 128, 1), num_classes=10):
    model = models.Sequential([
        layers.Input(shape=input_shape),

        data_augmentation,  # augmentacja danych

        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),

        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.3),

        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.4),

        layers.Flatten(),
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])
    return model

# -------------------------
# Tworzenie i kompilacja modelu
# -------------------------
model = build_light_cnn(input_shape=(IMG_SIZE[0], IMG_SIZE[1], 1), num_classes=num_classes)
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# -------------------------
# Callbacki
# -------------------------
callbacks = [
    EarlyStopping(
        monitor='val_accuracy',
        patience=6,
        restore_best_weights=True
    ),
    ModelCheckpoint(
        filepath="models/best_light_cnn.keras",
        monitor="val_accuracy",
        save_best_only=True
    )
]

# -------------------------
# Trenowanie modelu
# -------------------------
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    callbacks=callbacks
)

# -------------------------
# Wykres uczenia
# -------------------------
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history["accuracy"], label="train acc")
plt.plot(history.history["val_accuracy"], label="val acc")
plt.legend()
plt.title("Dokładność (accuracy)")

plt.subplot(1, 2, 2)
plt.plot(history.history["loss"], label="train loss")
plt.plot(history.history["val_loss"], label="val loss")
plt.legend()
plt.title("Strata (loss)")

plt.show()

# -------------------------
# Podgląd przykładowych danych
# -------------------------
for images, labels in train_ds.take(1):
    print("🔹 batch shape:", images.shape)
    print("🔹 zakres wartości:", tf.reduce_min(images).numpy(), "do", tf.reduce_max(images).numpy())
    print("🔹 przykładowe etykiety:", labels.numpy())
    plt.imshow(images[0].numpy().squeeze(), cmap="gray")
    plt.title(f"Etykieta: {labels[0].numpy()} ({class_names[labels[0].numpy()]})")
    plt.show()

# -------------------------
# Zapis finalnego modelu
# -------------------------
os.makedirs("models", exist_ok=True)
model.save("models/light_cnn_notes_final.keras")

print("✅ Model zapisany do: models/light_cnn_notes_final.keras")

# -------------------------
# Sprawdzenie liczby plików w każdej klasie
# -------------------------
print("\n📊 Ilość obrazków w każdej klasie:")
for cls in os.listdir(DATA_DIR):
    path = os.path.join(DATA_DIR, cls)
    if os.path.isdir(path):
        print(f"{cls:20s} -> {len(os.listdir(path))} plików")