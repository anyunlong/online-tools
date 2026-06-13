#!/usr/bin/env python3
"""Generate tool info (What/When/How/Related) for all 200 tools, EN + ZH."""
import json

TOOLS_PATH = "src/data/tools.json"
OUT_EN = "src/data/tool-info-en.json"
OUT_ZH = "src/data/tool-info-zh.json"

# ── Related tool pairings (tool_id → related_tool_id) ──
RELATED = {
    "password-generator": ("random-string", "Random String Generator"),
    "timestamp": ("countdown", "Countdown Timer"),
    "json-formatter": ("json-validator", "JSON Validator"),
    "base64": ("url-encode", "URL Encoder"),
    "url-encode": ("base64", "Base64 Encoder"),
    "word-counter": ("character-frequency", "Character Frequency Counter"),
    "md5": ("sha256", "SHA256 Hash"),
    "uuid-generator": ("random-string", "Random String Generator"),
    "unicode": ("utf8-encoder", "UTF-8 Encoder"),
    "case-converter": ("text-sort", "Text Line Sorter"),
    "qr-code": ("barcode-generator", "Barcode Generator"),
    "color-picker": ("color-palette", "Color Palette Generator"),
    "csv-to-json": ("json-to-csv", "JSON to CSV Converter"),
    "sha256": ("sha384", "SHA-384 Hash"),
    "html-entity": ("url-encode", "URL Encoder"),
    "ip-lookup": ("dns-lookup", "DNS Lookup"),
    "countdown": ("days-until", "Days Until Calculator"),
    "regex": ("text-diff", "Text Diff Checker"),
    "image-compress": ("image-resizer", "Image Resizer"),
    "number-base": ("binary-to-decimal", "Binary to Decimal"),
    "text-diff": ("json-diff", "JSON Diff Checker"),
    "lorem-ipsum": ("random-string", "Random String Generator"),
    "text-sort": ("case-converter", "Case Converter"),
    "slug-generator": ("text-to-slug", "URL Slug Generator"),
    "json-to-csv": ("csv-to-json", "CSV to JSON"),
    "markdown-preview": ("markdown-to-html", "Markdown to HTML"),
    "jwt-decoder": ("base64", "Base64 Encoder"),
    "css-minifier": ("js-minifier", "JavaScript Minifier"),
    "random-string": ("password-generator", "Password Generator"),
    "percentage-calculator": ("discount-calculator", "Discount Calculator"),
    "json-validator": ("json-formatter", "JSON Formatter"),
    "js-minifier": ("css-minifier", "CSS Minifier"),
    "html-minifier": ("css-minifier", "CSS Minifier"),
    "sql-formatter": ("json-formatter", "JSON Formatter"),
    "url-parser": ("url-encode", "URL Encoder"),
    "http-status": ("http-status-dog", "HTTP Status Code Reference"),
    "color-contrast": ("color-blind", "Color Blindness Simulator"),
    "date-calculator": ("days-until", "Days Until Calculator"),
    "stopwatch": ("countdown", "Countdown Timer"),
    "unit-converter": ("temperature-converter", "Temperature Converter"),
    "text-to-binary": ("binary-to-decimal", "Binary to Decimal"),
    "hex-to-text": ("hex-to-decimal", "Hex to Decimal"),
    "list-randomizer": ("team-generator", "Random Team Generator"),
    "meta-tag-generator": ("serp-preview", "Google SERP Preview"),
    "text-repeater": ("lorem-ipsum", "Lorem Ipsum Generator"),
    "bmi-calculator": ("ideal-weight", "Ideal Weight Calculator"),
    "age-calculator": ("days-until", "Days Until Calculator"),
    "pomodoro": ("countdown", "Countdown Timer"),
    "morse-code": ("base64", "Base64 Encoder"),
    "hash-compare": ("text-diff", "Text Diff Checker"),
    "gradient-generator": ("gradient-preview", "CSS Gradient Preview"),
    "random-number": ("coin-flip", "Coin Flip Simulator"),
    "random-color": ("hex-color-gen", "Random HEX Color Gen"),
    "dice-roller": ("coin-flip", "Coin Flip Simulator"),
    "nano-id": ("uuid-generator", "UUID Generator"),
    "password-strength": ("password-generator", "Password Generator"),
    "entropy-calculator": ("password-strength", "Password Strength"),
    "box-shadow": ("border-radius", "Border Radius Previewer"),
    "border-radius": ("box-shadow", "Box Shadow Generator"),
    "image-to-base64": ("base64", "Base64 Encoder"),
    "favicon-generator": ("meta-tag-generator", "Meta Tag Generator"),
    "svg-viewer": ("qr-code", "QR Code Generator"),
    "tip-calculator": ("split-bill", "Split Bill Calculator"),
    "factorial": ("exponent-calculator", "Exponent Calculator"),
    "fraction-calculator": ("percentage-calculator", "Percentage Calculator"),
    "mean-median-mode": ("percentage-calculator", "Percentage Calculator"),
    "extract-emails": ("extract-urls", "URL Extractor"),
    "extract-urls": ("extract-emails", "Email Extractor"),
    "css-triangle": ("css-specificity", "CSS Specificity Calculator"),
    "hmac-generator": ("sha256", "SHA256 Hash"),
    "bcrypt-checker": ("password-generator", "Password Generator"),
}
# Add reverse mappings
for tid, (rid, rname) in list(RELATED.items()):
    if rid not in RELATED:
        # Find original name
        pass  # already handled

