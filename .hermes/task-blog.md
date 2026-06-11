Create a Blog section for 4uses.com.

## WHAT TO DO

1. Create src/pages/blog/index.astro - Blog listing page
   - Title: "4uses Blog - Online Tools Tips & Guides"
   - Lists all blog posts with title, date, excerpt
   - Clean dark theme matching the site

2. Create src/pages/blog/[slug].astro - Blog post template
   - Dynamic route in Astro: src/pages/blog/[...slug].astro
   - Reads from src/content/blog/ directory
   - Includes breadcrumb: Home > Blog > Post Title
   - Social sharing meta tags

3. Create 5 initial blog posts in src/content/blog/:
   Blog post ideas (each 400-600 words, SEO-optimized):
   a) "top-10-free-online-tools-developers.md" - Best tools every developer should bookmark
   b) "json-formatter-vs-validator-difference.md" - Comparison guide
   c) "what-is-base64-encoding-guide.md" - Beginner's guide to Base64
   d) "how-to-generate-strong-passwords.md" - Password security 101  
   e) "md5-vs-sha256-hash-difference.md" - Hash algorithm comparison

Each blog post should:
- Have proper frontmatter: title, date, description, tags
- Include internal links to 4uses.com tool pages
- Be SEO-optimized (H2/H3 structure, keyword-rich)
- Include a CTA at the end linking to related tools

4. Add Blog link to SiteHeader navigation

5. Run npm run build
