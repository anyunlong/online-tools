#!/usr/bin/env python3
"""Replace placeholder JS in all new tool pages with real implementations."""
import json, os, re, sys

PROJECT = os.path.expanduser("~/projects/online-tools")
PAGES = os.path.join(PROJECT, "src/pages")

# Load tool definitions
with open(os.path.join(PROJECT, "src/data/tools.json")) as f:
    all_tools = {t['id']: t for t in json.load(f)}

# Load the JS definitions from the embedded dict below
exec(open(__file__).read().split("# ===JS_START===")[1].split("# ===JS_END===")[0])

updated = 0
skipped = 0
for tool_id, js_code in TOOL_JS.items():
    path = os.path.join(PAGES, f"{tool_id}.astro")
    if not os.path.exists(path):
        print(f"  ⚠️ {tool_id}: file not found")
        skipped += 1
        continue
    
    with open(path) as f:
        content = f.read()
    
    # Find the script section and replace the JS logic
    # Pattern: <script is:inline>\n  ... placeholder JS ... \nfunction clearAll/copyResult
    # We need to replace everything between <script is:inline> and function clearAll/copyResult
    
    # Escape backticks and dollar signs for the replacement
    escaped_js = js_code.replace('\\', '\\\\').replace('`', '\\`')
    
    # Try to find and replace the function body
    if 'function process()' in content:
        # Replace process function
        old_start = content.find('function process()')
        # Find the closing brace of process function
        # Look for clearAll or copyResult after it
        next_fn = content.find('function clearAll', old_start)
        if next_fn < 0:
            next_fn = content.find('function copyResult', old_start)
        if next_fn > old_start:
            new_content = content[:old_start] + js_code + '\n' + content[next_fn:]
            with open(path, 'w') as f:
                f.write(new_content)
            updated += 1
        else:
            print(f"  ⚠️ {tool_id}: could not find clearAll/copyResult")
            skipped += 1
    elif 'function generate()' in content:
        old_start = content.find('function generate()')
        next_fn = content.find('function copyResult', old_start)
        if next_fn > old_start:
            new_content = content[:old_start] + js_code + '\n' + content[next_fn:]
            with open(path, 'w') as f:
                f.write(new_content)
            updated += 1
        else:
            print(f"  ⚠️ {tool_id}: could not find copyResult after generate")
            skipped += 1
    else:
        print(f"  ⚠️ {tool_id}: no process/generate function found")
        skipped += 1

print(f"\n✅ Updated: {updated}")
print(f"⚠️ Skipped: {skipped}")
