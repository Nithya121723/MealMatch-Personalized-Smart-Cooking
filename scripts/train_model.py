import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import pandas as pd
import os

# Define dataset path (Fixed Path Issue)
DATASET_PATH = "C:/NITHU STUDIES/mealmatch/ingredient-finder/data"

TRAIN_DIR = os.path.join(DATASET_PATH, "train")
VALIDATION_DIR = os.path.join(DATASET_PATH, "validation")
TEST_DIR = os.path.join(DATASET_PATH, "test")

# Load ingredient alternatives CSV (Fixed FileNotFoundError)
ALTERNATIVES_CSV = "C:/NITHU STUDIES/mealmatch/ingredient-finder/data/ingredient_alternatives.csv"

if os.path.exists(ALTERNATIVES_CSV):
    ingredient_alternatives = pd.read_csv(ALTERNATIVES_CSV)
else:
    print(f"❌ Error: File '{ALTERNATIVES_CSV}' not found!")
    exit(1)  # Exit the script if the file is missing

# Image size and batch size
IMG_SIZE = (150, 150)
BATCH_SIZE = 32

# Data Augmentation for training
train_datagen = ImageDataGenerator(
    rescale=1.0/255.0,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
)

# Only rescaling for validation and test sets
val_test_datagen = ImageDataGenerator(rescale=1.0/255.0)

# Load datasets
train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode="categorical"
)

validation_generator = val_test_datagen.flow_from_directory(
    VALIDATION_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode="categorical"
)

test_generator = val_test_datagen.flow_from_directory(
    TEST_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode="categorical", shuffle=False
)

# Get class names
class_labels = list(train_generator.class_indices.keys())

# Build CNN Model
model = keras.Sequential([
    keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(150,150,3)),
    keras.layers.MaxPooling2D(2,2),
    
    keras.layers.Conv2D(64, (3,3), activation='relu'),
    keras.layers.MaxPooling2D(2,2),
    
    keras.layers.Conv2D(128, (3,3), activation='relu'),
    keras.layers.MaxPooling2D(2,2),
    
    keras.layers.Flatten(),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(len(class_labels), activation='softmax')
])

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Model summary
model.summary()

# Create a "models" directory if it doesn't exist
MODEL_DIR = "C:/NITHU STUDIES/mealmatch/ingredient-finder/models"
os.makedirs(MODEL_DIR, exist_ok=True)

# Model checkpoint to save the best model
checkpoint = keras.callbacks.ModelCheckpoint(
    os.path.join(MODEL_DIR, "best_model.h5"), save_best_only=True, monitor="val_accuracy", mode="max"
)

# Train the model
history = model.fit(train_generator, epochs=20, validation_data=validation_generator, callbacks=[checkpoint])

# Evaluate on test data
test_loss, test_acc = model.evaluate(test_generator)
print(f"✅ Test Accuracy: {test_acc:.2f}")

# Save final model
final_model_path = os.path.join(MODEL_DIR, "ingredient_recognition_model.h5")
model.save(final_model_path)
print(f"✅ Model saved at: {final_model_path}")
