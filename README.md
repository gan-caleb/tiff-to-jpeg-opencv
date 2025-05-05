# TIFF to JPEG Converter using OpenCV

This tool converts 16-bit TIFF images (like those from Time-of-Flight (ToF) depth and amplitude sensors) into 8-bit JPEG images using OpenCV. It automatically normalizes and optionally rotates the image.

| Type | Before | After
| --- | --- | ---
| Amplitude (TOF) | before | blah |
| Depth (TOF) | Show file differences that haven't been staged | blah |

---

## 📁 Folder Structure
```
tiff-to-jpeg-opencv/
├── input_tiff/
├── output_jpeg/
├── sample-images/
├── src/
│   └── tiff_to_jpeg_converter.py
├── requirements.txt
├── README.md
```

## 🚀 Quick Start

1. **Clone this repo**
   ```bash
   git clone https://github.com/gan-caleb/tiff-to-jpeg-opencv.git
   cd tiff-to-jpeg-opencv
   ```

2. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Drop your `.tiff images` into the `input_tiff/` folder**

4. **Run the converter**
   ```
   python3 src/tiff_to_jpeg_converter.py
   ```

## ⚙️ Configurable Options

Edit the top section of `tiff_to_jpeg_converter.py` to adjust:

- `JPEG_QUALITY` – Output quality (0 to 100)

- `SCALE_FACTOR` – Resize factor (e.g., 0.5 = half size)

- `ROTATE_IMAGE` – Rotate output (True/False)

- `ROTATION_ANGLE` – 90, 180, 270 degrees

- `NORMALIZATION_METHOD` – `'linear'` (default) or `'hist_eq'`