import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os

MODEL_PATH = "C:/NITHU STUDIES/mealmatch/ingredient-finder/models/ingredient_recognition_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

# Get class labels from the training directory
train_dir = r"C:\\NITHU STUDIES\\mealmatch\\ingredient-finder\\data\\train"
class_labels = sorted(os.listdir(train_dir))
print(class_labels)

def predict_ingredient(img_path):
    img = image.load_img(img_path, target_size=(150, 150))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    predictions = model.predict(img_array)
    predicted_class = class_labels[np.argmax(predictions)]
    return predicted_class
