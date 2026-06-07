# SEO + Search Console + AdSense 全链路方案

## 目标
让 4uses.com 被 Google 收录、在搜索结果中有竞争力、具备接广告的能力。

## 当前状态
- Astro 5 + Tailwind，21 页（首页 + 20 工具）
- 已部署 Vercel，域名 4uses.com，HTTPS 已生效
- BaseLayout 有基础 meta（og:title/description，twitter card）
- `site` 配置仍为 `online-tools.vercel.app`（需改为 4uses.com）

## 执行计划

### Phase 1: 代码层 SEO 优化 → OpenCode

| # | 任务 | 说明 |
|---|------|------|
| 1 | 改 site URL | astro.config.js: `site: 'https://4uses.com'` |
| 2 | 安装 @astrojs/sitemap | 自动生成 sitemap.xml |
| 3 | 添加 robots.txt | 放 public/robots.txt，允许所有爬虫，指向 sitemap |
| 4 | 改进 BaseLayout meta | 加 canonical、robots meta、og:url、og:locale |
| 5 | 优化页面标题 | 每个工具页面标题优化为 `{Tool Name} - Free Online Tool | 4uses` |
| 6 | 添加结构化数据 | 首页 WebSite schema，工具页 WebApplication schema |
| 7 | 添加 ads.txt | `google.com, pub-XXXXX, DIRECT, f08c47fec0942fa0`（先放占位，申请后更新） |
| 8 | 添加 breadcrumb 结构化数据 | 工具页加 BreadcrumbList schema |
| 9 | 首页加 hreflang | `en` (目前只有英文) |

### Phase 2: Search Console → 我

| # | 任务 |
|---|------|
| 1 | 用户登录 search.google.com/search-console |
| 2 | 添加属性 4uses.com（URL prefix 方式）|
| 3 | DNS 验证（在 Cloudflare 加 TXT 记录）|
| 4 | 提交 sitemap.xml |

### Phase 3: AdSense → 我 + 用户

| # | 任务 |
|---|------|
| 1 | 去 adsense.google.com 申请 |
| 2 | 填入 4uses.com |
| 3 | 等审核（通常 1-2 周）|
| 4 | 审核通过后更新 ads.txt 中的 pub-ID |
| 5 | 在页面中嵌入广告代码 |

## 验证
- `npm run build` 无错误
- 生成的 dist/ 包含 sitemap.xml、robots.txt、ads.txt
- 每个页面 `<head>` 包含 canonical、og 全套、schema ld+json
- 部署后 Google Search Console 能正常抓取
