from PIL import Image
import os
import sys

TARGET_W = 156
TARGET_H = 156

 # Created By Marius Celliers
 # Date 2026-04-09
 # image to bin converter for LVGL8 
 # Conversion to  : RGB565
 # Before you start, install Pillow : pip install pillow

def rgb888_to_rgb565(r, g, b):
    """Convert 8-bit RGB values to a single 16-bit RGB565 value."""
    return ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)


def prepare_image(img, fit_mode="contain", background=(0, 0, 0)):
    """
    Resize image to 156x156 using one of these modes:
    - contain: keep aspect ratio, add background padding
    - cover:   keep aspect ratio, crop to fill
    - stretch: ignore aspect ratio, stretch to fit
    """
    img = img.convert("RGB")

    if fit_mode == "stretch":
        return img.resize((TARGET_W, TARGET_H), Image.LANCZOS)

    src_w, src_h = img.size

    if fit_mode == "cover":
        scale = max(TARGET_W / src_w, TARGET_H / src_h)
        new_w = int(src_w * scale)
        new_h = int(src_h * scale)

        img = img.resize((new_w, new_h), Image.LANCZOS)

        left = (new_w - TARGET_W) // 2
        top = (new_h - TARGET_H) // 2
        return img.crop((left, top, left + TARGET_W, top + TARGET_H))

    # Default: contain
    scale = min(TARGET_W / src_w, TARGET_H / src_h)
    new_w = int(src_w * scale)
    new_h = int(src_h * scale)

    resized = img.resize((new_w, new_h), Image.LANCZOS)
    canvas = Image.new("RGB", (TARGET_W, TARGET_H), background)

    left = (TARGET_W - new_w) // 2
    top = (TARGET_H - new_h) // 2
    canvas.paste(resized, (left, top))

    return canvas


def convert_image_to_rgb565_swap_bin(input_path, output_path, fit_mode="contain"):
    img = Image.open(input_path)
    img = prepare_image(img, fit_mode=fit_mode)

    pixels = img.load()

    with open(output_path, "wb") as f:
        for y in range(TARGET_H):
            for x in range(TARGET_W):
                r, g, b = pixels[x, y]
                value = rgb888_to_rgb565(r, g, b)

                # RGB565 Swap = low byte first, then high byte
                low = value & 0xFF
                high = (value >> 8) & 0xFF
                #f.write(bytes([low, high]))
                f.write(bytes([high, low]))

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python lvgl_convert.py input_image [output_file] [contain|cover|stretch]")
        sys.exit(1)

    input_path = sys.argv[1]

    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        base, _ = os.path.splitext(input_path)
        output_path = base + ".bin"

    fit_mode = "contain"
    if len(sys.argv) >= 4:
        fit_mode = sys.argv[3].lower()

    if fit_mode not in ("contain", "cover", "stretch"):
        print("Invalid fit mode. Use: contain, cover, or stretch")
        sys.exit(1)

    convert_image_to_rgb565_swap_bin(input_path, output_path, fit_mode)
    print(f"Done: {output_path}")


if __name__ == "__main__":
    main()
