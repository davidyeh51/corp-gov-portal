# -*- coding: utf-8 -*-
"""
生成「執行長專業 (CEO Executive Mastery)」入口網站與《劉松博・公司治理30講》無雜訊顧問簡報知識庫
包含：
1. VitePress 全站配置 (含 base: '/corp-gov-portal/' 與繁體中文本地全文搜尋)
2. 顧問級無雜訊 16:9 簡報 CSS 視覺系統 (支援森秀明 8 大版型與 McKinsey/BCG/Accenture 主題色)
3. 執行長專業入口首頁 (docs/index.md)：涵蓋 A2.5 八大管理領域擴充架構 + 即時關鍵字搜尋器
4. 互動式 16:9 無雜訊簡報劇場 (docs/slides/index.md)：支援 16頁精華版 / 42頁完整百科切換、鍵盤左右翻頁、入門/進階視角切換、三段式講稿抽屜與 PPTX 下載
5. 跨講次因果邏輯與全書系統架構專頁 (docs/architecture/index.md，對應 #041)
6. 八大管理領域未來擴充館 (docs/domains/index.md，串聯孫子兵法、藍海策略、生態系競爭策略、團隊協作五大障礙、超級專案管理、黃崇仁經營哲學等)
7. 全 40 講深度知識萃取與簡報專頁 (docs/30-lectures/00.md ~ 39.md)：每頁皆含 16:9 無雜訊簡報圖卡（內嵌情境圖片与圖說）、🌱入門導讀與案例故事、🏛️進階思考模型與決策檢核表、🎙️三段式顧問講稿、🖼️原版課程圖表/金句卡、以及 OpenCC 繁體化完整課程逐字稿。
"""
import os
import re
import sys
import json
import glob
import opencc

sys.stdout.reconfigure(encoding='utf-8')

from data_part1 import LECTURES_PART1
from data_part2 import LECTURES_PART2

