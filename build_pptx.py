# -*- coding: utf-8 -*-
"""
生成「劉松博・公司治理30講」無雜訊顧問簡報 (.pptx)
遵循 /zero-noise-pptx (森秀明 8 大無雜訊版型 × McKinsey/BCG/Accenture 視覺規範)
並在每一頁簡報嵌入對應商業情境圖片與課程圖表輔助說明，同時內建「入門／進階」雙軌要點與三段式顧問講稿。
"""
import os
import sys
import shutil
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

sys.stdout.reconfigure(encoding='utf-8')

from normalize_data import get_all_normalized_lectures

ALL_LECTURES = get_all_normalized_lectures()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(BASE_DIR, "docs", "public")
DOWNLOAD_DIR = os.path.join(PUBLIC_DIR, "downloads")
SOURCE_FOLDER = os.path.abspath(os.path.join(BASE_DIR, "..", "刘松博_公司治理30讲"))

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
CROPPED_CACHE_DIR = os.path.join(BASE_DIR, ".cache_cropped_imgs")
os.makedirs(CROPPED_CACHE_DIR, exist_ok=True)

FONT_HEADING = "Microsoft JhengHei"
FONT_BODY = "Microsoft JhengHei"

THEMES = {
    "mckinsey": {
        "primary": RGBColor(5, 28, 44),       # #051C2C Deep Navy
        "secondary": RGBColor(0, 119, 200),   # #0077C8 Bright Blue
        "accent": RGBColor(0, 163, 224),      # #00A3E0 Cyan
        "bg": RGBColor(255, 255, 255),
        "card_bg": RGBColor(244, 246, 249),
        "panel_bg": RGBColor(248, 250, 252),
        "text_dark": RGBColor(26, 32, 44),
        "text_muted": RGBColor(100, 116, 139),
        "border": RGBColor(203, 213, 225),
        "badge_text": RGBColor(255, 255, 255),
    },
    "bcg": {
        "primary": RGBColor(0, 75, 43),       # #004B2B Deep Forest Green
        "secondary": RGBColor(23, 123, 87),   # #177B57 BCG Green
        "accent": RGBColor(46, 204, 113),     # #2ECC71 Emerald
        "bg": RGBColor(255, 255, 255),
        "card_bg": RGBColor(242, 248, 245),
        "panel_bg": RGBColor(247, 251, 249),
        "text_dark": RGBColor(26, 46, 35),
        "text_muted": RGBColor(90, 115, 101),
        "border": RGBColor(195, 220, 207),
        "badge_text": RGBColor(255, 255, 255),
    },
    "accenture": {
        "primary": RGBColor(45, 16, 84),      # #2D1054 Deep Violet
        "secondary": RGBColor(161, 0, 255),   # #A100FF Accenture Purple
        "accent": RGBColor(198, 102, 255),    # #C666FF Light Purple
        "bg": RGBColor(255, 255, 255),
        "card_bg": RGBColor(248, 245, 252),
        "panel_bg": RGBColor(250, 248, 253),
        "text_dark": RGBColor(34, 22, 51),
        "text_muted": RGBColor(110, 95, 130),
        "border": RGBColor(216, 204, 232),
        "badge_text": RGBColor(255, 255, 255),
    },
}


def get_cropped_image(rel_path, target_ratio=16/10):
    """將圖片中央裁切為指定比例並快取，確保放入 PPTX 不變形"""
    if not rel_path:
        return None
    clean_rel = rel_path.lstrip("/")
    full_path = os.path.join(PUBLIC_DIR, clean_rel.replace("/", os.sep))
    if not os.path.exists(full_path):
        return None
    cache_name = f"{os.path.basename(full_path)}_{int(target_ratio*100)}.jpg"
    cache_path = os.path.join(CROPPED_CACHE_DIR, cache_name)
    if os.path.exists(cache_path):
        return cache_path
    try:
        with Image.open(full_path) as im:
            im = im.convert("RGB")
            w, h = im.size
            curr_ratio = w / h
            if curr_ratio > target_ratio:
                new_w = int(h * target_ratio)
                left = (w - new_w) // 2
                im = im.crop((left, 0, left + new_w, h))
            elif curr_ratio < target_ratio:
                new_h = int(w / target_ratio)
                top = (h - new_h) // 2
                im = im.crop((0, top, w, top + new_h))
            im.thumbnail((1200, int(1200 / target_ratio)), Image.Resampling.LANCZOS)
            im.save(cache_path, "JPEG", quality=88)
            return cache_path
    except Exception as e:
        print(f"Warning: image process failed for {full_path}: {e}")
        return full_path


def add_textbox(slide, left, top, width, height, text, font_size=12, bold=False,
                color=RGBColor(0, 0, 0), align=PP_ALIGN.LEFT, font_name=FONT_BODY,
                valign=MSO_ANCHOR.TOP, line_spacing=1.18):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = valign
    tf.margin_left = Inches(0.06)
    tf.margin_right = Inches(0.06)
    tf.margin_top = Inches(0.04)
    tf.margin_bottom = Inches(0.04)

    lines = str(text).split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.alignment = align
        p.line_spacing = line_spacing
        for run in p.runs:
            run.font.name = font_name
            run.font.size = Pt(font_size)
            run.font.bold = bold
            run.font.color.rgb = color
    return box


