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
| 框架搭建 | ✅ | 首页 + 51 工具，13 大分类 |
| 首页重构 | ✅ | v0 设计：Hero/搜索/卡片/精选 |
| 英文化 | ✅ | i18n 中英双语切换 |
| JS 内联 | ✅ | 全静态无外部依赖 |
| GitHub 推送 | ✅ | SSH 443 直连（4s） |
| Vercel 部署 | ✅ | 自动部署 |
| Vercel Analytics | ✅ | 实时访客统计 |
| 域名绑定 | ✅ | 4uses.com + HTTPS |
| SEO 优化 | ✅ | sitemap/robots/JSON-LD/canonical |
| Search Console | ✅ | HTML 文件验证 |
| 工具页正文 | 🔄 | 51 页全加 What/When/How/Related |
| 新工具页面 | 🔜 | 目标 100 个工具（+49） |
| Blog 栏目 | 🔜 | 5 篇初始文章 + 工具教程 |
| AdSense | ❌ | 被拒（关联已停用账号） |
| Media.net | 🔜 | AdSense 替代方案 |

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
