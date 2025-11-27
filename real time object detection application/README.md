You can view the output of the project in output folder because unfortunately model is not available... 

Real-Time Object Detection Application

A Real-Time Object Detection Application built using YOLO, OpenCV, Tkinter, Pygame, and Label Studio. The application can detect and classify objects from PC webcam, mobile IP camera, video files, or images in real time with high accuracy.

🚀 Features

Real-Time Object Detection from:

Laptop/PC Webcam

Mobile Camera via IP Webcam App

Media Files (Videos & Images)

Custom Dataset Training – Create and train YOLO models using Label Studio.

Graphical User Interface (GUI) – Built with Tkinter for easy interaction.

Smooth Rendering – Uses Pygame + OpenCV for efficient real-time processing.

Bounding Box Visualization – Displays detected objects with class names & confidence.

Multi-Source Input – Choose between Live feed / Video / Image directly from the GUI.

🛠️ Tech Stack

Programming Language: Python

Libraries/Tools Used:

YOLO – Object detection model

OpenCV – Video/image processing & frame capture

Tkinter – GUI interface

Pygame – For smooth frame rendering and event handling

Label Studio – For annotation and dataset preparation

⚙️ Workflow

Dataset Preparation

Collect raw images.

Annotate using Label Studio.

Export dataset in YOLO format.

Model Training

Train YOLO on the dataset.

Save trained weights for detection.

Detection Process

Input Options:

Webcam Feed (PC/laptop camera)

Mobile Camera (IP Webcam App) – Stream captured frames via local IP address

Video File (MP4, AVI, etc.)

Image File (JPG, PNG, etc.)

Processing: OpenCV captures frames, YOLO model predicts objects.

Output: GUI shows results with bounding boxes, labels, and confidence scores.
