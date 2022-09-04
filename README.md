# Automatic-Weed-Detection

In the Indian agricultural industry, weedicides are sprayed to the crops collectively without taking into consideration whether weeds are present. Due to this, crop yielding plants are also damaged. To avoid such situations and to improve the food quality and productivity, it is necessary to have a system that removes only the weeds.

With the help of automatic weed removal system using robotic arm, it is possible to remove the weed more precisely rather than spraying weedicide over the whole field.

![Block Diagram][./Assets/BlockDiagram.jpeg]

First, a mapping module will be designed using Robot Operating System (ROS) and camera with raspberry pi.Then a image segmentation system will be designed using deep learning model for semantic segmentation of a captured image. The position of weeds will be determined using ROS. And a robotic arm will be employed to pluck the weeds.
