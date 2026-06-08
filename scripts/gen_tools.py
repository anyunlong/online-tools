#!/usr/bin/env python3
"""Batch tool generator for 4uses.com
Generates Astro pages, updates tools.json, zh.json, utils.js for new tools.
"""

import json, sys, os

PROJECT = os.path.expanduser("~/projects/online-tools")
PAGES = os.path.join(PROJECT, "src/pages")
TOOLS_JSON = os.path.join(PROJECT, "src/data/tools.json")
ZH_JSON = os.path.join(PROJECT, "src/i18n/zh.json")
UTILS_JS = os.path.join(PROJECT, "src/i18n/utils.js")

# ── Tool templates ──────────────────────────────────────────

TEMPLATE_PROCESSOR = '''---
import ToolLayout from '../components/ToolLayout.astro';
import Textarea from '../components/Textarea.astro';
import Button from '../components/Button.astro';
---

<ToolLayout
  title="{title_en}"
  description="{desc_en}"
  category="{category}"
  keywords={keywords}
>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
    <Textarea id="inp" label="Input" placeholder="{placeholder}" rows="12" class="tool-area" />
    <div>
      <label for="out" class="text-sm text-surface-300 mb-1.5 block font-medium">Output</label>
      <div id="out" class="w-full h-72 rounded-xl border border-surface-700 bg-surface-800/50 p-3 text-xs text-surface-100 overflow-auto font-mono"></div>
    </div>
  </div>
  <div class="flex gap-2 mt-4">
    <Button onclick="process()">{button_label}</Button>
    <Button variant="secondary" onclick="clearAll()">Clear</Button>
  </div>
  <div id="msg" class="text-xs mt-2 text-surface-400"></div>
<script is:inline>
{js_logic}
function clearAll() {
  document.getElementById('inp').value = '';
  document.getElementById('out').innerHTML = '';
  document.getElementById('msg').textContent = '';
}
</script>
<slot name="info" slot="info">
  <p>{howto_en}</p>
</slot>
</ToolLayout>
'''

TEMPLATE_GENERATOR = '''---
import ToolLayout from '../components/ToolLayout.astro';
import Button from '../components/Button.astro';
---

<ToolLayout
  title="{title_en}"
  description="{desc_en}"
  category="{category}"
  keywords={keywords}
>
  <div class="space-y-4">
    {config_html}
    <div class="flex gap-2">
      <Button onclick="generate()">{button_label}</Button>
      <Button variant="secondary" onclick="copyResult()">Copy</Button>
    </div>
    <div id="result" class="w-full min-h-[80px] rounded-xl border border-surface-700 bg-surface-800/50 p-4 text-sm text-surface-100 font-mono break-all"></div>
  </div>
<script is:inline>
{js_logic}
function copyResult() {
  const text = document.getElementById('result').textContent;
  if (!text) return;
  navigator.clipboard.writeText(text).then(() => {
    const btn = document.querySelector('[onclick="copyResult()"]');
    btn.textContent = 'Copied!';
    setTimeout(() => btn.textContent = 'Copy', 2000);
  });
}
</script>
<slot name="info" slot="info">
  <p>{howto_en}</p>
</slot>
</ToolLayout>
'''

# ── Helpers ──────────────────────────────────────────────────

def js_escape(s):
    """Escape a string for use in a JS single-quoted string."""
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')

# ── File loaders / savers ────────────────────────────────────

def load_json(path):
    with open(path) as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  ✓ {os.path.basename(path)}")

def read_file(path):
    with open(path) as f:
        return f.read()

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f"  ✓ {path}")

# ── Generator ───────────────────────────────────────────────

