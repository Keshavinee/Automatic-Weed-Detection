import torch

from yolov5.models.experimental import attempt_load

from yolov5.utils.general import non_max_suppression

from PIL import Image

from torchvision.transforms import functional as F



import serial

import time

# import the opencv library

import cv2

  

serial1 = serial.Serial('/dev/ttyACM0', 9600)

serial1.close()  # Close the serial connection initially

time.sleep(2)  # Wait for the serial connection to be established

serial1.open()  

# Load the YOLOv8 model from a saved weights file

model = attempt_load('best.pt') #, map_location=torch.device('cpu')



# define a video capture object

vid = cv2.VideoCapture(0)



# Set the desired width and height for the captured frame

desired_width = 640

desired_height = 480

vid.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)

vid.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)



# Get the current image from the webcam

ret, img = vid.read()



# Set the confidence threshold for predictions

conf_thresh = 0.25



# Set the maximum number of detections to keep after non-maximum suppression

max_det = 1000



# Set the IOU threshold for non-maximum suppression

iou_thresh = 0.45



# Load a single test image

# img = Image.open(r'test-image.jpg')



# Convert the image to RGB format

# img = img.convert('RGB')



# Convert the image to RGB format

img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)



#cv2.imshow(img)

cv2.imwrite('testimagef2.jpg', img)



# Resize the image to the model input size

#img = img.resize(size=(800, 800))

# Convert the image to a PyTorch tensor

img_tensor = F.to_tensor(img)



# Add a batch dimension to the tensor

img_tensor = img_tensor.unsqueeze(0)



# Predict bounding boxes on the input image using the loaded model

with torch.no_grad():

    output = model(img_tensor)



# Perform non-maximum suppression to remove overlapping detections

output = non_max_suppression(output, conf_thresh, iou_thresh, max_det=max_det)[0]



coords = []

for det in output:

    x1, y1, x2, y2, conf, cls = det.cpu().numpy()

    # print(cls)

    if (cls == 1):

        center_x = (x1 + x2) / 2

        center_y = (y1 + y2) / 2

        coords.append([center_x, center_y])

        x = int(center_x)

        y = int(center_y)

        data = str(x) + ',' + str(y)

        print(data)

        data = data.encode('utf-8')

        time.sleep(2)

        serial1.write(data)

        response = serial1.readline().decode().strip()

        print(response)

        if response != '0':

            time.sleep(100)

            pass

        coords.append([x,y])

print(coords)

        

