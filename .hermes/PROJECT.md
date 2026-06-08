# 4uses.com — Online Tools 项目全貌

> 最后更新：2026-06-07

## 项目背景

- **目标**：海外英文在线工具站，200+ 长尾工具，Google SEO 免费流量 → AdSense 被动收入
- **域名**：4uses.com（Cloudflare Registrar，$10.46/年）
- **仓库**：GitHub `anyunlong/online-tools`（私有）
- **部署**：Vercel（自动部署，git push 触发）
- **技术栈**：Astro 5 + Tailwind CSS，纯静态 SSG
- **策略**：不做头部大词，专攻长尾小词（每个日搜索 100-300），AI 批量生成工具页面

## 当前进度

| 项目 | 状态 | 备注 |
|------|------|------|
| 框架搭建 | ✅ | 21 页（首页 + 20 工具），9 大分类 |
| 英文化 | ✅ | 全部翻译英文，面向海外用户 |
| JS 内联 | ✅ | 所有脚本内联到页面，无外部文件 |
| GitHub 推送 | ✅ | commit 129aba1 |
| Vercel 部署 | ✅ | 自动部署已配置 |
| 域名绑定 | ✅ | 4uses.com + HTTPS |
| SEO 优化 | ✅ | sitemap.xml, robots.txt, JSON-LD, canonical, meta tags |
| Search Console | ✅ | HTML 文件验证完成（google4ae8b8da930e6f4f.html） |
| AdSense | 🔜 | 等用户申请 |
| ads.txt | ⚠️ | 已放占位，AdSense 通过后需更新真实 pub-ID |

## 项目文件关键路径

```
~/projects/online-tools/
├── astro.config.mjs          # site: https://4uses.com, sitemap 集成
├── src/
│   ├── layouts/BaseLayout.astro  # SEO meta + JSON-LD schema slot
│   ├── components/ToolLayout.astro # 工具页模板，title 格式 + schema
│   ├── pages/index.astro         # 首页，WebSite schema
│   ├── pages/*.astro             # 20 个工具页
│   └── data/tools.json           # 工具列表（id, name, desc, cat）
├── public/
│   ├── robots.txt
│   ├── ads.txt                   # 占位 pub-ID
│   └── tools/                    # 工具用到的静态资源
└── .hermes/plans/                # 项目计划
```

## OpenCode 工作流

- OpenCode 会话自动持久化到 SQLite：`~/.local/share/opencode/opencode.db`
- 用 `opencode run -c` 延续上一次会话上下文
- 笨笨负责拆任务、派活；OpenCode 负责写代码
- 用户是产品经理，笨笨是项目经理，OpenCode 是程序员

## TODO / 持续迭代

### 短期
- [x] 提交 Google Search Console（已验证）
- [x] 申请 Google AdSense（已提交审核）
- [ ] AdSense 审核通过后更新 ads.txt 真实 pub-ID
- [ ] 检查 Vercel 部署日志确认 SEO 改动已上线

### 中期
- [ ] 新增 10+ 工具页面（扩大长尾词覆盖）
- [ ] 每个工具页添加 FAQ 结构化数据（增加搜索曝光）
- [ ] 添加站点内搜索功能
- [ ] 性能优化（Lighthouse 100 分）

### 长期
- [ ] 工具数量达到 200+
- [ ] 看 Google Search Console 数据，优化低排名页面
- [ ] 日 UV 目标：3 个月 50-100 → 6 个月 1000+
- [ ] 月收入目标：$100 → $500 → $1000+

## 成本记录

| 项目 | 金额 | 日期 |
|------|------|------|
| 域名 4uses.com | $10.46 | 2026-06-07 |
| **合计** | **$10.46** | |
