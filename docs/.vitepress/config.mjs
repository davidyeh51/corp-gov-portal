import { defineConfig } from 'vitepress'

export default defineConfig({
  title: "公司治理知識庫",
  description: "專業、精準、整潔的企業管理參考簡報教材",
  base: '/corp-gov-portal/',
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
            { text: '知識庫總覽', link: '/30-lectures/' },
            { text: '搞懂公司里那些最要命的事', link: '/30-lectures/00' },
            { text: '公司：有企业，为什么还有公司？', link: '/30-lectures/01' },
            { text: '治理：公司如何对抗自身的缺陷？', link: '/30-lectures/02' },
            { text: '信任：公司到底是靠什么维系的？', link: '/30-lectures/03' },
            { text: '股东与股权：股权本质上到底是什么权？', link: '/30-lectures/04' },
            { text: '创业合伙人：该不该和朋友合伙开公司？', link: '/30-lectures/05' },
            { text: '股权的架构：公司怎么样避免踏进雷区？', link: '/30-lectures/06' },
            { text: '保住控制权：创始人如何防止被踢出局？', link: '/30-lectures/07' },
            { text: '同股不同权：为什么股份少也能说了算？', link: '/30-lectures/08' },
            { text: '企业家悖论：企业家会“害死”公司吗？', link: '/30-lectures/09' },
            { text: '透明化溢价：公司上市只是为了融资吗？', link: '/30-lectures/10' },
            { text: '上市的纠结：为什么企业家经常被打脸？', link: '/30-lectures/11' },
            { text: '权力的制衡：公司该如何治理控股股东？', link: '/30-lectures/12' },
            { text: '小股东维权：“庶民”要怎样取得胜利？', link: '/30-lectures/13' },
            { text: '三道防火线：外部治理要如何控制权力？', link: '/30-lectures/14' },
            { text: '董事会迷失：压舱石为什么常常靠不住？', link: '/30-lectures/15' },
            { text: '首席执行官：CEO和董事长谁的官儿更大？', link: '/30-lectures/16' },
            { text: '职业经理人：为什么经理总是和老板掐架？', link: '/30-lectures/17' },
            { text: '何为职业化：怎么才算优秀的职业经理人？', link: '/30-lectures/18' },
            { text: '管理层权力：高管薪酬为什么会越来越高？', link: '/30-lectures/19' },
            { text: '股权怎么发：为什么高管股权激励会失效？', link: '/30-lectures/20' },
            { text: '混合所有制：国有企业改革到底路在何方？', link: '/30-lectures/21' },
            { text: '家族与企业：富不过三代是传承的宿命吗？', link: '/30-lectures/22' },
            { text: '门口野蛮人：防内部人控制还是“失控”？', link: '/30-lectures/23' },
            { text: '利益相关者：股东至上原则为何没被取代？', link: '/30-lectures/24' },
            { text: '公司的目的：客户为什么应该排在最前面？', link: '/30-lectures/25' },
            { text: '德国监事会：德意志银行为何在破产边缘？', link: '/30-lectures/26' },
            { text: '员工共决制：员工如何强势参与公司治理？', link: '/30-lectures/27' },
            { text: '进化与惯性：日本治理如何奔向美国模式？', link: '/30-lectures/28' },
            { text: '事业合伙人：职业经理人包赢不包输怎么破？', link: '/30-lectures/29' },
            { text: '企业软治理：公司怎样让飘着的价值观落地？', link: '/30-lectures/30' },
            { text: '普惠制陷阱：全员持股到底是福利还是激励？', link: '/30-lectures/31' },
            { text: '裂变式创业：到底是灵丹妙药还是镜花水月？', link: '/30-lectures/32' },
            { text: '生态型组织：公司治理如何升维成生态治理？', link: '/30-lectures/33' },
            { text: '互联网平台：大数据杀熟为何惹得群情激愤？', link: '/30-lectures/34' },
            { text: '激励危机：如何应对经营困难与工资照发之间的矛盾？', link: '/30-lectures/35' },
            { text: '制度下的管理者：杰克·韦尔奇犯了什么错？', link: '/30-lectures/36' },
            { text: '37｜从OpenAI大战看AI时代的公司治理：尝试与常识', link: '/30-lectures/37' },
            { text: '你有权成为一个不寻常的人', link: '/30-lectures/38' },
            { text: '《公司治理》进阶书单', link: '/30-lectures/39' }
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
