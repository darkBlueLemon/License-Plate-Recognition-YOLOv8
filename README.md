# License Plate Recognition and Tracking using YOLOv8 and SORT 

Vehicle license plate detection and tracking system, which uses YOLO for detecting license plates in video frames and OpenCV for image processing. It also includes a Flask API for managing vehicle entries and exits, and an SQLite database for storing vehicle information.


## Features
### Car Detection using YOLOv8 and Tracking using SORT
# <img width="1275" alt="Screenshot 2024-06-07 at 17 27 33" src="https://github.com/darkBlueLemon/License-Plate-Recognition-YOLOv8/assets/97424704/8e30f8ce-f920-492b-aaa4-e99d60b84bf0">
### License Plate Detection
# ![WhatsApp Image 2024-06-07 at 17 36 52](https://github.com/darkBlueLemon/License-Plate-Recognition-YOLOv8/assets/97424704/26935ce4-cff0-4d58-b856-61548de87ca4)
### Preprocessing
# <img width="454" alt="Screenshot 2024-06-07 at 17 39 44" src="https://github.com/darkBlueLemon/License-Plate-Recognition-YOLOv8/assets/97424704/10b75d62-c18a-4685-969d-a1e0fc2c303d">
### UI for Management
# <img width="738" alt="Screenshot 2024-06-07 at 16 43 30" src="https://github.com/darkBlueLemon/License-Plate-Recognition-YOLOv8/assets/97424704/19a92063-97ef-4560-81c6-bcaa24e7d5a0">

## Prerequisites

```bash
flask
opencv-python
ultralytics
sqlite3
requests
sort
```

- Download the YOLO model weights (bestNew.pt) and place them in the models directory.

Install the required libraries using pip:
```bash
pip install opencv-python face-recognition numpy
```
## Installation

Clone the Repository:

```bash
git clone https://github.com/darkBlueLemon/License-Plate-Recognition-YOLOv8.git
cd License-Plate-Recognition-YOLOv8
```

Set Up Virtual Environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install Dependencies:

```bash
pip install -r requirements.txt
```

Set Up Database:
```bash
python app.py
```
## Usage

Run the Flask API:
```bash
python app.py
```
Run the main script to process the video and detect license plates:
```bash
python main.py
```