def add_rect(slide, left, top, width, height, fill_color, border_color=None,
             border_width=Pt(1), shape_type=MSO_SHAPE.RECTANGLE):
    shape = slide.shapes.add_shape(shape_type, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = border_width
    else:
        shape.line.fill.background()
    return shape


def set_speaker_notes(slide, lec):
    notes = lec.get("speaker_notes", {})
    beg = lec.get("beginner", {})
    adv = lec.get("advanced", {})
    lines = [
        f"【頁碼與主題】{lec['code']}｜{lec['title']} ({lec['layout_label']})",
        f"【結論 Action Title】{notes.get('conclusion', lec['conclusion_title'])}",
        f"【顧問說明】{notes.get('explanation', '')}",
        f"【鋪墊與轉場】{notes.get('transition', '')}",
        "",
        f"🌱【入門者導讀】{beg.get('summary', '')}",
        f"📖【商業故事案例】{beg.get('case_story', '')}",
        f"🏛️【進階思考模型：{adv.get('model_name', '')}】{adv.get('model_desc', '')}",
        f"🔗【跨講因果鏈】{adv.get('causal_link', '')}",
    ]
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = "\n".join(lines)


def add_slide_chrome(slide, lec, theme, page_num, total_pages):
    """頂部顧問眉標 + 行動結論標題 (Action Title) + 底部頁尾"""
    # 頂部細色帶
    add_rect(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.07), theme["primary"])

    # 類別眉標 + 版型標籤
    cat_text = f"{lec['category']}   ｜   {lec['layout_label']}   ｜   知識庫 {lec['kb_id']}"
    add_textbox(
        slide, Inches(0.55), Inches(0.16), Inches(12.2), Inches(0.28),
        cat_text, font_size=9.5, bold=True, color=theme["secondary"],
        font_name=FONT_HEADING
    )

    # Action Title (結論先行標題)
    title_text = lec["conclusion_title"]
    title_size = 18.5 if len(title_text) <= 40 else (16.5 if len(title_text) <= 50 else 15)
    add_textbox(
        slide, Inches(0.55), Inches(0.44), Inches(12.25), Inches(0.82),
        title_text, font_size=title_size, bold=True, color=theme["primary"],
        font_name=FONT_HEADING, line_spacing=1.15
    )

    # 副標題
    if lec.get("subtitle"):
        add_textbox(
            slide, Inches(0.55), Inches(1.24), Inches(12.25), Inches(0.32),
            lec["subtitle"], font_size=10.5, bold=False, color=theme["text_muted"]
        )

    # 標題下分隔線
    add_rect(slide, Inches(0.55), Inches(1.58), Inches(12.25), Inches(0.02), theme["border"])

    # 底部頁尾
    add_rect(slide, Inches(0.55), Inches(7.08), Inches(12.25), Inches(0.015), theme["border"])
    footer_left = f"{lec.get('footer', '')}  ｜  關鍵字：{' / '.join(lec.get('keywords', []))}"
    add_textbox(
        slide, Inches(0.55), Inches(7.12), Inches(10.5), Inches(0.28),
        footer_left, font_size=8.5, color=theme["text_muted"]
    )
    add_textbox(
        slide, Inches(11.2), Inches(7.12), Inches(1.6), Inches(0.28),
        f"{page_num} / {total_pages}", font_size=9, bold=True,
        color=theme["primary"], align=PP_ALIGN.RIGHT
    )


def render_right_visual_panel(slide, lec, theme):
    """
    右側視覺輔助與雙軌認知面板 (x: 8.95" ~ 12.80", y: 1.72" ~ 6.95")
    滿足需求 8 (每頁皆有圖片與輔助文字說明) 與 需求 5 (入門至進階思考架構)
    """
    p_left = Inches(8.95)
    p_top = Inches(1.72)
    p_w = Inches(3.85)
    p_h = Inches(5.22)

    # 外框底板
    add_rect(slide, p_left, p_top, p_w, p_h, theme["panel_bg"], border_color=theme["border"])
    # 頂部色條與標題
    add_rect(slide, p_left, p_top, p_w, Inches(0.32), theme["primary"])
    add_textbox(
        slide, p_left + Inches(0.08), p_top + Inches(0.02), p_w - Inches(0.16), Inches(0.28),
        "🖼️ 視覺情境輔助 ＆ 入門／進階雙軌導讀", font_size=9.5, bold=True,
        color=RGBColor(255, 255, 255), valign=MSO_ANCHOR.MIDDLE
    )

    # 嵌入商業情境圖片 (16:10 比例)
    img_path = get_cropped_image(lec.get("web_image"), target_ratio=16/10)
    img_left = p_left + Inches(0.12)
    img_top = p_top + Inches(0.40)
    img_w = Inches(3.61)
    img_h = Inches(2.25)

    if img_path and os.path.exists(img_path):
        slide.shapes.add_picture(img_path, img_left, img_top, width=img_w, height=img_h)
        # 圖片邊框
        border_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, img_left, img_top, img_w, img_h)
        border_box.fill.background()
        border_box.line.color.rgb = theme["border"]
        border_box.line.width = Pt(1)

    # 圖說文字框 (覆蓋或緊接圖片下方)
    cap_top = img_top + img_h + Inches(0.04)
    add_rect(slide, img_left, cap_top, img_w, Inches(0.54), RGBColor(255, 255, 255), border_color=theme["border"])
    add_textbox(
        slide, img_left + Inches(0.04), cap_top + Inches(0.02), img_w - Inches(0.08), Inches(0.50),
        f"📌 圖說：{lec.get('web_image_caption', '')}", font_size=8.5,
        color=theme["text_dark"], line_spacing=1.12
    )

    # 🌱 入門者秒懂卡片
    beg_top = cap_top + Inches(0.62)
    add_rect(slide, img_left, beg_top, img_w, Inches(0.92), RGBColor(255, 255, 255), border_color=theme["secondary"])
    add_rect(slide, img_left, beg_top, Inches(0.07), Inches(0.92), theme["secondary"])
    beg_summary = lec.get("beginner", {}).get("summary", "")
    if len(beg_summary) > 82:
        beg_summary = beg_summary[:80] + "…"
    add_textbox(
        slide, img_left + Inches(0.12), beg_top + Inches(0.03), img_w - Inches(0.16), Inches(0.24),
        "🌱 入門者核心秒懂（Plain-Language）", font_size=8.8, bold=True, color=theme["secondary"]
    )
    add_textbox(
        slide, img_left + Inches(0.12), beg_top + Inches(0.25), img_w - Inches(0.16), Inches(0.64),
        beg_summary, font_size=8.2, color=theme["text_dark"], line_spacing=1.12
    )

    # 🏛️ 進階者思考模型卡片
    adv_top = beg_top + Inches(0.98)
    adv = lec.get("advanced", {})
    add_rect(slide, img_left, adv_top, img_w, Inches(0.92), RGBColor(255, 255, 255), border_color=theme["primary"])
    add_rect(slide, img_left, adv_top, Inches(0.07), Inches(0.92), theme["primary"])
    adv_desc = adv.get("model_desc", "")
    if len(adv_desc) > 78:
        adv_desc = adv_desc[:76] + "…"
    add_textbox(
        slide, img_left + Inches(0.12), adv_top + Inches(0.03), img_w - Inches(0.16), Inches(0.24),
        f"🏛️ 進階架構：{adv.get('model_name', '')}", font_size=8.8, bold=True, color=theme["primary"]
    )
    add_textbox(
        slide, img_left + Inches(0.12), adv_top + Inches(0.25), img_w - Inches(0.16), Inches(0.64),
        adv_desc, font_size=8.2, color=theme["text_dark"], line_spacing=1.12
    )


