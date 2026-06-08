// Client-side i18n utilities
// Injects translations into window.__I18N__ and provides lookup helpers

import zh from './zh.json';

// Build English translations by inverting zh structure (keys are the EN values)
function buildEn() {
  const en = JSON.parse(JSON.stringify(zh)); // deep copy structure
  
  // Site
  en.site.name = 'Online Toolbox';
  en.site.tagline = 'All free · No registration · No data uploaded';
  en.site.subtitle = '20+ useful tools, continuously updated';

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
  };

  // Header
  en.header = { allTools: 'All Tools', about: 'About' };
  
  // Footer
  en.footer = { 
    about: 'About',
    contact: 'Contact',
    privacy: 'Privacy Policy',
    copyright: '© 2026 4uses.com · All free, no registration',
    tagline: 'All tools free to use · No registration · No data uploaded'
  };
  
  // Home
  en.home = {
    hero: 'Online Toolbox',
    desc: 'Free online tools: JSON Formatter, Base64 Encoder, Timestamp Converter, UUID Generator, QR Code Generator and 20+ more utilities. No registration required.'
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