def info_en(tool):
    """Generate English info content."""
    name = tool["name"]
    tid = tool["id"]
    cat = tool["cat"]
    desc = tool["desc"]
    
    what = f"{name} is a free online tool that helps you {desc.lower()}. It runs entirely in your browser using client-side JavaScript, so your data stays private and never leaves your device."
    
    when_map = {
        "Security": [
            f"Generating secure credentials, keys, or hashes for your applications",
            f"Checking or verifying security configurations and encryption settings",
            f"Learning about cryptographic concepts and security best practices",
        ],
        "Time": [
            f"Converting between timezones when scheduling international meetings",
            f"Calculating deadlines, durations, and countdowns for project planning",
            f"Figuring out date differences for travel, billing, or event planning",
        ],
        "Formatter": [
            f"Making minified code or data readable for debugging and review",
            f"Validating syntax and catching formatting errors before deployment",
            f"Preparing clean, consistently styled code for documentation or sharing",
        ],
        "Encode/Decode": [
            f"Preparing data for transmission in URLs, APIs, or emails",
            f"Converting between number bases when programming or debugging",
            f"Encoding special characters for safe storage in databases or files",
        ],
        "Text": [
            f"Analyzing or transforming text for writing, coding, or data cleaning",
            f"Counting, sorting, or formatting text in bulk without manual editing",
            f"Checking text properties like readability, uniqueness, or patterns",
        ],
        "Hash": [
            f"Verifying file integrity after downloads or transfers",
            f"Generating checksums for data deduplication or comparison",
            f"Learning how different hash algorithms work and when to use each",
        ],
        "Dev Tools": [
            f"Quick lookups during coding sessions without leaving your browser",
            f"Generating boilerplate configs, snippets, or reference documentation",
            f"Learning about development standards and best practices hands-on",
        ],
        "Generator": [
            f"Creating test data, placeholder content, or sample datasets",
            f"Generating unique IDs, tokens, or random values for applications",
            f"Coming up with creative names, prompts, or ideas for projects",
        ],
        "Design": [
            f"Quickly previewing CSS effects, colors, or layouts during design",
            f"Generating design assets like gradients, shadows, or color palettes",
            f"Checking accessibility compliance for colors and visual elements",
        ],
        "Convert": [
            f"Converting measurements when working across different unit systems",
            f"Switching between file formats like CSV, JSON, XML, and YAML",
            f"Translating data representations for compatibility between tools",
        ],
        "Image": [
            f"Quickly resizing, compressing, or converting images without installing software",
            f"Checking image metadata like dimensions, format, and file size",
            f"Generating QR codes or extracting information from images",
        ],
        "Math": [
            f"Checking homework solutions or exploring mathematical concepts",
            f"Performing quick calculations without a physical calculator",
            f"Verifying financial, statistical, or engineering computations",
        ],
        "Network": [
            f"Troubleshooting network issues and looking up DNS or IP information",
            f"Learning about networking concepts like ports, protocols, and headers",
            f"Quick reference for network configuration and diagnostics",
        ],
        "Finance": [
            f"Planning personal finances: loans, savings, investments, or budgets",
            f"Comparing financial scenarios to make informed money decisions",
            f"Quickly calculating tips, splits, taxes, or currency conversions",
        ],
        "SEO": [
            f"Optimizing your website for better search engine visibility",
            f"Generating proper meta tags, schema markup, and structured data",
            f"Checking technical SEO factors that affect your search rankings",
        ],
        "Health": [
            f"Estimating fitness metrics like BMI, ideal weight, or calorie needs",
            f"Tracking health-related calculations for personal wellness goals",
            f"Understanding formula-based health estimates for educational purposes",
        ],
        "Fun": [
            f"Adding randomness to games, activities, or decision-making",
            f"Generating creative prompts for writing, drawing, or brainstorming",
            f"Breaking decision paralysis when you just need a random pick",
        ],
        "Color": [
            f"Exploring color combinations for web design, branding, or art projects",
            f"Checking contrast and accessibility of color choices",
            f"Generating harmonious color palettes from a single base color",
        ],
    }
    
    when_use = when_map.get(cat, when_map["Dev Tools"])
    
    how = f"Enter your input in the field above, adjust any settings if available, and click the action button. Results appear instantly—no page reload, no server wait. All processing happens locally in your browser."
    
    rel = RELATED.get(tid)
    if rel:
        rel_id, rel_name = rel
        rel_text = f"Try our [{rel_name}](/{rel_id}/) for related functionality."
    else:
        rel_text = f"Check out our [full collection of free tools](/) to discover more utilities."
    
    return {
        "what": what,
        "when": when_use,
        "how": how,
        "related": rel_text,
    }


