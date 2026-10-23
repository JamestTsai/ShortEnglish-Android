# -*- coding: utf-8 -*-
"""
generate_play_assets.py
Generates Google Play Store visual assets for ShortEnglish:
- app_icon_512x512.png (512x512)
- feature_graphic_1024x500.png (1024x500)
- 5 Mobile Screenshots (1080x1920)
"""

import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = r"j:\_projectBook\_Eng\ShortAndroid\play_store_assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

FONT_JH_BD = r"C:\Windows\Fonts\msjhbd.ttc"
FONT_ARIAL_BD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_SEGOE_UI = r"C:\Windows\Fonts\segoeui.ttf"
FONT_SEGOE_UI_BD = r"C:\Windows\Fonts\segoeuib.ttf"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

# 1. App Icon 512x512
def generate_app_icon():
    img = Image.new("RGB", (512, 512), color=(15, 23, 42)) # Slate 900
    draw = ImageDraw.Draw(img)

    # Gradient-like background rounded card
    draw.rounded_rectangle([16, 16, 496, 496], radius=96, fill=(19, 27, 46), outline=(59, 130, 246), width=6)

    # Gold badge / banner
    draw.rounded_rectangle([130, 48, 382, 100], radius=16, fill=(245, 158, 11))
    f_badge = get_font(FONT_JH_BD, 26)
    draw.text((256, 74), "2,500 核心精選", font=f_badge, fill=(15, 23, 42), anchor="mm")

    # Center Text: "道地英語" + "短句王"
    f_title1 = get_font(FONT_JH_BD, 76)
    draw.text((256, 185), "道地英語", font=f_title1, fill=(255, 255, 255), anchor="mm")

    # Accent line
    draw.line([(80, 250), (432, 250)], fill=(59, 130, 246), width=5)

    f_title2 = get_font(FONT_JH_BD, 84)
    draw.text((256, 325), "短句王", font=f_title2, fill=(96, 165, 250), anchor="mm")

    # Sub-capsule: "1~6字極短成語 · 雙人會話"
    draw.rounded_rectangle([60, 400, 452, 456], radius=20, fill=(30, 41, 59), outline=(71, 85, 105), width=2)
    f_sub = get_font(FONT_JH_BD, 22)
    draw.text((256, 428), "1~6字極簡成語 · 聽力發音測驗", font=f_sub, fill=(226, 232, 240), anchor="mm")

    out_path = os.path.join(ASSETS_DIR, "app_icon_512x512.png")
    img.save(out_path, "PNG")
    print(f"Generated: {out_path}")

