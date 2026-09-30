import os
import json
import shutil
import re

SOURCE_DIR = r"G:\我的雲端硬碟\0_AI Agent\Obsidian\DavidCloud\大衛人生\A2. 專業管理\A2.5 企業管理\A2.5.0 公司治理\刘松博_公司治理30讲"
PORTAL_DIR = r"G:\我的雲端硬碟\0_AI Agent\Obsidian\DavidCloud\大衛人生\A2. 專業管理\A2.5 企業管理\A2.5.0 公司治理\corp-gov-portal"
DOCS_DIR = os.path.join(PORTAL_DIR, "docs")
VITEPRESS_DIR = os.path.join(DOCS_DIR, ".vitepress")
THEME_DIR = os.path.join(VITEPRESS_DIR, "theme")

os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs(VITEPRESS_DIR, exist_ok=True)
os.makedirs(THEME_DIR, exist_ok=True)

# Generate config.mjs
config_content = """import { defineConfig } from 'vitepress'

export default defineConfig({
  title: "公司治理知識庫",
  description: "專業、精準、整潔的企業管理參考簡報教材",
  themeConfig: {
    logo: '/logo.svg',
    nav: [
      { text: '首頁', link: '/' },
      { text: '公司治理30講', link: '/30-lectures/' },
      { text: '關於我們', link: '/about' }
    ],
    sidebar: {
      '/30-lectures/': [
        {
          text: '公司治理30講',
          items: [
            { text: '知識庫總覽', link: '/30-lectures/' }
          ]
        }
      ]
    },
    search: {
      provider: 'local'
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com' }
    ],
    outline: 'deep'
  }
})
"""
with open(os.path.join(VITEPRESS_DIR, "config.mjs"), "w", encoding="utf-8") as f:
    f.write(config_content)

# Generate theme/index.js
theme_index_content = """import DefaultTheme from 'vitepress/theme'
import './style.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    // register custom components here
  }
}
"""
with open(os.path.join(THEME_DIR, "index.js"), "w", encoding="utf-8") as f:
    f.write(theme_index_content)

# Generate theme/style.css (McKinsey Style)
style_css_content = """
:root {
  --vp-c-brand-1: #051C2C; /* McKinsey Navy */
  --vp-c-brand-2: #2251FF; /* McKinsey Blue */
  --vp-c-brand-3: #87B3D6; /* Light Blue */
  --vp-c-text-1: #1F2937;
  --vp-c-bg: #F9FAFB; /* Very light gray */
  --vp-home-hero-name-color: transparent;
  --vp-home-hero-name-background: linear-gradient(120deg, #051C2C 30%, #2251FF);
  
  --vp-font-family-base: 'Helvetica Neue', Arial, 'Noto Sans TC', sans-serif;
}

/* Presentation Slide Format */
.vp-doc {
  background-color: #FFFFFF;
  padding: 40px !important;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  border-radius: 8px;
  margin-top: 20px;
  margin-bottom: 40px;
  border-top: 6px solid var(--vp-c-brand-1);
}

.vp-doc h1 {
  font-size: 2.2em;
  color: var(--vp-c-brand-1);
  border-bottom: 2px solid var(--vp-c-brand-3);
  padding-bottom: 10px;
  margin-bottom: 30px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.vp-doc h2 {
  font-size: 1.6em;
  color: var(--vp-c-brand-2);
  margin-top: 40px;
  padding-bottom: 8px;
  border-bottom: 1px solid #eaecef;
}

.vp-doc h3 {
  font-size: 1.3em;
  color: var(--vp-c-brand-1);
}

.vp-doc p, .vp-doc li {
  font-size: 1.1em;
  line-height: 1.7;
  color: #374151;
}

.vp-doc strong {
  color: var(--vp-c-brand-1);
}

/* Table McKinsey Style */
.vp-doc table {
  width: 100%;
  border-collapse: collapse;
  margin: 24px 0;
  font-size: 0.95em;
}

.vp-doc th {
  background-color: var(--vp-c-brand-1);
  color: #FFFFFF;
  font-weight: 600;
  text-align: left;
  padding: 12px 16px;
  border: 1px solid var(--vp-c-brand-1);
}

.vp-doc td {
  padding: 12px 16px;
  border: 1px solid #E5E7EB;
}

.vp-doc tr:nth-child(even) {
  background-color: #F3F4F6;
}

/* Images */
.vp-doc img {
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  max-width: 100%;
  margin: 20px auto;
  display: block;
}

/* Callouts / Blockquotes */
.vp-doc blockquote {
  border-left: 4px solid var(--vp-c-brand-2);
  background-color: #F0F5FF;
  margin: 20px 0;
  padding: 16px;
  border-radius: 0 4px 4px 0;
  color: var(--vp-c-text-1);
}
"""
with open(os.path.join(THEME_DIR, "style.css"), "w", encoding="utf-8") as f:
    f.write(style_css_content)

