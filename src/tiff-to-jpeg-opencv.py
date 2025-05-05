import cv2
import os
import numpy as np

# ================= USER CONFIGURATION =================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(SCRIPT_DIR, "input-tiff")
OUTPUT_FOLDER = os.path.join(SCRIPT_DIR, "output-jpeg")
JPEG_QUALITY = 95                    # Range: 0 (low) to 100 (best)
SCALE_FACTOR = 1.0                   # e.g., 0.5 for half-size, 1.0 for original
ROTATE_IMAGE = True                 # Set to True to rotate image
ROTATION_ANGLE = 180                 # Degrees: 90, 180, 270
NORMALIZATION_METHOD = 'linear'     # Options: 'linear', 'hist_eq'

# ======================================================

def normalize_image(img, method='linear'):
    if method == 'linear':
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
    elif method == 'hist_eq' and len(img.shape) == 2:
        img = cv2.equalizeHist((img / 256).astype(np.uint8)) * 1.0
    else:
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
    return img.astype(np.uint8)

def convert_tiff_to_jpeg(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    supported_ext = ('.tif', '.tiff')

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(supported_ext):
            filepath = os.path.join(input_folder, filename)
            print(f"Processing: {filename}")

            # Load 16-bit image
            img = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)

            if img is None:
                print(f"Skipped (not readable): {filename}")
                continue

            # Normalize to 8-bit
            img_8bit = normalize_image(img, NORMALIZATION_METHOD)

            # Resize if needed
            if SCALE_FACTOR != 1.0:
                new_size = (int(img_8bit.shape[1] * SCALE_FACTOR), int(img_8bit.shape[0] * SCALE_FACTOR))
                img_8bit = cv2.resize(img_8bit, new_size, interpolation=cv2.INTER_AREA)

            # Rotate if needed
            if ROTATE_IMAGE:
                if ROTATION_ANGLE == 90:
                    img_8bit = cv2.rotate(img_8bit, cv2.ROTATE_90_CLOCKWISE)
                elif ROTATION_ANGLE == 180:
                    img_8bit = cv2.rotate(img_8bit, cv2.ROTATE_180)
                elif ROTATION_ANGLE == 270:
                    img_8bit = cv2.rotate(img_8bit, cv2.ROTATE_90_COUNTERCLOCKWISE)

            # Output path
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(output_folder, f"{base_name}.jpg")

            # Save JPEG
            cv2.imwrite(output_path, img_8bit, [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY])
            print(f"Saved: {output_path}")

    print("All images processed.")

if __name__ == "__main__":
    convert_tiff_to_jpeg(INPUT_FOLDER, OUTPUT_FOLDER)
