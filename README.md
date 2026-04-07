# 3D Room Viewer using Instant-NGP + COLMAP

This project converts a set of room images into a 3D NeRF scene using COLMAP and Instant-NGP.

## Folder structure

Create this structure first:

```text
C:\nerf_project\
    colmap2nerf.py
    resize_room.py
    fix.py
    auditorium\
        images\
```

Put your selected room images inside:

```text
C:\nerf_project\auditorium\images\
```

Extract Instant-NGP to:

```text
C:\Instant-NGP\
```

Extract COLMAP to:

```text
C:\colmap\
```

---

## Step 1: Install OpenCV

Open CMD and run:

```cmd
pip install opencv-python
```

---

## Step 2: Create `resize_room.py`

Save this file as:

```text
C:\nerf_project\resize_room.py
```

Code:

```python
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
```

Run it:

```cmd
cd C:\nerf_project
python resize_room.py
```

---

## Step 3: Edit `colmap2nerf.py`

Open `C:\nerf_project\colmap2nerf.py` and find this line:

```python
match_cmd = f"{colmap_binary} {args.colmap_matcher}_matcher --SiftMatching.guided_matching=true --database_path {db}"
```

Replace it with:

```python
match_cmd = f"{colmap_binary} {args.colmap_matcher}_matcher --database_path {db}"
```

---

## Step 4: Add COLMAP to PATH

Add this folder to your Windows PATH:

```text
C:\colmap\
```

Then close CMD and open a new CMD.

Test:

```cmd
colmap
```

---

## Step 5: Generate `transforms.json`

Open CMD and run:

```cmd
cd C:\nerf_project
python colmap2nerf.py --images "C:\nerf_project\auditorium\resized" --run_colmap --aabb_scale 2 --out "C:\nerf_project\auditorium\transforms.json"
```

This will create:

```text
C:\nerf_project\auditorium\transforms.json
```

---

## Step 6: Create `fix.py`

Save this file as:

```text
C:\nerf_project\fix.py
```

Code:

```python
import json

json_path = r"C:\nerf_project\auditorium\transforms.json"

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

for frame in data["frames"]:
    p = frame["file_path"].replace("\\", "/")
    p = p.replace("./auditorium/resized/", "./resized/")
    p = p.replace("./my_scene/resized/", "./resized/")
    p = p.replace("./my_scene//resized/", "./resized/")
    frame["file_path"] = p

data["aabb_scale"] = 2

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("transforms.json fixed.")
```

Run it:

```cmd
cd C:\nerf_project
python fix.py
```

---

## Step 7: Final folder check

Your folder should now look like this:

```text
C:\nerf_project\auditorium\
    images\
    resized\
    transforms.json
```

Inside `transforms.json`, image paths should look like this:

```json
"file_path": "./resized/0001.jpg"
```

---

## Step 8: Open Instant-NGP

Run:

```cmd
C:\Instant-NGP\instant-ngp.exe
```

---

## Step 9: Load the dataset

Inside Instant-NGP:

1. Press `Ctrl + O`
2. Select:

```text
C:\nerf_project\auditorium
```

Do not select the `images` folder or the `resized` folder directly.

---

## Step 10: Train the scene

Let it run for at least 2 to 5 minutes.

If the output is poor:

- use only 15 to 25 images
- keep images from one smaller region of the room
- avoid very similar frames
- keep `aabb_scale` at `2`

---

## Full command sequence only

```cmd
pip install opencv-python
cd C:\nerf_project
python resize_room.py
cd C:\nerf_project
python colmap2nerf.py --images "C:\nerf_project\auditorium\resized" --run_colmap --aabb_scale 2 --out "C:\nerf_project\auditorium\transforms.json"
cd C:\nerf_project
python fix.py
C:\Instant-NGP\instant-ngp.exe
```

---

## Notes

- Best starting range: 15 to 25 images
- Recommended image size: 640x480
- If Instant-NGP closes, reduce images further and focus on a smaller section of the room
- If `transforms.json` contains very few frames, your image selection needs improvement
