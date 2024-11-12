import os
from PIL import Image

def split_image(image_path, output_dir):
    image = Image.open(image_path)
    width, height = image.size

    if width <= 2000:
        return

    base_name = os.path.splitext(os.path.basename(image_path))[0]
    ext = os.path.splitext(image_path)[1]

    mid_width = width // 2
    mid_height = height // 2

    boxes = [
        (0, 0, mid_width, mid_height),
        (mid_width, 0, width, mid_height),
        (0, mid_height, mid_width, height),
        (mid_width, mid_height, width, height),
    ]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, box in enumerate(boxes):
        cropped_image = image.crop(box)
        output_path = os.path.join(output_dir, f"{base_name}_{i+1}{ext}")
        cropped_image.save(output_path)

def process_images_in_directory(directory, output_dir):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(
                (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".webp")
            ):
                image_path = os.path.join(root, file)
                split_image(image_path, output_dir)