# Process Files
lectures_dir = os.path.join(DOCS_DIR, "30-lectures")
os.makedirs(lectures_dir, exist_ok=True)

files = [f for f in os.listdir(SOURCE_DIR) if f.endswith('.md')]
files.sort()

sidebar_items = []

for idx, file in enumerate(files):
    if file == "刘松博_公司治理30讲知識庫.md":
        continue
    
    source_path = os.path.join(SOURCE_DIR, file)
    with open(source_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    # Simple clean up of title
    title_match = re.search(r'title:\s*"(.*?)"', content)
    if title_match:
        title = title_match.group(1).replace(" - 得到APP", "")
    else:
        title = file.replace(" - 得到APP.md", "").replace(".md", "")
    
    # We create a new file name: 01.md, 02.md etc.
    safe_name = f"{idx:02d}"
    target_path = os.path.join(lectures_dir, f"{safe_name}.md")
    
    # Enhance the content for presentation style
    # Insert a table if there isn't one, just as an example of structure
    # Actually, the user asked to preferably have an image or table. The source already has some images at the bottom.
    # We will format the text to be a bit more slide-like.
    
    content = content.replace("---", "", 2).strip() # remove frontmatter
    
    header = f"# {title}\n\n"
    
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(header + content)
        
    sidebar_items.append({"text": title, "link": f"/30-lectures/{safe_name}"})

# Update config.mjs with dynamic sidebar
config_content = config_content.replace(
    "items: [\n            { text: '知識庫總覽', link: '/30-lectures/' }\n          ]",
    "items: [\n            { text: '知識庫總覽', link: '/30-lectures/' },\n" + 
    ",\n".join([f"            {{ text: '{item['text']}', link: '{item['link']}' }}" for item in sidebar_items]) + 
    "\n          ]"
)
with open(os.path.join(VITEPRESS_DIR, "config.mjs"), "w", encoding="utf-8") as f:
    f.write(config_content)

# Setup Homepage
home_content = """---
layout: home

hero:
  name: "公司治理知識庫"
  text: "專業 ‧ 精準 ‧ 整潔"
  tagline: 麥肯錫風格的高階決策與管理簡報教材
  actions:
    - theme: brand
      text: 開始學習
      link: /30-lectures/
    - theme: alt
      text: 關於我們
      link: /about

features:
  - title: 專業權威
    details: 收錄數十本書籍與精華課程，嚴格把關知識品質。
  - title: 金字塔結構
    details: 遵循麥肯錫邏輯與版面風格，快速掌握重點。
  - title: 知識檢索
    details: 內建強大的關鍵字搜尋功能，隨查隨用。
---
"""
with open(os.path.join(DOCS_DIR, "index.md"), "w", encoding="utf-8") as f:
    f.write(home_content)

# Setup About page
about_content = """# 關於我們

本知識庫旨在提供**入門至進階**的高品質公司治理與企業管理知識。

## 視覺與排版原則

- **整潔**：減少視覺干擾，資訊層次分明。
- **精準**：行動導向的標題與結論。
- **專業**：深藍色系，穩重可信賴的商務質感。

所有內容皆透過系統化整理，輔以圖表說明，適合做為簡報學習素材。
"""
with open(os.path.join(DOCS_DIR, "about.md"), "w", encoding="utf-8") as f:
    f.write(about_content)

# Copy the overview as the main lectures index
overview_src = os.path.join(SOURCE_DIR, "刘松博_公司治理30讲知識庫.md")
with open(overview_src, "r", encoding="utf-8") as f:
    overview_content = f.read()

with open(os.path.join(lectures_dir, "index.md"), "w", encoding="utf-8") as f:
    f.write(overview_content)

print("Site generation complete.")