# ==============================================================================
# 左側主視覺區 (x: 0.55" ~ 8.75", width = 8.20", y: 1.72" ~ 6.94")
# 8 種森秀明無雜訊簡報版型渲染器
# ==============================================================================
LEFT_X = Inches(0.55)
LEFT_W = Inches(8.20)
TOP_Y = Inches(1.72)
AREA_H = Inches(5.22)


def render_one_to_one_left(slide, lec, theme):
    """① 一對一圖表 (One-to-One Bar Chart) + 關鍵洞察"""
    bars = lec.get("bars", [])
    n = max(len(bars), 1)
    row_h = min(Inches(1.18), Inches(4.8 / n))
    gap = Inches(0.14)

    for i, b in enumerate(bars):
        y = TOP_Y + i * (row_h + gap)
        is_hl = b.get("highlight", False)
        card_bg = RGBColor(255, 255, 255) if not is_hl else theme["card_bg"]
        border_c = theme["secondary"] if is_hl else theme["border"]
        add_rect(slide, LEFT_X, y, LEFT_W, row_h, card_bg, border_color=border_c,
                 border_width=Pt(1.5 if is_hl else 1))

        # 左側標籤與數值
        add_textbox(
            slide, LEFT_X + Inches(0.12), y + Inches(0.08), Inches(2.55), Inches(0.38),
            b.get("label", ""), font_size=11, bold=True,
            color=theme["primary"] if is_hl else theme["text_dark"]
        )
        # 橫向視覺長條
        val = max(min(int(b.get("value", 50)), 100), 8)
        bar_max_w = Inches(5.1)
        bar_w = Inches(5.1 * (val / 100.0))
        bar_x = LEFT_X + Inches(2.75)
        bar_y = y + Inches(0.12)
        add_rect(slide, bar_x, bar_y, bar_max_w, Inches(0.28), RGBColor(235, 240, 245))
        add_rect(slide, bar_x, bar_y, bar_w, Inches(0.28),
                 theme["secondary"] if is_hl else theme["primary"])
        add_textbox(
            slide, bar_x + Inches(0.08), bar_y - Inches(0.01), Inches(2.2), Inches(0.28),
            str(b.get("display", f"{val}%")), font_size=9.5, bold=True,
            color=RGBColor(255, 255, 255), valign=MSO_ANCHOR.MIDDLE
        )
        # 說明文字
        add_textbox(
            slide, LEFT_X + Inches(0.12), y + Inches(0.46), LEFT_W - Inches(0.24), row_h - Inches(0.50),
            b.get("desc", ""), font_size=9.5, color=theme["text_dark"], line_spacing=1.15
        )