ALL_LECTURES = LECTURES_PART1 + LECTURES_PART2
EXEC_16_IDS = ["00", "01", "03", "07", "09", "10", "11", "16", "17", "21", "24", "26", "29", "32"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
VP_DIR = os.path.join(DOCS_DIR, ".vitepress")
THEME_DIR = os.path.join(VP_DIR, "theme")
LECTURES_OUT_DIR = os.path.join(DOCS_DIR, "30-lectures")
SLIDES_OUT_DIR = os.path.join(DOCS_DIR, "slides")
ARCH_OUT_DIR = os.path.join(DOCS_DIR, "architecture")
DOMAINS_OUT_DIR = os.path.join(DOCS_DIR, "domains")
SOURCE_FOLDER = os.path.abspath(os.path.join(BASE_DIR, "..", "刘松博_公司治理30讲"))

for d in [DOCS_DIR, VP_DIR, THEME_DIR, LECTURES_OUT_DIR, SLIDES_OUT_DIR, ARCH_OUT_DIR, DOMAINS_OUT_DIR]:
    os.makedirs(d, exist_ok=True)

cc = opencc.OpenCC('s2twp')

SITE_BASE = "/corp-gov-portal"


def with_base(path_str):
    if not path_str:
        return ""
    if path_str.startswith("http://") or path_str.startswith("https://"):
        return path_str
    clean = path_str if path_str.startswith("/") else "/" + path_str
    return f"{SITE_BASE}{clean}"


def load_source_markdown_files():
    """讀取原始 40 講 .md 檔案，轉為繁體中文並提取本地圖片映射"""
    md_files = sorted(glob.glob(os.path.join(SOURCE_FOLDER, "*.md")))
    lecture_raw_map = {}
    idx = 0
    for fpath in md_files:
        fname = os.path.basename(fpath)
        if "知識庫" in fname or "知识库" in fname:
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            raw = f.read()
        # 移除音訊連結行
        raw = re.sub(r'🎧\s*\[收听音频\]\([^\)]+\)\s*', '', raw)
        # 轉換為繁體中文 (台灣常用詞彙)
        trad = cc.convert(raw)
        lec_id = f"{idx:02d}"
        # 將 umiwi 圖片網址替換為本地已下載的 /corp-gov-portal/images/lectures/lec_XX_Y.ext
        img_counter = [0]

        def repl_img(match):
            alt_txt = match.group(1)
            url = match.group(2)
            img_counter[0] += 1
            ext = ".png" if ".png" in url.lower() else ".jpg"
            local_rel = f"/images/lectures/lec_{lec_id}_{img_counter[0]}{ext}"
            local_full = os.path.join(DOCS_DIR, "public", local_rel.lstrip("/").replace("/", os.sep))
            if not os.path.exists(local_full):
                # 嘗試另一種副檔名
                alt_ext = ".jpg" if ext == ".png" else ".png"
                local_rel = f"/images/lectures/lec_{lec_id}_{img_counter[0]}{alt_ext}"
            return f'<img src="{with_base(local_rel)}" alt="{alt_txt}" style="max-width:100%; border-radius:8px; margin:12px 0;" />'

        trad = re.sub(r'!\[([^\]]*)\]\((https?://[^\)]+)\)', repl_img, trad)
        lecture_raw_map[lec_id] = trad
        idx += 1
    return lecture_raw_map


def render_slide_left_html(lec):
    """根據森秀明 8 種無雜訊版型，輸出對應的 HTML 圖解結構"""
    ltype = lec.get("type", "parallel")

    if ltype == "one_to_one":
        rows_html = []
        for b in lec.get("bars", []):
            hl_cls = "zn-highlight" if b.get("highlight") else ""
            val = max(min(int(b.get("value", 50)), 100), 10)
            rows_html.append(f"""
            <div class="zn-bar-card {hl_cls}">
              <div class="zn-bar-top">
                <span class="zn-bar-label">{b.get('label', '')}</span>
                <div class="zn-bar-track">
                  <div class="zn-bar-fill" style="width: {val}%;">
                    <span class="zn-bar-val">{b.get('display', '')}</span>
                  </div>
                </div>
              </div>
              <div class="zn-bar-desc">{b.get('desc', '')}</div>
            </div>
            """)
        return f'<div class="zn-layout-one-to-one">{"".join(rows_html)}</div>'

    elif ltype == "parallel":
        cards_html = []
        for c in lec.get("cards", []):
            hl_cls = "zn-highlight" if c.get("highlight") else ""
            cards_html.append(f"""
            <div class="zn-pcard {hl_cls}">
              <div class="zn-pcard-hdr">
                <span class="zn-pcard-tag">{c.get('tag', '')}</span>
                <span class="zn-pcard-metric">{c.get('metric', '')}</span>
              </div>
              <div class="zn-pcard-title">{c.get('title', '')}</div>
              <div class="zn-pcard-desc">{c.get('desc', '')}</div>
            </div>
            """)
        return f'<div class="zn-layout-parallel">{"".join(cards_html)}</div>'

    elif ltype == "combined":
        pillars_html = []
        for p in lec.get("pillars", []):
            hl_cls = "zn-highlight" if p.get("highlight") else ""
            pts_li = "".join([f"<li>{pt}</li>" for pt in p.get("points", [])])
            pillars_html.append(f"""
            <div class="zn-pillar {hl_cls}">
              <div class="zn-pillar-hdr">{p.get('title', '')}</div>
              <ul class="zn-pillar-list">{pts_li}</ul>
            </div>
            """)
        banner = lec.get("synthesis_banner", "")
        return f"""
        <div class="zn-layout-combined">
          <div class="zn-pillars-row">{"".join(pillars_html)}</div>
          <div class="zn-synthesis-banner">🎯 結合型核心綜效：{banner}</div>
        </div>
        """

    elif ltype == "chain":
        steps_html = []
        for s in lec.get("steps", []):
            hl_cls = "zn-highlight" if s.get("highlight") else ""
            steps_html.append(f"""
            <div class="zn-chain-step {hl_cls}">
              <div class="zn-chain-badge">{s.get('phase', '')}</div>
              <div class="zn-chain-body">
                <div class="zn-chain-title">{s.get('title', '')}</div>
                <div class="zn-chain-desc">{s.get('desc', '')}</div>
              </div>
            </div>
            """)
        return f'<div class="zn-layout-chain">{"".join(steps_html)}</div>'

    elif ltype == "mckinsey_flow":
        stages = lec.get("stages", [])
        rows = lec.get("rows", [])
        hdr_cells = "".join([f'<th class="zn-flow-stg">{stg}</th>' for stg in stages])
        body_rows = []
        for r in rows:
            tds = "".join([f'<td>{cell}</td>' for cell in r.get("cells", [])])
            body_rows.append(f'<tr><th class="zn-flow-rowlbl">{r.get("label", "")}</th>{tds}</tr>')
        return f"""
        <div class="zn-layout-flow">
          <table class="zn-flow-table">
            <thead>
              <tr><th class="zn-flow-corner">維度 \\ 階段</th>{hdr_cells}</tr>
            </thead>
            <tbody>{"".join(body_rows)}</tbody>
          </table>
        </div>
        """

    elif ltype == "opposition":
        l_title = lec.get("left_title", "對立極 A")
        r_title = lec.get("right_title", "對立極 B")
        dims_html = []
        for d in lec.get("dimensions", []):
            dims_html.append(f"""
            <tr>
              <th class="zn-opp-dim">{d.get('dim', '')}</th>
              <td class="zn-opp-left">{d.get('left', '')}</td>
              <td class="zn-opp-vs">⇄</td>
              <td class="zn-opp-right">{d.get('right', '')}</td>
            </tr>
            """)
        return f"""
        <div class="zn-layout-opposition">
          <table class="zn-opp-table">
            <thead>
              <tr>
                <th class="zn-opp-dim-hdr">比較維度</th>
                <th class="zn-opp-left-hdr">{l_title}</th>
                <th class="zn-opp-vs-hdr">VS</th>
                <th class="zn-opp-right-hdr">{r_title}</th>
              </tr>
            </thead>
            <tbody>{"".join(dims_html)}</tbody>
          </table>
        </div>
        """

    elif ltype == "comparison":
        l_pts = "".join([f"<li>{pt}</li>" for pt in lec.get("left_points", [])])
        c_pts = "".join([f"<li>{pt}</li>" for pt in lec.get("common_points", [])])
        r_pts = "".join([f"<li>{pt}</li>" for pt in lec.get("right_points", [])])
        return f"""
        <div class="zn-layout-comparison">
          <div class="zn-comp-col">
            <div class="zn-comp-hdr">{lec.get('left_title', '')}</div>
            <ul class="zn-comp-list">{l_pts}</ul>
          </div>
          <div class="zn-comp-col zn-comp-center">
            <div class="zn-comp-hdr">{lec.get('common_title', '')}</div>
            <ul class="zn-comp-list">{c_pts}</ul>
          </div>
          <div class="zn-comp-col">
            <div class="zn-comp-hdr">{lec.get('right_title', '')}</div>
            <ul class="zn-comp-list">{r_pts}</ul>
          </div>
        </div>
        """

    elif ltype == "bcg_matrix":
        q_html = []
        for q in lec.get("quadrants", [])[:4]:
            hl_cls = "zn-highlight" if q.get("highlight") else ""
            q_html.append(f"""
            <div class="zn-quad {hl_cls}">
              <div class="zn-quad-pos">{q.get('pos', '')}</div>
              <div class="zn-quad-title">{q.get('title', '')}</div>
              <div class="zn-quad-desc">{q.get('desc', '')}</div>
            </div>
            """)
        return f"""
        <div class="zn-layout-matrix">
          <div class="zn-matrix-axis-y">▲ 縱軸：{lec.get('y_axis', '')}</div>
          <div class="zn-matrix-grid">{"".join(q_html)}</div>
          <div class="zn-matrix-axis-x">橫軸：{lec.get('x_axis', '')} ▶</div>
        </div>
        """
    return ""


def render_full_slide_card_html(lec, page_idx=1, total_pages=40):
    """生成完整 16:9 無雜訊顧問簡報 HTML 卡片（左側 8 大版型圖解 ＋ 右側視覺情境圖片與雙軌導讀）"""
    style_cls = f"zn-theme-{lec.get('style', 'mckinsey')}"
    left_html = render_slide_left_html(lec)
    web_img_url = with_base(lec.get("web_image", "/images/unsplash/topic_00.jpg"))
    kw_tags = " / ".join(lec.get("keywords", []))
    beg_summary = lec.get("beginner", {}).get("summary", "")
    adv_name = lec.get("advanced", {}).get("model_name", "")
    adv_desc = lec.get("advanced", {}).get("model_desc", "")

    return f"""
<div class="zn-slide-frame {style_cls}">
  <div class="zn-slide-top-bar"></div>
  <div class="zn-slide-header">
    <div class="zn-slide-eyebrow">
      <span class="zn-badge-cat">{lec.get('category', '')}</span>
      <span class="zn-badge-layout">{lec.get('layout_label', '')}</span>
      <span class="zn-badge-kb">知識庫 {lec.get('kb_id', '')}</span>
    </div>
    <h2 class="zn-slide-action-title">{lec.get('conclusion_title', '')}</h2>
    <p class="zn-slide-subtitle">{lec.get('subtitle', '')}</p>
  </div>

  <div class="zn-slide-body">
    <div class="zn-slide-main">
      {left_html}
    </div>
    <div class="zn-slide-visual-panel">
      <div class="zn-vpanel-hdr">🖼️ 視覺情境輔助 ＆ 入門／進階雙軌快照</div>
      <div class="zn-vpanel-img-wrap">
        <img src="{web_img_url}" alt="{lec.get('title', '')}" loading="lazy" />
        <div class="zn-vpanel-caption">📌 {lec.get('web_image_caption', '')}</div>
      </div>
      <div class="zn-vpanel-dual">
        <div class="zn-mini-box zn-mini-beg">
          <div class="zn-mini-title">🌱 入門者核心秒懂</div>
          <div class="zn-mini-text">{beg_summary}</div>
        </div>
        <div class="zn-mini-box zn-mini-adv">
          <div class="zn-mini-title">🏛️ 進階架構：{adv_name}</div>
          <div class="zn-mini-text">{adv_desc}</div>
        </div>
      </div>
    </div>
  </div>

  <div class="zn-slide-footer">
    <span>{lec.get('footer', '')} ｜ 關鍵字：{kw_tags}</span>
    <span class="zn-slide-pagenum">SLIDE {page_idx} / {total_pages}</span>
  </div>
</div>
"""


def write_vitepress_config():
    """生成 docs/.vitepress/config.mjs，確保包含 base: '/corp-gov-portal/' 與本地全文搜尋"""
    sidebar_m1 = []
    sidebar_m2 = []
    sidebar_m3 = []
    sidebar_m4 = []

    for lec in ALL_LECTURES:
        item = {
            "text": f"{lec['code']}｜{lec['short_title']}",
            "link": f"/30-lectures/{lec['id']}"
        }
        mid = lec.get("module_id", "m1")
        if mid == "m1":
            sidebar_m1.append(item)
        elif mid == "m2":
            sidebar_m2.append(item)
        elif mid == "m3":
            sidebar_m3.append(item)
        else:
            sidebar_m4.append(item)

    config_js = f"""import {{ defineConfig }} from 'vitepress'

export default defineConfig({{
  base: '/corp-gov-portal/',
  ignoreDeadLinks: true,
  lang: 'zh-TW',
  title: '執行長專業知識庫｜CEO Executive Mastery',
  description: 'A2.5 企業管理頂層入口網站 × 劉松博《公司治理30講》無雜訊顧問簡報與雙軌思考架構百科',
  cleanUrls: true,
  head: [
    ['link', {{ rel: 'icon', href: '/corp-gov-portal/images/lectures/lec_00_1.jpg' }}]
  ],
  themeConfig: {{
    siteTitle: '🏛️ 執行長專業知識庫',
    nav: [
      {{ text: '🏠 執行長入口首頁', link: '/' }},
      {{ text: '🎯 無雜訊顧問簡報劇場', link: '/slides/' }},
      {{ text: '🧭 全書因果架構 (#041)', link: '/architecture/' }},
      {{
        text: '📚 公司治理30講 (全40講)',
        items: [
          {{ text: '模組一：基礎與演進 (00~05)', link: '/30-lectures/00' }},
          {{ text: '模組二：股權與股東 (06~14)', link: '/30-lectures/06' }},
          {{ text: '模組三：董事會與監事會 (15~22)', link: '/30-lectures/15' }},
          {{ text: '模組四：經理人、控制權與家族 (23~39)', link: '/30-lectures/23' }}
        ]
      }},
      {{ text: '🗂️ 八大管理領域擴充館', link: '/domains/' }},
      {{
        text: '📥 下載 PPTX 簡報',
        items: [
          {{ text: '📊 下載精華 16 頁決策簡報 (.pptx)', link: 'https://davidyeh51.github.io/corp-gov-portal/downloads/劉松博_公司治理30講_無雜訊顧問簡報_精華16頁.pptx' }},
          {{ text: '📘 下載全 40 講完整簡報百科 (.pptx)', link: 'https://davidyeh51.github.io/corp-gov-portal/downloads/劉松博_公司治理30講_全40講無雜訊顧問簡報庫.pptx' }}
        ]
      }}
    ],
    sidebar: [
      {{
        text: '🏛️ 執行長專業總覽與簡報中心',
        collapsed: false,
        items: [
          {{ text: '🏠 執行長專業入口首頁 (含關鍵字檢索)', link: '/' }},
          {{ text: '🎯 16:9 無雜訊顧問簡報互動劇場', link: '/slides/' }},
          {{ text: '🧭 跨講次因果邏輯與全書架構 (#041)', link: '/architecture/' }},
          {{ text: '🗂️ A2.5 八大管理領域擴充館', link: '/domains/' }}
        ]
      }},
      {{
        text: '模組一：公司治理基礎與演進 (00~05)',
        collapsed: false,
        items: {json.dumps(sidebar_m1, ensure_ascii=False)}
      }},
      {{
        text: '模組二：股權結構與股東治理 (06~14)',
        collapsed: false,
        items: {json.dumps(sidebar_m2, ensure_ascii=False)}
      }},
      {{
        text: '模組三：董事會與監事會運作 (15~22)',
        collapsed: false,
        items: {json.dumps(sidebar_m3, ensure_ascii=False)}
      }},
      {{
        text: '模組四：經理人激勵、控制權與家族治理 (23~39)',
        collapsed: false,
        items: {json.dumps(sidebar_m4, ensure_ascii=False)}
      }}
    ],
    search: {{
      provider: 'local',
      options: {{
        detailedView: true,
        translations: {{
          button: {{
            buttonText: '🔍 搜尋知識庫、案例、模型、關鍵字...',
            buttonAriaLabel: '搜尋知識庫'
          }},
          modal: {{
            displayDetails: '顯示詳細內容',
            resetButtonTitle: '清除搜尋',
            backButtonTitle: '返回',
            noResultsText: '找不到相關內容，請嘗試搜尋「股權」「萬科」「獨立董事」「毒丸」「AB股」等關鍵字',
            footer: {{
              selectText: '前往閱讀',
              navigateText: '上下切換',
              closeText: '關閉 (ESC)'
            }}
          }}
        }}
      }}
    }},
    outline: {{
      level: [2, 3],
      label: '本頁知識導覽'
    }},
    docFooter: {{
      prev: '上一講',
      next: '下一講'
    }},
    footer: {{
      message: 'A2.5 企業管理｜執行長專業知識庫（Zero-Noise Consulting Presentation & Dual-Track Knowledge Portal）',
      copyright: 'Built for DavidCloud Executive Mastery｜遵循森秀明無雜訊簡報 8 大版型與三大顧問公司視覺規範'
    }}
  }}
}})
"""
    with open(os.path.join(VP_DIR, "config.mjs"), "w", encoding="utf-8") as f:
        f.write(config_js)
    print("[OK] Wrote docs/.vitepress/config.mjs")


def write_custom_theme():
    """生成 docs/.vitepress/theme/index.js 與 style.css"""
    theme_idx = """import DefaultTheme from 'vitepress/theme'
import './style.css'

export default {
  extends: DefaultTheme
}
"""
    with open(os.path.join(THEME_DIR, "index.js"), "w", encoding="utf-8") as f:
        f.write(theme_idx)

    css_content = """/* ==========================================================================
   CEO Executive Mastery Portal & Zero-Noise Consulting Slide System
   Morihideaki 8 Archetypes × McKinsey / BCG / Accenture Visual Tokens
   ========================================================================== */

:root {
  --vp-c-brand-1: #0077C8;
  --vp-c-brand-2: #051C2C;
  --vp-c-brand-3: #00A3E0;
  --vp-layout-max-width: 1520px;
}

.VPDoc.has-aside .content-container {
  max-width: 1120px !important;
}

/* --------------------------------------------------------------------------
   16:9 Zero-Noise Consulting Slide Frame
   -------------------------------------------------------------------------- */
.zn-slide-frame {
  --zn-primary: #051C2C;
  --zn-secondary: #0077C8;
  --zn-accent: #00A3E0;
  --zn-card-bg: #F4F6F9;
  --zn-panel-bg: #F8FAFC;
  --zn-border: #CBD5E1;
  --zn-text: #1E293B;
  --zn-muted: #64748B;

  background: #FFFFFF;
  color: var(--zn-text);
  border: 1px solid var(--zn-border);
  border-radius: 10px;
  box-shadow: 0 12px 32px -8px rgba(5, 28, 44, 0.14), 0 4px 12px -2px rgba(5, 28, 44, 0.06);
  overflow: hidden;
  margin: 1.5rem 0 2.2rem 0;
  display: flex;
  flex-direction: column;
  position: relative;
}

.zn-theme-bcg {
  --zn-primary: #004B2B;
  --zn-secondary: #177B57;
  --zn-accent: #2ECC71;
  --zn-card-bg: #F2F8F5;
  --zn-panel-bg: #F7FBF9;
  --zn-border: #C3DCCF;
}

.zn-theme-accenture {
  --zn-primary: #2D1054;
  --zn-secondary: #A100FF;
  --zn-accent: #C666FF;
  --zn-card-bg: #F8F5FC;
  --zn-panel-bg: #FAF8FD;
  --zn-border: #D8CCE8;
}

.zn-slide-top-bar {
  height: 7px;
  background: linear-gradient(90deg, var(--zn-primary) 0%, var(--zn-secondary) 70%, var(--zn-accent) 100%);
  width: 100%;
}

.zn-slide-header {
  padding: 16px 24px 12px 24px;
  border-bottom: 1.5px solid var(--zn-border);
  background: #FFFFFF;
}

.zn-slide-eyebrow {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  margin-bottom: 8px;
}

.zn-badge-cat {
  font-size: 12px;
  font-weight: 700;
  color: var(--zn-secondary);
  letter-spacing: 0.03em;
}

.zn-badge-layout {
  font-size: 11.5px;
  font-weight: 700;
  background: var(--zn-primary);
  color: #FFFFFF;
  padding: 2px 10px;
  border-radius: 999px;
}

.zn-badge-kb {
  font-size: 11.5px;
  font-weight: 600;
  background: var(--zn-card-bg);
  color: var(--zn-primary);
  border: 1px solid var(--zn-border);
  padding: 1px 8px;
  border-radius: 6px;
}

.zn-slide-action-title {
  margin: 0 !important;
  padding: 0 !important;
  border: none !important;
  font-size: 21px !important;
  line-height: 1.32 !important;
  font-weight: 800 !important;
  color: var(--zn-primary) !important;
  letter-spacing: -0.01em;
}

.zn-slide-subtitle {
  margin: 5px 0 0 0 !important;
  font-size: 13.5px !important;
  line-height: 1.4 !important;
  color: var(--zn-muted) !important;
}

.zn-slide-body {
  display: grid;
  grid-template-columns: 64% 36%;
  gap: 0;
  min-height: 430px;
  background: #FFFFFF;
}

@media (max-width: 960px) {
  .zn-slide-body {
    grid-template-columns: 1fr;
  }
}

.zn-slide-main {
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

/* Right Visual & Dual-Track Panel */
.zn-slide-visual-panel {
  background: var(--zn-panel-bg);
  border-left: 1px solid var(--zn-border);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 14px 16px;
}

.zn-vpanel-hdr {
  background: var(--zn-primary);
  color: #FFFFFF;
  font-size: 12px;
  font-weight: 700;
  padding: 6px 10px;
  border-radius: 6px;
  margin-bottom: 10px;
}

.zn-vpanel-img-wrap {
  background: #FFFFFF;
  border: 1px solid var(--zn-border);
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 10px;
}

.zn-vpanel-img-wrap img {
  width: 100%;
  height: 175px;
  object-fit: cover;
  display: block;
}

.zn-vpanel-caption {
  padding: 7px 10px;
  font-size: 11.5px;
  line-height: 1.38;
  color: var(--zn-text);
  background: #FFFFFF;
  border-top: 1px solid var(--zn-border);
}

.zn-vpanel-dual {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.zn-mini-box {
  background: #FFFFFF;
  border: 1px solid var(--zn-border);
  border-radius: 6px;
  padding: 8px 10px;
}

.zn-mini-beg {
  border-left: 4px solid var(--zn-secondary);
}

.zn-mini-adv {
  border-left: 4px solid var(--zn-primary);
}

.zn-mini-title {
  font-size: 11.5px;
  font-weight: 800;
  color: var(--zn-primary);
  margin-bottom: 3px;
}

.zn-mini-beg .zn-mini-title {
  color: var(--zn-secondary);
}

.zn-mini-text {
  font-size: 11.5px;
  line-height: 1.38;
  color: var(--zn-text);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.zn-slide-footer {
  padding: 8px 22px;
  background: #F8FAFC;
  border-top: 1px solid var(--zn-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 11.5px;
  color: var(--zn-muted);
}

.zn-slide-pagenum {
  font-weight: 800;
  color: var(--zn-primary);
}

/* --------------------------------------------------------------------------
   8 Morihideaki Zero-Noise Layouts (Left Main Zone)
   -------------------------------------------------------------------------- */

/* ① One-to-One Bar Chart */
.zn-layout-one-to-one {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.zn-bar-card {
  border: 1px solid var(--zn-border);
  border-radius: 7px;
  padding: 10px 14px;
  background: #FFFFFF;
}

.zn-bar-card.zn-highlight {
  background: var(--zn-card-bg);
  border-color: var(--zn-secondary);
  border-width: 1.5px;
}

.zn-bar-top {
  display: grid;
  grid-template-columns: 36% 64%;
  align-items: center;
  gap: 10px;
  margin-bottom: 6px;
}

.zn-bar-label {
  font-size: 13.5px;
  font-weight: 800;
  color: var(--zn-primary);
}

.zn-bar-track {
  background: #E2E8F0;
  height: 24px;
  border-radius: 5px;
  overflow: hidden;
}

.zn-bar-fill {
  height: 100%;
  background: var(--zn-primary);
  display: flex;
  align-items: center;
  padding-left: 10px;
  border-radius: 5px;
}

.zn-bar-card.zn-highlight .zn-bar-fill {
  background: var(--zn-secondary);
}

.zn-bar-val {
  color: #FFFFFF;
  font-size: 11.5px;
  font-weight: 800;
  white-space: nowrap;
}

.zn-bar-desc {
  font-size: 12.5px;
  line-height: 1.42;
  color: var(--zn-text);
}

/* ② Parallel 2x2 Grid */
.zn-layout-parallel {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

@media (max-width: 640px) {
  .zn-layout-parallel {
    grid-template-columns: 1fr;
  }
}

.zn-pcard {
  border: 1px solid var(--zn-border);
  border-top: 4px solid var(--zn-primary);
  border-radius: 7px;
  padding: 12px 14px;
  background: #FFFFFF;
}

.zn-pcard.zn-highlight {
  background: var(--zn-card-bg);
  border-color: var(--zn-secondary);
  border-top: 4px solid var(--zn-secondary);
}

.zn-pcard-hdr {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.zn-pcard-tag {
  background: var(--zn-primary);
  color: #FFFFFF;
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 999px;
}

.zn-pcard.zn-highlight .zn-pcard-tag {
  background: var(--zn-secondary);
}

.zn-pcard-metric {
  font-size: 12px;
  font-weight: 800;
  color: var(--zn-secondary);
}

.zn-pcard-title {
  font-size: 14.5px;
  font-weight: 800;
  color: var(--zn-primary);
  margin-bottom: 6px;
}

.zn-pcard-desc {
  font-size: 12.5px;
  line-height: 1.45;
  color: var(--zn-text);
}

/* ③ Combined Pillars + Synthesis Banner */
.zn-layout-combined {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.zn-pillars-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

@media (max-width: 640px) {
  .zn-pillars-row {
    grid-template-columns: 1fr;
  }
}

.zn-pillar {
  border: 1px solid var(--zn-border);
  border-radius: 7px;
  overflow: hidden;
  background: #FFFFFF;
}

.zn-pillar.zn-highlight {
  background: var(--zn-card-bg);
  border-color: var(--zn-secondary);
  border-width: 1.5px;
}

.zn-pillar-hdr {
  background: var(--zn-primary);
  color: #FFFFFF;
  font-size: 13px;
  font-weight: 800;
  padding: 9px 10px;
  text-align: center;
}

.zn-pillar.zn-highlight .zn-pillar-hdr {
  background: var(--zn-secondary);
}

.zn-pillar-list {
  margin: 0 !important;
  padding: 10px 12px 10px 26px !important;
  font-size: 12.2px;
  line-height: 1.45;
}

.zn-pillar-list li {
  margin-bottom: 6px;
}

.zn-synthesis-banner {
  background: var(--zn-primary);
  color: #FFFFFF;
  padding: 11px 16px;
  border-radius: 7px;
  font-size: 13px;
  font-weight: 700;
  line-height: 1.42;
}

/* ④ Causal Chain */
.zn-layout-chain {
  display: flex;
  flex-direction: column;
  gap: 9px;
}

.zn-chain-step {
  display: grid;
  grid-template-columns: 125px 1fr;
  border: 1px solid var(--zn-border);
  border-radius: 7px;
  overflow: hidden;
  background: #FFFFFF;
}

.zn-chain-step.zn-highlight {
  background: var(--zn-card-bg);
  border-color: var(--zn-secondary);
  border-width: 1.5px;
}

.zn-chain-badge {
  background: var(--zn-primary);
  color: #FFFFFF;
  font-size: 12px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 6px;
}

.zn-chain-step.zn-highlight .zn-chain-badge {
  background: var(--zn-secondary);
}

.zn-chain-body {
  padding: 8px 14px;
}

.zn-chain-title {
  font-size: 13.8px;
  font-weight: 800;
  color: var(--zn-primary);
  margin-bottom: 3px;
}

.zn-chain-step.zn-highlight .zn-chain-title {
  color: var(--zn-secondary);
}

.zn-chain-desc {
  font-size: 12.2px;
  line-height: 1.4;
  color: var(--zn-text);
}

/* ⑤ McKinsey Flow Matrix */
.zn-flow-table, .zn-opp-table {
  width: 100%;
  border-collapse: collapse;
  margin: 0 !important;
  font-size: 12.2px;
}

.zn-flow-table th, .zn-flow-table td,
.zn-opp-table th, .zn-opp-table td {
  border: 1px solid var(--zn-border);
  padding: 8px 10px;
  vertical-align: middle;
  line-height: 1.4;
}

.zn-flow-corner {
  background: var(--zn-primary);
  color: #FFFFFF;
  width: 100px;
  text-align: center;
}

.zn-flow-stg {
  background: var(--zn-secondary);
  color: #FFFFFF;
  font-weight: 800;
  text-align: center;
}

.zn-flow-rowlbl {
  background: var(--zn-card-bg);
  color: var(--zn-primary);
  font-weight: 800;
  text-align: center;
}

/* ⑥ Opposition Table */
.zn-opp-dim-hdr {
  background: var(--zn-card-bg);
  color: var(--zn-primary);
  width: 105px;
  text-align: center;
}

.zn-opp-left-hdr {
  background: #64748B;
  color: #FFFFFF;
  text-align: center;
}

.zn-opp-vs-hdr, .zn-opp-vs {
  width: 36px;
  text-align: center;
  font-weight: 800;
  color: var(--zn-secondary);
  background: #F8FAFC;
}

.zn-opp-right-hdr {
  background: var(--zn-primary);
  color: #FFFFFF;
  text-align: center;
}

.zn-opp-dim {
  background: var(--zn-card-bg);
  color: var(--zn-primary);
  font-weight: 800;
  text-align: center;
}

.zn-opp-right {
  background: var(--zn-card-bg);
  font-weight: 600;
}

/* ⑦ Comparison 3-Column Overlap */
.zn-layout-comparison {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

@media (max-width: 640px) {
  .zn-layout-comparison {
    grid-template-columns: 1fr;
  }
}

.zn-comp-col {
  border: 1px solid var(--zn-border);
  border-radius: 7px;
  overflow: hidden;
  background: #FFFFFF;
}

.zn-comp-center {
  background: var(--zn-card-bg);
  border-color: var(--zn-secondary);
  border-width: 2px;
}

.zn-comp-hdr {
  background: var(--zn-primary);
  color: #FFFFFF;
  font-size: 12.8px;
  font-weight: 800;
  padding: 9px;
  text-align: center;
}

.zn-comp-center .zn-comp-hdr {
  background: var(--zn-secondary);
}

.zn-comp-list {
  margin: 0 !important;
  padding: 10px 12px 10px 26px !important;
  font-size: 12.2px;
  line-height: 1.45;
}

.zn-comp-list li {
  margin-bottom: 7px;
}

/* ⑧ 2x2 Matrix */
.zn-layout-matrix {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.zn-matrix-axis-y {
  font-size: 12px;
  font-weight: 800;
  color: var(--zn-primary);
}

.zn-matrix-axis-x {
  font-size: 12px;
  font-weight: 800;
  color: var(--zn-primary);
  text-align: right;
}

.zn-matrix-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

@media (max-width: 640px) {
  .zn-matrix-grid {
    grid-template-columns: 1fr;
  }
}

.zn-quad {
  border: 1px solid var(--zn-border);
  border-radius: 7px;
  overflow: hidden;
  background: #FFFFFF;
}

.zn-quad.zn-highlight {
  background: var(--zn-card-bg);
  border-color: var(--zn-secondary);
  border-width: 1.8px;
}

.zn-quad-pos {
  background: var(--zn-primary);
  color: #FFFFFF;
  font-size: 11.5px;
  font-weight: 800;
  padding: 5px 10px;
}

.zn-quad.zn-highlight .zn-quad-pos {
  background: var(--zn-secondary);
}

.zn-quad-title {
  font-size: 13.8px;
  font-weight: 800;
  color: var(--zn-primary);
  padding: 8px 12px 4px 12px;
}

.zn-quad-desc {
  font-size: 12px;
  line-height: 1.42;
  padding: 0 12px 10px 12px;
}

/* --------------------------------------------------------------------------
   Dual-Track Cards (Beginner vs Advanced) & Portal Hub Components
   -------------------------------------------------------------------------- */
.dual-track-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
  margin: 1.5rem 0;
}

@media (max-width: 840px) {
  .dual-track-grid {
    grid-template-columns: 1fr;
  }
}

.track-card {
  border-radius: 10px;
  padding: 20px 22px;
  border: 1px solid #CBD5E1;
  background: #FFFFFF;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}

.track-beginner {
  border-top: 5px solid #0077C8;
  background: linear-gradient(180deg, #F0F9FF 0%, #FFFFFF 140px);
}

.track-advanced {
  border-top: 5px solid #051C2C;
  background: linear-gradient(180deg, #F8FAFC 0%, #FFFFFF 140px);
}

.track-badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 800;
  margin-bottom: 10px;
}

.track-beginner .track-badge {
  background: #0077C8;
  color: #FFFFFF;
}

.track-advanced .track-badge {
  background: #051C2C;
  color: #FFFFFF;
}

/* Portal Search & Filter UI */
.portal-search-box {
  background: linear-gradient(135deg, #051C2C 0%, #0A2E46 100%);
  padding: 28px;
  border-radius: 14px;
  color: #FFFFFF;
  margin: 1.5rem 0 2rem 0;
  box-shadow: 0 12px 28px rgba(5, 28, 44, 0.18);
}

.portal-search-input {
  width: 100%;
  padding: 14px 18px;
  font-size: 16px;
  border-radius: 8px;
  border: 2px solid #00A3E0;
  background: #FFFFFF;
  color: #0F172A;
  font-weight: 600;
  margin-top: 10px;
}

.portal-tag-btn {
  background: rgba(255, 255, 255, 0.12);
  color: #E2E8F0;
  border: 1px solid rgba(255, 255, 255, 0.22);
  padding: 5px 12px;
  border-radius: 999px;
  font-size: 12.5px;
  cursor: pointer;
  transition: all 0.18s;
}

.portal-tag-btn:hover, .portal-tag-btn.active {
  background: #00A3E0;
  color: #051C2C;
  border-color: #00A3E0;
  font-weight: 700;
}

.domain-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(310px, 1fr));
  gap: 16px;
  margin: 1.2rem 0 2rem 0;
}

.domain-card {
  border: 1px solid #CBD5E1;
  border-radius: 10px;
  padding: 18px;
  background: #FFFFFF;
  transition: transform 0.18s, box-shadow 0.18s;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.domain-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 24px rgba(5, 28, 44, 0.1);
}

.domain-card.flagship {
  border: 2px solid #0077C8;
  background: linear-gradient(180deg, #F0F9FF 0%, #FFFFFF 120px);
}
"""
    with open(os.path.join(THEME_DIR, "style.css"), "w", encoding="utf-8") as f:
        f.write(css_content)
    print("[OK] Wrote docs/.vitepress/theme/index.js & style.css")


def write_lecture_pages(lecture_raw_map):
    """生成 docs/30-lectures/00.md ~ 39.md 共 40 個深度知識與無雜訊簡報頁面"""
    total = len(ALL_LECTURES)
    for idx, lec in enumerate(ALL_LECTURES):
        lid = lec["id"]
        slide_html = render_full_slide_card_html(lec, idx + 1, total)
        beg = lec.get("beginner", {})
        adv = lec.get("advanced", {})
        notes = lec.get("speaker_notes", {})
        course_img = with_base(lec.get("course_image", "/images/lectures/lec_00_1.jpg"))

        # 組合關鍵術語列表
        term_lines = []
        for t in beg.get("key_terms", []):
            if isinstance(t, dict):
                term_lines.append(f"- **{t.get('term', '')}**：{t.get('def', '')}")
            else:
                s = str(t)
                if "：" in s:
                    k, v = s.split("：", 1)
                    term_lines.append(f"- **{k}**：{v}")
                else:
                    term_lines.append(f"- **{s}**")
        terms_md = "\n".join(term_lines)
        # 組合進階檢核表
        chk_md = "\n".join([f"- [ ] {item}" for item in adv.get("checklist", [])])
        # 關鍵字徽章
        kw_badges = " ".join([f"`#{kw}`" for kw in lec.get("keywords", [])])

        raw_transcript = lecture_raw_map.get(lid, "（原課程文本載入中）")

        md_content = f"""---
title: "{lec['code']}｜{lec['title']}"
description: "{lec['conclusion_title']}"
---

# {lec['code']}｜{lec['title']}

> **所屬模組**：`{lec['module']}` ｜ **對應知識庫**：`{lec['kb_id']}` ｜ **無雜訊版型**：`{lec['layout_label']}`  
> **檢索關鍵字**：{kw_badges}

<div style="display:flex; flex-wrap:wrap; gap:10px; margin: 14px 0;">
  <a href="{with_base('/slides/')}?lec={lid}" style="background:#051C2C; color:#fff; padding:7px 14px; border-radius:6px; text-decoration:none; font-size:13px; font-weight:700;">🎯 在全螢幕簡報劇場開啟本頁</a>
  <a href="{with_base('/downloads/劉松博_公司治理30講_全40講無雜訊顧問簡報庫.pptx')}" download style="background:#0077C8; color:#fff; padding:7px 14px; border-radius:6px; text-decoration:none; font-size:13px; font-weight:700;">📥 下載全 40 講無雜訊 PPTX</a>
  <a href="{with_base('/downloads/劉松博_公司治理30講_無雜訊顧問簡報_精華16頁.pptx')}" download style="background:#F1F5F9; color:#051C2C; border:1px solid #CBD5E1; padding:7px 14px; border-radius:6px; text-decoration:none; font-size:13px; font-weight:700;">📊 下載精華 16 頁執行長簡報 PPTX</a>
</div>

---

## 📊 無雜訊顧問簡報（Zero-Noise Consulting Slide）

{slide_html}

---

## 🌱 入門者導讀 ＆ 🏛️ 進階者思考架構（Dual-Track Cognitive Guide）

<div class="dual-track-grid">
  <div class="track-card track-beginner">
    <span class="track-badge">🌱 入門者導讀（Plain-Language & Story）</span>
    <h3 style="margin-top:4px; color:#051C2C;">一分鐘白話秒懂本講核心</h3>
    <p style="font-size:14.5px; line-height:1.65;">{beg.get('summary', '')}</p>
    <h4 style="color:#0077C8; margin-top:14px;">📖 經典商業案例故事</h4>
    <p style="font-size:14px; line-height:1.65; background:#FFFFFF; padding:12px; border-radius:8px; border:1px solid #BAE6FD;">{beg.get('case_story', '')}</p>
  </div>

  <div class="track-card track-advanced">
    <span class="track-badge">🏛️ 進階者思考架構（CEO Mental Model）</span>
    <h3 style="margin-top:4px; color:#051C2C;">{adv.get('model_name', '')}</h3>
    <p style="font-size:14.5px; line-height:1.65;">{adv.get('model_desc', '')}</p>
    <h4 style="color:#051C2C; margin-top:14px;">🔗 跨講次因果鏈（承上啟下）</h4>
    <p style="font-size:14px; line-height:1.65; background:#FFFFFF; padding:12px; border-radius:8px; border:1px solid #CBD5E1;">{adv.get('causal_link', '')}</p>
  </div>
</div>

### 🔑 入門必備關鍵術語解析（Key Terms）
{terms_md}

### ✅ 進階執行長／董事會決策檢核表（Executive Checklist）
{chk_md}

---

## 🎙️ 顧問三段式講稿備忘錄（Speaker Notes）

::: info 💡 【結論】（切入頁首 Action Title）
{notes.get('conclusion', '')}
:::

::: tip 📊 【說明】（拆解圖表數據與商業實證）
{notes.get('explanation', '')}
:::

::: warning 🔗 【鋪墊】（跨講次邏輯轉場與下一步行動）
{notes.get('transition', '')}
:::

---

## 🖼️ 課程原版視覺圖表／核心金句卡

<div style="background:#F8FAFC; border:1px solid #CBD5E1; border-radius:10px; padding:16px; margin:16px 0; text-align:center;">
  <img src="{course_img}" alt="{lec.get('course_image_caption', '')}" style="max-height:420px; margin:0 auto; border-radius:6px; box-shadow:0 4px 12px rgba(0,0,0,0.08);" />
  <p style="margin:10px 0 0 0; font-size:13px; color:#475569; font-weight:600;">▲ {lec.get('course_image_caption', '')}</p>
</div>

---

## 📜 原課程完整知識文本（繁體中文精校版）

<details style="background:#F8FAFC; border:1px solid #CBD5E1; border-radius:8px; padding:14px 18px; margin-top:16px;">
<summary style="cursor:pointer; font-weight:800; color:#051C2C; font-size:15px;">📖 點擊展開／收合《{lec['code']} {lec['title']}》完整原版課程文稿（含課後問答與圖表）</summary>

<div style="margin-top:16px; border-top:1px solid #E2E8F0; padding-top:16px;">

{raw_transcript}

</div>
</details>
"""
        out_file = os.path.join(LECTURES_OUT_DIR, f"{lid}.md")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(md_content)

    print(f"[OK] Generated all {total} lecture pages in docs/30-lectures/")


def write_slides_theatre_page():
    """生成 docs/slides/index.md：互動式 16:9 無雜訊簡報劇場（支援 16頁精華 / 42頁完整切換、鍵盤控制、關鍵字篩選）"""
    # 將每講預先渲染好的 HTML 與中繼資料打包為 JSON 供 Vue 互動切換
    slides_payload = []

    # 加入封面與全書架構作為完整簡報的前兩張
    cover_html = f"""
    <div class="zn-slide-frame" style="background:linear-gradient(135deg, #051C2C 0%, #0A2E46 100%); color:#FFFFFF; min-height:510px;">
      <div class="zn-slide-top-bar"></div>
      <div style="display:grid; grid-template-columns:58% 42%; gap:24px; padding:32px; align-items:center; flex:1;">
        <div>
          <span style="background:#0077C8; color:#fff; padding:4px 12px; border-radius:999px; font-size:12px; font-weight:800;">EXECUTIVE BRIEFING & ENCYCLOPEDIA｜無雜訊顧問簡報</span>
          <h2 style="color:#FFFFFF !important; font-size:30px !important; line-height:1.25 !important; margin:16px 0 12px 0 !important; border:none !important;">劉松博《公司治理 30 講》<br/>執行長決策與思考架構簡報庫</h2>
          <p style="color:#CBD5E1 !important; font-size:14.5px !important; line-height:1.6 !important;">遵循前 BCG 顧問森秀明「8 大無雜訊簡報版型」與 McKinsey / BCG / Accenture 視覺規範，將 40 講課程與 41 節知識庫濃縮為「結論先行、每頁雙圖輔助、入門至進階雙軌並重」的執行長互動簡報。</p>
          <div style="background:rgba(255,255,255,0.08); border-left:4px solid #00A3E0; padding:12px 16px; border-radius:6px; margin-top:18px; font-size:13px; line-height:1.55; color:#F1F5F9;">
            <div>🌱 <b>入門者視角</b>：一分鐘白話概念拆解 ＋ 萬科、安隆、國美、巴林銀行等 40 個真實商業故事</div>
            <div style="margin-top:4px;">🏛️ <b>進階者視角</b>：CEO 頂層思考模型 ＋ 跨講次因果邏輯鏈 (#041) ＋ 董事會實務檢核表</div>
          </div>
        </div>
        <div style="display:flex; flex-direction:column; gap:12px;">
          <img src="{with_base('/images/unsplash/topic_cover.jpg')}" alt="Cover" style="width:100%; height:220px; object-fit:cover; border-radius:8px; border:2px solid rgba(255,255,255,0.2);" />
          <img src="{with_base('/images/lectures/lec_00_1.jpg')}" alt="Architecture" style="width:100%; height:170px; object-fit:cover; border-radius:8px; border:2px solid rgba(255,255,255,0.2);" />
          <div style="font-size:11.5px; color:#94A3B8; text-align:center;">▲ 企業董事會治理決策場景 ＆ 原版《公司治理30講》全書知識地圖</div>
        </div>
      </div>
    </div>
    """
    slides_payload.append({
        "id": "cover",
        "code": "COVER",
        "title": "封面：劉松博《公司治理30講》無雜訊執行長簡報",
        "module": "總覽與架構",
        "module_id": "all",
        "layout_label": "封面 (Cover)",
        "in_exec16": True,
        "keywords": ["公司治理", "無雜訊簡報", "執行長知識庫"],
        "html": cover_html,
        "beginner_summary": "歡迎進入《公司治理30講》無雜訊顧問簡報劇場！您可以使用鍵盤「⬅️ ➡️ 方向鍵」翻頁，或切換「精華 16 頁決策版」與「全 42 頁完整百科版」。",
        "case_story": "本簡報庫涵蓋巴林銀行、萬科控制權大戰、安隆破產、阿里巴巴合夥人、福耀玻璃傳承等 40 個經典治理實案。",
        "model_name": "執行長公司治理雙軌認知系統",
        "model_desc": "結合「結論先行 Action Title」、「森秀明 8 大視覺版型」與「入門白話 × 進階心智模型」，讓知識即刻轉化為治理決策。",
        "causal_link": "從第一頁全書地圖出發，串聯基礎演進、股權設計、兩會運作與經理人激勵四大模組。",
        "checklist": ["選擇上方「精華 16 頁」快速掌握核心，或選擇「全 42 頁」逐講精讀", "點擊下方講稿與雙軌面板，對照檢視自身企業的股權與董事會制度"],
        "notes_conclusion": "這套簡報將劉松博教授 40 講公司治理課程萃取為零雜訊顧問圖解。",
        "notes_explanation": "每一頁都嚴格遵循「一頁一結論」、「左側邏輯版型圖解」、「右側情境照片與雙軌快照」。",
        "notes_transition": "請按下一頁檢視全書四大模組的跨講次因果架構圖 (#041)。",
        "doc_link": with_base("/architecture/")
    })

    for idx, lec in enumerate(ALL_LECTURES):
        slides_payload.append({
            "id": lec["id"],
            "code": lec["code"],
            "title": f"{lec['code']}｜{lec['title']}",
            "short_title": lec["short_title"],
            "conclusion_title": lec["conclusion_title"],
            "module": lec["module"],
            "module_id": lec["module_id"],
            "layout_label": lec["layout_label"],
            "in_exec16": lec["id"] in EXEC_16_IDS,
            "keywords": lec.get("keywords", []),
            "html": render_full_slide_card_html(lec, idx + 1, len(ALL_LECTURES)),
            "beginner_summary": lec.get("beginner", {}).get("summary", ""),
            "case_story": lec.get("beginner", {}).get("case_story", ""),
            "model_name": lec.get("advanced", {}).get("model_name", ""),
            "model_desc": lec.get("advanced", {}).get("model_desc", ""),
            "causal_link": lec.get("advanced", {}).get("causal_link", ""),
            "checklist": lec.get("advanced", {}).get("checklist", []),
            "notes_conclusion": lec.get("speaker_notes", {}).get("conclusion", ""),
            "notes_explanation": lec.get("speaker_notes", {}).get("explanation", ""),
            "notes_transition": lec.get("speaker_notes", {}).get("transition", ""),
            "course_image": with_base(lec.get("course_image", "")),
            "course_image_caption": lec.get("course_image_caption", ""),
            "doc_link": with_base(f"/30-lectures/{lec['id']}")
        })

    slides_json = json.dumps(slides_payload, ensure_ascii=False)

    theatre_md = f"""---
layout: doc
aside: false
title: "16:9 無雜訊顧問簡報互動劇場"
---

<script setup>
import {{ ref, computed, onMounted, onUnmounted }} from 'vue'

const allSlides = {slides_json}

const deckMode = ref('all') // 'exec16' or 'all'
const moduleFilter = ref('all')
const searchQuery = ref('')
const currentIndex = ref(0)
const activeTab = ref('dual') // 'dual' | 'notes' | 'diagram'

const filteredSlides = computed(() => {{
  return allSlides.filter(s => {{
    if (deckMode.value === 'exec16' && !s.in_exec16) return false
    if (moduleFilter.value !== 'all' && s.module_id !== moduleFilter.value) return false
    if (searchQuery.value.trim() !== '') {{
      const q = searchQuery.value.trim().toLowerCase()
      const hay = [
        s.title, s.conclusion_title || '', s.layout_label,
        s.beginner_summary, s.case_story, s.model_name, s.model_desc,
        ...(s.keywords || [])
      ].join(' ').toLowerCase()
      return hay.includes(q)
    }}
    return true
  }})
}})

const currentSlide = computed(() => {{
  if (filteredSlides.value.length === 0) return null
  const idx = Math.min(Math.max(currentIndex.value, 0), filteredSlides.value.length - 1)
  return filteredSlides.value[idx]
}})

function setDeckMode(mode) {{
  deckMode.value = mode
  currentIndex.value = 0
}}

function setModule(m) {{
  moduleFilter.value = m
  currentIndex.value = 0
}}

function prevSlide() {{
  if (currentIndex.value > 0) currentIndex.value--
}}

function nextSlide() {{
  if (currentIndex.value < filteredSlides.value.length - 1) currentIndex.value++
}}

function handleKeydown(e) {{
  if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT')) return
  if (e.key === 'ArrowRight') nextSlide()
  if (e.key === 'ArrowLeft') prevSlide()
}}

onMounted(() => {{
  window.addEventListener('keydown', handleKeydown)
  const params = new URLSearchParams(window.location.search)
  const lecParam = params.get('lec')
  if (lecParam) {{
    deckMode.value = 'all'
    const foundIdx = allSlides.findIndex(s => s.id === lecParam)
    if (foundIdx >= 0) currentIndex.value = foundIdx
  }}
}})

onUnmounted(() => {{
  window.removeEventListener('keydown', handleKeydown)
}})
</script>

# 🎯 無雜訊顧問簡報互動劇場（16:9 Web Slide Player）

> **操作提示**：支援鍵盤 **`⬅️ 左方向鍵`** ／ **`➡️ 右方向鍵`** 快速翻頁。可隨時切換 **「精華 16 頁執行長決策版」** 與 **「全 41 頁完整百科版」**，或直接下載 `.pptx` 檔案於 PowerPoint 簡報使用。

<div style="background:#051C2C; color:#FFFFFF; padding:18px 22px; border-radius:12px; margin:16px 0;">
  <div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:12px;">
    <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center;">
      <button @click="setDeckMode('exec16')" :style="{{ background: deckMode==='exec16' ? '#00A3E0' : 'rgba(255,255,255,0.12)', color: deckMode==='exec16' ? '#051C2C' : '#fff', fontWeight: '800', padding: '7px 14px', borderRadius: '8px', border: 'none', cursor: 'pointer' }}">
        ⭐ 精華 16 頁決策簡報 ({{ allSlides.filter(s=>s.in_exec16).length }} 頁)
      </button>
      <button @click="setDeckMode('all')" :style="{{ background: deckMode==='all' ? '#00A3E0' : 'rgba(255,255,255,0.12)', color: deckMode==='all' ? '#051C2C' : '#fff', fontWeight: '800', padding: '7px 14px', borderRadius: '8px', border: 'none', cursor: 'pointer' }}">
        📚 全 40 講完整簡報百科 ({{ allSlides.length }} 頁)
      </button>
    </div>

    <div style="display:flex; flex-wrap:wrap; gap:8px;">
      <a href="{with_base('/downloads/劉松博_公司治理30講_無雜訊顧問簡報_精華16頁.pptx')}" download style="background:#0077C8; color:#fff; padding:7px 14px; border-radius:8px; text-decoration:none; font-size:13px; font-weight:700;">📥 下載精華 16 頁 .pptx</a>
      <a href="{with_base('/downloads/劉松博_公司治理30講_全40講無雜訊顧問簡報庫.pptx')}" download style="background:#177B57; color:#fff; padding:7px 14px; border-radius:8px; text-decoration:none; font-size:13px; font-weight:700;">📥 下載完整 42 頁 .pptx</a>
    </div>
  </div>

  <!-- 模組篩選與關鍵字即時檢索 -->
  <div style="display:grid; grid-template-columns: 1fr 280px; gap:12px; margin-top:14px; align-items:center;">
    <div style="display:flex; flex-wrap:wrap; gap:6px;">
      <button @click="setModule('all')" :class="['portal-tag-btn', moduleFilter==='all' ? 'active' : '']">全部模組</button>
      <button @click="setModule('m1')" :class="['portal-tag-btn', moduleFilter==='m1' ? 'active' : '']">模組一：基礎與演進 (00-05)</button>
      <button @click="setModule('m2')" :class="['portal-tag-btn', moduleFilter==='m2' ? 'active' : '']">模組二：股權與股東 (06-14)</button>
      <button @click="setModule('m3')" :class="['portal-tag-btn', moduleFilter==='m3' ? 'active' : '']">模組三：董事與監事 (15-22)</button>
      <button @click="setModule('m4')" :class="['portal-tag-btn', moduleFilter==='m4' ? 'active' : '']">模組四：經理人與控制權 (23-39)</button>
    </div>
    <div>
      <input v-model="searchQuery" @input="currentIndex=0" type="text" placeholder="🔍 篩選簡報關鍵字 (如：萬科、AB股、獨董)..." style="width:100%; padding:7px 12px; border-radius:6px; border:1px solid #00A3E0; background:#fff; color:#0F172A; font-size:13px;" />
    </div>
  </div>

  <!-- 頁碼導覽列 -->
  <div v-if="filteredSlides.length > 0" style="display:flex; justify-content:space-between; align-items:center; margin-top:14px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.15);">
    <button @click="prevSlide" :disabled="currentIndex <= 0" style="background:rgba(255,255,255,0.15); color:#fff; padding:6px 16px; border-radius:6px; border:none; cursor:pointer; font-weight:700;">⬅️ 上一頁</button>
    
    <div style="display:flex; align-items:center; gap:10px;">
      <span style="font-size:13px; color:#CBD5E1;">快速跳頁：</span>
      <select v-model="currentIndex" style="padding:6px 12px; border-radius:6px; background:#0F172A; color:#fff; border:1px solid #00A3E0; font-size:13px; max-width:420px;">
        <option v-for="(s, idx) in filteredSlides" :key="s.id" :value="idx">
          第 {{ idx + 1 }} 頁｜{{ s.title }} ({{ s.layout_label }})
        </option>
      </select>
      <span style="font-weight:800; color:#00A3E0; font-size:14px;">{{ currentIndex + 1 }} / {{ filteredSlides.length }}</span>
    </div>

    <button @click="nextSlide" :disabled="currentIndex >= filteredSlides.length - 1" style="background:#0077C8; color:#fff; padding:6px 16px; border-radius:6px; border:none; cursor:pointer; font-weight:700;">下一頁 ➡️</button>
  </div>
</div>

<!-- 簡報主畫面 -->
<div v-if="currentSlide">
  <div v-html="currentSlide.html"></div>

  <!-- 簡報下方：入門/進階雙軌解析 ＆ 三段式顧問講稿切換面板 -->
  <div style="background:#FFFFFF; border:1px solid #CBD5E1; border-radius:10px; padding:20px; margin-top:16px; box-shadow:0 4px 12px rgba(0,0,0,0.04);">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; border-bottom:1px solid #E2E8F0; padding-bottom:12px; margin-bottom:16px;">
      <div style="display:flex; gap:8px;">
        <button @click="activeTab='dual'" :style="{{ background: activeTab==='dual' ? '#051C2C' : '#F1F5F9', color: activeTab==='dual' ? '#fff' : '#051C2C', padding: '6px 14px', borderRadius: '6px', border: 'none', fontWeight: '700', cursor: 'pointer' }}">
          🌱 入門導讀 × 🏛️ 進階思考架構
        </button>
        <button @click="activeTab='notes'" :style="{{ background: activeTab==='notes' ? '#051C2C' : '#F1F5F9', color: activeTab==='notes' ? '#fff' : '#051C2C', padding: '6px 14px', borderRadius: '6px', border: 'none', fontWeight: '700', cursor: 'pointer' }}">
          🎙️ 顧問三段式講稿備忘錄
        </button>
        <button v-if="currentSlide.course_image" @click="activeTab='diagram'" :style="{{ background: activeTab==='diagram' ? '#051C2C' : '#F1F5F9', color: activeTab==='diagram' ? '#fff' : '#051C2C', padding: '6px 14px', borderRadius: '6px', border: 'none', fontWeight: '700', cursor: 'pointer' }}">
          🖼️ 原版課程圖表／金句卡
        </button>
      </div>
      <a :href="currentSlide.doc_link" style="color:#0077C8; font-weight:800; text-decoration:none; font-size:14px;">📖 前往本講完整深度知識頁 ➔</a>
    </div>

    <div v-if="activeTab==='dual'" class="dual-track-grid" style="margin:0;">
      <div class="track-card track-beginner">
        <span class="track-badge">🌱 入門者導讀（Plain-Language & Case）</span>
        <p style="font-size:14px; line-height:1.6; margin:8px 0;">{{ currentSlide.beginner_summary }}</p>
        <div style="background:#fff; padding:10px 12px; border-radius:6px; border:1px solid #BAE6FD; font-size:13.5px; line-height:1.55;">
          <b>📖 商業案例故事：</b>{{ currentSlide.case_story }}
        </div>
      </div>
      <div class="track-card track-advanced">
        <span class="track-badge">🏛️ 進階者思考架構：{{ currentSlide.model_name }}</span>
        <p style="font-size:14px; line-height:1.6; margin:8px 0;">{{ currentSlide.model_desc }}</p>
        <div style="background:#fff; padding:10px 12px; border-radius:6px; border:1px solid #CBD5E1; font-size:13.5px; line-height:1.55;">
          <b>🔗 跨講因果鏈：</b>{{ currentSlide.causal_link }}
        </div>
      </div>
    </div>

    <div v-if="activeTab==='notes'" style="display:flex; flex-direction:column; gap:10px; font-size:14px; line-height:1.6;">
      <div style="background:#F0F9FF; border-left:4px solid #0077C8; padding:10px 14px; border-radius:6px;">
        <b>💡 【結論】：</b>{{ currentSlide.notes_conclusion }}
      </div>
      <div style="background:#F8FAFC; border-left:4px solid #051C2C; padding:10px 14px; border-radius:6px;">
        <b>📊 【說明】：</b>{{ currentSlide.notes_explanation }}
      </div>
      <div style="background:#FEFCE8; border-left:4px solid #EAB308; padding:10px 14px; border-radius:6px;">
        <b>🔗 【鋪墊】：</b>{{ currentSlide.notes_transition }}
      </div>
    </div>

    <div v-if="activeTab==='diagram' && currentSlide.course_image" style="text-align:center;">
      <img :src="currentSlide.course_image" style="max-height:380px; margin:0 auto; border-radius:8px;" />
      <p style="margin-top:8px; font-size:13px; color:#475569;">▲ {{ currentSlide.course_image_caption }}</p>
    </div>
  </div>
</div>

<div v-else style="padding:40px; text-align:center; background:#F8FAFC; border-radius:10px; border:1px solid #CBD5E1;">
  <h3>找不到符合篩選條件的簡報頁</h3>
  <button @click="searchQuery=''; moduleFilter='all'" style="background:#0077C8; color:#fff; padding:8px 16px; border-radius:6px; border:none; cursor:pointer;">清除篩選條件</button>
</div>
"""
    with open(os.path.join(SLIDES_OUT_DIR, "index.md"), "w", encoding="utf-8") as f:
        f.write(theatre_md)
    print("[OK] Wrote docs/slides/index.md (Interactive 16:9 Slide Player)")


def write_architecture_page():
    """生成 docs/architecture/index.md：對應 #041 跨講次因果邏輯與全書系統架構"""
    arch_md = f"""---
title: "跨講次因果邏輯與全書系統架構 (#041)"
description: "劉松博《公司治理30講》全書四大模組、五條核心因果鏈與執行長診斷體系"
---

# 🧭 跨講次因果邏輯與全書系統架構（對應知識庫 `#041`）

> **全書核心命題**：公司治理不是零散的法條，而是解決 **「所有權與經營權分離後，權力如何分配、如何制衡、如何激勵」** 的系統工程。

<div style="background:#F8FAFC; border:1px solid #CBD5E1; border-radius:10px; padding:18px; margin:18px 0; text-align:center;">
  <img src="{with_base('/images/lectures/lec_00_1.jpg')}" alt="劉松博公司治理30講原版架構圖" style="max-height:440px; margin:0 auto; border-radius:8px; box-shadow:0 6px 18px rgba(0,0,0,0.08);" />
  <p style="margin:10px 0 0 0; font-size:13.5px; color:#334155; font-weight:700;">▲ 劉松博《公司治理30講》原版全書知識結構圖：以利益相關者為外環，股東會、董事會、監事會、高層經理人為核心內環</p>
</div>

---

## 🔗 全書五條核心跨講次因果鏈（Executive Causal Chains）

### 因果鏈一：制度起源鏈（為何需要公司治理？）
- **[01 公司起源](/30-lectures/01)**（有限責任與獨立人格創造集資奇蹟） ➔ **[02 兩權分離](/30-lectures/02)**（東印度公司開啟所有權與經營權分離，埋下代理人衝突） ➔ **[03 公司治理定義](/30-lectures/03)**（巴林銀行因失去制衡而倒閉，確立「責權利對等」原則） ➔ **[04 利益相關者](/30-lectures/04)**（決定治理服務對象：股東至上 vs 社會責任邊界） ➔ **[05 治理主體](/30-lectures/05)**（區分個人、機構與政府三類股東的不同動機）。

### 因果鏈二：股權與控制權槓桿鏈（如何用少數資金掌控全局？）
- **[06 股權高度集中](/30-lectures/06)**（一股獨大雖決策快，但易掏空小股東） ➔ **[07 股權過度分散](/30-lectures/07)**（50:50 真功夫僵局比一股獨大更致命；海底撈張勇以 68:32 破局） ➔ **[08 股東協議](/30-lectures/08)**（以一致行動人與委託投票權簽署股權「婚前協議」） ➔ **[09 金字塔股權](/30-lectures/09)** ＆ **[10 AB股雙層架構](/30-lectures/10)** ＆ **[11 合夥人制度](/30-lectures/11)**（三大「同股不同權」控制權放大器） ➔ **[12 控制權與現金流權分離](/30-lectures/12)**（揭露兩權分離度越大、大股東掏空動機越強的財務本質）。

### 因果鏈三：股東會與董事會制衡鏈（如何把大股東與董事關進制度籠子？）
- **[15 股東會決議有效](/30-lectures/15)**（程序正義高於大股東個人意志） ➔ **[16 董事會定位](/30-lectures/16)**（萬科王石案例：董事會採「一人一票」，非大股東橡皮圖章） ➔ **[17 董事會規模與結構](/30-lectures/17)**（7~11 人單數黃金規模＋四大專門委員會） ➔ **[18 獨立董事](/30-lectures/18)** ＆ **[20 累積投票制](/30-lectures/20)**（保障中小股東將代言人送進董事會的數學武器） ➔ **[21 監事會](/30-lectures/21)** ＆ **[22 治理模式演進](/30-lectures/22)**（單層制、雙層制與混合制的全球收斂）。

### 因果鏈四：委託代理與經理人激勵鏈（如何讓 CEO 像老闆一樣拼命？）
- **[23 選拔優秀經理人](/30-lectures/23)**（人品與契約精神優先於單純業績） ➔ **[24 委託代理問題](/30-lectures/24)**（拆解代理人偷懶、短期行為與帝國建造三大代理成本） ➔ **[25 經營者激勵體系](/30-lectures/25)** ＆ **[26 股權激勵實操](/30-lectures/26)**（打造「基本薪資＋年度獎金＋長期限制性股票/期權」金手銬） ➔ **[27 經理人更換](/30-lectures/27)**（建立制度化接班梯隊）。

### 因果鏈五：外部控制權市場與家族傳承鏈（如何抵禦野蠻人並實現基業長青？）
- **[28 資本市場與控制權市場](/30-lectures/28)**（外部接管是懸在平庸管理層頭上的達摩克利斯之劍） ➔ **[29 控制權爭奪與反收購](/30-lectures/29)**（萬科寶能之爭、國美陳曉與黃光裕之爭：毒丸計畫、白衣騎士與交錯董事會） ➔ **[30~31 家族企業治理與傳承](/30-lectures/30)**（福耀玻璃曹德旺接班：跨越企業、家族、產權三環重疊區） ➔ **[35~37 創投對賭與有限合夥](/30-lectures/35)**（GP/LP 架構與對賭協議底線）。

---

## 📊 全 40 講無雜訊版型與雙軌模型總索引表

| 講次 | 主題名稱 | 無雜訊簡報版型 | 🌱 入門核心案例 | 🏛️ 進階思考模型 |
| :--- | :--- | :--- | :--- | :--- |
"""
    rows_md = []
    for lec in ALL_LECTURES:
        link = f"/30-lectures/{lec['id']}"
        rows_md.append(
            f"| **[{lec['code']}]({link})** | [{lec['short_title']}]({link}) | `{lec['layout_label']}` | {lec['beginner']['case_story'][:28]}… | **{lec['advanced']['model_name']}** |"
        )
    arch_md += "\n".join(rows_md) + "\n"

    with open(os.path.join(ARCH_OUT_DIR, "index.md"), "w", encoding="utf-8") as f:
        f.write(arch_md)
    print("[OK] Wrote docs/architecture/index.md")


def write_domains_page():
    """生成 docs/domains/index.md：A2.5 企業管理八大領域擴充架構館"""
    domains_md = f"""---
title: "A2.5 企業管理｜八大專業領域擴充架構館"
description: "執行長專業知識庫的模組化擴充底座，串聯公司治理、策略管理、營運、行銷、人資、研發、專案與綜合研討"
---

# 🗂️ A2.5 企業管理｜八大專業領域知識庫與簡報擴充館

> **設計理念（Requirement 1 & 2）**：本入口網站採用 **「頂層執行長知識中樞 ＋ 模組化課程簡報倉」** 架構。除了目前已全量上線的旗艦模組 **`A2.5.0 公司治理（劉松博・公司治理30講）`** 外，已完整盤點並預留 `A2.5.1` 至 `A2.5.7` 各資料夾既有教材之擴充接口，未來新增任何一門課程皆可一鍵掛載無雜訊簡報與雙軌知識庫。

<div class="domain-grid">
  <div class="domain-card flagship">
    <div>
      <span style="background:#0077C8; color:#fff; padding:3px 10px; border-radius:999px; font-size:11.5px; font-weight:800;">🟢 已全量上線 FLAGSHIP</span>
      <h3 style="margin:10px 0 6px 0; color:#051C2C;">A2.5.0 公司治理（Corporate Governance）</h3>
      <p style="font-size:13.5px; color:#334155; line-height:1.55;">
        <b>核心教材</b>：《劉松博・公司治理30講》（全 40 講知識庫 ＋ 41 節萃取 ＋ 16/42 頁無雜訊簡報）<br/>
        <b>核心議題</b>：股權設計、67/51/34% 控制線、AB股、合夥人、董事會運作、獨立董事、CEO 股權激勵、反收購與家族傳承。
      </p>
    </div>
    <div style="display:flex; gap:8px; margin-top:12px;">
      <a href="{with_base('/slides/')}" style="background:#051C2C; color:#fff; padding:6px 12px; border-radius:6px; font-size:12.5px; font-weight:700; text-decoration:none;">🎯 開啟簡報劇場</a>
      <a href="{with_base('/30-lectures/00')}" style="background:#0077C8; color:#fff; padding:6px 12px; border-radius:6px; font-size:12.5px; font-weight:700; text-decoration:none;">📚 進入 40 講百科</a>
    </div>
  </div>

  <div class="domain-card">
    <div>
      <span style="background:#0F766E; color:#fff; padding:3px 10px; border-radius:999px; font-size:11.5px; font-weight:800;">📘 既有知識庫已盤點（擴充預備）</span>
      <h3 style="margin:10px 0 6px 0; color:#051C2C;">A2.5.1 策略管理（Strategic Management）</h3>
      <p style="font-size:13.5px; color:#334155; line-height:1.55;">
        <b>已盤點資料夾教材</b>：<br/>
        1. 《孫子兵法》華杉講透十三篇 ＆ 宮玉振《孫子兵法十二講》<br/>
        2. 《藍海策略（Blue Ocean Strategy）》價值創新框架<br/>
        3. 《生態系競爭策略（Winning the Right Game）》<br/>
        4. 《競合策略（Co-opetition）》商業賽局理論
      </p>
    </div>
    <div style="margin-top:12px; font-size:12px; color:#0F766E; font-weight:700;">⚡ 支援套用 /zero-noise-pptx 轉化為策略顧問簡報</div>
  </div>

  <div class="domain-card">
    <div>
      <span style="background:#64748B; color:#fff; padding:3px 10px; border-radius:999px; font-size:11.5px; font-weight:800;">🏗️ 架構預留 SLOT READY</span>
      <h3 style="margin:10px 0 6px 0; color:#051C2C;">A2.5.2 營運管理（Operations Management）</h3>
      <p style="font-size:13.5px; color:#334155; line-height:1.55;">
        <b>規劃擴充主題</b>：精實管理（Lean Operations）、供應鏈韌性、TOC 限制理論、跨部門流程最佳化與數位營運儀表板（OKR/KPI 閉環）。
      </p>
    </div>
    <div style="margin-top:12px; font-size:12px; color:#64748B; font-weight:700;">📂 對應目錄：A2.5.2 營運管理</div>
  </div>

  <div class="domain-card">
    <div>
      <span style="background:#64748B; color:#fff; padding:3px 10px; border-radius:999px; font-size:11.5px; font-weight:800;">🏗️ 架構預留 SLOT READY</span>
      <h3 style="margin:10px 0 6px 0; color:#051C2C;">A2.5.3 行銷管理（Marketing Management）</h3>
      <p style="font-size:13.5px; color:#334155; line-height:1.55;">
        <b>規劃擴充主題</b>：策略品牌定位（Positioning）、B2B 大客戶價值行銷、定價心理學與漏斗轉換率診斷模型。
      </p>
    </div>
    <div style="margin-top:12px; font-size:12px; color:#64748B; font-weight:700;">📂 對應目錄：A2.5.3 行銷管理</div>
  </div>

  <div class="domain-card">
    <div>
      <span style="background:#0F766E; color:#fff; padding:3px 10px; border-radius:999px; font-size:11.5px; font-weight:800;">📘 既有知識庫已盤點（擴充預備）</span>
      <h3 style="margin:10px 0 6px 0; color:#051C2C;">A2.5.4 人資與組織（HR & Organization）</h3>
      <p style="font-size:13.5px; color:#334155; line-height:1.55;">
        <b>已盤點資料夾教材</b>：<br/>
        1. 《團隊協作的五大障礙（The Five Dysfunctions of a Team）》知識庫（缺乏信任、懼怕衝突、欠缺投入、逃避責任、忽視結果）<br/>
        <b>與公司治理連動</b>：銜接第 23~27 講高階經理人選拔、接班梯隊與股權激勵。
      </p>
    </div>
    <div style="margin-top:12px; font-size:12px; color:#0F766E; font-weight:700;">⚡ 支援套用 /zero-noise-pptx 轉化為組織診斷簡報</div>
  </div>

  <div class="domain-card">
    <div>
      <span style="background:#64748B; color:#fff; padding:3px 10px; border-radius:999px; font-size:11.5px; font-weight:800;">🏗️ 架構預留 SLOT READY</span>
      <h3 style="margin:10px 0 6px 0; color:#051C2C;">A2.5.5 研發管理（R&D Management）</h3>
      <p style="font-size:13.5px; color:#334155; line-height:1.55;">
        <b>規劃擴充主題</b>：IPD 整合產品開發流程、技術路線圖（Technology Roadmap）、創新雙元組織與研發人員長期激勵。
      </p>
    </div>
    <div style="margin-top:12px; font-size:12px; color:#64748B; font-weight:700;">📂 對應目錄：A2.5.5 研發管理</div>
  </div>

  <div class="domain-card">
    <div>
      <span style="background:#0F766E; color:#fff; padding:3px 10px; border-radius:999px; font-size:11.5px; font-weight:800;">📘 既有知識庫已盤點（擴充預備）</span>
      <h3 style="margin:10px 0 6px 0; color:#051C2C;">A2.5.6 專案管理（Project Management）</h3>
      <p style="font-size:13.5px; color:#334155; line-height:1.55;">
        <b>已盤點資料夾教材</b>：<br/>
        1. 《超級專案管理（How Big Things Get Done）》傅以斌教授知識庫（慢思快行、模組化複製、基準線預測、克服樂觀偏誤）。
      </p>
    </div>
    <div style="margin-top:12px; font-size:12px; color:#0F766E; font-weight:700;">⚡ 支援套用 /zero-noise-pptx 轉化為大型專案決策簡報</div>
  </div>

  <div class="domain-card">
    <div>
      <span style="background:#0F766E; color:#fff; padding:3px 10px; border-radius:999px; font-size:11.5px; font-weight:800;">📘 既有知識庫已盤點（擴充預備）</span>
      <h3 style="margin:10px 0 6px 0; color:#051C2C;">A2.5.7 綜合研討（Executive Synthesis）</h3>
      <p style="font-size:13.5px; color:#334155; line-height:1.55;">
        <b>已盤點資料夾教材</b>：<br/>
        1. 《黃崇仁經營哲學專訪》台灣半導體與力積電資本運作智慧<br/>
        2. 《劉瀾・一句話學管理》大師管理命題濃縮庫
      </p>
    </div>
    <div style="margin-top:12px; font-size:12px; color:#0F766E; font-weight:700;">⚡ 支援套用 /zero-noise-pptx 轉化為經營哲學簡報</div>
  </div>
</div>

---

## 🛠️ 未來新教材一鍵擴充標準流程（Standard Expansion Pipeline）

當您未來在 `A2.5.1` ~ `A2.5.7` 放入新的課程或讀書筆記時，只需依循以下 3 步驟即可自動生成無雜訊簡報與網站專區：

1. **知識萃取（Knowledge Extraction）**：將原始 `.md` 或 `.pdf` 萃取為結構化資料（包含 `conclusion_title`、森秀明 8 種版型欄位、`beginner` 入門故事、`advanced` 進階思考模型與 `speaker_notes` 三段式講稿）。
2. **簡報生成（`python build_pptx.py`）**：自動產出包含情境圖片與雙軌導讀的 16:9 `.pptx` 顧問簡報，存入 `docs/public/downloads/`。
3. **門戶發布（`python build_site.py && git push`）**：自動更新 VitePress 導覽列、全文搜尋索引與互動式簡報劇場，透過 GitHub Actions 直接發布至 GitHub Pages。
"""
    with open(os.path.join(DOMAINS_OUT_DIR, "index.md"), "w", encoding="utf-8") as f:
        f.write(domains_md)
    print("[OK] Wrote docs/domains/index.md")


def write_portal_homepage():
    """生成 docs/index.md：執行長專業入口網站首頁（含即時關鍵字搜尋器、八大領域入口、全40講快速檢索牆）"""
    search_items = []
    for lec in ALL_LECTURES:
        search_items.append({
            "id": lec["id"],
            "code": lec["code"],
            "kb_id": lec["kb_id"],
            "title": lec["title"],
            "short_title": lec["short_title"],
            "module": lec["module"],
            "module_id": lec["module_id"],
            "layout_label": lec["layout_label"],
            "conclusion_title": lec["conclusion_title"],
            "beginner_summary": lec["beginner"]["summary"],
            "case_story": lec["beginner"]["case_story"],
            "model_name": lec["advanced"]["model_name"],
            "keywords": lec["keywords"],
            "web_image": with_base(lec["web_image"]),
            "doc_link": with_base(f"/30-lectures/{lec['id']}"),
            "slide_link": with_base(f"/slides/?lec={lec['id']}")
        })

    items_json = json.dumps(search_items, ensure_ascii=False)

    index_md = f"""---
layout: doc
aside: false
title: "執行長專業知識庫｜CEO Executive Mastery Portal"
---

<script setup>
import {{ ref, computed }} from 'vue'

const lectures = {items_json}
const query = ref('')
const activeModule = ref('all')
const activeLevel = ref('both') // 'both' | 'beginner' | 'advanced'

const hotKeywords = [
  '萬科', '巴林銀行', 'AB股', '合夥人', '67%', '獨立董事',
  '累積投票制', '代理成本', '股權激勵', '毒丸計畫', '家族企業', '對賭協議'
]

const filteredLectures = computed(() => {{
  return lectures.filter(item => {{
    if (activeModule.value !== 'all' && item.module_id !== activeModule.value) return false
    if (query.value.trim() !== '') {{
      const q = query.value.trim().toLowerCase()
      const text = [
        item.code, item.kb_id, item.title, item.conclusion_title,
        item.beginner_summary, item.case_story, item.model_name,
        item.layout_label, ...(item.keywords || [])
      ].join(' ').toLowerCase()
      return text.includes(q)
    }}
    return true
  }})
}})

function toggleKeyword(kw) {{
  if (query.value === kw) {{
    query.value = ''
  }} else {{
    query.value = kw
  }}
}}
</script>

<!-- Hero Banner -->
<div style="background:linear-gradient(135deg, #051C2C 0%, #0A2E46 65%, #004B2B 100%); color:#FFFFFF; border-radius:16px; padding:36px 32px; margin:10px 0 28px 0; box-shadow:0 16px 36px rgba(5,28,44,0.22);">
  <div style="display:grid; grid-template-columns: 62% 38%; gap:24px; align-items:center;">
    <div>
      <div style="display:inline-flex; gap:8px; align-items:center; background:rgba(0,163,224,0.2); border:1px solid #00A3E0; color:#7DD3FC; padding:4px 12px; border-radius:999px; font-size:12.5px; font-weight:800; margin-bottom:14px;">
        🏛️ A2.5 企業管理頂層門戶 ｜ CEO EXECUTIVE MASTERY PORTAL
      </div>
      <h1 style="color:#FFFFFF !important; font-size:34px !important; line-height:1.22 !important; margin:0 0 14px 0 !important; border:none !important;">
        執行長專業知識庫 ＆<br/>無雜訊顧問簡報中心
      </h1>
      <p style="color:#E2E8F0 !important; font-size:15.5px !important; line-height:1.65 !important; margin:0 0 22px 0 !important;">
        整合 <b>「A2.5 八大企業管理領域」</b>，首發旗艦收錄 <b>《劉松博・公司治理 30 講》（全 40 講完整知識庫）</b>。採用前 BCG 顧問森秀明 <b>「8 大無雜訊簡報版型」</b>，為 <b>🌱 入門者</b> 提供白話解析與商業故事，為 <b>🏛️ 進階執行長</b> 建立頂層思考模型與董事會檢核表。
      </p>
      <div style="display:flex; flex-wrap:wrap; gap:12px;">
        <a href="{with_base('/slides/')}" style="background:#00A3E0; color:#051C2C; padding:11px 20px; border-radius:8px; font-weight:800; text-decoration:none; font-size:14.5px; box-shadow:0 4px 14px rgba(0,163,224,0.4);">
          🎯 進入 16:9 無雜訊簡報互動劇場
        </a>
        <a href="{with_base('/downloads/劉松博_公司治理30講_無雜訊顧問簡報_精華16頁.pptx')}" download style="background:#FFFFFF; color:#051C2C; padding:11px 18px; border-radius:8px; font-weight:800; text-decoration:none; font-size:14px;">
          📥 下載精華 16 頁 PPTX
        </a>
        <a href="{with_base('/downloads/劉松博_公司治理30講_全40講無雜訊顧問簡報庫.pptx')}" download style="background:rgba(255,255,255,0.14); color:#FFFFFF; border:1px solid rgba(255,255,255,0.35); padding:11px 18px; border-radius:8px; font-weight:700; text-decoration:none; font-size:14px;">
          📘 下載全 40 講完整 PPTX (42頁)
        </a>
      </div>
    </div>
    <div style="display:flex; flex-direction:column; gap:10px;">
      <img src="{with_base('/images/unsplash/topic_cover.jpg')}" alt="Executive Boardroom" style="width:100%; height:200px; object-fit:cover; border-radius:10px; border:2px solid rgba(255,255,255,0.25);" />
      <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:8px; text-align:center;">
        <div style="background:rgba(255,255,255,0.1); padding:10px 6px; border-radius:8px;">
          <div style="font-size:20px; font-weight:900; color:#00A3E0;">40 講</div>
          <div style="font-size:11.5px; color:#CBD5E1;">完整知識萃取</div>
        </div>
        <div style="background:rgba(255,255,255,0.1); padding:10px 6px; border-radius:8px;">
          <div style="font-size:20px; font-weight:900; color:#2ECC71;">8 種</div>
          <div style="font-size:11.5px; color:#CBD5E1;">無雜訊顧問版型</div>
        </div>
        <div style="background:rgba(255,255,255,0.1); padding:10px 6px; border-radius:8px;">
          <div style="font-size:20px; font-weight:900; color:#FBBF24;">100%</div>
          <div style="font-size:11.5px; color:#CBD5E1;">每頁雙圖輔助</div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- 即時關鍵字與認知雙軌檢索中心 -->
<div class="portal-search-box">
  <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
    <div>
      <h2 style="color:#FFFFFF !important; margin:0 !important; border:none !important; font-size:22px !important;">🔍 執行長知識庫即時關鍵字檢索器</h2>
      <p style="color:#CBD5E1 !important; margin:4px 0 0 0 !important; font-size:13.5px !important;">輸入任何公司治理概念、企業案例（如：萬科、安隆、國美、巴林銀行）、股權比例（67%、34%）或思考模型名稱即時過濾</p>
    </div>
    <div style="display:flex; gap:6px; background:rgba(0,0,0,0.25); padding:4px; border-radius:8px;">
      <button @click="activeLevel='both'" :style="{{ background: activeLevel==='both' ? '#00A3E0' : 'transparent', color: activeLevel==='both' ? '#051C2C' : '#fff', border:'none', padding:'5px 12px', borderRadius:'6px', fontSize:'12.5px', fontWeight:'700', cursor:'pointer' }}">🌱+🏛️ 雙軌全顯</button>
      <button @click="activeLevel='beginner'" :style="{{ background: activeLevel==='beginner' ? '#00A3E0' : 'transparent', color: activeLevel==='beginner' ? '#051C2C' : '#fff', border:'none', padding:'5px 12px', borderRadius:'6px', fontSize:'12.5px', fontWeight:'700', cursor:'pointer' }}">🌱 入門者模式</button>
      <button @click="activeLevel='advanced'" :style="{{ background: activeLevel==='advanced' ? '#00A3E0' : 'transparent', color: activeLevel==='advanced' ? '#051C2C' : '#fff', border:'none', padding:'5px 12px', borderRadius:'6px', fontSize:'12.5px', fontWeight:'700', cursor:'pointer' }}">🏛️ 進階者模式</button>
    </div>
  </div>

  <input v-model="query" type="text" class="portal-search-input" placeholder="🔍 請輸入關鍵字搜尋（例如：同股不同權、AB股、獨立董事、累積投票制、毒丸計畫、代理成本、家族憲章）..." />

  <!-- 熱門關鍵字標籤 -->
  <div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:14px; align-items:center;">
    <span style="font-size:12.5px; color:#94A3B8; font-weight:700;">🔥 熱門檢索詞：</span>
    <button v-for="kw in hotKeywords" :key="kw" @click="toggleKeyword(kw)" :class="['portal-tag-btn', query===kw ? 'active' : '']">
      #{{ kw }}
    </button>
    <button v-if="query" @click="query=''" style="background:#EF4444; color:#fff; border:none; padding:4px 10px; border-radius:999px; font-size:12px; cursor:pointer; font-weight:700;">✖ 清除搜尋</button>
  </div>

  <!-- 四大模組篩選 -->
  <div style="display:flex; flex-wrap:wrap; gap:8px; margin-top:12px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.14); align-items:center;">
    <span style="font-size:12.5px; color:#94A3B8; font-weight:700;">📂 模組篩選：</span>
    <button @click="activeModule='all'" :class="['portal-tag-btn', activeModule==='all' ? 'active' : '']">全部 40 講 ({{ lectures.length }})</button>
    <button @click="activeModule='m1'" :class="['portal-tag-btn', activeModule==='m1' ? 'active' : '']">模組一：基礎與演進 (00~05)</button>
    <button @click="activeModule='m2'" :class="['portal-tag-btn', activeModule==='m2' ? 'active' : '']">模組二：股權與股東 (06~14)</button>
    <button @click="activeModule='m3'" :class="['portal-tag-btn', activeModule==='m3' ? 'active' : '']">模組三：董事會與監事會 (15~22)</button>
    <button @click="activeModule='m4'" :class="['portal-tag-btn', activeModule==='m4' ? 'active' : '']">模組四：經理人、控制權與家族 (23~39)</button>
    <span style="margin-left:auto; font-size:13px; color:#7DD3FC; font-weight:800;">顯示 {{ filteredLectures.length }} / 40 講</span>
  </div>
</div>

<!-- 檢索結果卡片牆 -->
<div style="display:grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap:18px; margin-bottom:36px;">
  <div v-for="item in filteredLectures" :key="item.id" style="border:1px solid #CBD5E1; border-radius:12px; overflow:hidden; background:#FFFFFF; display:flex; flex-direction:column; justify-content:space-between; box-shadow:0 4px 12px rgba(0,0,0,0.04);">
    <div>
      <div style="position:relative; height:155px; overflow:hidden; background:#0F172A;">
        <img :src="item.web_image" :alt="item.title" loading="lazy" style="width:100%; height:100%; object-fit:cover; opacity:0.92;" />
        <div style="position:absolute; top:10px; left:10px; display:flex; gap:6px;">
          <span style="background:#051C2C; color:#fff; padding:3px 9px; border-radius:6px; font-size:11.5px; font-weight:800;">{{ item.code }}</span>
          <span style="background:#0077C8; color:#fff; padding:3px 9px; border-radius:6px; font-size:11px; font-weight:700;">{{ item.layout_label }}</span>
        </div>
        <div style="position:absolute; bottom:8px; right:10px; background:rgba(5,28,44,0.85); color:#7DD3FC; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:700;">
          知識庫 {{ item.kb_id }}
        </div>
      </div>

      <div style="padding:14px 16px;">
        <div style="font-size:11.5px; color:#64748B; font-weight:700; margin-bottom:4px;">{{ item.module }}</div>
        <h3 style="margin:0 0 8px 0 !important; font-size:16.5px !important; line-height:1.35 !important; color:#051C2C !important;">
          <a :href="item.doc_link" style="color:#051C2C; text-decoration:none;">{{ item.title }}</a>
        </h3>
        <div style="background:#F8FAFC; border-left:3px solid #0077C8; padding:7px 10px; font-size:12.5px; font-weight:700; color:#1E293B; line-height:1.42; margin-bottom:10px;">
          💡 {{ item.conclusion_title }}
        </div>

        <div v-if="activeLevel==='both' || activeLevel==='beginner'" style="font-size:12.5px; color:#334155; line-height:1.5; margin-bottom:8px;">
          <span style="color:#0077C8; font-weight:800;">🌱 入門導讀：</span>{{ item.beginner_summary.slice(0, 68) }}…
        </div>
        <div v-if="activeLevel==='both' || activeLevel==='advanced'" style="font-size:12.5px; color:#1E293B; line-height:1.5; background:#F1F5F9; padding:6px 10px; border-radius:6px;">
          <span style="color:#051C2C; font-weight:800;">🏛️ 進階模型：</span><b>{{ item.model_name }}</b>
        </div>
      </div>
    </div>

    <div style="padding:10px 16px; background:#F8FAFC; border-top:1px solid #E2E8F0; display:flex; justify-content:space-between; align-items:center;">
      <a :href="item.doc_link" style="color:#0077C8; font-size:13px; font-weight:800; text-decoration:none;">📖 完整教材與雙軌解析</a>
      <a :href="item.slide_link" style="background:#051C2C; color:#fff; padding:4px 10px; border-radius:5px; font-size:12px; font-weight:700; text-decoration:none;">🎯 簡報預覽</a>
    </div>
  </div>
</div>

---

## 🗂️ A2.5 企業管理｜八大執行長專業領域擴充架構（Future Expansion Hub）

> 本知識庫已預先建立 **A2.5.0 ～ A2.5.7 八大管理領域** 的模組化擴充底座，可由下方入口直接前往各領域之簡報與知識庫：

<div class="domain-grid">
  <div class="domain-card flagship">
    <div>
      <span style="background:#0077C8; color:#fff; padding:2px 8px; border-radius:999px; font-size:11px; font-weight:800;">🟢 FLAGSHIP LIVE</span>
      <h4 style="margin:8px 0 4px 0; color:#051C2C;">A2.5.0 公司治理（劉松博30講）</h4>
      <p style="font-size:12.8px; color:#334155; margin:0;">全 40 講無雜訊顧問簡報、雙軌思考模型與 41 節知識庫全量上線。</p>
    </div>
    <div style="margin-top:10px;"><a href="{with_base('/slides/')}" style="color:#0077C8; font-weight:800; font-size:13px;">➔ 進入簡報劇場與知識庫</a></div>
  </div>

  <div class="domain-card">
    <div>
      <span style="background:#0F766E; color:#fff; padding:2px 8px; border-radius:999px; font-size:11px; font-weight:800;">📘 擴充預備</span>
      <h4 style="margin:8px 0 4px 0; color:#051C2C;">A2.5.1 策略管理</h4>
      <p style="font-size:12.8px; color:#334155; margin:0;">涵蓋《孫子兵法十三篇》、《藍海策略》、《生態系競爭策略》與《競合策略》。</p>
    </div>
    <div style="margin-top:10px;"><a href="{with_base('/domains/')}" style="color:#0F766E; font-weight:800; font-size:13px;">➔ 查看領域擴充館</a></div>
  </div>

  <div class="domain-card">
    <div>
      <span style="background:#0F766E; color:#fff; padding:2px 8px; border-radius:999px; font-size:11px; font-weight:800;">📘 擴充預備</span>
      <h4 style="margin:8px 0 4px 0; color:#051C2C;">A2.5.4 人資與組織</h4>
      <p style="font-size:12.8px; color:#334155; margin:0;">涵蓋《團隊協作的五大障礙》知識庫、高管激勵與接班人計畫。</p>
    </div>
    <div style="margin-top:10px;"><a href="{with_base('/domains/')}" style="color:#0F766E; font-weight:800; font-size:13px;">➔ 查看領域擴充館</a></div>
  </div>

  <div class="domain-card">
    <div>
      <span style="background:#0F766E; color:#fff; padding:2px 8px; border-radius:999px; font-size:11px; font-weight:800;">📘 擴充預備</span>
      <h4 style="margin:8px 0 4px 0; color:#051C2C;">A2.5.6 專案管理 ＆ A2.5.7 綜合研討</h4>
      <p style="font-size:12.8px; color:#334155; margin:0;">涵蓋《超級專案管理》、《黃崇仁經營哲學專訪》與《一句話學管理》。</p>
    </div>
    <div style="margin-top:10px;"><a href="{with_base('/domains/')}" style="color:#0F766E; font-weight:800; font-size:13px;">➔ 查看八大領域完整架構</a></div>
  </div>
</div>
"""
    with open(os.path.join(DOCS_DIR, "index.md"), "w", encoding="utf-8") as f:
        f.write(index_md)
    print("[OK] Wrote docs/index.md (CEO Executive Portal Homepage)")


def main():
    lecture_raw_map = load_source_markdown_files()
    print(f"[OK] Loaded and converted {len(lecture_raw_map)} raw lecture files to Traditional Chinese")
    write_vitepress_config()
    write_custom_theme()
    write_lecture_pages(lecture_raw_map)
    write_slides_theatre_page()
    write_architecture_page()
    write_domains_page()
    write_portal_homepage()
    print("[SUCCESS] All VitePress portal pages generated!")


if __name__ == "__main__":
    main()
