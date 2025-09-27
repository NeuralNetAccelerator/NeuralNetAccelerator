#disable tensorflow errors
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf

ALPHA = 1.0 #smallest possible for mobilenetv2
PATH = "model/smallmodel.tflite"

#download model 
print(f"Downloading model at alpha {ALPHA}...")
model = tf.keras.applications.MobileNetV2(weights="imagenet")

print("Quantizing model to int8...")
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]  # INT8 
tflite_model = converter.convert()


#print out stats
print("\n\n\n\n")
print("Params:", model.count_params())
print(f"Final length: {len(tflite_model)}")
print(f"\n\nwritting model to {PATH}")

with open(PATH, "wb") as f:
    f.write(tflite_model)