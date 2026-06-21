# 4uses.com — Online Tools 项目全貌

> 最后更新：2026-06-14

## 项目背景

- **目标**：海外英文在线工具站，200+ 长尾工具，Google SEO 免费流量 → AdSense 被动收入
- **域名**：4uses.com（Cloudflare Registrar，$10.46/年）
- **仓库**：GitHub `anyunlong/online-tools`（私有）
- **部署**：Vercel（自动部署，git push 触发）
- **技术栈**：Astro 5 + Tailwind CSS，纯静态 SSG
- **策略**：不做头部大词，专攻长尾小词（每个日搜索 100-300），AI 批量生成工具页面

> 最后更新：2026-06-21

## 当前进度

| 项目 | 状态 | 备注 |
|------|------|------|
| 框架搭建 | ✅ | 首页 + **203 工具**，210 页面 |
| 工具质量 | ✅ | 4 轮 bug 修复：空按钮×2、MD5假算法、sha256 DOM错、PGP→AES、时区错、bcrypt假算法、99页占位文字、uuid copy反馈 |
| 翻墙方案 | ✅ | 飞鸟云订阅（38节点，VLESS+HY2）替代 VPS |
| VPS | ❌ 已销毁 | 0 实例，0 费用 |
| AdSense | ❌ | 被拒（关联已停用账号），后续走 Media.net |
| Media.net | 🔜 | 等日均 UV 200+ 时申请 |
| Search Console | ⏳ | 仍在沙盒期，Google爬取中 |
| **日 UV** | **~7** | 累计 105 访客 / 15 天，PV ~1100 |
| 沙盒阶段 | 第 2 周 | 预期 4-8 周出沙盒 |
| Email 转发 | ✅ | hello@4uses.com → Gmail（Cloudflare Email Routing） |
| Git email | ✅ | 已修正为 chinaanyunlong@gmail.com，历史已重写 |

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
