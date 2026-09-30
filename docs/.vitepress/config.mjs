import { defineConfig } from 'vitepress'

export default defineConfig({
  base: '/corp-gov-portal/',
  ignoreDeadLinks: true,
  lang: 'zh-TW',
  title: '執行長專業知識庫｜CEO Executive Mastery',
  description: 'A2.5 企業管理頂層入口網站 × 劉松博《公司治理30講》無雜訊顧問簡報與雙軌思考架構百科',
  cleanUrls: true,
  head: [
    ['link', { rel: 'icon', href: '/corp-gov-portal/images/lectures/lec_00_1.jpg' }]
  ],
  themeConfig: {
    siteTitle: '🏛️ 執行長專業知識庫',
    nav: [
      { text: '🏠 執行長入口首頁', link: '/' },
      { text: '🎯 無雜訊顧問簡報劇場', link: '/slides/' },
      { text: '🧭 全書因果架構 (#041)', link: '/architecture/' },
      {
        text: '📚 公司治理30講 (全40講)',
        items: [
          { text: '模組一：基礎與演進 (00~05)', link: '/30-lectures/00' },
          { text: '模組二：股權與股東 (06~14)', link: '/30-lectures/06' },
          { text: '模組三：董事會與監事會 (15~22)', link: '/30-lectures/15' },
          { text: '模組四：經理人、控制權與家族 (23~39)', link: '/30-lectures/23' }
        ]
      },
      { text: '🗂️ 八大管理領域擴充館', link: '/domains/' },
      {
        text: '📥 下載 PPTX 簡報',
        items: [
          { text: '📊 下載精華 16 頁決策簡報 (.pptx)', link: 'https://davidyeh51.github.io/corp-gov-portal/downloads/劉松博_公司治理30講_無雜訊顧問簡報_精華16頁.pptx' },
          { text: '📘 下載全 40 講完整簡報百科 (.pptx)', link: 'https://davidyeh51.github.io/corp-gov-portal/downloads/劉松博_公司治理30講_全40講無雜訊顧問簡報庫.pptx' }
        ]
      }
    ],
    sidebar: [
      {
        text: '🏛️ 執行長專業總覽與簡報中心',
        collapsed: false,
        items: [
          { text: '🏠 執行長專業入口首頁 (含關鍵字檢索)', link: '/' },
          { text: '🎯 16:9 無雜訊顧問簡報互動劇場', link: '/slides/' },
          { text: '🧭 跨講次因果邏輯與全書架構 (#041)', link: '/architecture/' },
          { text: '🗂️ A2.5 八大管理領域擴充館', link: '/domains/' }
        ]
      },
      {
        text: '模組一：公司治理基礎與演進 (00~05)',
        collapsed: false,
        items: [{"text": "00｜00 發刊詞：治理與管理的頂層分野", "link": "/30-lectures/00"}, {"text": "01｜01 公司制度：有限責任與獨立法人", "link": "/30-lectures/01"}, {"text": "02｜02 治理本質：對抗兩大先天制度缺陷", "link": "/30-lectures/02"}, {"text": "03｜03 信任機制：從人際信任走向制度信任", "link": "/30-lectures/03"}]
      },
      {
        text: '模組二：股權結構與股東治理 (06~14)',
        collapsed: false,
        items: [{"text": "04｜04 股權本質：剩餘索取權與剩餘控制權", "link": "/30-lectures/04"}, {"text": "05｜05 創業合夥人：AIV 三維遴選模型", "link": "/30-lectures/05"}, {"text": "06｜06 股權架構：避開三大奪命雷區", "link": "/30-lectures/06"}, {"text": "07｜07 保住控制權：四大控制權防禦武器", "link": "/30-lectures/07"}, {"text": "08｜08 同股不同權：AB 股的效率與風險", "link": "/30-lectures/08"}, {"text": "09｜09 企業家悖論：成也蕭何、敗也蕭何", "link": "/30-lectures/09"}, {"text": "10｜10 透明化溢價：陽光是最好的防腐劑", "link": "/30-lectures/10"}, {"text": "11｜11 上市決策：收益、代價與情境動態重評", "link": "/30-lectures/11"}, {"text": "12｜12 制衡控股股東：聯合制衡與事前協議", "link": "/30-lectures/12"}, {"text": "13｜13 小股東維權：累積投票制與結盟限制", "link": "/30-lectures/13"}, {"text": "14｜14 外部治理：資訊、市場與司法三防線", "link": "/30-lectures/14"}, {"text": "15｜15 董事會迷失：獨立性困境與激勵悖論", "link": "/30-lectures/15"}]
      },
      {
        text: '模組三：董事會與監事會運作 (15~22)',
        collapsed: false,
        items: [{"text": "16｜16 CEO與董事長：職銜不等於實權", "link": "/30-lectures/16"}, {"text": "17｜17 職業經理人衝突：代理問題與心理所有權", "link": "/30-lectures/17"}, {"text": "18｜18 何為職業化：技能、態度與契約道德", "link": "/30-lectures/18"}, {"text": "19｜19 高管薪酬：錦標賽激勵與管理層權力", "link": "/30-lectures/19"}, {"text": "20｜20 股權激勵：失效條件與五大成功法則", "link": "/30-lectures/20"}, {"text": "21｜21 國企混改：產權清晰與政企邊界", "link": "/30-lectures/21"}, {"text": "22｜22 家族企業：家族治理與公司治理分離", "link": "/30-lectures/22"}, {"text": "23｜23 門口野蠻人：敵意收購的雙面刃", "link": "/30-lectures/23"}, {"text": "24｜24 利益相關者：股東至上 vs. 多方兼顧", "link": "/30-lectures/24"}, {"text": "25｜25 公司的目的：利益中心與權力中心分離", "link": "/30-lectures/25"}, {"text": "26｜26 德國監事會：高位階不保證獨立監督", "link": "/30-lectures/26"}, {"text": "27｜27 員工共決制：勞方保障與決策效率取捨", "link": "/30-lectures/27"}, {"text": "28｜28 日本治理改革：制度進化與路徑依賴", "link": "/30-lectures/28"}]
      },
      {
        text: '模組四：經理人激勵、控制權與家族治理 (23~39)',
        collapsed: false,
        items: [{"text": "29｜29 事業合夥人：從共享收益走向共擔風險", "link": "/30-lectures/29"}, {"text": "30｜30 企業軟治理：價值觀落地三部曲", "link": "/30-lectures/30"}, {"text": "31｜31 全員持股：福利與激勵的分界", "link": "/30-lectures/31"}, {"text": "32｜32 裂變式創業：創新特區與複製型擴張", "link": "/30-lectures/32"}, {"text": "33｜33 生態治理：投資不控股與底線規則", "link": "/30-lectures/33"}, {"text": "34｜34 平台治理：三重屬性與演算法公平", "link": "/30-lectures/34"}, {"text": "35｜35 激勵危機：現金流保衛與危機留才", "link": "/30-lectures/35"}, {"text": "36｜36 韋爾奇反思：管理巨人與治理制度邊界", "link": "/30-lectures/36"}, {"text": "37｜37 OpenAI 大戰：AI 時代的治理嘗試與常識", "link": "/30-lectures/37"}, {"text": "A1｜A1 結語：從企業家精神到企業家自覺", "link": "/30-lectures/38"}, {"text": "A2｜A2 進階書單：五大治理問題閱讀地圖", "link": "/30-lectures/39"}]
      }
    ],
    search: {
      provider: 'local',
      options: {
        detailedView: true,
        translations: {
          button: {
            buttonText: '🔍 搜尋知識庫、案例、模型、關鍵字...',
            buttonAriaLabel: '搜尋知識庫'
          },
          modal: {
            displayDetails: '顯示詳細內容',
            resetButtonTitle: '清除搜尋',
            backButtonTitle: '返回',
            noResultsText: '找不到相關內容，請嘗試搜尋「股權」「萬科」「獨立董事」「毒丸」「AB股」等關鍵字',
            footer: {
              selectText: '前往閱讀',
              navigateText: '上下切換',
              closeText: '關閉 (ESC)'
            }
          }
        }
      }
    },
    outline: {
      level: [2, 3],
      label: '本頁知識導覽'
    },
    docFooter: {
      prev: '上一講',
      next: '下一講'
    },
    footer: {
      message: 'A2.5 企業管理｜執行長專業知識庫（Zero-Noise Consulting Presentation & Dual-Track Knowledge Portal）',
      copyright: 'Built for DavidCloud Executive Mastery｜遵循森秀明無雜訊簡報 8 大版型與三大顧問公司視覺規範'
    }
  }
})
