# -*- coding: utf-8 -*-
"""
export_android_assets.py
1. Exports all 2,500 short sentences to JSON for Android.
2. Generates app icons for all mipmap densities:
   - Background: Pure black (#0A0A0E) with subtle rounded corner & gold border accent
   - Top line: "英語" in crisp white (#FFFFFF)
   - Bottom line: "短句大師" in bright gold/yellow (#FACC15)
"""

import os
import sys
import json
import re

sys.path.insert(0, r"J:\_projectBook\_Eng\Short")

from PIL import Image, ImageDraw, ImageFont
from quiz_engine import DB, build_literal_trap_zh, build_chinglish_trap_en

from update_corpus_translations import translate_dialogue

dest_assets_dir = r"J:\_projectBook\_Eng\ShortAndroid\app\src\main\assets"
os.makedirs(dest_assets_dir, exist_ok=True)

sentences_list = []
for it in DB.items:
    en = it["en"]
    zh = it["zh"]
    words = [w for w in en.split() if w]
    wc = len(words)
    lit_zh = build_literal_trap_zh(en, zh)
    ch_en = build_chinglish_trap_en(en, zh)
    
    zh_a, zh_b = translate_dialogue({
        "en": en,
        "zh": zh,
        "spkA": it["dialogue"][0],
        "spkB": it["dialogue"][1]
    })

    sentences_list.append({
        "id": it["id"],
        "en": en,
        "zh": zh,
        "wordCount": wc,
        "category": it["category"],
        "spkA": it["dialogue"][0],
        "spkAZh": zh_a,
        "spkB": it["dialogue"][1],
        "spkBZh": zh_b,
        "note": it["note"],
        "litTrapZh": lit_zh,
        "chinglishTrapEn": ch_en
    })

json_path = os.path.join(dest_assets_dir, "sentences_2500.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(sentences_list, f, ensure_ascii=False, indent=2)

print(f"Exported {len(sentences_list)} items to {json_path}")

# 2. Generate Icons
# Dimensions: 512x512 base canvas
def generate_master_icon(size=512, is_round=False):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background: Deep rich black
    bg_color = (13, 13, 17, 255)
    border_color = (250, 204, 21, 200) # Gold accent border

    if is_round:
        draw.ellipse([(0, 0), (size-1, size-1)], fill=bg_color, outline=border_color, width=max(2, size // 64))
    else:
        # Rounded rectangle
        corner_radius = size // 5
        draw.rounded_rectangle([(0, 0), (size-1, size-1)], radius=corner_radius, fill=bg_color, outline=border_color, width=max(2, size // 64))

    # Inner decorative subtle ring
    pad = size // 16
    if is_round:
        draw.ellipse([(pad, pad), (size-1-pad, size-1-pad)], outline=(255, 255, 255, 30), width=max(1, size // 128))
    else:
        draw.rounded_rectangle([(pad, pad), (size-1-pad, size-1-pad)], radius=corner_radius - pad//2, outline=(255, 255, 255, 30), width=max(1, size // 128))

    # Fonts
    font_path = "C:/Windows/Fonts/msjhbd.ttc"
    
    # Line 1: "英文" (White)
    font_size_top = int(size * 0.28)
    font_top = ImageFont.truetype(font_path, font_size_top)
    text_top = "英文"
    bbox_top = draw.textbbox((0, 0), text_top, font=font_top)
    w_top = bbox_top[2] - bbox_top[0]
    h_top = bbox_top[3] - bbox_top[1]
    
    # Line 2: "口語大師" (Yellow)
    font_size_bot = int(size * 0.22)
    font_bot = ImageFont.truetype(font_path, font_size_bot)
    text_bot = "口語大師"
    bbox_bot = draw.textbbox((0, 0), text_bot, font=font_bot)
    w_bot = bbox_bot[2] - bbox_bot[0]
    h_bot = bbox_bot[3] - bbox_bot[1]

    # Center vertically with pleasant spacing
    gap = int(size * 0.05)
    total_h = h_top + gap + h_bot
    start_y = (size - total_h) // 2 - int(size * 0.02)

    # Draw Top Line (White text + subtle shadow)
    x_top = (size - w_top) // 2
    y_top = start_y
    # shadow
    draw.text((x_top + 2, y_top + 2), text_top, fill=(0, 0, 0, 180), font=font_top)
    draw.text((x_top, y_top), text_top, fill=(255, 255, 255, 255), font=font_top)

    # Draw Horizontal Divider
    div_y = y_top + h_top + gap // 2
    div_w = int(size * 0.65)
    div_x1 = (size - div_w) // 2
    div_x2 = div_x1 + div_w
    draw.line([(div_x1, div_y), (div_x2, div_y)], fill=(250, 204, 21, 100), width=max(1, size // 120))

    # Draw Bottom Line (Yellow text + subtle shadow)
    x_bot = (size - w_bot) // 2
    y_bot = y_top + h_top + gap
    # shadow
    draw.text((x_bot + 2, y_bot + 2), text_bot, fill=(0, 0, 0, 180), font=font_bot)
    draw.text((x_bot, y_bot), text_bot, fill=(250, 204, 21, 255), font=font_bot)

    return img

# Generate Base 512x512
master_sq = generate_master_icon(512, is_round=False)
master_rd = generate_master_icon(512, is_round=True)

# Save play store asset
play_asset_dir = r"J:\_projectBook\_Eng\ShortAndroid\play_store_assets"
os.makedirs(play_asset_dir, exist_ok=True)
master_sq.save(os.path.join(play_asset_dir, "icon_512.png"))

# Densities
densities = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192
}

res_dir = r"J:\_projectBook\_Eng\ShortAndroid\app\src\main\res"

for folder, dim in densities.items():
    folder_path = os.path.join(res_dir, folder)
    os.makedirs(folder_path, exist_ok=True)
    
    # Square
    sq_resized = master_sq.resize((dim, dim), Image.Resampling.LANCZOS)
    sq_resized.save(os.path.join(folder_path, "ic_launcher.png"))
    
    # Round
    rd_resized = master_rd.resize((dim, dim), Image.Resampling.LANCZOS)
    rd_resized.save(os.path.join(folder_path, "ic_launcher_round.png"))

# In-app Logo Drawable
drawable_dir = os.path.join(res_dir, "drawable")
os.makedirs(drawable_dir, exist_ok=True)
in_app_logo = master_sq.resize((256, 256), Image.Resampling.LANCZOS)
in_app_logo.save(os.path.join(drawable_dir, "ic_app_logo.png"))

print("All Android launcher icons and in-app logos generated successfully!")
