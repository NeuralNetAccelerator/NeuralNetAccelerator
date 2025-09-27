from datasets import load_dataset
import numpy as np
import tensorflow as tf
from PIL import Image


print("Loading imagenet dataset")
ds = load_dataset("ILSVRC/imagenet-1k")

# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load and preprocess an image (example: resize to model input size, normalize if needed)
img = Image.open("test.jpg").convert("RGB")

# Get input shape (e.g. [1, 224, 224, 3])
input_shape = input_details[0]['shape']
target_size = (input_shape[2], input_shape[1])  # (width, height)
img = img.resize(target_size)

# Convert to numpy and add batch dimension
input_data = np.expand_dims(img, axis=0).astype(input_details[0]['dtype'])

# If model expects normalized data, scale [0,255] → [0,1]
if np.issubdtype(input_details[0]['dtype'], np.floating):
    input_data = input_data / 255.0

# Set input tensor
interpreter.set_tensor(input_details[0]['index'], input_data)

# Run inference
interpreter.invoke()

# Get output
output_data = interpreter.get_tensor(output_details[0]['index'])
print("Raw model output:", output_data)

# If classification model → argmax for predicted class
predicted_class = np.argmax(output_data)
print("Predicted class:", predicted_class)
