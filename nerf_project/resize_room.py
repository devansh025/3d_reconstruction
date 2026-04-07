import cv2
import os

input_folder = r"C:\nerf_project\auditorium\images"
output_folder = r"C:\nerf_project\auditorium\resized"

os.makedirs(output_folder, exist_ok=True)

for file in os.listdir(input_folder):
    in_path = os.path.join(input_folder, file)
    img = cv2.imread(in_path)
    if img is None:
        continue
    img = cv2.resize(img, (640, 480))
    cv2.imwrite(os.path.join(output_folder, file), img)

print("Done resizing.")