def add_tools(tools: list[dict]):
    """Add tools. Each tool dict:
    {
        "id": "tool-id",
        "name_en": "Tool Name",
        "desc_en": "Short description",
        "name_zh": "工具名",
        "desc_zh": "简短描述",
        "howto_en": "How to use...",
        "howto_zh": "使用方法...",
        "cat": "Category",
        "keywords": ["kw1", "kw2"],
        "type": "processor" | "generator",
        "js": "function process() { ... }",
        "placeholder": "Enter text...",
        "button_label": "Process",
        "config_html": "<div>...</div>"  # for generator type
    }
    """
    # 1. Update tools.json
    tools_data = load_json(TOOLS_JSON)
    existing_ids = {t['id'] for t in tools_data}
    for t in tools:
        if t['id'] not in existing_ids:
            tools_data.append({
                "id": t['id'],
                "name": t['name_en'],
                "desc": t['desc_en'],
                "cat": t['cat']
            })
    save_json(TOOLS_JSON, tools_data)

    # 2. Update zh.json
    zh = load_json(ZH_JSON)
    for t in tools:
        zh['tools'][t['id']] = {
            "name": t['name_zh'],
            "desc": t['desc_zh'],
            "howto": t['howto_zh']
        }
    save_json(ZH_JSON, zh)

    # 3. Update utils.js - add English howto for new tools
    utils = read_file(UTILS_JS)
    
    for t in tools:
        tid = t['id']
        howto_en = js_escape(t['howto_en'])
        name_safe = js_escape(t['name_en'])
        desc_safe = js_escape(t['desc_en'])
        marker = f"'{tid}': {{"
        idx = utils.find(marker)
        if idx != -1:
            # Existing entry: add howto if missing
            if 'howto:' not in utils[idx:idx+200]:
                close = utils.index('}', idx + len(marker) + 50)
                utils = utils[:close] + f", howto: '{howto_en}' " + utils[close:]
        else:
            # New entry: insert before closing of tools object
            insert_point = utils.find("  };\n\n  // Header")
            if insert_point != -1:
                # Check if previous line needs a comma
                before = utils[:insert_point].rstrip()
                if not before.endswith(','):
                    # Add comma after last entry
                    last_brace = before.rfind('}')
                    if last_brace != -1:
                        utils = utils[:last_brace+1] + ',' + utils[last_brace+1:]
                        insert_point += 1  # account for added comma
                entry = f"    '{tid}': {{ name: '{name_safe}', desc: '{desc_safe}', howto: '{howto_en}' }},\n"
                utils = utils[:insert_point] + entry + utils[insert_point:]
    
    write_file(UTILS_JS, utils)

    # 4. Generate page files
    for t in tools:
        fname = f"{t['id']}.astro"
        path = os.path.join(PAGES, fname)
        
        if os.path.exists(path):
            print(f"  ⚠ {fname} already exists, skipping")
            continue

        keywords = json.dumps(t.get('keywords', []))
        
        if t['type'] == 'generator':
            html = TEMPLATE_GENERATOR
            html = html.replace('{title_en}', t['name_en'])
            html = html.replace('{desc_en}', t['desc_en'])
            html = html.replace('{category}', t['cat'])
            html = html.replace('{keywords}', '{' + keywords + '}')
            html = html.replace('{config_html}', t.get('config_html', ''))
            html = html.replace('{button_label}', t.get('button_label', 'Generate'))
            html = html.replace('{js_logic}', t['js'])
            html = html.replace('{howto_en}', t['howto_en'])
        else:
            html = TEMPLATE_PROCESSOR
            html = html.replace('{title_en}', t['name_en'])
            html = html.replace('{desc_en}', t['desc_en'])
            html = html.replace('{category}', t['cat'])
            html = html.replace('{keywords}', '{' + keywords + '}')
            html = html.replace('{placeholder}', t.get('placeholder', 'Enter text...'))
            html = html.replace('{button_label}', t.get('button_label', 'Process'))
            html = html.replace('{js_logic}', t['js'])
            html = html.replace('{howto_en}', t['howto_en'])
        write_file(path, html)
    
    print(f"\n✅ Added {len(tools)} tools")

# ── Main ─────────────────────────────────────────────────────

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 gen_tools.py <tools.json>")
        print("  tools.json: array of tool definitions")
        sys.exit(1)
    
    with open(sys.argv[1]) as f:
        tools = json.load(f)
    add_tools(tools)
