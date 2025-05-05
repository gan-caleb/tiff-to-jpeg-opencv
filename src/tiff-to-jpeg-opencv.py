import cv2
import os
import numpy as np

# ================= USER CONFIGURATION =================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(SCRIPT_DIR, "input-tiff")
OUTPUT_FOLDER = os.path.join(SCRIPT_DIR, "output-jpeg")
JPEG_QUALITY = 95  # Range: 0 (low) to 100 (best)
SCALE_FACTOR = 1.0  # e.g., 0.5 for half-size, 1.0 for original
ROTATE_IMAGE = True  # Set to True to rotate image
ROTATION_ANGLE = 180  # Degrees: 90, 180, 270
NORMALIZATION_METHOD = 'linear'  # Options: 'linear', 'hist_eq'
DEPTH_CLIP_MIN = 1000     # Increase to make near objects darker
DEPTH_CLIP_MAX = 3000     # Decrease to make far objects brighter

# ======================================================

def normalize_image(img, method='linear', is_depth=False, clip_min=None, clip_max=None):
    if is_depth:
        # Mask out extreme background/far values before inversion
        if clip_min is not None and clip_max is not None:
            img_clipped = np.clip(img, clip_min, clip_max)
            mask = (img >= clip_min) & (img <= clip_max)
            img_inverted = clip_max - img_clipped
            img_normalized = cv2.normalize(img_inverted, None, 0, 255, cv2.NORM_MINMAX)
            img_result = np.zeros_like(img_normalized, dtype=np.uint8)
            img_result[mask] = img_normalized[mask]  # apply only to valid pixels
            return img_result
        else:
            # fallback
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

            # Auto-detect image type
            is_depth = 'dep' in filename.lower()
            is_amplitude = 'amp' in filename.lower()

            img_8bit = normalize_image(
                img,
                method=NORMALIZATION_METHOD,
                is_depth=is_depth,
                clip_min=DEPTH_CLIP_MIN if is_depth else None,
                clip_max=DEPTH_CLIP_MAX if is_depth else None
            )

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

            # Save with original filename
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(output_folder, f"{base_name}.jpg")
            cv2.imwrite(output_path, img_8bit, [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY])
            print(f"Saved: {output_path}")


    print("All images processed.")

if __name__ == "__main__":
    convert_tiff_to_jpeg(INPUT_FOLDER, OUTPUT_FOLDER)
