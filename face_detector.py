#!/usr/bin/python3
"""Example using PyCoral to detect objects in a given image.
To run this code, you must attach an Edge TPU attached to the host and
install the Edge TPU runtime (`libedgetpu.so`) and `tflite_runtime`. For
device setup instructions, see coral.ai/docs/setup.
Example usage:
```
bash examples/install_requirements.sh detect_image.py
python3 examples/detect_image.py \
  --model test_data/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite \
  --labels test_data/coco_labels.txt \
  --input test_data/grace_hopper.bmp \
  --output ${HOME}/grace_hopper_processed.bmp
```
"""

import argparse
import time

from PIL import Image
from PIL import ImageDraw

from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from bleak import BleakClient

import io
import picamera
import asyncio
import sys
import cv2
import time
import numpy as np

async def speakerCommand(client, write_characteristic, command):
    try:
        await client.write_gatt_char(write_characteristic, bytes(command))
        if(command == 'p'):
          print("started playing music")
        else:
          print("stopped playing music")
    except Exception as inst:
        print("Unexpected error:", inst)
        print("oh no")

async def connect(client):
    try:
        await client.connect()
        await client.pair()
        print("connected succesfully")
    except Exception as inst:
        print("Unexpected error:", inst)
        print("Did not connect to bluetooth module")

def draw_objects(draw, objs, labels):
  """Draws the bounding box and label for each object."""
  for obj in objs:
    bbox = obj.bbox
    draw.rectangle([(bbox.xmin, bbox.ymin), (bbox.xmax, bbox.ymax)],
                   outline='red')
    draw.text((bbox.xmin + 10, bbox.ymin + 10),
              '%s\n%.2f' % (labels.get(obj.id, obj.id), obj.score),
              fill='red')


def main():
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('-m', '--model', required=True,
                      help='File path of .tflite file')
  parser.add_argument('-l', '--labels', help='File path of labels file')
  parser.add_argument('-t', '--threshold', type=float, default=0.4,
                      help='Score threshold for detected objects')
  parser.add_argument('-o', '--output',
                      help='File path for the result image with annotations')
  parser.add_argument('-c', '--count', type=int, default=5,
                      help='Number of times to run inference')
  args = parser.parse_args()

  labels = read_label_file(args.labels) if args.labels else {}
  interpreter = make_interpreter(args.model)
  interpreter.allocate_tensors()

  cap = cv2.VideoCapture(0)
  # HM-10 Module MAC Address and UUID
  address = "64:69:4E:89:2B:C5"
  #address = ("DC5D07D7-38D1-4B52-94DA-4BDC300F5506") #uncomment for macos
  write_characteristic = "0000FFE1-0000-1000-8000-00805f9b34fb"

  # Connecting to Bluetooth Module
  client = BleakClient(address)

  if not client.is_connected:
    asyncio.run(connect(client))

  #initialize eye detector
  eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


  print('----INFERENCE TIME----')
  print('Note: The first inference is slow because it includes',
        'loading the model into Edge TPU memory.')


  stream = io.BytesIO()
  #with picamera.PiCamera() as camera:
    #camera.start_preview()
  while True:
    #camera.capture(stream, format='jpeg')
    #image = Image.open(stream)
    ret, frame = cap.read()
    image = Image.fromarray(frame)
    _, scale = common.set_resized_input(
      interpreter, image.size, lambda size: image.resize(size, Image.ANTIALIAS))
    start = time.perf_counter()
    interpreter.invoke()
    inference_time = time.perf_counter() - start
    objs = detect.get_objects(interpreter, args.threshold, scale)
    print('%.2f ms' % (inference_time * 1000))

    print('-------RESULTS--------')
    if not objs:
      print('No objects detected')

    else:
        #If more than one face is detected, just use whatever is at index 0.
        face = objs[0]
        #extract bounding box coordinates
        left = face.bbox[0]
        right = face.bbox[2]
        bottom = face.bbox[1]
        top = face.bbox[3]
        #convert video frame to a numpy array
        numpy_frame = np.array(frame)
        #crop out the drivers face using bbox coordinates
        cropped_numpy_frame = numpy_frame[bottom:top, left:right]
        #run eye detector
        eyes = eye_cascade.detectMultiScale(roi_color, minSize = (int(w/20),int(h/20)), maxSize=(int(w/6),int(h/6)), minNeighbors=5)
        num_eyes_detected = len(eyes)
        print(num_eyes_detected, "Eyes Detected")
        if(num_eyes_detected < 2):
            print("HOLY SHIT THE DRIVER IS DISTRACTED AHHHH")

    #dont need this, but might be good to reference
    '''for obj in objs:
      print(labels.get(obj.id, obj.id))
      print('  id:    ', obj.id)
      print('  score: ', obj.score)
      print('  bbox:  ', obj.bbox)'''

    #stream.seek(0)
    #stream.truncate()
    if args.output:
      image = image.convert('RGB')
      draw_objects(ImageDraw.Draw(image), objs, labels)
      image.save(args.output)
      image.show()

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

  cap.release()
  cv2.destroyAllWindows()


if __name__ == '__main__':
  main()
