from tensorflow.keras.models import load_model
import numpy as np
from utils import strokes_to_image

model = load_model("model/my_model.keras")

def recognize_handwriting(strokes):
    img = strokes_to_image(strokes)  # Convert strokes to 28x28 image
    img = img.reshape(1, 28, 28, 1) / 255.0  # Normalize
    prediction = model.predict(img)
    predicted_class = np.argmax(prediction)
    
    # Convert class to character (e.g., 0 = 'a', 1 = 'b', ...)
    predicted_char = chr(ord('a') + predicted_class)
    return predicted_char
