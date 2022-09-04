import random
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
import numpy as np
import torch.utils.data
import cv2
import torchvision.models.segmentation
import torch
import os

def loadData():
    batch_Imgs=[]
    batch_Data=[]# load images and masks
    for i in range(batchSize):
        idx=random.randint(0,len(imgs)-1)
        
        img = cv2.imread(imgs[idx])

        # mapping input image to ouput image
        mask = ""
        for i in range(len(imgs)):
          if path[idx] == output[i]:
            mask = output[i]
            break

        if mask:
          masks = cv2.imread(trainOutput+'/'+mask)
        else:
          return loadData()

        gray = cv2.cvtColor(masks,cv2.COLOR_BGR2GRAY) # converting to output img to gray scale
        thresh = cv2.threshold(gray,17,255,cv2.THRESH_BINARY)[1]

        # get contours
        contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) >= 2 else contours[1]
        boxes = torch.zeros([len(contours),4], dtype=torch.float32)
        i = 0
        for cntr in contours:
            x,y,w,h = cv2.boundingRect(cntr)
            boxes[i] = torch.tensor([x, y, x+w, y+h])
            i+=1
      
        masks = torch.as_tensor(masks, dtype=torch.uint8)
        img = torch.as_tensor(img, dtype=torch.float32)
        data = {}
        data["boxes"] =  boxes
        data["labels"] =  torch.ones((len(contours),), dtype=torch.int64)   # no.of labels = no.of bounding boxes
        data["masks"] = masks
        batch_Imgs.append(img)
        batch_Data.append(data)  # load images and masks

    batch_Imgs = torch.stack([torch.as_tensor(d) for d in batch_Imgs], 0)
    batch_Imgs = batch_Imgs.swapaxes(1, 3).swapaxes(2, 3)
    return batch_Imgs, batch_Data


batchSize=2
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')   # train on the GPU or on the CPU, if a GPU is not available
trainInput="/content/drive/MyDrive/train_images/rgb" # path to training dataset
trainOutput="/content/drive/MyDrive/train_images/colorCleaned" #  path to training result images

imgs=[]
path=[]
for pth in os.listdir(trainInput):
    if pth[-7:] != '(1).png':
      imgs.append(trainInput+"/"+pth)
      path.append(pth)

output=[]
for pth in os.listdir(trainOutput):
    if pth[-7:] != '(1).png':
      output.append(pth)

# Training the model

model = torchvision.models.detection.maskrcnn_resnet50_fpn(pretrained=True)  # load an instance segmentation model pre-trained pre-trained on COCO
in_features = model.roi_heads.box_predictor.cls_score.in_features  # get number of input features for the classifier
model.roi_heads.box_predictor = FastRCNNPredictor(in_features,num_classes=2)  # replace the pre-trained head with a new one
model.to(device)# move model to the right device

optimizer = torch.optim.AdamW(params=model.parameters(), lr=1e-5)
model.train()

for i in range(51):
            images, targets = loadData()
            images = list(image.to(device) for image in images)
            targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

            optimizer.zero_grad()
            loss_dict = model(images, targets)

            losses = sum(loss for loss in loss_dict.values())
            losses.backward()
            optimizer.step()
            print(i,'loss:', losses.item())
            if i%50==0:
                torch.save(model.state_dict(), "rcnn"+".torch")