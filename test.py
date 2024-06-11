import csv
import cv2
from ultralytics import YOLO

# Define the function to read bounding box data from CSV
def read_bbox_data_from_csv(csv_file_path):
    bbox_data = []
    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header row
        for row in csv_reader:
            count, x1, y1, x2, y2, score = row
            bbox_data.append((int(count), float(x1), float(y1), float(x2), float(y2), float(score)))
    return bbox_data

# Detect license plates and write results to a CSV file
def detect_and_save_license_plates(image_path, model_path, csv_file_path):
    frame = cv2.imread(image_path)
    license_plate_detector = YOLO(model_path)

    # Detect license plates
    license_plates = license_plate_detector(frame)[0]

    # Prepare results for CSV
    results = []
    count = 0
    for license_plate in license_plates.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = license_plate
        results.append([count, x1, y1, x2, y2, score])
        count += 1

    # Write results to a CSV file
    with open(csv_file_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['ID', 'x1', 'y1', 'x2', 'y2', 'score'])  # Writing the header
        csv_writer.writerows(results)

    print(f"Results written to {csv_file_path}")

# Draw bounding boxes on the image using data from CSV
def draw_bboxes_from_csv(image_path, csv_file_path, output_image_path):
    # Read bounding box data from CSV
    bbox_data = read_bbox_data_from_csv(csv_file_path)

    # Load the image
    image = cv2.imread(image_path)

    # Draw the bounding boxes on the image
    for bbox in bbox_data:
        _, x1, y1, x2, y2, score = bbox
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        # Draw the rectangle
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # Put the score text
        label = f"{score:.2f}"
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Save the image with bounding boxes
    cv2.imwrite(output_image_path, image)

    # Display the image with bounding boxes
    cv2.imshow('Image with Bounding Boxes', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Define file paths
image_path = 'L1.jpg'
model_path = './models/bestNewOld.pt'
csv_file_path = 'license_plates.csv'
output_image_path = 'L1_with_bboxesNew.jpg'

# Detect and save license plates to CSV
detect_and_save_license_plates(image_path, model_path, csv_file_path)

# Draw bounding boxes on the image using data from CSV
draw_bboxes_from_csv(image_path, csv_file_path, output_image_path)