def render_parallel_left(slide, lec, theme):
    """② 並列型 (Parallel 2x2 Grid Cards)"""
    cards = lec.get("cards", [])
    cols = 2
    rows = 2
    gap_x = Inches(0.18)
    gap_y = Inches(0.18)
    card_w = (LEFT_W - gap_x) / cols
    card_h = (AREA_H - gap_y) / rows

    for idx, c in enumerate(cards[:4]):
        r = idx // cols
        col = idx % cols
        x = LEFT_X + col * (card_w + gap_x)
        y = TOP_Y + r * (card_h + gap_y)
        is_hl = c.get("highlight", False)

        add_rect(slide, x, y, card_w, card_h,
                 theme["card_bg"] if is_hl else RGBColor(255, 255, 255),
                 border_color=theme["secondary"] if is_hl else theme["border"],
                 border_width=Pt(1.5 if is_hl else 1))
        add_rect(slide, x, y, card_w, Inches(0.07),
                 theme["secondary"] if is_hl else theme["primary"])

        # 標籤膠囊
        tag_box = add_rect(slide, x + Inches(0.12), y + Inches(0.14), Inches(1.25), Inches(0.26),
                           theme["secondary"] if is_hl else theme["primary"],
                           shape_type=MSO_SHAPE.ROUNDED_RECTANGLE)
        add_textbox(slide, x + Inches(0.12), y + Inches(0.14), Inches(1.25), Inches(0.26),
                    c.get("tag", f"要點 {idx+1}"), font_size=8.5, bold=True,
                    color=RGBColor(255, 255, 255), align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

        # 指標值
        if c.get("metric"):
            add_textbox(slide, x + Inches(1.42), y + Inches(0.13), card_w - Inches(1.52), Inches(0.28),
                        c.get("metric", ""), font_size=9.5, bold=True,
                        color=theme["secondary"], align=PP_ALIGN.RIGHT)

        # 標題
        add_textbox(slide, x + Inches(0.12), y + Inches(0.46), card_w - Inches(0.24), Inches(0.42),
                    c.get("title", ""), font_size=11.5, bold=True, color=theme["primary"])

        # 內文
        add_textbox(slide, x + Inches(0.12), y + Inches(0.90), card_w - Inches(0.24), card_h - Inches(0.98),
                    c.get("desc", ""), font_size=9.5, color=theme["text_dark"], line_spacing=1.18)


def render_combined_left(slide, lec, theme):
    """③ 結合型 (Combined Pillars -> 頂層或者底部總合橫幅)"""
    pillars = lec.get("pillars", [])
    n = max(len(pillars), 1)
    gap = Inches(0.14)
    col_w = (LEFT_W - gap * (n - 1)) / n
    pillar_h = Inches(3.95)

    for i, p in enumerate(pillars):
        x = LEFT_X + i * (col_w + gap)
        y = TOP_Y
        is_hl = p.get("highlight", False)

        add_rect(slide, x, y, col_w, pillar_h,
                 theme["card_bg"] if is_hl else RGBColor(255, 255, 255),
                 border_color=theme["secondary"] if is_hl else theme["border"],
                 border_width=Pt(1.5 if is_hl else 1))
        # 頂部支柱標題塊
        add_rect(slide, x, y, col_w, Inches(0.76),
                 theme["secondary"] if is_hl else theme["primary"])
        add_textbox(slide, x + Inches(0.08), y + Inches(0.06), col_w - Inches(0.16), Inches(0.64),
                    p.get("title", ""), font_size=10.5, bold=True,
                    color=RGBColor(255, 255, 255), align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

        # 條列要點
        pts = p.get("points", [])
        pt_text = "\n\n".join([f"▪ {pt}" for pt in pts])
        add_textbox(slide, x + Inches(0.10), y + Inches(0.86), col_w - Inches(0.20), pillar_h - Inches(0.96),
                    pt_text, font_size=9.3, color=theme["text_dark"], line_spacing=1.18)

    # 底部總合結論橫幅
    syn_y = TOP_Y + pillar_h + Inches(0.16)
    syn_h = AREA_H - pillar_h - Inches(0.16)
    add_rect(slide, LEFT_X, syn_y, LEFT_W, syn_h, theme["primary"],
             shape_type=MSO_SHAPE.ROUNDED_RECTANGLE)
    add_textbox(
        slide, LEFT_X + Inches(0.18), syn_y + Inches(0.08), LEFT_W - Inches(0.36), syn_h - Inches(0.16),
        f"🎯 結合型核心綜效：{lec.get('synthesis_banner', '')}",
        font_size=10.2, bold=True, color=RGBColor(255, 255, 255),
        valign=MSO_ANCHOR.MIDDLE, line_spacing=1.18
    )


def render_chain_left(slide, lec, theme):
    """④ 連鎖型 (Causal Chain / Step-by-Step Progression)"""
    steps = lec.get("steps", [])
    n = max(len(steps), 1)
    gap = Inches(0.11)
    row_h = (AREA_H - gap * (n - 1)) / n

    for i, s in enumerate(steps):
        y = TOP_Y + i * (row_h + gap)
        is_hl = s.get("highlight", False)

        add_rect(slide, LEFT_X, y, LEFT_W, row_h,
                 theme["card_bg"] if is_hl else RGBColor(255, 255, 255),
                 border_color=theme["secondary"] if is_hl else theme["border"],
                 border_width=Pt(1.5 if is_hl else 1))

        # 左側步驟徽章
        badge_w = Inches(1.35)
        add_rect(slide, LEFT_X, y, badge_w, row_h,
                 theme["secondary"] if is_hl else theme["primary"])
        add_textbox(slide, LEFT_X + Inches(0.04), y, badge_w - Inches(0.08), row_h,
                    s.get("phase", f"STEP {i+1}"), font_size=9.5, bold=True,
                    color=RGBColor(255, 255, 255), align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

        # 步驟標題與說明
        add_textbox(slide, LEFT_X + badge_w + Inches(0.14), y + Inches(0.06),
                    LEFT_W - badge_w - Inches(0.24), Inches(0.30),
                    s.get("title", ""), font_size=10.8, bold=True,
                    color=theme["secondary"] if is_hl else theme["primary"])
        add_textbox(slide, LEFT_X + badge_w + Inches(0.14), y + Inches(0.36),
                    LEFT_W - badge_w - Inches(0.24), row_h - Inches(0.40),
                    s.get("desc", ""), font_size=9.2, color=theme["text_dark"], line_spacing=1.14)


def render_mckinsey_flow_left(slide, lec, theme):
    """⑤ 流程矩陣 (McKinsey Chevron Flow + Matrix Table)"""
    stages = lec.get("stages", [])
    rows = lec.get("rows", [])
    n_cols = max(len(stages), 1)
    label_w = Inches(1.28)
    gap_x = Inches(0.08)
    col_w = (LEFT_W - label_w - gap_x * n_cols) / n_cols

    # 頂部階段 Chevron 橫軸
    chev_h = Inches(0.62)
    add_rect(slide, LEFT_X, TOP_Y, label_w, chev_h, theme["primary"])
    add_textbox(slide, LEFT_X, TOP_Y, label_w, chev_h, "治理維度 \\ 階段",
                font_size=9.2, bold=True, color=RGBColor(255, 255, 255),
                align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    for c_idx, stg in enumerate(stages):
        cx = LEFT_X + label_w + gap_x + c_idx * (col_w + gap_x)
        shape = add_rect(slide, cx, TOP_Y, col_w, chev_h, theme["secondary"],
                         shape_type=MSO_SHAPE.CHEVRON)
        add_textbox(slide, cx + Inches(0.08), TOP_Y, col_w - Inches(0.18), chev_h,
                    stg, font_size=9.2, bold=True, color=RGBColor(255, 255, 255),
                    align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    # 下方矩陣列
    n_rows = max(len(rows), 1)
    gap_y = Inches(0.10)
    avail_h = AREA_H - chev_h - Inches(0.12)
    row_h = (avail_h - gap_y * (n_rows - 1)) / n_rows

    for r_idx, r in enumerate(rows):
        ry = TOP_Y + chev_h + Inches(0.12) + r_idx * (row_h + gap_y)
        add_rect(slide, LEFT_X, ry, label_w, row_h, theme["card_bg"], border_color=theme["primary"])
        add_textbox(slide, LEFT_X + Inches(0.06), ry, label_w - Inches(0.12), row_h,
                    r.get("label", ""), font_size=9.5, bold=True, color=theme["primary"],
                    align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

        cells = r.get("cells", [])
        for c_idx in range(n_cols):
            cx = LEFT_X + label_w + gap_x + c_idx * (col_w + gap_x)
            cell_text = cells[c_idx] if c_idx < len(cells) else ""
            add_rect(slide, cx, ry, col_w, row_h, RGBColor(255, 255, 255), border_color=theme["border"])
            add_textbox(slide, cx + Inches(0.08), ry + Inches(0.06), col_w - Inches(0.16), row_h - Inches(0.12),
                        cell_text, font_size=8.8, color=theme["text_dark"], line_spacing=1.15)


def render_opposition_left(slide, lec, theme):
    """⑥ 對立型 (Opposition / Two-Pole Tension Comparison)"""
    left_title = lec.get("left_title", "模式 A")
    right_title = lec.get("right_title", "模式 B")
    dims = lec.get("dimensions", [])

    dim_w = Inches(1.40)
    vs_w = Inches(0.44)
    side_w = (LEFT_W - dim_w - vs_w - Inches(0.16)) / 2
    left_col_x = LEFT_X + dim_w + Inches(0.08)
    vs_col_x = left_col_x + side_w
    right_col_x = vs_col_x + vs_w

    # 表頭
    hdr_h = Inches(0.58)
    add_rect(slide, LEFT_X, TOP_Y, dim_w, hdr_h, theme["card_bg"], border_color=theme["border"])
    add_textbox(slide, LEFT_X, TOP_Y, dim_w, hdr_h, "對立維度", font_size=9.5, bold=True,
                color=theme["primary"], align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    add_rect(slide, left_col_x, TOP_Y, side_w, hdr_h, RGBColor(100, 116, 139))
    add_textbox(slide, left_col_x + Inches(0.08), TOP_Y, side_w - Inches(0.16), hdr_h,
                left_title, font_size=9.8, bold=True, color=RGBColor(255, 255, 255),
                align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    add_textbox(slide, vs_col_x, TOP_Y, vs_w, hdr_h, "VS", font_size=10, bold=True,
                color=theme["secondary"], align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    add_rect(slide, right_col_x, TOP_Y, side_w, hdr_h, theme["primary"])
    add_textbox(slide, right_col_x + Inches(0.08), TOP_Y, side_w - Inches(0.16), hdr_h,
                right_title, font_size=9.8, bold=True, color=RGBColor(255, 255, 255),
                align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    # 對立維度列
    n = max(len(dims), 1)
    gap_y = Inches(0.10)
    avail_h = AREA_H - hdr_h - Inches(0.12)
    row_h = (avail_h - gap_y * (n - 1)) / n

    for i, d in enumerate(dims):
        ry = TOP_Y + hdr_h + Inches(0.12) + i * (row_h + gap_y)
        add_rect(slide, LEFT_X, ry, dim_w, row_h, theme["card_bg"], border_color=theme["border"])
        add_textbox(slide, LEFT_X + Inches(0.06), ry, dim_w - Inches(0.12), row_h,
                    d.get("dim", ""), font_size=9.2, bold=True, color=theme["primary"],
                    align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

        add_rect(slide, left_col_x, ry, side_w, row_h, RGBColor(248, 250, 252), border_color=theme["border"])
        add_textbox(slide, left_col_x + Inches(0.08), ry + Inches(0.06), side_w - Inches(0.16), row_h - Inches(0.12),
                    d.get("left", ""), font_size=8.8, color=theme["text_dark"], line_spacing=1.14)

        add_textbox(slide, vs_col_x, ry, vs_w, row_h, "⇄", font_size=12, bold=True,
                    color=theme["secondary"], align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

        add_rect(slide, right_col_x, ry, side_w, row_h, theme["card_bg"], border_color=theme["secondary"],
                 border_width=Pt(1.2))
        add_textbox(slide, right_col_x + Inches(0.08), ry + Inches(0.06), side_w - Inches(0.16), row_h - Inches(0.12),
                    d.get("right", ""), font_size=8.8, bold=False, color=theme["text_dark"], line_spacing=1.14)


def render_comparison_left(slide, lec, theme):
    """⑦ 對比型 (Venn / 3-Column Overlap Comparison)"""
    gap = Inches(0.12)
    col_w = (LEFT_W - gap * 2) / 3
    cols_data = [
        (lec.get("left_title", "左側要素"), lec.get("left_points", []), theme["primary"], False),
        (lec.get("common_title", "核心交集／均衡區"), lec.get("common_points", []), theme["secondary"], True),
        (lec.get("right_title", "右側要素"), lec.get("right_points", []), theme["primary"], False),
    ]

    for i, (title, pts, hdr_color, is_center) in enumerate(cols_data):
        x = LEFT_X + i * (col_w + gap)
        add_rect(slide, x, TOP_Y, col_w, AREA_H,
                 theme["card_bg"] if is_center else RGBColor(255, 255, 255),
                 border_color=theme["secondary"] if is_center else theme["border"],
                 border_width=Pt(1.8 if is_center else 1))
        add_rect(slide, x, TOP_Y, col_w, Inches(0.68), hdr_color)
        add_textbox(slide, x + Inches(0.08), TOP_Y + Inches(0.04), col_w - Inches(0.16), Inches(0.60),
                    title, font_size=10, bold=True, color=RGBColor(255, 255, 255),
                    align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

        body_text = "\n\n".join([f"● {pt}" for pt in pts])
        add_textbox(slide, x + Inches(0.12), TOP_Y + Inches(0.80), col_w - Inches(0.24), AREA_H - Inches(0.92),
                    body_text, font_size=9.2, color=theme["text_dark"], line_spacing=1.18)


def render_bcg_matrix_left(slide, lec, theme):
    """⑧ 2x2 矩陣 (BCG Strategic Four-Quadrant Matrix)"""
    quads = lec.get("quadrants", [])
    axis_label_space = Inches(0.36)
    grid_x = LEFT_X + axis_label_space
    grid_y = TOP_Y
    grid_w = LEFT_W - axis_label_space
    grid_h = AREA_H - axis_label_space

    # Y 軸與 X 軸標籤
    add_textbox(slide, LEFT_X, TOP_Y, axis_label_space, grid_h,
                f"▲\n{lec.get('y_axis', '縱軸維度')}", font_size=8.8, bold=True,
                color=theme["primary"], align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
    add_textbox(slide, grid_x, TOP_Y + grid_h + Inches(0.04), grid_w, Inches(0.30),
                f"{lec.get('x_axis', '橫軸維度')}  ▶", font_size=9.2, bold=True,
                color=theme["primary"], align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    gap = Inches(0.14)
    qw = (grid_w - gap) / 2
    qh = (grid_h - gap) / 2

    for idx, q in enumerate(quads[:4]):
        r = idx // 2
        c = idx % 2
        qx = grid_x + c * (qw + gap)
        qy = grid_y + r * (qh + gap)
        is_hl = q.get("highlight", False)

        add_rect(slide, qx, qy, qw, qh,
                 theme["card_bg"] if is_hl else RGBColor(255, 255, 255),
                 border_color=theme["secondary"] if is_hl else theme["border"],
                 border_width=Pt(1.8 if is_hl else 1))
        add_rect(slide, qx, qy, qw, Inches(0.40),
                 theme["secondary"] if is_hl else theme["primary"])
        add_textbox(slide, qx + Inches(0.10), qy + Inches(0.03), qw - Inches(0.20), Inches(0.34),
                    q.get("pos", f"象限 {idx+1}"), font_size=9.2, bold=True,
                    color=RGBColor(255, 255, 255), valign=MSO_ANCHOR.MIDDLE)

        add_textbox(slide, qx + Inches(0.12), qy + Inches(0.46), qw - Inches(0.24), Inches(0.40),
                    q.get("title", ""), font_size=10.8, bold=True, color=theme["primary"])
        add_textbox(slide, qx + Inches(0.12), qy + Inches(0.88), qw - Inches(0.24), qh - Inches(0.96),
                    q.get("desc", ""), font_size=9.0, color=theme["text_dark"], line_spacing=1.15)


LAYOUT_RENDERERS = {
    "one_to_one": render_one_to_one_left,
    "parallel": render_parallel_left,
    "combined": render_combined_left,
    "chain": render_chain_left,
    "mckinsey_flow": render_mckinsey_flow_left,
    "opposition": render_opposition_left,
    "comparison": render_comparison_left,
    "bcg_matrix": render_bcg_matrix_left,
}


def add_cover_slide(prs, title, subtitle, deck_label, total_pages):
    """封面頁 (含高品質企業治理視覺大圖)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    theme = THEMES["mckinsey"]
    add_rect(slide, Inches(0), Inches(0), Inches(13.333), Inches(7.5), theme["primary"])
    add_rect(slide, Inches(0), Inches(0), Inches(0.22), Inches(7.5), theme["secondary"])

    # 左側標題區
    add_rect(slide, Inches(0.75), Inches(0.85), Inches(4.5), Inches(0.36), theme["secondary"],
             shape_type=MSO_SHAPE.ROUNDED_RECTANGLE)
    add_textbox(slide, Inches(0.85), Inches(0.87), Inches(4.3), Inches(0.32),
                deck_label, font_size=10.5, bold=True, color=RGBColor(255, 255, 255),
                valign=MSO_ANCHOR.MIDDLE)

    add_textbox(slide, Inches(0.75), Inches(1.55), Inches(7.2), Inches(1.8),
                title, font_size=30, bold=True, color=RGBColor(255, 255, 255),
                font_name=FONT_HEADING, line_spacing=1.2)

    add_textbox(slide, Inches(0.75), Inches(3.45), Inches(7.2), Inches(1.2),
                subtitle, font_size=13.5, color=RGBColor(203, 213, 225), line_spacing=1.35)

    # 雙軌設計徽章
    add_rect(slide, Inches(0.75), Inches(4.95), Inches(7.1), Inches(1.45),
             RGBColor(12, 43, 68), border_color=theme["secondary"])
    add_textbox(
        slide, Inches(0.95), Inches(5.08), Inches(6.7), Inches(1.2),
        "🌱 入門者導讀（Plain-Language & Cases）：白話拆解核心定義＋萬科、安隆、國美、福耀等 40 個真實商業故事\n"
        "🏛️ 進階者架構（Executive Mental Models）：CEO 頂層思考模型＋#041 跨講次因果鏈＋董事會決策檢核表\n"
        "🎨 無雜訊顧問視覺（Zero-Noise 8 Archetypes）：森秀明 8 大邏輯版型 × McKinsey/BCG/Accenture 視覺系統",
        font_size=10.2, color=RGBColor(241, 245, 249), line_spacing=1.35
    )

    # 右側視覺圖片與原版課程架構圖預覽
    cover_img = get_cropped_image("/images/unsplash/topic_cover.jpg", target_ratio=4/3)
    if cover_img and os.path.exists(cover_img):
        slide.shapes.add_picture(cover_img, Inches(8.25), Inches(0.85), width=Inches(4.45), height=Inches(3.34))

    course_map_img = get_cropped_image("/images/lectures/lec_00_1.jpg", target_ratio=16/10)
    if course_map_img and os.path.exists(course_map_img):
        slide.shapes.add_picture(course_map_img, Inches(8.25), Inches(4.35), width=Inches(4.45), height=Inches(2.05))

    add_textbox(slide, Inches(8.25), Inches(6.45), Inches(4.45), Inches(0.45),
                "▲ 視覺輔助：企業董事會決策場景 ＆ 劉松博《公司治理30講》原版全書知識地圖",
                font_size=8.8, color=RGBColor(148, 163, 184), align=PP_ALIGN.CENTER)

    add_textbox(slide, Inches(0.75), Inches(6.95), Inches(11.8), Inches(0.35),
                f"A2.5 企業管理｜執行長專業知識庫 Flagship Deck   ｜   1 / {total_pages}",
                font_size=9.5, color=RGBColor(148, 163, 184))


def add_architecture_slide(prs, total_pages):
    """第 2 頁：全書四大模組 × 跨講因果架構總覽頁 (含原版課程圖表)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    theme = THEMES["mckinsey"]
    fake_lec = {
        "code": "ARCH",
        "kb_id": "#041",
        "title": "全書四大模組與跨講次因果邏輯總覽",
        "category": "執行長專業知識庫｜全書系統架構 (#041)",
        "layout_label": "⑤ 流程矩陣 (Architecture Map)",
        "conclusion_title": "公司治理以「權力分配與制衡」為核心，串聯股權、兩會運作與經理人激勵四大閉環",
        "subtitle": "從「我是誰（公司主體）」到「誰說了算（股權）」、「如何共治（董事會）」、「如何代理（CEO激勵與家族傳承）」",
        "footer": "全書架構總覽｜對應知識庫 #041 跨講次因果關係與全書邏輯架構",
        "keywords": ["四大模組", "所有權與經營權分離", "股權制衡", "董事會治理", "委託代理理論"],
        "web_image": "/images/lectures/lec_00_1.jpg",
        "web_image_caption": "劉松博《公司治理30講》原版全書知識結構圖：以利益相關者為外環，股東會、董事會、監事會、高層經理人為核心內環。",
        "beginner": {
            "summary": "把公司治理想成「開飛機的規則」：第一模組認識飛機構造（公司與有限責任），第二模組決定誰握有方向盤所有權（股權），第三模組設計駕駛艙儀表板與副駕駛監督（董事會與監事會），第四模組則是如何獎勵機長安全飛抵目的地（CEO聘任與激勵）。"
        },
        "advanced": {
            "model_name": "公司治理四階因果漏斗 (4-Stage Governance Funnel)",
            "model_desc": "制度起源（有限責任＋兩權分離）➔ 產權配置（股權結構＋控制權槓桿）➔ 機構制衡（董事會獨立性＋表決程序＋監事會）➔ 代理對齊（外部市場接管＋長期股權激勵＋家族憲章）。"
        },
        "speaker_notes": {
            "conclusion": "在進入各講細節前，請先掌握這張全書因果架構圖：40 講內容並非零散知識，而是一條嚴密的制度演化鏈。",
            "explanation": "四大模組環環相扣：因為現代公司採行「有限責任」與「兩權分離」（模組一），才衍生出大股東與小股東的「股權爭奪與設計」（模組二）；為了避免股東天天吵架並引進專業決策，必須透過「董事會與監事會」（模組三）進行集體治理；最終落實到「如何選拔、監督與激勵 CEO 及合夥人」（模組四）。",
            "transition": "接下來我們將依序拆解每一講的無雜訊顧問簡報。"
        }
    }
    add_slide_chrome(slide, fake_lec, theme, 2, total_pages)

    # 左側渲染四大模組矩陣
    fake_lec["stages"] = ["模組一：基礎與演進\n(00~05講)", "模組二：股權與股東\n(06~14講)", "模組三：董事與監事\n(15~22講)", "模組四：經理人與控制\n(23~39講)"]
    fake_lec["rows"] = [
        {"label": "核心命題", "cells": [
            "企業制度起源、有限責任奇蹟、兩權分離與利益相關者邊界",
            "股權生命線（67/51/34%）、一致行動人、AB股、金字塔與國企混改",
            "股東會程序正義、董事會規模與結構、獨立董事、累積投票與監事會",
            "CEO選拔標準、代理成本、股權激勵、敵意收購防禦、合夥人與家族治理"
        ]},
        {"label": "解決痛點", "cells": [
            "打破「企業＝老闆私產」迷思，確立獨立法人財產與治理制衡底線",
            "消滅五五開僵局、防範金字塔掏空、用少數資金鎖定公司控制權",
            "防止一言堂與人情董事會，落實「一人一票、會議決策、程序合規」",
            "化解「經理人偷懶與帝國建造」，防止野蠻人突襲與家族富不過三代"
        ]},
        {"label": "代表案例", "cells": [
            "巴林銀行倒閉案、東印度公司、安隆(Enron)破產案、優步(Uber)",
            "真功夫50:50僵局、海底撈68:32破局、Facebook AB股、阿里巴巴合夥人",
            "萬科王石與華潤之爭、樂視網獨董辭職潮、中集集團累積投票制",
            "萬科寶能控制權大戰、國美黃光裕陳曉之爭、福耀玻璃曹德旺接班"
        ]}
    ]
    render_mckinsey_flow_left(slide, fake_lec, theme)
    render_right_visual_panel(slide, fake_lec, theme)
    set_speaker_notes(slide, fake_lec)


def build_deck(lectures_subset, output_filename, deck_title, deck_subtitle, deck_label):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    total_pages = len(lectures_subset) + 2
    add_cover_slide(prs, deck_title, deck_subtitle, deck_label, total_pages)
    add_architecture_slide(prs, total_pages)

    for idx, lec in enumerate(lectures_subset):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        style_key = lec.get("style", "mckinsey")
        theme = THEMES.get(style_key, THEMES["mckinsey"])
        page_num = idx + 3

        add_slide_chrome(slide, lec, theme, page_num, total_pages)
        ltype = lec.get("type", "parallel")
        renderer = LAYOUT_RENDERERS.get(ltype, render_parallel_left)
        renderer(slide, lec, theme)
        render_right_visual_panel(slide, lec, theme)
        set_speaker_notes(slide, lec)

    out_path_public = os.path.join(DOWNLOAD_DIR, output_filename)
    prs.save(out_path_public)
    print(f"[OK] Saved PPTX to public downloads: {out_path_public} ({total_pages} slides)")

    if os.path.exists(SOURCE_FOLDER):
        out_path_source = os.path.join(SOURCE_FOLDER, output_filename)
        shutil.copy2(out_path_public, out_path_source)
        print(f"[OK] Copied PPTX to source folder: {out_path_source}")


def main():
    # 1. 精華 16 頁執行長決策簡報 (Cover + Architecture + 14 核心講次，完整涵蓋四大模組與 8 種版型)
    exec_ids = ["00", "01", "03", "07", "09", "10", "11", "16", "17", "21", "24", "26", "29", "32"]
    exec_lectures = [lec for lec in ALL_LECTURES if lec["id"] in exec_ids]
    build_deck(
        exec_lectures,
        "劉松博_公司治理30講_無雜訊顧問簡報_精華16頁.pptx",
        "劉松博《公司治理30講》\n無雜訊執行長決策簡報（精華 16 頁）",
        "從入門概念到 CEO 頂層思考架構｜涵蓋股權設計、董事會制衡、經理人激勵與控制權防禦",
        "EXECUTIVE BRIEFING｜16-SLIDE ZERO-NOISE DECK"
    )

    # 2. 全 40 講完整無雜訊顧問簡報庫 (Cover + Architecture + 40 講全收錄 = 42 頁)
    build_deck(
        ALL_LECTURES,
        "劉松博_公司治理30講_全40講無雜訊顧問簡報庫.pptx",
        "劉松博《公司治理30講》\n全 40 講無雜訊顧問簡報完整百科（42 頁）",
        "完整萃取 00 發刊詞、01~34 正課、35~37 加餐與結語書單｜每頁配備視覺情境圖片與雙軌思考模型",
        "COMPLETE 42-SLIDE ENCYCLOPEDIA｜ZERO-NOISE CONSULTING DECK"
    )


if __name__ == "__main__":
    main()