def info_zh(tool):
    """Generate Chinese info content."""
    name = tool["name"]
    tid = tool["id"]
    cat = tool["cat"]
    desc = tool["desc"]
    
    # Chinese tool name mapping
    zh_names = {
        "Password Generator": "密码生成器", "Timestamp Converter": "时间戳转换器",
        "JSON Formatter": "JSON格式化器", "Base64 Encoder": "Base64编解码器",
        "URL Encoder": "URL编解码器", "Word Counter": "字数统计器",
        "MD5 Hash": "MD5哈希", "UUID Generator": "UUID生成器",
        "Unicode Converter": "Unicode转换器", "Case Converter": "大小写转换器",
        "QR Code Generator": "二维码生成器", "Color Picker": "颜色选择器",
        "CSV to JSON": "CSV转JSON", "SHA256 Hash": "SHA256哈希",
        "HTML Entity Encoder": "HTML实体编解码", "IP Lookup": "IP查询",
        "Countdown Timer": "倒计时器", "Regex Tester": "正则测试器",
        "Image Compressor": "图片压缩器", "Number Base Converter": "进制转换器",
        "Text Diff Checker": "文本差异对比", "Lorem Ipsum Generator": "Lorem Ipsum生成器",
        "Text Line Sorter": "文本排序器", "URL Slug Generator": "URL Slug生成器",
        "JSON to CSV Converter": "JSON转CSV", "Markdown Preview": "Markdown预览",
        "JWT Decoder": "JWT解码器", "CSS Minifier": "CSS压缩器",
        "Random String Generator": "随机字符串生成器", "Percentage Calculator": "百分比计算器",
        "JSON Validator": "JSON验证器", "JavaScript Minifier": "JS压缩器",
        "HTML Minifier": "HTML压缩器",
    }
    
    zh_name = zh_names.get(name, name)
    
    what = f"{zh_name}是一个免费的在线工具，帮助你{desc}。它完全在浏览器中运行，使用客户端JavaScript，因此你的数据保持私密，永远不会离开你的设备。"
    
    when_map = {
        "Security": ["为你的应用程序生成安全的凭据、密钥或哈希值","检查或验证安全配置和加密设置","学习加密概念和安全最佳实践"],
        "Time": ["安排国际会议时在不同时区之间转换时间","计算项目规划中的截止日期、持续时间和倒计时","为旅行、账单或活动规划计算日期差异"],
        "Formatter": ["使压缩的代码或数据变得可读，便于调试和审查","在部署前验证语法并捕获格式错误","准备干净、风格一致的代码用于文档或分享"],
        "Encode/Decode": ["准备数据以便在URL、API或邮件中传输","编程或调试时在不同进制之间转换","为安全存储在数据库或文件中编码特殊字符"],
        "Text": ["分析或转换文本，用于写作、编程或数据清理","批量计数、排序或格式化文本，无需手动编辑","检查文本属性，如可读性、唯一性或模式"],
        "Hash": ["下载或传输后验证文件完整性","生成校验和用于数据去重或对比","学习不同哈希算法的工作原理及使用场景"],
        "Dev Tools": ["编码过程中快速查阅，无需离开浏览器","生成样板配置、代码片段或参考文档","实践中学习开发标准和最佳实践"],
        "Generator": ["创建测试数据、占位内容或样本数据集","为应用程序生成唯一ID、令牌或随机值","为项目想出创意名称、提示或想法"],
        "Design": ["设计过程中快速预览CSS效果、颜色或布局","生成设计素材，如渐变、阴影或颜色调色板","检查颜色和视觉元素的无障碍合规性"],
        "Convert": ["在不同单位制之间工作时转换度量","在CSV、JSON、XML和YAML等文件格式之间切换","为工具间的兼容性转换数据表示方式"],
        "Image": ["无需安装软件即可快速调整大小、压缩或转换图片","检查图片元数据，如尺寸、格式和文件大小","生成二维码或从图片中提取信息"],
        "Math": ["检查作业答案或探索数学概念","无需实体计算器即可进行快速计算","验证财务、统计或工程计算结果"],
        "Network": ["排查网络问题，查询DNS或IP信息","学习网络概念，如端口、协议和请求头","快速参考网络配置和诊断"],
        "Finance": ["规划个人财务：贷款、储蓄、投资或预算","比较不同财务方案，做出明智的理财决策","快速计算小费、分账、税费或货币换算"],
        "SEO": ["优化你的网站以获得更好的搜索引擎可见性","生成合适的meta标签、schema标记和结构化数据","检查影响搜索排名的技术性SEO因素"],
        "Health": ["估算健身指标，如BMI、理想体重或卡路里需求","为个人健康目标跟踪健康相关计算","出于教育目的理解基于公式的健康估算"],
        "Fun": ["为游戏、活动或决策增添随机元素","为写作、绘画或头脑风暴生成创意提示","当你需要随机选择时打破决策困难"],
        "Color": ["为网页设计、品牌或艺术项目探索色彩组合","检查色彩选择的无障碍性和对比度","从单一基础色生成和谐的调色板"],
    }
    
    when_use = when_map.get(cat, when_map["Dev Tools"])
    
    how = "在上方输入框中输入你的内容，如有设置项可进行调整，然后点击操作按钮。结果即时显示——无需页面刷新，无需等待服务器。所有处理都在你的浏览器本地完成。"
    
    rel = RELATED.get(tid)
    if rel:
        rel_id, rel_name = rel
        rel_zh_name = zh_names.get(rel_name, rel_name)
        rel_text = f"试试我们的[{rel_zh_name}](/{rel_id}/)获取相关功能。"
    else:
        rel_text = f"查看我们的[完整免费工具集合](/)发现更多实用工具。"
    
    return {
        "what": what,
        "when": when_use,
        "how": how,
        "related": rel_text,
    }


def main():
    with open(TOOLS_PATH) as f:
        tools = json.load(f)
    
    info_en_data = {}
    info_zh_data = {}
    
    for tool in tools:
        tid = tool["id"]
        info_en_data[tid] = info_en(tool)
        info_zh_data[tid] = info_zh(tool)
    
    with open(OUT_EN, "w") as f:
        json.dump(info_en_data, f, indent=2, ensure_ascii=False)
    with open(OUT_ZH, "w") as f:
        json.dump(info_zh_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ EN: {len(info_en_data)} tools")
    print(f"✅ ZH: {len(info_zh_data)} tools")


if __name__ == "__main__":
    main()