# 2. Feature Graphic 1024x500
def generate_feature_graphic():
    img = Image.new("RGB", (1024, 500), color=(15, 23, 42))
    draw = ImageDraw.Draw(img)

    # Right side decorative cards (mock floating English dialogue cards)
    card_x, card_y = 560, 45
    cards_data = [
        ("Enough is enough.", "適可而止。", (37, 99, 235)),
        ("Follow the rules.", "遵守規則。", (16, 185, 129)),
        ("Time heals all.", "時間能治癒一切。", (139, 92, 246)),
        ("Fair enough.", "說得過去。 / 算合理。", (245, 158, 11)),
    ]
    f_en = get_font(FONT_ARIAL_BD, 24)
    f_zh = get_font(FONT_JH_BD, 18)

    for i, (en_t, zh_t, border_c) in enumerate(cards_data):
        cy = card_y + i * 105
        # Card body
        draw.rounded_rectangle([card_x, cy, card_x + 420, cy + 90], radius=14, fill=(30, 41, 59), outline=border_c, width=2)
        # Audio icon circle
        draw.ellipse([card_x + 20, cy + 25, card_x + 60, cy + 65], fill=(15, 23, 42), outline=border_c, width=2)
        draw.text((card_x + 40, cy + 45), "🔊", font=get_font(FONT_SEGOE_UI, 18), fill=(255, 255, 255), anchor="mm")
        # Text
        draw.text((card_x + 75, cy + 32), en_t, font=f_en, fill=(255, 255, 255), anchor="lm")
        draw.text((card_x + 75, cy + 62), zh_t, font=f_zh, fill=(148, 163, 184), anchor="lm")

    # Left content: Main Title & Features
    f_main = get_font(FONT_JH_BD, 52)
    f_sub = get_font(FONT_JH_BD, 22)
    f_badge = get_font(FONT_JH_BD, 18)

    # Top Pill
    draw.rounded_rectangle([60, 45, 290, 85], radius=10, fill=(245, 158, 11))
    draw.text((175, 65), "🎯 2,500 句道地必備", font=f_badge, fill=(15, 23, 42), anchor="mm")

    # Titles
    draw.text((60, 135), "道地英語短句2500", font=f_main, fill=(255, 255, 255), anchor="lm")
    draw.text((60, 195), "1~6 字高頻成語 · 雙人生活實境會話", font=f_sub, fill=(96, 165, 250), anchor="lm")
    draw.text((60, 230), "真人美語語音 · 3 選項實戰測驗 · 弱點錯題本", font=f_sub, fill=(148, 163, 184), anchor="lm")

    # Badges grid
    badges = [
        ("📚 2,500 完整道地語庫", (30, 58, 138)),
        ("💬 雙人原汁原味例句", (6, 78, 59)),
        ("🔊 TTS 全句真人發音", (107, 33, 168)),
        ("✍️ 3 選項智能評量測驗", (133, 77, 14))
    ]
    for idx, (b_txt, b_bg) in enumerate(badges):
        bx = 60 if idx % 2 == 0 else 295
        by = 285 if idx < 2 else 345
        draw.rounded_rectangle([bx, by, bx + 220, by + 45], radius=10, fill=b_bg, outline=(255, 255, 255, 40), width=1)
        draw.text((bx + 110, by + 22), b_txt, font=f_badge, fill=(255, 255, 255), anchor="mm")

    # Bottom footer tag
    f_foot = get_font(FONT_JH_BD, 17)
    draw.text((60, 445), "⚡ 支援離線學習 · 零延遲秒查秒背 · 專為母語思維打造", font=f_foot, fill=(203, 213, 225), anchor="lm")

    out_path = os.path.join(ASSETS_DIR, "feature_graphic_1024x500.png")
    img.save(out_path, "PNG")
    print(f"Generated: {out_path}")

