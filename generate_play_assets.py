# -*- coding: utf-8 -*-
"""
generate_play_assets.py
Regenerates Google Play Store visual assets for ShortEnglish:
- 5 Mobile Screenshots (1080x1920) 100% faithful to Compose UI
- Feature Graphic (1024x500)
- App Icon (512x512)
"""

import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = r"j:\_projectBook\_Eng\ShortAndroid\play_store_assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

FONT_JH_BD = r"C:\Windows\Fonts\msjhbd.ttc"
FONT_JH = r"C:\Windows\Fonts\msjh.ttc"
FONT_ARIAL_BD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_SEGOE_UI = r"C:\Windows\Fonts\segoeui.ttf"
FONT_SEGOE_UI_BD = r"C:\Windows\Fonts\segoeuib.ttf"
FONT_EMOJI = r"C:\Windows\Fonts\seguiemj.ttf"

LOGO_PATH = r"j:\_projectBook\_Eng\ShortAndroid\app\src\main\res\drawable\ic_app_logo.png"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def draw_top_nav_bar(draw, px1, px2, py, active_tab_idx, logo_img):
    # Top bar container: y: py to py + 160
    # py ~ 290
    draw.rectangle([px1, py, px2, py + 155], fill=(15, 23, 42))

    # Logo (46x46)
    if logo_img:
        logo_resized = logo_img.resize((46, 46), Image.Resampling.LANCZOS)
        # paste with mask if RGBA
        mask = logo_resized if logo_resized.mode == 'RGBA' else None
        draw._image.paste(logo_resized, (px1 + 18, py + 12), mask)
    else:
        draw.rounded_rectangle([px1 + 18, py + 12, px1 + 64, py + 58], radius=8, fill=(37, 99, 235))

    # Title & Subtitle
    f_t = get_font(FONT_JH_BD, 25)
    f_sub = get_font(FONT_JH, 15)
    draw.text((px1 + 74, py + 24), "道地英語短句2500", font=f_t, fill=(255, 255, 255), anchor="lm")
    draw.text((px1 + 74, py + 48), "核心成語短句 · 聽力發音測驗", font=f_sub, fill=(148, 163, 184), anchor="lm")

    # Right stats badges
    f_stat = get_font(FONT_JH_BD, 15)
    # Bookmarks badge
    draw.rounded_rectangle([px2 - 165, py + 20, px2 - 95, py + 48], radius=6, fill=(133, 77, 14))
    draw.text((px2 - 130, py + 34), "★ 12", font=f_stat, fill=(254, 240, 138), anchor="mm")
    # Wrongs badge
    draw.rounded_rectangle([px2 - 85, py + 20, px2 - 20, py + 48], radius=6, fill=(153, 27, 27))
    draw.text((px2 - 52, py + 34), "❌ 5", font=f_stat, fill=(254, 202, 202), anchor="mm")

    # 4 Tabs Row: y: py + 78 to py + 140
    tabs = ["📖 課本研讀", "測驗(英)", "測驗(中)", "各種標記"]
    tab_w = (px2 - px1 - 36) // 4
    f_tab = get_font(FONT_JH_BD, 18)

    for i, tab_title in enumerate(tabs):
        tx1 = px1 + 18 + i * (tab_w + 3)
        tx2 = tx1 + tab_w
        ty1 = py + 86
        ty2 = ty1 + 54
        is_active = (i == active_tab_idx)
        bg_col = (37, 99, 235) if is_active else (30, 41, 59)
        border_col = (59, 130, 246) if is_active else (51, 65, 85)
        txt_col = (255, 255, 255) if is_active else (148, 163, 184)
        draw.rounded_rectangle([tx1, ty1, tx2, ty2], radius=10, fill=bg_col, outline=border_col, width=2 if is_active else 1)
        draw.text(((tx1 + tx2) // 2, (ty1 + ty2) // 2), tab_title, font=f_tab, fill=txt_col, anchor="mm")

def draw_admob_bottom(draw, px1, px2, py):
    # py ~ 1730
    draw.rectangle([px1, py, px2, py + 95], fill=(15, 23, 42), outline=(51, 65, 85), width=1)
    f_ad_label = get_font(FONT_JH_BD, 14)
    draw.text(((px1 + px2) // 2, py + 16), "贊助商廣告 (點擊支持開發者)", font=f_ad_label, fill=(148, 163, 184), anchor="mm")

    # Banner inside
    draw.rounded_rectangle([px1 + 40, py + 32, px2 - 40, py + 86], radius=8, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
    f_ad_text = get_font(FONT_JH_BD, 18)
    draw.text(((px1 + px2) // 2, py + 59), "Google AdMob 官方橫幅廣告展示區", font=f_ad_text, fill=(203, 213, 225), anchor="mm")

def draw_phone_frame(draw, px1, py1, px2, py2):
    # Outer Bezel
    draw.rounded_rectangle([px1 - 8, py1 - 8, px2 + 8, py2 + 8], radius=44, fill=(11, 15, 25), outline=(51, 65, 85), width=4)
    # Inner Phone Display Canvas
    draw.rounded_rectangle([px1, py1, px2, py2], radius=38, fill=(11, 15, 25))

    # Status Bar: py1 + 8 to py1 + 42
    f_status = get_font(FONT_ARIAL_BD, 17)
    draw.text((px1 + 35, py1 + 25), "09:41", font=f_status, fill=(255, 255, 255), anchor="lm")
    draw.text((px2 - 35, py1 + 25), "5G  100%", font=f_status, fill=(255, 255, 255), anchor="rm")
    # Camera pill notch
    draw.rounded_rectangle([(px1 + px2)//2 - 60, py1 + 14, (px1 + px2)//2 + 60, py1 + 34], radius=10, fill=(30, 41, 59))

def generate_screenshots():
    logo_img = None
    if os.path.exists(LOGO_PATH):
        try:
            logo_img = Image.open(LOGO_PATH).convert("RGBA")
        except:
            pass

    # 1. SCREENSHOT 1: 課本研讀（📖 課本研讀）#1 Enough is enough.
    def make_screen_1():
        img = Image.new("RGB", (1080, 1920), color=(11, 15, 25))
        draw = ImageDraw.Draw(img)

        # Marketing Top Header
        f_pill = get_font(FONT_JH_BD, 22)
        draw.rounded_rectangle([390, 36, 690, 80], radius=12, fill=(37, 99, 235))
        draw.text((540, 58), "🎯 2,500 句核心收錄", font=f_pill, fill=(255, 255, 255), anchor="mm")

        f_main_title = get_font(FONT_JH_BD, 52)
        f_sub_title = get_font(FONT_JH, 26)
        draw.text((540, 126), "海量 2,500 句道地英語短句庫", font=f_main_title, fill=(255, 255, 255), anchor="mm")
        draw.text((540, 184), "1~6 字高頻口語 · 左右滑動輕鬆切換 · 深度情境會話", font=f_sub_title, fill=(148, 163, 184), anchor="mm")

        # Phone Container
        px1, py1, px2, py2 = 60, 230, 1020, 1860
        draw_phone_frame(draw, px1, py1, px2, py2)
        draw_top_nav_bar(draw, px1, px2, py1 + 46, active_tab_idx=0, logo_img=logo_img)

        # Textbook Controls: py: 440
        # Category Chips
        cats = ["全部(2500題.左右移)", "🎯 堅定拒絕", "💼 職場應對", "☕ 社交破冰", "🔥 情緒表達"]
        cx = px1 + 18
        f_cat = get_font(FONT_JH_BD, 17)
        for idx, cat in enumerate(cats):
            is_sel = (idx == 0)
            cw = 175 if idx == 0 else 135
            draw.rounded_rectangle([cx, 442, cx + cw, 484], radius=8, fill=(59, 130, 246) if is_sel else (30, 41, 59))
            draw.text((cx + cw//2, 463), cat, font=f_cat, fill=(255, 255, 255) if is_sel else (203, 213, 225), anchor="mm")
            cx += cw + 10

        # Search Bar + Jump
        sy = 498
        # Search input
        draw.rounded_rectangle([px1 + 18, sy, px1 + 540, sy + 58], radius=10, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
        f_input = get_font(FONT_JH, 20)
        draw.text((px1 + 36, sy + 29), "🔍  搜尋關鍵字...", font=f_input, fill=(100, 116, 139), anchor="lm")
        # Jump input
        draw.rounded_rectangle([px1 + 555, sy, px1 + 685, sy + 58], radius=10, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
        f_jump = get_font(FONT_ARIAL_BD, 22)
        draw.text((px1 + 620, sy + 29), "1", font=f_jump, fill=(255, 255, 255), anchor="mm")
        # Go button
        draw.rounded_rectangle([px1 + 700, sy, px1 + 810, sy + 58], radius=10, fill=(37, 99, 235))
        f_btn = get_font(FONT_JH_BD, 20)
        draw.text((px1 + 755, sy + 29), "前往", font=f_btn, fill=(255, 255, 255), anchor="mm")
        # Keyboard dismiss
        draw.rounded_rectangle([px1 + 825, sy, px2 - 18, sy + 58], radius=10, fill=(51, 65, 85))
        draw.text(((px1 + 825 + px2 - 18)//2, sy + 29), "⌨✕", font=f_btn, fill=(226, 232, 240), anchor="mm")

        # Main Card Container
        my = 574
        draw.rounded_rectangle([px1 + 18, my, px2 - 18, my + 940], radius=20, fill=(19, 27, 46), outline=(30, 41, 59), width=2)

        # Lesson Counter Row
        f_counter = get_font(FONT_JH_BD, 21)
        draw.text((px1 + 42, my + 38), "第 1 / 2500 課 (#1)", font=f_counter, fill=(56, 189, 248), anchor="lm")

        # Badges Row: [🗣️ 日常口語] [3字] [★ 收藏]
        by = my + 70
        f_badge = get_font(FONT_JH_BD, 16)
        draw.rounded_rectangle([px1 + 42, by, px1 + 160, by + 36], radius=6, fill=(49, 46, 129))
        draw.text((px1 + 101, by + 18), "🗣️ 日常口語", font=f_badge, fill=(165, 180, 252), anchor="mm")

        draw.rounded_rectangle([px1 + 172, by, px1 + 240, by + 36], radius=6, fill=(30, 41, 59))
        draw.text((px1 + 206, by + 18), "3字", font=f_badge, fill=(148, 163, 184), anchor="mm")

        draw.rounded_rectangle([px1 + 252, by, px1 + 338, by + 36], radius=6, fill=(133, 77, 14))
        draw.text((px1 + 295, by + 18), "★ 收藏", font=f_badge, fill=(254, 240, 138), anchor="mm")

        # English Headline
        f_en = get_font(FONT_ARIAL_BD, 48)
        draw.text((px1 + 42, my + 155), "Enough is enough.", font=f_en, fill=(255, 255, 255), anchor="lm")

        # Pronunciation & Bookmark Buttons
        pby = my + 202
        draw.rounded_rectangle([px1 + 42, pby, px1 + 240, pby + 52], radius=10, fill=(37, 99, 235))
        f_pbtn = get_font(FONT_JH_BD, 20)
        draw.text((px1 + 141, pby + 26), "🔊 朗讀發音", font=f_pbtn, fill=(255, 255, 255), anchor="mm")

        draw.rounded_rectangle([px1 + 256, pby, px1 + 400, pby + 52], radius=10, fill=(180, 83, 9))
        draw.text((px1 + 328, pby + 26), "★ 已收藏", font=f_pbtn, fill=(254, 230, 138), anchor="mm")

        # Traditional Chinese Meaning Box
        mby = my + 276
        draw.rounded_rectangle([px1 + 42, mby, px2 - 42, mby + 115], radius=14, fill=(23, 37, 84), outline=(30, 64, 175), width=2)
        f_mtitle = get_font(FONT_JH_BD, 18)
        draw.text((px1 + 65, mby + 26), "🈯 道地核心釋義", font=f_mtitle, fill=(147, 197, 253), anchor="lm")
        f_mzh = get_font(FONT_JH_BD, 34)
        draw.text((px1 + 65, mby + 72), "適可而止。", font=f_mzh, fill=(219, 234, 254), anchor="lm")

        # Dialogue Scenario Box
        dby = my + 412
        draw.rounded_rectangle([px1 + 42, dby, px2 - 42, dby + 480], radius=16, fill=(15, 23, 42), outline=(30, 41, 59), width=2)
        f_dtitle = get_font(FONT_JH_BD, 20)
        draw.text((px1 + 65, dby + 34), "💬 經典生活對話示範", font=f_dtitle, fill=(245, 158, 11), anchor="lm")

        # Sentence 1
        f_diag_en = get_font(FONT_SEGOE_UI, 20)
        f_diag_zh = get_font(FONT_JH, 19)
        draw.text((px1 + 65, dby + 80), "We have spent three hours arguing about the exact same", font=f_diag_en, fill=(203, 213, 225), anchor="lm")
        draw.text((px1 + 65, dby + 112), "contract clause without making any progress.", font=f_diag_en, fill=(203, 213, 225), anchor="lm")
        draw.text((px1 + 65, dby + 150), "我們花了三個小時爭論同一個合約條款，卻毫無進展。", font=f_diag_zh, fill=(148, 163, 184), anchor="lm")

        # Sentence 2 (Highlighted Core)
        s2y = dby + 200
        draw.rounded_rectangle([px1 + 55, s2y, px2 - 55, s2y + 240], radius=12, fill=(30, 41, 59), outline=(16, 185, 129), width=2)
        f_diag_core_en = get_font(FONT_SEGOE_UI_BD, 22)
        draw.text((px1 + 75, s2y + 40), "Enough is enough.", font=f_diag_core_en, fill=(110, 231, 183), anchor="lm")
        draw.text((px1 + 75, s2y + 75), "Let's take a break and revisit this tomorrow.", font=f_diag_en, fill=(255, 255, 255), anchor="lm")
        draw.text((px1 + 75, s2y + 120), "適可而止吧。我們先休息一下，明天再來討論。", font=f_diag_zh, fill=(167, 243, 208), anchor="lm")

        # Play audio button for dialogue
        draw.rounded_rectangle([px1 + 75, s2y + 162, px1 + 280, s2y + 212], radius=8, fill=(15, 23, 42), outline=(16, 185, 129), width=1)
        f_sbtn = get_font(FONT_JH_BD, 17)
        draw.text((px1 + 177, s2y + 187), "🔊 朗讀對話例句", font=f_sbtn, fill=(110, 231, 183), anchor="mm")

        # Bottom Prev/Next Navigation
        nby = my + 960
        f_nav = get_font(FONT_JH_BD, 20)
        draw.rounded_rectangle([px1 + 18, nby, px1 + 280, nby + 56], radius=10, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
        draw.text((px1 + 149, nby + 28), "◀ 上一課", font=f_nav, fill=(226, 232, 240), anchor="mm")

        draw.rounded_rectangle([px1 + 300, nby, px2 - 300, nby + 56], radius=10, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
        draw.text(((px1 + px2)//2, nby + 28), "🎲 隨機跳題", font=f_nav, fill=(245, 158, 11), anchor="mm")

        draw.rounded_rectangle([px2 - 280, nby, px2 - 18, nby + 56], radius=10, fill=(37, 99, 235))
        draw.text((px2 - 149, nby + 28), "下一課 ▶", font=f_nav, fill=(255, 255, 255), anchor="mm")

        # AdMob Banner at Bottom
        draw_admob_bottom(draw, px1, px2, py2 - 100)

        out = os.path.join(ASSETS_DIR, "screenshot_1_home.png")
        img.save(out, "PNG")
        print(f"Generated: {out}")

    # 2. SCREENSHOT 2: 情境對話示範 #1768 Follow the rules.
    def make_screen_2():
        img = Image.new("RGB", (1080, 1920), color=(11, 15, 25))
        draw = ImageDraw.Draw(img)

        # Marketing Top Header
        f_pill = get_font(FONT_JH_BD, 22)
        draw.rounded_rectangle([380, 36, 700, 80], radius=12, fill=(16, 185, 129))
        draw.text((540, 58), "💬 母語真實生活會話", font=f_pill, fill=(255, 255, 255), anchor="mm")

        f_main_title = get_font(FONT_JH_BD, 52)
        f_sub_title = get_font(FONT_JH, 26)
        draw.text((540, 126), "雙人生活實境對話示範", font=f_main_title, fill=(255, 255, 255), anchor="mm")
        draw.text((540, 184), "自然融入真實生活對話 · 告別死背 · 雙語同步對照", font=f_sub_title, fill=(148, 163, 184), anchor="mm")

        # Phone Container
        px1, py1, px2, py2 = 60, 230, 1020, 1860
        draw_phone_frame(draw, px1, py1, px2, py2)
        draw_top_nav_bar(draw, px1, px2, py1 + 46, active_tab_idx=0, logo_img=logo_img)

        # Category Chips
        cats = ["全部(2500題)", "🎯 堅定拒絕", "💼 職場應對", "☕ 社交破冰", "🔥 情緒表達"]
        cx = px1 + 18
        f_cat = get_font(FONT_JH_BD, 17)
        for idx, cat in enumerate(cats):
            is_sel = (idx == 1) # [🎯 堅定拒絕] Active
            cw = 145 if idx == 0 else 145
            draw.rounded_rectangle([cx, 442, cx + cw, 484], radius=8, fill=(59, 130, 246) if is_sel else (30, 41, 59))
            draw.text((cx + cw//2, 463), cat, font=f_cat, fill=(255, 255, 255) if is_sel else (203, 213, 225), anchor="mm")
            cx += cw + 10

        # Search & Jump
        sy = 498
        draw.rounded_rectangle([px1 + 18, sy, px1 + 540, sy + 58], radius=10, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
        f_input = get_font(FONT_JH, 20)
        draw.text((px1 + 36, sy + 29), "🔍  搜尋關鍵字...", font=f_input, fill=(100, 116, 139), anchor="lm")

        draw.rounded_rectangle([px1 + 555, sy, px1 + 685, sy + 58], radius=10, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
        f_jump = get_font(FONT_ARIAL_BD, 22)
        draw.text((px1 + 620, sy + 29), "1768", font=f_jump, fill=(255, 255, 255), anchor="mm")

        draw.rounded_rectangle([px1 + 700, sy, px1 + 810, sy + 58], radius=10, fill=(37, 99, 235))
        f_btn = get_font(FONT_JH_BD, 20)
        draw.text((px1 + 755, sy + 29), "前往", font=f_btn, fill=(255, 255, 255), anchor="mm")

        draw.rounded_rectangle([px1 + 825, sy, px2 - 18, sy + 58], radius=10, fill=(51, 65, 85))
        draw.text(((px1 + 825 + px2 - 18)//2, sy + 29), "⌨✕", font=f_btn, fill=(226, 232, 240), anchor="mm")

        # Main Card Container
        my = 574
        draw.rounded_rectangle([px1 + 18, my, px2 - 18, my + 940], radius=20, fill=(19, 27, 46), outline=(30, 41, 59), width=2)

        # Lesson Counter Row
        f_counter = get_font(FONT_JH_BD, 21)
        draw.text((px1 + 42, my + 38), "第 1768 / 2500 課 (#1768)", font=f_counter, fill=(56, 189, 248), anchor="lm")

        # Badges Row: [🎯 堅定拒絕] [3字] [★ 已收藏]
        by = my + 70
        f_badge = get_font(FONT_JH_BD, 16)
        draw.rounded_rectangle([px1 + 42, by, px1 + 160, by + 36], radius=6, fill=(49, 46, 129))
        draw.text((px1 + 101, by + 18), "🎯 堅定拒絕", font=f_badge, fill=(165, 180, 252), anchor="mm")

        draw.rounded_rectangle([px1 + 172, by, px1 + 240, by + 36], radius=6, fill=(30, 41, 59))
        draw.text((px1 + 206, by + 18), "3字", font=f_badge, fill=(148, 163, 184), anchor="mm")

        draw.rounded_rectangle([px1 + 252, by, px1 + 358, by + 36], radius=6, fill=(133, 77, 14))
        draw.text((px1 + 305, by + 18), "★ 已收藏", font=f_badge, fill=(254, 240, 138), anchor="mm")

        # English Headline
        f_en = get_font(FONT_ARIAL_BD, 48)
        draw.text((px1 + 42, my + 155), "Follow the rules.", font=f_en, fill=(255, 255, 255), anchor="lm")

        # Pronunciation & Bookmark Buttons
        pby = my + 202
        draw.rounded_rectangle([px1 + 42, pby, px1 + 240, pby + 52], radius=10, fill=(37, 99, 235))
        f_pbtn = get_font(FONT_JH_BD, 20)
        draw.text((px1 + 141, pby + 26), "🔊 朗讀發音", font=f_pbtn, fill=(255, 255, 255), anchor="mm")

        draw.rounded_rectangle([px1 + 256, pby, px1 + 400, pby + 52], radius=10, fill=(180, 83, 9))
        draw.text((px1 + 328, pby + 26), "★ 已收藏", font=f_pbtn, fill=(254, 230, 138), anchor="mm")

        # Meaning Box
        mby = my + 276
        draw.rounded_rectangle([px1 + 42, mby, px2 - 42, mby + 115], radius=14, fill=(23, 37, 84), outline=(30, 64, 175), width=2)
        f_mtitle = get_font(FONT_JH_BD, 18)
        draw.text((px1 + 65, mby + 26), "🈯 道地核心釋義", font=f_mtitle, fill=(147, 197, 253), anchor="lm")
        f_mzh = get_font(FONT_JH_BD, 34)
        draw.text((px1 + 65, mby + 72), "遵守規則。", font=f_mzh, fill=(219, 234, 254), anchor="lm")

        # Dialogue Scenario Box
        dby = my + 412
        draw.rounded_rectangle([px1 + 42, dby, px2 - 42, dby + 480], radius=16, fill=(15, 23, 42), outline=(30, 41, 59), width=2)
        f_dtitle = get_font(FONT_JH_BD, 20)
        draw.text((px1 + 65, dby + 34), "💬 經典生活對話示範", font=f_dtitle, fill=(245, 158, 11), anchor="lm")

        # Sentence 1
        f_diag_en = get_font(FONT_SEGOE_UI, 20)
        f_diag_zh = get_font(FONT_JH, 19)
        draw.text((px1 + 65, dby + 80), "Sometimes I feel overwhelmed by unexpected obstacles", font=f_diag_en, fill=(203, 213, 225), anchor="lm")
        draw.text((px1 + 65, dby + 112), "in my career.", font=f_diag_en, fill=(203, 213, 225), anchor="lm")
        draw.text((px1 + 65, dby + 150), "有時我會被職涯中出乎意料的阻礙壓得喘不過氣來。", font=f_diag_zh, fill=(148, 163, 184), anchor="lm")

        # Sentence 2 (Highlighted Core)
        s2y = dby + 200
        draw.rounded_rectangle([px1 + 55, s2y, px2 - 55, s2y + 240], radius=12, fill=(30, 41, 59), outline=(16, 185, 129), width=2)
        f_diag_core_en = get_font(FONT_SEGOE_UI_BD, 22)
        draw.text((px1 + 75, s2y + 40), "Follow the rules.", font=f_diag_core_en, fill=(110, 231, 183), anchor="lm")
        draw.text((px1 + 75, s2y + 75), "I couldn't have summarized it better myself.", font=f_diag_en, fill=(255, 255, 255), anchor="lm")
        draw.text((px1 + 75, s2y + 120), "遵守規則。我自己來總結也不會比這更貼切了。", font=f_diag_zh, fill=(167, 243, 208), anchor="lm")

        # Dialogue audio
        draw.rounded_rectangle([px1 + 75, s2y + 162, px1 + 280, s2y + 212], radius=8, fill=(15, 23, 42), outline=(16, 185, 129), width=1)
        f_sbtn = get_font(FONT_JH_BD, 17)
        draw.text((px1 + 177, s2y + 187), "🔊 朗讀對話例句", font=f_sbtn, fill=(110, 231, 183), anchor="mm")

        # Bottom Prev/Next Navigation
        nby = my + 960
        f_nav = get_font(FONT_JH_BD, 20)
        draw.rounded_rectangle([px1 + 18, nby, px1 + 280, nby + 56], radius=10, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
        draw.text((px1 + 149, nby + 28), "◀ 上一課", font=f_nav, fill=(226, 232, 240), anchor="mm")

        draw.rounded_rectangle([px1 + 300, nby, px2 - 300, nby + 56], radius=10, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
        draw.text(((px1 + px2)//2, nby + 28), "🎲 隨機跳題", font=f_nav, fill=(245, 158, 11), anchor="mm")

        draw.rounded_rectangle([px2 - 280, nby, px2 - 18, nby + 56], radius=10, fill=(37, 99, 235))
        draw.text((px2 - 149, nby + 28), "下一課 ▶", font=f_nav, fill=(255, 255, 255), anchor="mm")

        # AdMob Banner
        draw_admob_bottom(draw, px1, px2, py2 - 100)

        out = os.path.join(ASSETS_DIR, "screenshot_2_dialogue.png")
        img.save(out, "PNG")
        print(f"Generated: {out}")

    # 3. SCREENSHOT 3: 英文測驗（🅰️ 測驗(英) - 英翻中 3 選項實戰）
    def make_screen_3():
        img = Image.new("RGB", (1080, 1920), color=(11, 15, 25))
        draw = ImageDraw.Draw(img)

        # Marketing Top Header
        f_pill = get_font(FONT_JH_BD, 22)
        draw.rounded_rectangle([370, 36, 710, 80], radius=12, fill=(234, 88, 12))
        draw.text((540, 58), "🅰️ 3 選項實戰測驗", font=f_pill, fill=(255, 255, 255), anchor="mm")

        f_main_title = get_font(FONT_JH_BD, 52)
        f_sub_title = get_font(FONT_JH, 26)
        draw.text((540, 126), "英翻中實戰測驗 (3 選項)", font=f_main_title, fill=(255, 255, 255), anchor="mm")
        draw.text((540, 184), "告別生硬直譯陷阱 · 柔和色彩提示 · 答題後即聽例句發音", font=f_sub_title, fill=(148, 163, 184), anchor="mm")

        # Phone Container
        px1, py1, px2, py2 = 60, 230, 1020, 1860
        draw_phone_frame(draw, px1, py1, px2, py2)
        draw_top_nav_bar(draw, px1, px2, py1 + 46, active_tab_idx=1, logo_img=logo_img) # [測驗(英)] Active

        # Quiz Header Bar: py: 442
        qy = 442
        # Back button
        draw.rounded_rectangle([px1 + 18, qy, px1 + 180, qy + 46], radius=8, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
        f_qbtn = get_font(FONT_JH_BD, 16)
        draw.text((px1 + 99, qy + 23), "◀ 回到上一階", font=f_qbtn, fill=(241, 245, 249), anchor="mm")

        # Switch pills [英文題] [中文題]
        draw.rounded_rectangle([px1 + 195, qy, px1 + 395, qy + 46], radius=8, fill=(15, 23, 42), outline=(30, 41, 59), width=1)
        draw.rounded_rectangle([px1 + 197, qy + 2, px1 + 295, qy + 44], radius=6, fill=(37, 99, 235))
        draw.text((px1 + 246, qy + 23), "英文題", font=f_qbtn, fill=(255, 255, 255), anchor="mm")
        draw.text((px1 + 345, qy + 23), "中文題", font=f_qbtn, fill=(148, 163, 184), anchor="mm")

        # Category pill
        draw.rounded_rectangle([px1 + 410, qy, px1 + 540, qy + 46], radius=8, fill=(49, 46, 129))
        draw.text((px1 + 475, qy + 23), "🔥 情緒表達", font=f_qbtn, fill=(165, 180, 252), anchor="mm")

        # Question Card
        qcy = 506
        draw.rounded_rectangle([px1 + 18, qcy, px2 - 18, qcy + 220], radius=18, fill=(19, 27, 46), outline=(30, 41, 59), width=2)
        f_qprompt = get_font(FONT_JH_BD, 18)
        draw.text((px1 + 42, qcy + 36), "題目 (請選擇道地中文意義)：", font=f_qprompt, fill=(147, 197, 253), anchor="lm")

        f_qphrase = get_font(FONT_ARIAL_BD, 42)
        draw.text((px1 + 42, qcy + 96), "Follow the rules.", font=f_qphrase, fill=(255, 255, 255), anchor="lm")

        # Speaker button
        draw.rounded_rectangle([px1 + 42, qcy + 144, px1 + 230, qcy + 192], radius=8, fill=(37, 99, 235))
        f_spk = get_font(FONT_JH_BD, 18)
        draw.text((px1 + 136, qcy + 168), "🔊 朗讀題目", font=f_spk, fill=(255, 255, 255), anchor="mm")

        # 3 Choices
        choices = [
            ("A", "遵守規則。", True),
            ("B", "這項流程通常需要花費多長時間？", False),
            ("C", "今天能請你幫個忙嗎？", False)
        ]
        chy = qcy + 246
        f_choice = get_font(FONT_JH_BD, 22)
        f_badge_correct = get_font(FONT_JH_BD, 16)

        for i, (letter, text, is_correct) in enumerate(choices):
            box_y = chy + i * 115
            if is_correct:
                # Correct choice (Green highlighted)
                draw.rounded_rectangle([px1 + 18, box_y, px2 - 18, box_y + 98], radius=16, fill=(6, 78, 59), outline=(16, 185, 129), width=3)
                draw.rounded_rectangle([px1 + 36, box_y + 24, px1 + 86, box_y + 74], radius=8, fill=(16, 185, 129))
                draw.text((px1 + 61, box_y + 49), letter, font=f_choice, fill=(15, 23, 42), anchor="mm")
                draw.text((px1 + 105, box_y + 49), text, font=f_choice, fill=(255, 255, 255), anchor="lm")
                # Correct checkmark badge
                draw.rounded_rectangle([px2 - 150, box_y + 32, px2 - 36, box_y + 68], radius=6, fill=(16, 185, 129))
                draw.text((px2 - 93, box_y + 50), "✅ 正確答案", font=f_badge_correct, fill=(15, 23, 42), anchor="mm")
            else:
                draw.rounded_rectangle([px1 + 18, box_y, px2 - 18, box_y + 98], radius=16, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
                draw.rounded_rectangle([px1 + 36, box_y + 24, px1 + 86, box_y + 74], radius=8, fill=(15, 23, 42))
                draw.text((px1 + 61, box_y + 49), letter, font=f_choice, fill=(148, 163, 184), anchor="mm")
                draw.text((px1 + 105, box_y + 49), text, font=f_choice, fill=(226, 232, 240), anchor="lm")

        # Explanation Box
        ex_y = chy + 3 * 115 + 16
        draw.rounded_rectangle([px1 + 18, ex_y, px2 - 18, ex_y + 280], radius=16, fill=(15, 23, 42), outline=(16, 185, 129), width=2)
        f_exp_title = get_font(FONT_JH_BD, 20)
        draw.text((px1 + 42, ex_y + 34), "【✅ 正確答案解析】", font=f_exp_title, fill=(110, 231, 183), anchor="lm")

        f_exp_body = get_font(FONT_JH, 19)
        draw.text((px1 + 42, ex_y + 78), "「Follow the rules.」是母語者最常用、最簡潔道地的表達，", font=f_exp_body, fill=(203, 213, 225), anchor="lm")
        draw.text((px1 + 42, ex_y + 110), "準確傳達「遵守規則。」，簡潔有力且合乎文化語境。", font=f_exp_body, fill=(203, 213, 225), anchor="lm")

        # Audio Pronunciation Button for Example Sentence
        draw.rounded_rectangle([px1 + 42, ex_y + 150, px1 + 280, ex_y + 204], radius=10, fill=(37, 99, 235))
        f_ebtn = get_font(FONT_JH_BD, 18)
        draw.text((px1 + 161, ex_y + 177), "🔊 朗讀題目例句", font=f_ebtn, fill=(255, 255, 255), anchor="mm")

        # Next question button
        draw.rounded_rectangle([px1 + 300, ex_y + 150, px2 - 42, ex_y + 204], radius=10, fill=(16, 185, 129))
        draw.text(((px1 + 300 + px2 - 42)//2, ex_y + 177), "下一題 ▶", font=f_ebtn, fill=(15, 23, 42), anchor="mm")

        # AdMob Banner
        draw_admob_bottom(draw, px1, px2, py2 - 100)

        out = os.path.join(ASSETS_DIR, "screenshot_3_quiz.png")
        img.save(out, "PNG")
        print(f"Generated: {out}")

    # 4. SCREENSHOT 4: 中文測驗（🀄 測驗(中) - 中翻英 直覺測驗）
    def make_screen_4():
        img = Image.new("RGB", (1080, 1920), color=(11, 15, 25))
        draw = ImageDraw.Draw(img)

        # Marketing Top Header
        f_pill = get_font(FONT_JH_BD, 22)
        draw.rounded_rectangle([370, 36, 710, 80], radius=12, fill=(147, 51, 234))
        draw.text((540, 58), "🀄 中翻英直覺反應", font=f_pill, fill=(255, 255, 255), anchor="mm")

        f_main_title = get_font(FONT_JH_BD, 52)
        f_sub_title = get_font(FONT_JH, 26)
        draw.text((540, 126), "中翻英直覺反應測驗", font=f_main_title, fill=(255, 255, 255), anchor="mm")
        draw.text((540, 184), "看中文選道地短句 · 答題防偷聽機制 · 訓練母語思維", font=f_sub_title, fill=(148, 163, 184), anchor="mm")

        # Phone Container
        px1, py1, px2, py2 = 60, 230, 1020, 1860
        draw_phone_frame(draw, px1, py1, px2, py2)
        draw_top_nav_bar(draw, px1, px2, py1 + 46, active_tab_idx=2, logo_img=logo_img) # [測驗(中)] Active

        # Quiz Header Bar
        qy = 442
        draw.rounded_rectangle([px1 + 18, qy, px1 + 180, qy + 46], radius=8, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
        f_qbtn = get_font(FONT_JH_BD, 16)
        draw.text((px1 + 99, qy + 23), "◀ 回到上一階", font=f_qbtn, fill=(241, 245, 249), anchor="mm")

        # Switch pills [英文題] [中文題] (中文題 Active)
        draw.rounded_rectangle([px1 + 195, qy, px1 + 395, qy + 46], radius=8, fill=(15, 23, 42), outline=(30, 41, 59), width=1)
        draw.text((px1 + 246, qy + 23), "英文題", font=f_qbtn, fill=(148, 163, 184), anchor="mm")
        draw.rounded_rectangle([px1 + 295, qy + 2, px1 + 393, qy + 44], radius=6, fill=(37, 99, 235))
        draw.text((px1 + 344, qy + 23), "中文題", font=f_qbtn, fill=(255, 255, 255), anchor="mm")

        # Category pill
        draw.rounded_rectangle([px1 + 410, qy, px1 + 540, qy + 46], radius=8, fill=(49, 46, 129))
        draw.text((px1 + 475, qy + 23), "🗣️ 日常口語", font=f_qbtn, fill=(165, 180, 252), anchor="mm")

        # Question Card
        qcy = 506
        draw.rounded_rectangle([px1 + 18, qcy, px2 - 18, qcy + 220], radius=18, fill=(19, 27, 46), outline=(30, 41, 59), width=2)
        f_qprompt = get_font(FONT_JH_BD, 18)
        draw.text((px1 + 42, qcy + 36), "題目 (看中文選道地短句)：", font=f_qprompt, fill=(147, 197, 253), anchor="lm")

        f_qphrase_zh = get_font(FONT_JH_BD, 42)
        draw.text((px1 + 42, qcy + 96), "適可而止。", font=f_qphrase_zh, fill=(250, 204, 21), anchor="lm")

        # Pronunciation Button: Now active because question is answered
        draw.rounded_rectangle([px1 + 42, qcy + 144, px1 + 280, qcy + 192], radius=8, fill=(37, 99, 235))
        f_spk = get_font(FONT_JH_BD, 18)
        draw.text((px1 + 161, qcy + 168), "🔊 朗讀正確英文", font=f_spk, fill=(255, 255, 255), anchor="mm")

        # 3 English Choices
        choices = [
            ("A", "Fair enough.", False),
            ("B", "Enough is enough.", True),
            ("C", "Time heals all.", False)
        ]
        chy = qcy + 246
        f_choice_en = get_font(FONT_ARIAL_BD, 26)
        f_choice_letter = get_font(FONT_JH_BD, 22)
        f_badge_correct = get_font(FONT_JH_BD, 16)

        for i, (letter, text, is_correct) in enumerate(choices):
            box_y = chy + i * 115
            if is_correct:
                # Correct choice
                draw.rounded_rectangle([px1 + 18, box_y, px2 - 18, box_y + 98], radius=16, fill=(6, 78, 59), outline=(16, 185, 129), width=3)
                draw.rounded_rectangle([px1 + 36, box_y + 24, px1 + 86, box_y + 74], radius=8, fill=(16, 185, 129))
                draw.text((px1 + 61, box_y + 49), letter, font=f_choice_letter, fill=(15, 23, 42), anchor="mm")
                draw.text((px1 + 105, box_y + 49), text, font=f_choice_en, fill=(255, 255, 255), anchor="lm")

                draw.rounded_rectangle([px2 - 150, box_y + 32, px2 - 36, box_y + 68], radius=6, fill=(16, 185, 129))
                draw.text((px2 - 93, box_y + 50), "✅ 正確答案", font=f_badge_correct, fill=(15, 23, 42), anchor="mm")
            else:
                draw.rounded_rectangle([px1 + 18, box_y, px2 - 18, box_y + 98], radius=16, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
                draw.rounded_rectangle([px1 + 36, box_y + 24, px1 + 86, box_y + 74], radius=8, fill=(15, 23, 42))
                draw.text((px1 + 61, box_y + 49), letter, font=f_choice_letter, fill=(148, 163, 184), anchor="mm")
                draw.text((px1 + 105, box_y + 49), text, font=f_choice_en, fill=(226, 232, 240), anchor="lm")

        # Explanation Box
        ex_y = chy + 3 * 115 + 16
        draw.rounded_rectangle([px1 + 18, ex_y, px2 - 18, ex_y + 280], radius=16, fill=(15, 23, 42), outline=(16, 185, 129), width=2)
        f_exp_title = get_font(FONT_JH_BD, 20)
        draw.text((px1 + 42, ex_y + 34), "【✅ 正確答案解析】", font=f_exp_title, fill=(110, 231, 183), anchor="lm")

        f_exp_body = get_font(FONT_JH, 19)
        draw.text((px1 + 42, ex_y + 78), "「Enough is enough.」是母語者最道地自然、合乎文化習慣", font=f_exp_body, fill=(203, 213, 225), anchor="lm")
        draw.text((px1 + 42, ex_y + 110), "的表達方式，準確傳達「適可而止。」的堅決語氣。", font=f_exp_body, fill=(203, 213, 225), anchor="lm")

        # Action buttons
        draw.rounded_rectangle([px1 + 42, ex_y + 150, px1 + 280, ex_y + 204], radius=10, fill=(37, 99, 235))
        f_ebtn = get_font(FONT_JH_BD, 18)
        draw.text((px1 + 161, ex_y + 177), "🔊 聽標準美語發音", font=f_ebtn, fill=(255, 255, 255), anchor="mm")

        draw.rounded_rectangle([px1 + 300, ex_y + 150, px2 - 42, ex_y + 204], radius=10, fill=(16, 185, 129))
        draw.text(((px1 + 300 + px2 - 42)//2, ex_y + 177), "下一題 ▶", font=f_ebtn, fill=(15, 23, 42), anchor="mm")

        # AdMob Banner
        draw_admob_bottom(draw, px1, px2, py2 - 100)

        out = os.path.join(ASSETS_DIR, "screenshot_4_chinese_quiz.png")
        img.save(out, "PNG")
        print(f"Generated: {out}")

    # 5. SCREENSHOT 5: 各種標記與錯題本（⭐ 各種標記 / 筆記本）
    def make_screen_5():
        img = Image.new("RGB", (1080, 1920), color=(11, 15, 25))
        draw = ImageDraw.Draw(img)

        # Marketing Top Header
        f_pill = get_font(FONT_JH_BD, 22)
        draw.rounded_rectangle([370, 36, 710, 80], radius=12, fill=(217, 119, 6))
        draw.text((540, 58), "⭐ 弱點標記與錯題本", font=f_pill, fill=(255, 255, 255), anchor="mm")

        f_main_title = get_font(FONT_JH_BD, 52)
        f_sub_title = get_font(FONT_JH, 26)
        draw.text((540, 126), "專屬弱點錯題本與收藏", font=f_main_title, fill=(255, 255, 255), anchor="mm")
        draw.text((540, 184), "自動記錄測驗錯題 · 精準消除學習盲點 · 支援一鍵跳轉研讀", font=f_sub_title, fill=(148, 163, 184), anchor="mm")

        # Phone Container
        px1, py1, px2, py2 = 60, 230, 1020, 1860
        draw_phone_frame(draw, px1, py1, px2, py2)
        draw_top_nav_bar(draw, px1, px2, py1 + 46, active_tab_idx=3, logo_img=logo_img) # [各種標記] Active

        # Notebook Sub-tabs Row (⭐ 收藏 / ❌ 錯題)
        ny = 442
        draw.rectangle([px1, ny, px2, ny + 62], fill=(19, 27, 46))
        subtab_w = (px2 - px1 - 36) // 2
        f_subtab = get_font(FONT_JH_BD, 20)

        # [⭐ 收藏 (12)] Active
        draw.rounded_rectangle([px1 + 18, ny + 6, px1 + 18 + subtab_w, ny + 56], radius=10, fill=(37, 99, 235))
        draw.text((px1 + 18 + subtab_w//2, ny + 31), "⭐ 收藏清單 (12)", font=f_subtab, fill=(255, 255, 255), anchor="mm")

        # [❌ 錯題 (5)] Inactive
        draw.rounded_rectangle([px1 + 24 + subtab_w, ny + 6, px2 - 18, ny + 56], radius=10, fill=(30, 41, 59))
        draw.text(((px1 + 24 + subtab_w + px2 - 18)//2, ny + 31), "❌ 錯題記錄 (5)", font=f_subtab, fill=(148, 163, 184), anchor="mm")

        # Batch Action Bar: py: 516
        ay = 516
        draw.rectangle([px1, ay, px2, ay + 56], fill=(15, 23, 42))
        f_act = get_font(FONT_JH_BD, 17)

        # Select all checkbox pill
        draw.rounded_rectangle([px1 + 18, ay + 8, px1 + 180, ay + 48], radius=8, fill=(30, 41, 59), outline=(51, 65, 85), width=1)
        draw.text((px1 + 99, ay + 28), "☐ 全選 (12)", font=f_act, fill=(203, 213, 225), anchor="mm")

        # Delete selected
        draw.rounded_rectangle([px2 - 180, ay + 8, px2 - 18, ay + 48], radius=8, fill=(153, 27, 27))
        draw.text(((px2 - 180 + px2 - 18)//2, ay + 28), "🗑️ 批次移除", font=f_act, fill=(254, 202, 202), anchor="mm")

        # List of Saved Items
        items = [
            (1, "Enough is enough.", "適可而止。", "🗣️ 日常口語"),
            (15, "Time will tell.", "時間會證明一切。", "⏳ 時機狀態"),
            (1768, "Follow the rules.", "遵守規則。", "🎯 堅定拒絕"),
            (1963, "The smart student drank black coffee.", "聰明的學生喝了黑咖啡。", "🗣️ 日常口語"),
            (2105, "Actions speak louder than words.", "坐而言不如起而行。", "⚖️ 認同妥協")
        ]

        f_item_num = get_font(FONT_JH_BD, 17)
        f_item_en = get_font(FONT_ARIAL_BD, 26)
        f_item_zh = get_font(FONT_JH_BD, 20)
        f_card_btn = get_font(FONT_JH_BD, 16)

        ly = 585
        card_h = 205
        for i, (num, en, zh, cat) in enumerate(items):
            cy = ly + i * (card_h + 14)
            draw.rounded_rectangle([px1 + 18, cy, px2 - 18, cy + card_h], radius=16, fill=(19, 27, 46), outline=(30, 41, 59), width=2)

            # Checkbox & Number tag
            draw.rounded_rectangle([px1 + 36, cy + 22, px1 + 60, cy + 46], radius=4, fill=(15, 23, 42), outline=(71, 85, 105), width=2)
            draw.text((px1 + 75, cy + 34), f"#{num} · {cat}", font=f_item_num, fill=(56, 189, 248), anchor="lm")

            # English Phrase
            draw.text((px1 + 36, cy + 80), en, font=f_item_en, fill=(255, 255, 255), anchor="lm")

            # Chinese Meaning
            draw.text((px1 + 36, cy + 124), zh, font=f_item_zh, fill=(147, 197, 253), anchor="lm")

            # Buttons: [🔊 朗讀] [📖 跳轉研讀]
            draw.rounded_rectangle([px2 - 280, cy + 145, px2 - 165, cy + 190], radius=8, fill=(37, 99, 235))
            draw.text((px2 - 222, cy + 167), "🔊 朗讀", font=f_card_btn, fill=(255, 255, 255), anchor="mm")

            draw.rounded_rectangle([px2 - 150, cy + 145, px2 - 36, cy + 190], radius=8, fill=(30, 41, 59), outline=(59, 130, 246), width=1)
            draw.text((px2 - 93, cy + 167), "📖 課本研讀", font=f_card_btn, fill=(147, 197, 253), anchor="mm")

        # AdMob Banner
        draw_admob_bottom(draw, px1, px2, py2 - 100)

        out = os.path.join(ASSETS_DIR, "screenshot_5_wrongs.png")
        img.save(out, "PNG")
        print(f"Generated: {out}")

    make_screen_1()
    make_screen_2()
    make_screen_3()
    make_screen_4()
    make_screen_5()

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
        ("⚡ 離線隨身背", (37, 99, 235)),
        ("🎧 真人標準語音", (16, 185, 129)),
        ("📝 繁體道地釋義", (139, 92, 246)),
        ("🎯 雙向題型測驗", (234, 88, 12))
    ]
    for idx, (b_txt, b_bg) in enumerate(badges):
        bx = 60 + (idx % 2) * 240
        by = 290 + (idx // 2) * 65
        draw.rounded_rectangle([bx, by, bx + 220, by + 45], radius=10, fill=b_bg, outline=(255, 255, 255), width=1)
        draw.text((bx + 110, by + 22), b_txt, font=f_badge, fill=(255, 255, 255), anchor="mm")

    # Bottom footer tag
    f_foot = get_font(FONT_JH_BD, 17)
    draw.text((60, 445), "⚡ 支援離線學習 · 零延遲秒查秒背 · 專為母語思維打造", font=f_foot, fill=(203, 213, 225), anchor="lm")

    out_path = os.path.join(ASSETS_DIR, "feature_graphic_1024x500.png")
    img.save(out_path, "PNG")
    print(f"Generated: {out_path}")

if __name__ == "__main__":
    generate_screenshots()
    generate_feature_graphic()
