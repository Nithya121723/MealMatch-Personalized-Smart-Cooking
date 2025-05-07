import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# Set paths
DATASET_PATH = "C:/NITHU STUDIES/mealmatch/ingredient-finder/data"
TEST_DIR = os.path.join(DATASET_PATH, "test")
MODEL_PATH = "C:/NITHU STUDIES/mealmatch/ingredient-finder/models/best_model.h5"

# Image configuration
IMG_SIZE = (150, 150)
BATCH_SIZE = 32

# Load model
model = keras.models.load_model(MODEL_PATH)
print("✅ Model loaded successfully!")

# Prepare test data generator
test_datagen = ImageDataGenerator(rescale=1.0/255.0)
test_generator = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    shuffle=False
)

# Evaluate model
loss, accuracy = model.evaluate(test_generator)
print(f"✅ Test Accuracy: {accuracy:.2f}")
print(f"📉 Test Loss: {loss:.2f}")
