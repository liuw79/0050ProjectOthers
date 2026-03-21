import os
import shutil

src = "C:\\Users\\com\\Desktop\\"
dst = "C:\\backup\\desktop"

files = os.listdir(src)

print(files)
for file in files:
    print("Moving file:", file)
    try:
        shutil.move(src + file, dst)
    except Exception as e:
        print("Failed to move file:", file, "Error:", e)
