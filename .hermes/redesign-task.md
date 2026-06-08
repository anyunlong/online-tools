# 4uses.com 首页重构任务

## 设计参考
设计稿在 ~/projects/v0-4uses/，请先阅读以下组件：
- components/site-header.tsx
- components/hero-section.tsx
- components/tool-card.tsx
- components/tools-explorer.tsx
- components/featured-tools.tsx
- components/social-proof.tsx
- components/site-footer.tsx
- app/globals.css（颜色系统）

## 要做的事（按顺序，每步跑 npm run build 验证）

### 1. 更新设计系统 (src/styles/global.css)
把颜色替换为 v0 的 oklch 深色主题：
- background: oklch(0.13 0.02 280)
- card: oklch(0.18 0.025 280)
- primary: oklch(0.62 0.21 285) 蓝紫
- accent: oklch(0.68 0.18 320) 紫粉
- border: oklch(1 0 0 / 8%)
- ring: oklch(0.62 0.21 285)
- radius: 0.75rem
加 .gradient-text 类（渐变文字动画）
保留 .tool-area 和滚动条样式

### 2-8. 创建组件 (src/components/)
每个组件对应 v0 的同名组件，翻译成 Astro 语法，图标用 emoji 替代 lucide-react：
2. SiteHeader.astro（替换 Header.astro）
3. HeroSection.astro
4. ToolCard.astro（接收 tool props）
5. ToolsExplorer.astro（搜索+分类过滤，vanilla JS 内联交互）
6. FeaturedTools.astro（横向滚动精选）
7. SocialProof.astro（统计数据）
8. SiteFooter.astro（替换 Footer.astro）

### 9. 重写首页 (src/pages/index.astro)
保留 BaseLayout + JSON-LD schema + SEO props
内容：SiteHeader → HeroSection → ToolsExplorer → FeaturedTools → SocialProof → SiteFooter

## 约束
- 不修改工具页面文件（src/pages/md5.astro 等）
- 不修改 src/i18n/
- 不修改 src/data/tools.json
- 不引入外部依赖
- 客户端交互用内联 <script>
