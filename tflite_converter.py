import tensorflow as tf
'''
Convert a tensorflow .pb file to a .tflite file for Coral TPU deployment
'''
# Convert the model
converter = tf.lite.TFLiteConverter.from_saved_model('ssd_mobilenet_v2_320x320_coco17_tpu-8/saved_model') # path to the SavedModel directory

tflite_model = converter.convert()

# Save the model.
with open('model.tflite', 'wb') as f:
  f.write(tflite_model)
