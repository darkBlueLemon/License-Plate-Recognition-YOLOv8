# from zmq import device
from requestUtil import RequestUtil

# Create an instance of RequestUtil with the base URL of your Flask API
request_util = RequestUtil(base_url='http://127.0.0.1:5000')

from ultralytics import YOLO
import cv2

import util
from util import read_license_plate, write_csv

results = {}

# load models
license_plate_detector = YOLO('./models/bestNew.pt')
license_plate_detector.to(device="mps")

# load video
cap = cv2.VideoCapture('./sample.mp4')
# cap = cv2.VideoCapture(0)
# img_frame = cv2.imread('L1.jpg')

vehicles = [2, 3, 5, 7]

# read frames
frame_nmr = -1
ret = True
while ret:
    frame_nmr += 1
    ret, frame = cap.read()
    if ret:
        results[frame_nmr] = {}

        # detect license plates
        license_plates = license_plate_detector(frame)[0]
        for license_plate in license_plates.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = license_plate

            # crop license plate
            license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]

            # Check if the cropped image is not empty
            if license_plate_crop.size == 0:
                # print("Cropped image is empty")
                continue

            # output_path = "cropped_license_plate.jpg"
            # cv2.imwrite(output_path, license_plate_crop)

            # process license plate
            license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
            # _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)
            # _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 150, 255, cv2.THRESH_BINARY_INV)
            license_plate_crop_thresh = cv2.adaptiveThreshold(license_plate_crop_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

            output_path = "thresh_license_plate.jpg"
            cv2.imwrite(output_path, license_plate_crop_thresh)

            # read license plate number
            license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)
            # license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_gray)

            if license_plate_text is not None:
                results[frame_nmr] = {'license_plate': {'bbox': [x1, y1, x2, y2],
                                                                'text': license_plate_text,
                                                                'bbox_score': score,
                                                                'text_score': license_plate_text_score}}
                # print(license_plate_text) 
                response_add_entry_exit = request_util.add_entry_exit(license_plate_text, 'exit')

# Add a new vehicle
# response_add_vehicle = request_util.add_vehicle('UK08X6831', 'Parth', 'Suzuki')
# print(response_add_vehicle)

# Add an entry or exit event
# response_add_entry_exit = request_util.add_entry_exit('XYZ456', 'entry')
# print(response_add_entry_exit)

# Fetch all vehicles inside and outside
# response_vehicles_inside = request_util.get_vehicles_inside()
# print(response_vehicles_inside)

# response_vehicles_outside = request_util.get_vehicles_outside()
# print(response_vehicles_outside)

# Fetch activity for a specific vehicle
# response_vehicle_activity = request_util.get_vehicle_activity('XYZ456')
# print(response_vehicle_activity)

# print(results)
# write results
write_csv(results, './test.csv')