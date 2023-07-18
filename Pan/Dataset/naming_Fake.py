import os
from PIL import Image

folder_path = r"C:\Users\admin\OneDrive\Desktop\Document_verification\Pan\Dataset\Fake"  # Specify the path to the folder containing the images
prefix = "Fake_Pan_"
count = 1

for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join(folder_path, filename)
        new_filename = prefix + str(count) + ".jpg"
        new_image_path = os.path.join(folder_path, new_filename)
        
        image = Image.open(image_path)
        image = image.convert("RGB")  # Convert image to RGB format
        
        image.save(new_image_path, "JPEG")
        image.close()
        
        os.remove(image_path)  # Remove the original image file
        count += 1
