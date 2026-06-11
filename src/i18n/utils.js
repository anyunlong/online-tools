// Client-side i18n utilities
// Injects translations into window.__I18N__ and provides lookup helpers

import zh from './zh.json';

// Build English translations by inverting zh structure (keys are the EN values)
function buildEn() {
  const en = JSON.parse(JSON.stringify(zh)); // deep copy structure
  
  // Site
  en.site.name = '4uses';
  en.site.tagline = 'All free · No registration · No data uploaded';
  en.site.subtitle = '100+ useful tools, continuously updated';

  // UI
  en.ui.generate = 'Generate';
  en.ui.copy = 'Copy';
  en.ui.copied = 'Copied!';
  en.ui.clear = 'Clear';
  en.ui.download = 'Download';
  en.ui.encode = 'Encode';
  en.ui.decode = 'Decode';
  en.ui.format = 'Format';
  en.ui.compress = 'Compress';
  en.ui.validate = 'Validate';
  en.ui.convert = 'Convert';
  en.ui.calculate = 'Calculate';
  en.ui.result = 'Result';
  en.ui.input = 'Input';
  en.ui.output = 'Output';
  en.ui.upload = 'Upload';
  en.ui.reset = 'Reset';
  en.ui.submit = 'Submit';
  en.ui.settings = 'Settings';
  en.ui.loading = 'Loading...';
  en.ui.error = 'Error';
  en.ui.success = 'Success';
  en.ui.back = 'Back';
  en.ui.home = 'Home';

  // Categories
  en.categories = {
    Security: 'Security', Time: 'Time', Formatter: 'Formatter',
    'Encode/Decode': 'Encode/Decode', Text: 'Text', Hash: 'Hash',
    'Dev Tools': 'Dev Tools', Generator: 'Generator', Design: 'Design',
    Convert: 'Convert', Image: 'Image', Math: 'Math', Network: 'Network'
  };

  // Tools
  en.tools = {
    'password-generator': { name: 'Password Generator', desc: 'Generate strong random passwords', howto: 'Choose password length and character types (uppercase, lowercase, numbers, symbols), then click Generate for a secure random password. We recommend 16+ characters. All generation happens locally in your browser.' },
    'timestamp': { name: 'Timestamp Converter', desc: 'Convert Unix timestamps to dates', howto: 'Enter a Unix timestamp (seconds or milliseconds) to convert to a readable date, or pick a date to get its timestamp. Supports timezone switching. Useful for API debugging and log analysis.' },
    'json-formatter': { name: 'JSON Formatter', desc: 'Format, compress & validate JSON', howto: 'Paste JSON into the input box. Click Format to beautify or Compress to minify. Automatically validates JSON syntax and shows errors with location. All processing happens in your browser — data is never uploaded.' },
    'base64': { name: 'Base64 Encoder', desc: 'Encode and decode Base64', howto: 'Enter text and click Encode to get Base64, or paste Base64 and click Decode to restore. Common uses: data transfer, Data URLs, and API authentication. All done locally.' },
    'url-encode': { name: 'URL Encoder', desc: 'URL encoding and decoding', howto: 'Enter text or a URL to encode (special characters → %XX) or decode (restore readable format). Useful for building API requests and processing query parameters.' },
    'word-counter': { name: 'Word Counter', desc: 'Count characters, words & lines', howto: 'Paste or type text to see real-time counts: total characters, words, lines, paragraphs, and Chinese characters. Great for writing, translation, and essays. Data never leaves your browser.' },
    'md5': { name: 'MD5 Hash', desc: 'Calculate MD5 hash values', howto: 'Enter text or upload a file to generate a 32-character MD5 hash. Useful for file integrity checks and data deduplication. Note: MD5 is not secure for passwords — use SHA256 instead.' },
    'uuid-generator': { name: 'UUID Generator', desc: 'Generate random UUID v4', howto: 'Click Generate to get a random UUID v4 (128-bit universally unique identifier). Perfect for database primary keys, distributed system IDs, and file naming. Each generation is unique.' },
    'unicode': { name: 'Unicode Converter', desc: 'Convert between Unicode and Chinese', howto: 'Enter Chinese text to automatically convert to Unicode escape sequences (\\\\uXXXX), or paste Unicode to restore Chinese. Handy for string escaping and JSON encoding in programming.' },
    'case-converter': { name: 'Case Converter', desc: 'UPPER, lower, Title & camelCase', howto: 'Enter text and choose a transformation: UPPERCASE, lowercase, Title Case, Sentence case, camelCase, snake_case, and more. Great for code variable naming and document formatting.' },
    'qr-code': { name: 'QR Code Generator', desc: 'Generate QR codes online', howto: 'Enter a URL or text to instantly generate a QR code. Adjust size and download as PNG. Perfect for sharing links, WiFi passwords, and contact info. Generation is entirely local.' },
    'color-picker': { name: 'Color Picker', desc: 'Pick colors & convert HEX/RGB/HSL', howto: 'Use the color picker to select a color, and instantly see conversions to HEX, RGB, HSL, and other formats. Ideal for designers and frontend developers.' },
    'csv-to-json': { name: 'CSV to JSON', desc: 'Convert CSV data to JSON', howto: 'Paste CSV data or upload a CSV file to automatically convert to JSON array format. Supports custom delimiters and header detection. All conversion happens in your browser.' },
    'sha256': { name: 'SHA256 Hash', desc: 'Calculate SHA256 hash values', howto: 'Enter text or upload a file to generate a 64-character SHA256 hash. SHA256 is far more secure than MD5 — suitable for password storage, digital signatures, and blockchain verification.' },
    'html-entity': { name: 'HTML Entity Encoder', desc: 'Encode and decode HTML entities', howto: 'Enter text and click Encode to convert special characters to HTML entities (e.g., &lt;), or Decode to restore. Useful for web development and XSS prevention.' },
    'ip-lookup': { name: 'IP Lookup', desc: 'Lookup public IP & geolocation', howto: 'Automatically displays your current public IP address. Enter any IP to look up its location (country/city/ISP). Useful for network diagnostics and traffic analysis.' },
    'countdown': { name: 'Countdown Timer', desc: 'Custom date countdown timer', howto: 'Select a target date and time to see the remaining days, hours, minutes, and seconds. Perfect for event countdowns, project deadlines, and birthday reminders.' },
    'regex': { name: 'Regex Tester', desc: 'Test regex patterns with highlighting', howto: 'Enter a regex pattern and test text to see real-time highlighting of matches. Supports flags (g/i/m) and shows capture group info. Great for debugging and learning regex.' },
    'image-compress': { name: 'Image Compressor', desc: 'Compress images in browser', howto: 'Upload PNG, JPEG, or WebP images, adjust compression quality, and download. All processing happens locally — original images are never uploaded to any server, protecting your privacy.' },
    'number-base': { name: 'Number Base Converter', desc: 'Binary, Octal, Decimal & Hex', howto: 'Enter a number in any base to automatically convert to binary, octal, decimal, and hexadecimal. Useful for programming, computer architecture study, and embedded development.' },
    'text-diff': { name: 'Text Diff Checker', desc: 'Compare two texts and find differences', howto: 'Paste two texts into the left and right panels, then click Compare. Differences are highlighted: additions in green, deletions in red. Great for comparing code versions, document revisions, and configuration files.' },
    'lorem-ipsum': { name: 'Lorem Ipsum Generator', desc: 'Generate placeholder text for designs', howto: 'Choose the number of paragraphs, words, or sentences, then click Generate. Lorem Ipsum is the standard placeholder text used in design and typesetting since the 1500s.' },
    'text-sort': { name: 'Text Line Sorter', desc: 'Sort text lines alphabetically', howto: 'Paste your text and choose sort order: ascending (A-Z), descending (Z-A), or random shuffle. Optionally remove duplicate lines. Useful for organizing lists, cleaning data, and alphabetizing references.' },
    'slug-generator': { name: 'URL Slug Generator', desc: 'Convert text to URL-friendly slugs', howto: 'Enter any text and it will be automatically converted to a URL-friendly slug (lowercase, spaces to hyphens, special characters removed). Perfect for blog post URLs, file names, and SEO optimization.' },
    'json-to-csv': { name: 'JSON to CSV Converter', desc: 'Convert JSON data to CSV format', howto: 'Paste a JSON array of objects and click Convert to get CSV output. Handles nested objects by flattening with dot notation. All processing happens locally in your browser.' },
    'markdown-preview': { name: 'Markdown Preview', desc: 'Write and preview Markdown in real time', howto: 'Type or paste Markdown on the left to see a live preview on the right. Supports headings, lists, code blocks, tables, links, images, and more. Great for drafting README files and documentation.' },
    'jwt-decoder': { name: 'JWT Decoder', desc: 'Decode and inspect JWT tokens', howto: 'Paste a JWT token to decode its header and payload. Displays expiration time, issued-at, subject, and all claims. Decoding happens entirely in your browser — the token is never sent to any server.' },
    'css-minifier': { name: 'CSS Minifier', desc: 'Minify CSS to reduce file size', howto: 'Paste your CSS code and click Minify to remove whitespace, comments, and unnecessary characters. Compare original and minified sizes instantly. All processing is local.' },
    'random-string': { name: 'Random String Generator', desc: 'Generate random strings with custom rules', howto: 'Choose character types (uppercase, lowercase, numbers, symbols) and string length, then generate random strings. Useful for API keys, tokens, temporary passwords, and test data.' },
    'percentage-calculator': { name: 'Percentage Calculator', desc: 'Calculate percentages quickly', howto: 'Calculate percentage of a number, find what percent one number is of another, or compute percentage increase/decrease. Three calculators in one simple interface.' },
    'json-validator': { name: 'JSON Validator', desc: 'Validate and format JSON online', howto: 'Paste JSON text and instantly see if it\'s valid. Shows exact error location for invalid JSON. Click Format to beautify. All processing stays in your browser.' },
    'js-minifier': { name: 'JavaScript Minifier', desc: 'Minify JavaScript to reduce file size', howto: 'Paste your JavaScript code and click Minify to remove whitespace, comments, and shorten variable names where safe. Compare original and minified sizes. All local.' },
    'html-minifier': { name: 'HTML Minifier', desc: 'Minify HTML to reduce page size', howto: 'Paste your HTML code and click Minify to remove whitespace and comments. Compare before and after sizes. All processing stays local.' },
    'sql-formatter': { name: 'SQL Formatter', desc: 'Format and beautify SQL queries', howto: 'Paste your SQL query and click Format to add proper indentation and line breaks. Makes complex queries readable. Supports SELECT, INSERT, UPDATE, DELETE, and JOIN clauses.' },
    'url-parser': { name: 'URL Parser', desc: 'Parse and decode URL components', howto: 'Paste any URL to see its components broken down: protocol, hostname, port, path, query parameters, and hash. Each query parameter is shown individually in a table.' },
    'http-status': { name: 'HTTP Status Codes', desc: 'Reference for all HTTP status codes', howto: 'Browse all HTTP status codes organized by category: 1xx Informational, 2xx Success, 3xx Redirection, 4xx Client Error, 5xx Server Error. Search by code number or description.' },
    'color-contrast': { name: 'Color Contrast Checker', desc: 'Check WCAG color contrast ratios', howto: 'Enter foreground and background colors in HEX format to check their contrast ratio. Shows WCAG compliance levels for normal text (AA/AAA) and large text. Essential for accessible web design.' },
    'date-calculator': { name: 'Date Calculator', desc: 'Add or subtract days from a date', howto: 'Pick a date and add or subtract days, weeks, or months. Also calculate the difference between two dates. Perfect for project planning, deadline tracking, and event scheduling.' },
    'stopwatch': { name: 'Online Stopwatch', desc: 'Precise online stopwatch and timer', howto: 'Click Start to begin timing. Use Lap to record split times, Pause to temporarily stop, and Reset to clear. Displays hours, minutes, seconds, and milliseconds. Runs entirely in your browser.' },
    'unit-converter': { name: 'Unit Converter', desc: 'Convert between common units', howto: 'Select a category (Length, Weight, Temperature, Area, Volume, Speed, Time), enter a value, and get instant conversions to all related units. Supports metric and imperial units.' },
    'text-to-binary': { name: 'Text to Binary Converter', desc: 'Convert text to binary representation', howto: 'Enter any text and see its binary representation (8-bit per character). Also converts binary back to text. Great for learning how computers encode characters.' },
    'hex-to-text': { name: 'Hex to Text Converter', desc: 'Convert between hexadecimal and text', howto: 'Enter text to convert to hexadecimal, or paste hex bytes to decode back to text. Each character becomes two hex digits. Useful for debugging, data analysis, and low-level programming.' },
    'list-randomizer': { name: 'List Randomizer', desc: 'Randomize the order of any list', howto: 'Paste a list (one item per line) and click Shuffle to randomize the order. Great for raffles, team assignments, playlist shuffling, and random sampling.' },
    'meta-tag-generator': { name: 'Meta Tag Generator', desc: 'Generate SEO meta tags for web pages', howto: 'Fill in your page title, description, keywords, and author to generate complete HTML meta tags. Includes Open Graph tags for social media and basic SEO tags. Copy and paste into your HTML head.' },
    'text-repeater': { name: 'Text Repeater', desc: 'Repeat text multiple times', howto: 'Enter text and specify how many times to repeat it. Choose a separator (newline, space, comma, or custom). Useful for generating test data and placeholder content.' },
    'bmi-calculator': { name: 'BMI Calculator', desc: 'Calculate your Body Mass Index', howto: 'Enter your height and weight to calculate your BMI. Supports metric (cm/kg) and imperial (ft/in/lbs) units. Shows your BMI category from Underweight to Obese based on WHO standards.' },
    'age-calculator': { name: 'Age Calculator', desc: 'Calculate exact age from birth date', howto: 'Enter your birth date to calculate your exact age in years, months, and days. Also shows total months, weeks, days, hours, and even seconds lived. Fun and useful!' },
    'pomodoro': { name: 'Pomodoro Timer', desc: 'Focus timer using the Pomodoro technique', howto: 'Work for 25 minutes, then take a 5-minute break. After 4 work sessions, take a longer 15-minute break. The Pomodoro Technique helps maintain focus and prevent burnout.' },
    'morse-code': { name: 'Morse Code Translator', desc: 'Convert text to Morse code and back', howto: 'Enter text to convert to Morse code (dots and dashes), or paste Morse code to decode back to text. Includes the full international Morse code alphabet and numbers.' },
    'emoji-picker': { name: 'Emoji Keyboard', desc: 'Browse and copy emoji characters', howto: 'Browse emojis by category: Smileys, People, Animals, Food, Activities, Travel, Objects, Symbols. Click any emoji to copy it to clipboard. Use the search to find emojis by name.' },
    'rot13': { name: 'ROT13 Cipher', desc: 'Encode and decode text with ROT13 cipher', howto: 'Enter text and click Encode/Decode. ROT13 works both ways since applying it twice restores the original text. All processing happens locally in your browser.' },
    'ascii-table': { name: 'ASCII Table', desc: 'Complete ASCII character reference table', howto: 'Browse the full ASCII table (characters 0-127) showing decimal, hex, octal, and character representations. Use the search to filter by code, character, or description. All content loads instantly.' },
    'sha1': { name: 'SHA1 Hash Generator', desc: 'Generate SHA1 hash values from text', howto: 'Enter text and click Generate SHA1 to create a 40-character hexadecimal hash. SHA1 is cryptographically broken for security but still useful for checksums. All hashing happens locally.' },
    'sha512': { name: 'SHA512 Hash Generator', desc: 'Generate SHA512 hash values from text', howto: 'Enter text and click Generate SHA512 to create a 128-character hash. SHA512 is the strongest in the SHA-2 family. All processing stays in your browser.' },
    'crc32': { name: 'CRC32 Checksum', desc: 'Calculate CRC32 checksum for text', howto: 'Enter any text and click Calculate to get the 8-character hex CRC32 checksum. CRC32 is fast and ideal for integrity checking in network protocols and file formats. Computed entirely in your browser.' },
    'text-reverse': { name: 'Text Reverser', desc: 'Reverse any text string instantly', howto: 'Enter text to see it reversed character by character in real time. Use Copy to grab the result. All processing happens locally.' },
    'duplicate-remover': { name: 'Duplicate Line Remover', desc: 'Remove duplicate lines from text', howto: 'Paste your text and click Remove Duplicates. The deduplicated result, original line count, unique count, and removed count are shown. All processing is local.' },
    'levenshtein-distance': { name: 'Levenshtein Distance', desc: 'Calculate string similarity using Levenshtein distance', howto: 'Enter two strings and click Calculate Distance to see the edit distance (insertions, deletions, substitutions) and similarity percentage. All computation happens in your browser.' },
    'bytes-converter': { name: 'Bytes Converter', desc: 'Convert between bytes, KB, MB, GB, and TB', howto: 'Enter a value and select the unit to see instant conversions to all five digital storage units. Uses the binary standard (1 KB = 1024 bytes). All conversions are computed locally.' },
    'roman-numerals': { name: 'Roman Numerals Converter', desc: 'Convert between Roman numerals and numbers', howto: 'Toggle between Number to Roman and Roman to Number modes. Enter your input and see the instant conversion. Supports numbers 1-3999.' },
    'timezone-converter': { name: 'Timezone Converter', desc: 'Convert time between different timezones', howto: 'Set a date/time, choose source and target timezones, and click Convert. See the converted time instantly. Supports major timezones worldwide with automatic DST handling.' },
    'cron-parser': { name: 'Cron Expression Parser', desc: 'Parse and explain cron schedule expressions', howto: 'Enter a 5-field cron expression and click Parse to see what each field means in plain English. Also shows the next 5 execution times. All parsing happens locally.' },
    'day-of-week': { name: 'Day of Week Finder', desc: 'Find what day of the week any date falls on', howto: 'Pick any date to instantly see what day of the week it falls on, its day number within the year, and current week number. All calculations happen in your browser.' },
    'sleep-calculator': { name: 'Sleep Cycle Calculator', desc: 'Calculate optimal sleep and wake times based on sleep cycles', howto: 'Choose "I want to wake up at..." for ideal bedtimes or "Im going to bed at..." for optimal wake times. Based on 90-minute sleep cycles. All computed locally.' },
    'xml-to-json': { name: 'XML to JSON Converter', desc: 'Convert XML data to JSON format', howto: 'Paste your XML and click Convert to JSON. Attributes are prefixed with @ for easy identification. All conversion happens in your browser.' },
    'json-to-xml': { name: 'JSON to XML Converter', desc: 'Convert JSON data to XML format', howto: 'Paste valid JSON and click Convert to XML to get properly formatted XML output. All conversion happens locally.' },
    'xml-formatter': { name: 'XML Formatter', desc: 'Format and beautify XML code', howto: 'Paste messy or minified XML code and click Format XML to add proper indentation and line breaks. All formatting happens in your browser.' },
    'css-beautifier': { name: 'CSS Beautifier', desc: 'Beautify and format CSS code', howto: 'Paste compressed or messy CSS code and click Beautify CSS to add proper indentation and spacing. All processing is local.' },
    'html-beautifier': { name: 'HTML Beautifier', desc: 'Beautify and format HTML code', howto: 'Paste minified or messy HTML code and click Beautify HTML to add consistent indentation and line breaks. Recognizes void elements. All local.' },
    'js-beautifier': { name: 'JavaScript Beautifier', desc: 'Beautify and format JavaScript/TypeScript code', howto: 'Paste compressed JavaScript code and click Beautify JS to add proper indentation and formatting while preserving strings and comments. All processing stays in your browser.' },
    'user-agent-parser': { name: 'User Agent Parser', desc: 'Parse and decode browser user agent strings', howto: 'Paste a user agent string or click Load My UA to see your browser, operating system, device type, and rendering engine. All parsing happens locally.' },
    'mime-lookup': { name: 'MIME Type Lookup', desc: 'Look up MIME types by file extension or type', howto: 'Browse the reference table or search by file extension, MIME type, or description. Find the correct Content-Type for any file format. All data loads instantly.' },
    'yaml-to-json': { name: 'YAML to JSON Converter', desc: 'Convert YAML data to JSON format', howto: 'Paste YAML and click Convert to JSON. Supports nested objects, arrays, booleans, and numbers. All conversion happens locally in your browser.' },
    'json-to-yaml': { name: 'JSON to YAML Converter', desc: 'Convert JSON data to YAML format', howto: 'Paste valid JSON and click Convert to YAML to get clean, indented YAML output. All conversion happens in your browser.' },
    'http-headers-checker': { name: 'HTTP Headers Reference', desc: 'Reference for common HTTP request and response headers', howto: 'Browse the full reference of HTTP headers organized by type (Request, Response, General, Entity). Search by header name or description. All content loads instantly.' },
    'dns-lookup': { name: 'DNS Lookup', desc: 'Perform DNS record lookups for any domain', howto: 'Enter a domain name, select a record type (A, AAAA, MX, CNAME, etc.), and click Lookup. Queries performed via Google DNS over HTTPS from your browser.' },
    'port-checker': { name: 'Port Reference', desc: 'Common TCP/UDP network port numbers reference', howto: 'Browse the complete port reference table or search by port number, service name, or description. Covers well-known ports from 20-50000.' },
    'git-cheatsheet': { name: 'Git Cheatsheet', desc: 'Quick reference for common Git commands', howto: 'Browse all 46 commonly used Git commands organized by workflow. Search by command name or description to find the exact command you need. All content loads instantly.' },
    'hash-compare': { name: 'Hash Compare', desc: 'Compare two hash values side by side', howto: 'Paste the expected and actual hash values into the two fields. The tool instantly shows if they match and whether file integrity is verified. All processing is local.' },
    'gradient-generator': { name: 'CSS Gradient Generator', desc: 'Create and preview CSS linear gradients', howto: 'Pick two colors and adjust the angle. The live preview updates in real time. Copy the CSS code and paste it into your stylesheet. All processing is local.' },
    'random-number': { name: 'Random Number Generator', desc: 'Generate random numbers within a range', howto: 'Set your minimum and maximum values, choose how many numbers to generate, and click Generate. Numbers are displayed with one-click copy. All generation happens locally.' },
    'random-color': { name: 'Random Color Generator', desc: 'Generate random colors with HEX codes', howto: 'Click Generate to create new random color swatches with their HEX codes. Click any color swatch to copy its code to clipboard. All generation is local.' },
    'dice-roller': { name: 'Dice Roller', desc: 'Roll virtual dice for games and RPGs', howto: 'Click any die button (d4 through d100) to roll. Results highlight green for max rolls and red for rolls of 1. The last 20 rolls are shown in history. All local.' },
    'nano-id': { name: 'Nano ID Generator', desc: 'Generate compact, URL-friendly unique IDs', howto: 'Choose a length and count, then click Generate to create URL-friendly unique IDs. Click Copy on any ID to copy it to clipboard. All generation is local.' },
    'password-strength': { name: 'Password Strength Checker', desc: 'Check how strong your password is', howto: 'Type any password to see its strength rating (Weak to Very Strong), entropy in bits, and which character types are present. All analysis happens locally in your browser.' },
    'entropy-calculator': { name: 'Entropy Calculator', desc: 'Calculate Shannon entropy of text', howto: 'Enter any text to see its Shannon entropy in bits per character, randomness level, unique character count, and efficiency. All computation happens locally.' },
    'box-shadow': { name: 'Box Shadow Generator', desc: 'Create CSS box-shadow effects visually', howto: 'Adjust offset, blur, spread, color, and opacity sliders. The live preview updates in real time. Supports inset shadows. Copy the generated CSS instantly.' },
    'border-radius': { name: 'Border Radius Previewer', desc: 'Visualize and generate CSS border-radius values', howto: 'Adjust each corner radius independently or use presets (Sharp, 8px, 16px, Pill). The live preview shows your design. Copy the CSS when satisfied.' },
    'image-to-base64': { name: 'Image to Base64', desc: 'Convert images to Base64 data URLs', howto: 'Upload any image to instantly generate a Base64 data URL. Preview the image, copy the data URL, or download as a standalone HTML file. All conversion happens locally.' },
    'favicon-generator': { name: 'Favicon Generator', desc: 'Generate favicon HTML tags for your website', howto: 'Enter an image URL or upload a file. Copy the complete set of favicon HTML tags (traditional, modern PNG, Apple touch icon) into your websites head section.' },
    'svg-viewer': { name: 'SVG Viewer', desc: 'Paste SVG code for live preview', howto: 'Paste any SVG code into the editor to see a live preview on the right side. Copy or download the SVG when ready. All rendering happens in your browser.' },
    'tip-calculator': { name: 'Tip Calculator', desc: 'Calculate tips and split bills easily', howto: 'Enter the bill amount, choose a tip percentage (10%-25% or custom), and set the number of people. See the tip amount, total bill, and per-person split instantly.' },
    'factorial': { name: 'Factorial Calculator', desc: 'Calculate factorials (n!) for large numbers', howto: 'Enter a number (0-1000) and click Calculate n! to see the full factorial result with digit count. Uses arbitrary-precision arithmetic for exact results. All local.' },
    'fraction-calculator': { name: 'Fraction Calculator', desc: 'Add, subtract, multiply, and divide fractions', howto: 'Enter two fractions and click an operator (+, −, ×, ÷). The result is simplified automatically and shown as both a mixed number and decimal. All computation happens locally.' },
    'mean-median-mode': { name: 'Mean, Median, Mode Calculator', desc: 'Calculate statistical measures from a set of numbers', howto: 'Enter numbers separated by commas, spaces, or newlines and click Calculate to see count, mean, median, mode, and range instantly. All computation happens in your browser.' },
    'extract-emails': { name: 'Email Extractor', desc: 'Extract email addresses from any text', howto: 'Paste any text containing email addresses and click Extract Emails. Shows total matches and unique addresses. Copy all results in one click. All processing is local.' },
    'extract-urls': { name: 'URL Extractor', desc: 'Extract URLs and links from any text', howto: 'Paste any text containing URLs and click Extract URLs. Shows total matches and unique links. Copy all results in one click. All processing happens in your browser.' },
    'css-triangle': { name: 'CSS Triangle Generator', desc: 'Generate pure CSS triangles for tooltips and UI', howto: 'Adjust width, height, color, and direction (up/down/left/right). See the live preview and copy the generated pure-CSS triangle code. All processing is local.' },
    'hmac-generator': { name: 'HMAC Generator', desc: 'Generate HMAC signatures with SHA256', howto: 'Enter a secret key and message, then click Generate HMAC-SHA256 to create a hex-encoded signature. Useful for API authentication and message verification. All computation happens locally.' },
    'bcrypt-checker': { name: 'Bcrypt Checker', desc: 'Hash passwords with bcrypt and verify hashes', howto: 'Enter a password to generate a secure salted hash using PBKDF2-SHA512 with 200,000 iterations (comparable to bcrypt cost 12). The output includes algorithm, iterations, salt, and hash. All processing is local.' },
  };

  // Header
  en.header = { allTools: 'All Tools', about: 'About', blog: 'Blog' };
  
  // Footer
  en.footer = { 
    about: 'About',
    contact: 'Contact',
    privacy: 'Privacy Policy',
    blog: 'Blog',
    copyright: '© 2026 4uses.com · All rights reserved',
    tagline: 'All tools free to use · No registration · No data uploaded',
    tools: 'Tools',
    categories: 'Categories',
    company: 'Company',
    description: '100+ free online utilities for everyday tasks. No sign-up, no limits, fully private in your browser.',
  };
  
  // Home
  en.home = {
    hero: 'Online Toolbox',
    desc: 'Free online tools: JSON Formatter, Base64 Encoder, Timestamp Converter, UUID Generator, QR Code Generator and 100+ more utilities. No registration required.',
    heroBadge: '100+ free utilities, always growing',
    heroSubtitle: '100+ free utilities — no sign-up, no limits. Encode, format, convert and generate, all in your browser.',
    exploreTools: 'Explore Tools',
    popularTools: 'Popular Tools',
    searchPlaceholder: 'Search for a tool...',
    allCategory: 'All',
    allToolsHeading: 'All Tools',
    noToolsFound: 'No tools found for',
    mostPopular: 'Most Popular',
    popularDesc: 'The tools our users reach for the most.',
    useNow: 'Use Now',
    trustedWorldwide: 'Trusted by developers worldwide',
    monthlyUsers: 'Monthly Users',
    toolsAvailable: 'Tools Available',
    averageRating: 'Average Rating',
    tools: 'Tools',
    free: 'Free',
    registration: 'No Registration',
  };

  // Privacy Policy
  en.privacy = {
    title: 'Privacy Policy',
    lastUpdated: 'Last updated: May 30, 2026',
    overview: {
      title: '1. Overview',
      text: '4uses.com ("we", "our", or "us") is committed to protecting your privacy. All tools on this website run locally in your browser — we do not upload, store, or process your data on any server.'
    },
    data: {
      title: '2. Data We Collect',
      text: 'We do not require registration and do not collect personal information. Your usage data (files, text, images) stays in your browser and is never transmitted to our servers.'
    },
    cookies: {
      title: '3. Cookies & Advertising',
      text: 'We use Google AdSense to display advertisements. Google and its partners use cookies to serve ads based on your prior visits to this site and other websites.',
      optout: 'You may opt out of personalized advertising by visiting Google Ads Settings. We also use Google\'s CMP (Consent Management Platform) to obtain your consent for cookies in accordance with GDPR.'
    },
    thirdParty: {
      title: '4. Third-Party Services',
      text: 'We use the following third-party services that may collect information:',
      adsense: 'Google AdSense — advertising network (privacy policy at policies.google.com)',
      analytics: 'Google Analytics — anonymous traffic analysis (if enabled)'
    },
    rights: {
      title: '5. Your Rights (GDPR)',
      text: 'If you are in the European Economic Area (EEA), the UK, or Switzerland, you have the right to access, correct, or delete your personal data. Since we do not collect personal data, these rights are inherently upheld. For questions, please contact us.'
    },
    contact: {
      title: '6. Contact',
      text: 'If you have questions about this Privacy Policy, please visit our Contact page.'
    }
  };

  // About
  en.about = {
    title: 'About 4uses',
    what: {
      title: 'What is 4uses?',
      text: '4uses.com is a collection of free, browser-based online tools. From JSON formatting to image compression, hash calculation to QR code generation — all tools work directly in your browser with no registration, no uploads, and no limits.'
    },
    why: {
      title: 'Why "4uses"?',
      text: 'The name stands for "for uses" — tools for every use case you encounter in daily work and life. Our goal is to provide simple, fast, privacy-respecting utilities that just work.'
    },
    privacy: {
      title: 'Our Philosophy',
      text: 'We believe online tools should respect your privacy. Every tool on 4uses runs entirely in your browser using client-side JavaScript. Your files and data never leave your device. No accounts, no tracking beyond basic analytics, no nonsense.'
    },
    contact: {
      title: 'Get in Touch',
      text: 'Have a suggestion or found a bug? We\'d love to hear from you! Visit our Contact page to get in touch.'
    }
  };

  // Contact
  en.contact = {
    title: 'Contact Us',
    reach: {
      title: 'Reach Out',
      text: 'We welcome your feedback, suggestions, and bug reports. Whether you\'ve found an issue with a tool, have an idea for a new one, or just want to say hello — we\'d love to hear from you.'
    },
    email: {
      title: 'Email',
      label: 'Email us at:'
    },
    response: {
      title: 'Response Time',
      text: 'We strive to respond to all messages within 24-48 hours. For urgent matters, please include "[Urgent]" in your subject line.'
    }
  };

  return en;
}

const en = buildEn();

// Deep get: "site.name" -> "Online Toolbox"
function deepGet(obj, path) {
  return path.split('.').reduce((o, k) => (o || {})[k], obj) || '';
}

export { en, zh, deepGet };
