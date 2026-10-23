# -*- coding: utf-8 -*-
"""
create_all_icons.py
Generates application icon with:
- "道地英語" (上)
- "短句2500" (下)
Exports to 512x512, 256x256, and all Android mipmap resolutions (square + round).
"""

import os
from PIL import Image, ImageDraw, ImageFont

FONT_JH_BD = r"C:\Windows\Fonts\msjhbd.ttc"
FONT_ARIAL_BD = r"C:\Windows\Fonts\arialbd.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def create_base_icon_512():
    # 512 x 512 canvas
    img = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Base rounded rect with dark navy gradient feel (#0F172A)
    # Background
    draw.rounded_rectangle([12, 12, 500, 500], radius=100, fill=(15, 23, 42), outline=(59, 130, 246), width=6)

    # Inner subtle glow outline
    draw.rounded_rectangle([20, 20, 492, 492], radius=92, outline=(30, 58, 138), width=3)

    # Top decorative small capsule: "2500 EXPRESSIONS" or "AUTHENTIC ENGLISH"
    draw.rounded_rectangle([136, 46, 376, 92], radius=14, fill=(30, 41, 59), outline=(245, 158, 11), width=2)
    f_capsule = get_font(FONT_ARIAL_BD, 22)
    draw.text((256, 68), "AUTHENTIC ENGLISH", font=f_capsule, fill=(245, 158, 11), anchor="mm")

    # Upper text: "道地英語" 為上
    f_top = get_font(FONT_JH_BD, 84)
    draw.text((256, 185), "道地英語", font=f_top, fill=(255, 255, 255), anchor="mm")

    # Dividing sleek stylish bar
    draw.line([(70, 256), (442, 256)], fill=(59, 130, 246), width=4)
    # Center accent dot / diamond on line
    draw.ellipse([246, 246, 266, 266], fill=(245, 158, 11))

    # Lower text: "短句2500" 為下
    f_bottom = get_font(FONT_JH_BD, 82)
    draw.text((256, 340), "短句2500", font=f_bottom, fill=(96, 165, 250), anchor="mm")

    # Bottom badge: "1~6字極簡口語 · 真人發音"
    draw.rounded_rectangle([76, 416, 436, 466], radius=16, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
    f_sub = get_font(FONT_JH_BD, 22)
    draw.text((256, 440), "1~6字極簡成語 · 實戰測驗", font=f_sub, fill=(226, 232, 240), anchor="mm")

    return img

def create_round_icon(base_img):
    size = base_img.size
    mask = Image.new("L", size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse([10, 10, size[0] - 10, size[1] - 10], fill=255)

    # Background circle
    round_img = Image.new("RGBA", size, (0, 0, 0, 0))
    round_draw = ImageDraw.Draw(round_img)
    round_draw.ellipse([10, 10, size[0] - 10, size[1] - 10], fill=(15, 23, 42), outline=(59, 130, 246), width=6)

    # Paste base on top using mask
    round_img.paste(base_img, (0, 0), mask)
    # Draw border
    round_draw.ellipse([10, 10, size[0] - 10, size[1] - 10], outline=(59, 130, 246), width=6)
    return round_img

def main():
    base_512 = create_base_icon_512()
    
    # RGB 512 for Play Store
    rgb_512 = Image.new("RGB", (512, 512), (15, 23, 42))
    rgb_512.paste(base_512, (0, 0), base_512)
    play_icon_path = r"j:\_projectBook\_Eng\ShortAndroid\play_store_assets\app_icon_512x512.png"
    rgb_512.save(play_icon_path, "PNG")
    print(f"Saved: {play_icon_path}")

    # 256 for in-app drawable ic_app_logo.png
    logo_256 = base_512.resize((256, 256), Image.Resampling.LANCZOS)
    rgb_logo_256 = Image.new("RGB", (256, 256), (15, 23, 42))
    rgb_logo_256.paste(logo_256, (0, 0), logo_256)
    logo_path = r"j:\_projectBook\_Eng\ShortAndroid\app\src\main\res\drawable\ic_app_logo.png"
    rgb_logo_256.save(logo_path, "PNG")
    print(f"Saved: {logo_path}")

    # Mipmap densities
    densities = {
        "mipmap-mdpi": 48,
        "mipmap-hdpi": 72,
        "mipmap-xhdpi": 96,
        "mipmap-xxhdpi": 144,
        "mipmap-xxxhdpi": 192,
    }

    round_base = create_round_icon(base_512)

    res_root = r"j:\_projectBook\_Eng\ShortAndroid\app\src\main\res"
    for folder, dim in densities.items():
        target_dir = os.path.join(res_root, folder)
        os.makedirs(target_dir, exist_ok=True)

        # Square icon
        sq = base_512.resize((dim, dim), Image.Resampling.LANCZOS)
        sq.save(os.path.join(target_dir, "ic_launcher.png"), "PNG")

        # Round icon
        rd = round_base.resize((dim, dim), Image.Resampling.LANCZOS)
        rd.save(os.path.join(target_dir, "ic_launcher_round.png"), "PNG")
        print(f"Generated {folder} ({dim}x{dim}) square & round")

if __name__ == "__main__":
    main()
