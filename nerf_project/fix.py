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