# 3. Five Mobile Screenshots (1080x1920)
def generate_screenshots():
    screens = [
        {
            "name": "screenshot_1_home.png",
            "title": "海量 2,500 句道地英語短句庫",
            "sub": "嚴格精選 1~6 字極簡成語 · 依字數與主題隨選隨學",
            "cards": [
                ("1", "Enough is enough.", "適可而止。", "🗣️ 日常口語"),
                ("2", "Says who?", "誰說的？", "⚡ 態度反詰"),
                ("3", "Fair enough.", "說得過去。 / 算合理。", "🤝 溝通協商"),
                ("1768", "Follow the rules.", "遵守規則。", "🎯 處世智慧"),
                ("1963", "The smart student drank black coffee.", "聰明的學生喝了黑咖啡。", "🗣️ 日常口語")
            ]
        },
        {
            "name": "screenshot_2_dialogue.png",
            "title": "雙人生活實境會話 · 沉浸式母語對話",
            "sub": "精準繁體中譯對照 · 深度核心語用筆記 · 一鍵語音朗讀",
            "dialogue": {
                "en": "Follow the rules.",
                "zh": "遵守規則。",
                "spkA": "Sometimes I feel overwhelmed by unexpected obstacles in my career.",
                "spkAZh": "有時我會被職涯中出乎意料的阻礙壓得喘不過氣來。",
                "spkB": "Follow the rules. I couldn't have summarized it better myself.",
                "spkBZh": "遵守規則。我自己來總結也不會比這更貼切了。",
                "note": "【核心含義】表達「遵守規則」。\n【母語語用】屬於「🎯 處世智慧」範疇。"
            }
        },
        {
            "name": "screenshot_3_quiz.png",
            "title": "3 選項實戰測驗 · 即時比對與解析",
            "sub": "擺脫生硬直譯陷阱 · 柔和色彩對錯提示 · 答題後即聽例句發音",
            "quiz": {
                "q": "Follow the rules.",
                "options": [
                    ("A", "遵守規則。", True),
                    ("B", "這項流程通常需要花費多長時間？", False),
                    ("C", "今天能請你幫個忙嗎？", False)
                ],
                "exp": "【✅ 正確答案】「Follow the rules.」是道地英語慣用語，意思就是「遵守規則。」。"
            }
        },
        {
            "name": "screenshot_4_chinese_quiz.png",
            "title": "中翻英實戰測驗 · 訓練母語直覺",
            "sub": "看中文選道地短成語 · 答題前遮罩防偷聽 · 答題後啟動發音",
            "quiz_zh": {
                "q": "適可而止。",
                "options": [
                    ("A", "Fair enough.", False),
                    ("B", "Enough is enough.", True),
                    ("C", "Time heals all.", False)
                ],
                "exp": "【✅ 正確答案】「Enough is enough.」是母語者最道地自然、合乎文化習慣的表達方式。"
            }
        },
        {
            "name": "screenshot_5_wrongs.png",
            "title": "專屬弱點錯題本 · 精準複習 100% 盲點",
            "sub": "自動記錄英翻中與中翻英錯題 · 一鍵重測與快速移除 · 學習零漏洞",
            "wrongs": [
                ("15", "Time will tell.", "時間會證明一切。"),
                ("606", "Bless you!", "祝你健康！ / 保重！"),
                ("1768", "Follow the rules.", "遵守規則。"),
                ("1963", "The smart student drank black coffee.", "聰明的學生喝了黑咖啡。")
            ]
        }
    ]

    f_head = get_font(FONT_JH_BD, 50)
    f_sub = get_font(FONT_JH_BD, 28)
    f_card_en = get_font(FONT_ARIAL_BD, 34)
    f_card_zh = get_font(FONT_JH_BD, 26)
    f_tag = get_font(FONT_JH_BD, 20)

    for item in screens:
        img = Image.new("RGB", (1080, 1920), color=(15, 23, 42))
        draw = ImageDraw.Draw(img)

        # Header bar
        draw.text((540, 110), item["title"], font=f_head, fill=(255, 255, 255), anchor="mm")
        draw.text((540, 175), item["sub"], font=f_sub, fill=(148, 163, 184), anchor="mm")

        # Phone mockup container
        phone_x1, phone_y1 = 80, 240
        phone_x2, phone_y2 = 1000, 1840
        draw.rounded_rectangle([phone_x1, phone_y1, phone_x2, phone_y2], radius=44, fill=(19, 27, 46), outline=(51, 65, 85), width=8)

        # Inner app header
        draw.rounded_rectangle([phone_x1 + 10, phone_y1 + 10, phone_x2 - 10, phone_y1 + 100], radius=34, fill=(30, 41, 59))
        draw.text((540, phone_y1 + 55), "道地英語短句 2500", font=get_font(FONT_JH_BD, 32), fill=(255, 255, 255), anchor="mm")

        # Screen content
        if "cards" in item:
            start_y = phone_y1 + 120
            for idx, (num, en, zh, cat) in enumerate(item["cards"]):
                cy = start_y + idx * 280
                draw.rounded_rectangle([phone_x1 + 30, cy, phone_x2 - 30, cy + 250], radius=20, fill=(30, 41, 59), outline=(59, 130, 246), width=2)
                # Category pill
                draw.rounded_rectangle([phone_x1 + 50, cy + 20, phone_x1 + 250, cy + 60], radius=10, fill=(37, 99, 235))
                draw.text((phone_x1 + 150, cy + 40), f"#{num} · {cat}", font=f_tag, fill=(255, 255, 255), anchor="mm")
                # English & Chinese
                draw.text((phone_x1 + 50, cy + 105), en, font=f_card_en, fill=(255, 255, 255), anchor="lm")
                draw.text((phone_x1 + 50, cy + 160), zh, font=f_card_zh, fill=(203, 213, 225), anchor="lm")
                # Audio Button
                draw.rounded_rectangle([phone_x2 - 180, cy + 185, phone_x2 - 50, cy + 235], radius=10, fill=(15, 23, 42), outline=(59, 130, 246), width=1)
                draw.text((phone_x2 - 115, cy + 210), "🔊 發音", font=f_tag, fill=(96, 165, 250), anchor="mm")

        elif "dialogue" in item:
            d = item["dialogue"]
            # Main card
            draw.rounded_rectangle([phone_x1 + 30, phone_y1 + 140, phone_x2 - 30, phone_y1 + 450], radius=24, fill=(30, 41, 59), outline=(16, 185, 129), width=3)
            draw.text((540, phone_y1 + 220), d["en"], font=get_font(FONT_ARIAL_BD, 48), fill=(255, 255, 255), anchor="mm")
            draw.text((540, phone_y1 + 290), d["zh"], font=get_font(FONT_JH_BD, 36), fill=(110, 231, 183), anchor="mm")
            draw.rounded_rectangle([420, phone_y1 + 350, 660, phone_y1 + 415], radius=14, fill=(16, 185, 129))
            draw.text((540, phone_y1 + 382), "🔊 朗讀發音", font=get_font(FONT_JH_BD, 26), fill=(15, 23, 42), anchor="mm")

            # Conversation box
            draw.rounded_rectangle([phone_x1 + 30, phone_y1 + 480, phone_x2 - 30, phone_y1 + 1050], radius=24, fill=(15, 23, 42), outline=(71, 85, 105), width=2)
            draw.text((phone_x1 + 60, phone_y1 + 530), "💬 生活實境對話", font=get_font(FONT_JH_BD, 32), fill=(245, 158, 11), anchor="lm")
            
            # Sentence A
            draw.text((phone_x1 + 60, phone_y1 + 610), "「" + d["spkA"] + "」", font=get_font(FONT_SEGOE_UI, 24), fill=(203, 213, 225), anchor="lm")
            draw.text((phone_x1 + 60, phone_y1 + 665), d["spkAZh"], font=get_font(FONT_JH_BD, 22), fill=(148, 163, 184), anchor="lm")
            
            # Sentence B (Highlight)
            draw.rounded_rectangle([phone_x1 + 45, phone_y1 + 725, phone_x2 - 45, phone_y1 + 890], radius=16, fill=(30, 41, 59), outline=(16, 185, 129), width=2)
            draw.text((phone_x1 + 65, phone_y1 + 775), "「" + d["spkB"] + "」", font=get_font(FONT_SEGOE_UI, 24), fill=(255, 255, 255), anchor="lm")
            draw.text((phone_x1 + 65, phone_y1 + 835), d["spkBZh"], font=get_font(FONT_JH_BD, 22), fill=(110, 231, 183), anchor="lm")

            # Note box
            draw.rounded_rectangle([phone_x1 + 30, phone_y1 + 1090, phone_x2 - 30, phone_y1 + 1320], radius=20, fill=(30, 41, 59))
            draw.text((phone_x1 + 60, phone_y1 + 1150), d["note"].split("\n")[0], font=get_font(FONT_JH_BD, 26), fill=(255, 255, 255), anchor="lm")
            draw.text((phone_x1 + 60, phone_y1 + 1220), d["note"].split("\n")[1], font=get_font(FONT_JH_BD, 26), fill=(148, 163, 184), anchor="lm")

        elif "quiz" in item or "quiz_zh" in item:
            q_data = item.get("quiz") or item.get("quiz_zh")
            # Question card
            draw.rounded_rectangle([phone_x1 + 30, phone_y1 + 140, phone_x2 - 30, phone_y1 + 380], radius=20, fill=(30, 41, 59), outline=(59, 130, 246), width=2)
            draw.text((540, phone_y1 + 220), "請選出道地釋義：", font=get_font(FONT_JH_BD, 26), fill=(148, 163, 184), anchor="mm")
            draw.text((540, phone_y1 + 300), q_data["q"], font=get_font(FONT_ARIAL_BD, 44), fill=(255, 255, 255), anchor="mm")

            # 3 Options
            for o_idx, (let, txt, is_corr) in enumerate(q_data["options"]):
                oy = phone_y1 + 420 + o_idx * 160
                bg_c = (6, 78, 59) if is_corr else (30, 41, 59)
                brd_c = (16, 185, 129) if is_corr else (51, 65, 85)
                draw.rounded_rectangle([phone_x1 + 30, oy, phone_x2 - 30, oy + 130], radius=16, fill=bg_c, outline=brd_c, width=2)
                prefix = f"✓ {let}." if is_corr else f"  {let}."
                draw.text((phone_x1 + 60, oy + 65), f"{prefix}  {txt}", font=get_font(FONT_JH_BD, 28), fill=(255, 255, 255), anchor="lm")

            # Explanation card
            draw.rounded_rectangle([phone_x1 + 30, phone_y1 + 940, phone_x2 - 30, phone_y1 + 1200], radius=20, fill=(15, 23, 42), outline=(16, 185, 129), width=2)
            draw.text((phone_x1 + 60, phone_y1 + 1000), q_data["exp"], font=get_font(FONT_JH_BD, 24), fill=(110, 231, 183), anchor="lm")
            draw.rounded_rectangle([phone_x1 + 60, phone_y1 + 1070, phone_x1 + 260, phone_y1 + 1140], radius=12, fill=(37, 99, 235))
            draw.text((phone_x1 + 160, phone_y1 + 1105), "🔊 例句發音", font=get_font(FONT_JH_BD, 22), fill=(255, 255, 255), anchor="mm")

        elif "wrongs" in item:
            # Header
            draw.rounded_rectangle([phone_x1 + 30, phone_y1 + 140, phone_x2 - 30, phone_y1 + 260], radius=20, fill=(239, 68, 68, 30), outline=(239, 68, 68), width=2)
            draw.text((540, phone_y1 + 185), "⚠️ 弱點錯題複習庫 (4 題待複習)", font=get_font(FONT_JH_BD, 30), fill=(254, 202, 202), anchor="mm")
            draw.text((540, phone_y1 + 225), "點擊可單獨移除 · 一鍵重測直到 100% 掌握", font=get_font(FONT_JH_BD, 20), fill=(148, 163, 184), anchor="mm")

            start_y = phone_y1 + 290
            for idx, (num, en, zh) in enumerate(item["wrongs"]):
                cy = start_y + idx * 240
                draw.rounded_rectangle([phone_x1 + 30, cy, phone_x2 - 30, cy + 210], radius=18, fill=(30, 41, 59), outline=(71, 85, 105), width=2)
                draw.text((phone_x1 + 60, cy + 45), f"錯題 #{num}", font=f_tag, fill=(239, 68, 68), anchor="lm")
                draw.text((phone_x1 + 60, cy + 105), en, font=f_card_en, fill=(255, 255, 255), anchor="lm")
                draw.text((phone_x1 + 60, cy + 160), zh, font=f_card_zh, fill=(203, 213, 225), anchor="lm")
                # Remove button
                draw.rounded_rectangle([phone_x2 - 190, cy + 140, phone_x2 - 50, cy + 190], radius=10, fill=(71, 85, 105))
                draw.text((phone_x2 - 120, cy + 165), "移出租庫", font=f_tag, fill=(255, 255, 255), anchor="mm")

        out_path = os.path.join(ASSETS_DIR, item["name"])
        img.save(out_path, "PNG")
        print(f"Generated: {out_path}")

if __name__ == "__main__":
    generate_app_icon()
    generate_feature_graphic()
    generate_screenshots()
    print("All visual assets generated successfully!")
