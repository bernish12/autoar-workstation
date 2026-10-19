import base64
import os

# A tiny 1x1 pixel red JPEG
jpeg_b64 = "/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////wgALCAABAAEBAREA/8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPxA="
jpeg_bytes = base64.b64decode(jpeg_b64)

# A second tiny 1x1 pixel blue JPEG (just to have two)
jpeg2_b64 = "/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////wgALCAABAAEBAREA/8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPxA="
# Actually I'll just reuse the first one with a slight change if possible, but let's just use the same one twice
jpeg2_bytes = base64.b64decode(jpeg_b64)

print("Creating fake_drive.img (2MB)...")
with open("fake_drive.img", "wb") as f:
    f.write(os.urandom(1024 * 500)) # 500KB garbage
    f.write(jpeg_bytes) # First hidden photo
    f.write(os.urandom(1024 * 800)) # 800KB garbage
    f.write(jpeg_bytes) # Second hidden photo
    f.write(os.urandom(1024 * 700)) # 700KB garbage

print("fake_drive.img created! It contains 2 permanently deleted photos hidden among 2MB of random disk sectors.")
