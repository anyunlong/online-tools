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
    'password-generator': { name: 'Password Generator', desc: 'Generate strong random passwords' },
    'timestamp': { name: 'Timestamp Converter', desc: 'Convert Unix timestamps to dates' },
    'json-formatter': { name: 'JSON Formatter', desc: 'Format, compress & validate JSON' },
    'base64': { name: 'Base64 Encoder', desc: 'Encode and decode Base64' },
    'url-encode': { name: 'URL Encoder', desc: 'URL encoding and decoding' },
    'word-counter': { name: 'Word Counter', desc: 'Count characters, words & lines' },
    'md5': { name: 'MD5 Hash', desc: 'Calculate MD5 hash values' },
    'uuid-generator': { name: 'UUID Generator', desc: 'Generate random UUID v4' },
    'unicode': { name: 'Unicode Converter', desc: 'Convert between Unicode and Chinese' },
    'case-converter': { name: 'Case Converter', desc: 'UPPER, lower, Title & camelCase' },
    'qr-code': { name: 'QR Code Generator', desc: 'Generate QR codes online' },
    'color-picker': { name: 'Color Picker', desc: 'Pick colors & convert HEX/RGB/HSL' },
    'csv-to-json': { name: 'CSV to JSON', desc: 'Convert CSV data to JSON' },
    'sha256': { name: 'SHA256 Hash', desc: 'Calculate SHA256 hash values' },
    'html-entity': { name: 'HTML Entity Encoder', desc: 'Encode and decode HTML entities' },
    'ip-lookup': { name: 'IP Lookup', desc: 'Lookup public IP & geolocation' },
    'countdown': { name: 'Countdown Timer', desc: 'Custom date countdown timer' },
    'regex': { name: 'Regex Tester', desc: 'Test regex patterns with highlighting' },
    'image-compress': { name: 'Image Compressor', desc: 'Compress images in browser' },
    'number-base': { name: 'Number Base Converter', desc: 'Binary, Octal, Decimal & Hex' }
  };

  // Header
  en.header = { allTools: 'All Tools', about: 'About' };
  
  // Footer
  en.footer = { 
    copyright: '© 2026 4uses.com · All free, no registration',
    tagline: 'All tools free to use · No registration · No data uploaded',
    privacy: 'All computation runs locally in your browser, keeping your data secure'
  };
  
  // Home
  en.home = {
    hero: 'Online Toolbox',
    desc: 'Free online tools: JSON Formatter, Base64 Encoder, Timestamp Converter, UUID Generator, QR Code Generator and 20+ more utilities. No registration required.'
  };

  return en;
}

const en = buildEn();

// Deep get: "site.name" -> "Online Toolbox"
function deepGet(obj, path) {
  return path.split('.').reduce((o, k) => (o || {})[k], obj) || '';
}

export { en, zh, deepGet };
