from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt

# Load a model
model = YOLO('best_ocr.pt')  # pretrained YOLOv8n model

# Run batched inference on a list of images
results = model("bien-so-xe-cac-tinh-thanh-pho-cua-nuoc-ta-1.jpg")  # return a list of Results objects

# cv2 load image
image = cv2.imread("bien-so-xe-cac-tinh-thanh-pho-cua-nuoc-ta-1.jpg", cv2.IMREAD_COLOR)
imageRectangle = image.copy()

# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bbox outputs
    h, w = result.orig_shape
    for i in boxes.xyxyn:
        m, n, p, q = i
        cv2.rectangle(imageRectangle, (int(h*m), int(w*n)), (int(h*p), int(w*q)), (255, 0, 255), thickness=5, lineType=cv2.LINE_8)
        
# Display the image
plt.imshow(imageRectangle[:, :, ::-1])