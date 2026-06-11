Create 49 NEW tool pages to bring the total from 51 to 100.

## Current tools (src/data/tools.json - 51 tools)
Categories and counts:
- Encode/Decode: base64, url-encode, unicode, html-entity, hex-to-text, text-to-binary, morse-code, jwt-decoder (8)
- Hash: md5, sha256 (2)
- Text: word-counter, case-converter, text-diff, text-sort, slug-generator, list-randomizer, text-repeater, emoji-picker, lorem-ipsum, markdown-preview, regex (11)
- Time: timestamp, countdown, date-calculator, stopwatch, age-calculator, pomodoro (6)
- Dev Tools: uuid-generator, css-minifier, js-minifier, html-minifier, sql-formatter, url-parser, json-validator, http-status, meta-tag-generator (9)
- Convert: csv-to-json, json-to-csv, number-base, unit-converter (4)
- Formatter: json-formatter, json-validator (2)
- Generator: qr-code, password-generator, random-string (3)
- Security: password-generator (overlap with Generator)
- Design: color-picker, color-contrast (2)
- Image: image-compress (1)
- Math: percentage-calculator, bmi-calculator (2)
- Network: ip-lookup (1)

## 49 New Tools (spread across ALL categories, fill gaps)
Pick tools that are:
- Useful for developers, writers, designers
- Searchable (people actually Google for them)
- Implementable with vanilla JS (no external APIs, no server needed)

Good candidates:
- Encode/Decode: URL decoder, HTML decoder, ROT13, Punycode converter, ASCII table, binary decoder
- Hash: SHA1, SHA512, CRC32, Bcrypt checker, hash compare, HMAC generator
- Text: character counter, line sorter, duplicate remover, text reverser, string splitter, text joiner, whitespace trimmer, text replace, markdown to HTML, HTML to markdown
- Time: timezone converter, cron expression parser, date diff, week number, day of year, sleep calculator
- Dev Tools: YAML to JSON, XML formatter, JSON to XML, CSV viewer, JSON diff, API tester (GET only), git cheatsheet, DNS lookup (client-side via public API), user agent parser, MIME type lookup
- Convert: XML to JSON, YAML to JSON, JSON to YAML, celsius to fahrenheit, bytes to KB/MB/GB, roman numerals
- Formatter: XML formatter, CSS beautifier, HTML beautifier, JavaScript beautifier
- Generator: random number, random color, UUID v1, nano ID, hash generator (pick from list), lorem ipsum (paragraphs), dice roller
- Security: password strength checker, SSL checker (via API), entropy calculator
- Design: gradient generator, shadow generator, border radius preview, flexbox playground, CSS grid generator
- Image: favicon generator, image to base64, SVG optimizer, EXIF viewer
- Math: random number generator, scientific calculator, fraction calculator, tip calculator, currency converter (static rates), square root
- Network: HTTP headers checker, ping tester, port checker, WHOIS lookup (via API)

## FOR EACH NEW TOOL
1. Create src/pages/{tool-id}.astro following the pattern of existing pages
2. Add entry to src/data/tools.json: {"id","name","desc","cat"}
3. Add i18n entry to src/i18n/utils.js (name, desc, howto)
4. Add i18n entry to src/i18n/zh.json (name, desc, howto in Chinese)
5. Include the SEO content pattern (What is / When to Use / How to Use / Related Tools)
6. Each tool MUST have functional vanilla JS (in <script is:inline>)

## CRITICAL
- Do NOT introduce npm dependencies
- All JS inline, no external files
- Use existing components: Textarea, Button, DualPane, StatCard
- Each page ~150-250 words SEO content
- Run npm run build after every 10 tools to catch errors early
- FINAL: npm run build must pass for all 100 tools
