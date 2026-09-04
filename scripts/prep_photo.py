from pathlib import Path
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import remove


def main():
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("source-photo.jpg")
    output_path = Path("source-prepped.png")

    if not input_path.exists():
        print(f"ERROR: Could not find {input_path}")
        sys.exit(1)

    print("Removing background...")

    # Open image
    image = Image.open(input_path).convert("RGBA")

    # Remove background
    cutout = remove(image)

    # Convert to numpy array
    rgba = np.array(cutout)

    # Extract RGB and alpha
    rgb = rgba[:, :, :3]
    alpha = rgba[:, :, 3]

    # Convert to grayscale
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

    # Improve local contrast
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )
    enhanced = clahe.apply(gray)

    # White background
    white = np.full_like(enhanced, 255)

    # Composite subject over white
    alpha_float = alpha.astype(np.float32) / 255.0

    result = (
        enhanced.astype(np.float32) * alpha_float
        + white.astype(np.float32) * (1 - alpha_float)
    )

    result = np.clip(result, 0, 255).astype(np.uint8)

    # Save
    Image.fromarray(result, mode="L").save(output_path)

    print(f"Done!")
    print(f"Created: {output_path}")


if __name__ == "__main__":
    main()