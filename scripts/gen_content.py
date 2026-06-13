#!/usr/bin/env python3
"""Batch generate FAQ + DeepDive/Tips/Mistakes for tools missing content.
Uses category-based templates for consistency and quality.
"""

import json
from typing import Dict, List, Any

TOOLS_PATH = "src/data/tools.json"
FAQ_PATH = "src/data/faq.json"
CONTENT_PATH = "src/data/tool-content.json"

# ── FAQ Templates by Category ──
FAQ_TEMPLATES: Dict[str, List[Dict[str, str]]] = {
    "Finance": [
        {
            "q": "How accurate is the {name} compared to professional financial software?",
            "a": "The {name} uses standard mathematical formulas identical to those in professional financial calculators and spreadsheet software like Excel. For basic calculations, results are exact. For complex scenarios involving compound interest with irregular payments, slight rounding differences may occur but are typically within 0.01%. Always verify critical financial decisions with a qualified advisor."
        },
        {
            "q": "Can I use the {name} for my business or tax planning?",
            "a": "Yes, the {name} is suitable for quick estimates and planning scenarios. However, it provides approximate calculations and should not replace professional accounting software for official tax filings or legal financial documents. Use it for budgeting, comparing loan options, or understanding financial concepts before consulting professionals."
        },
        {
            "q": "Does the {name} account for inflation, fees, or variable interest rates?",
            "a": "Basic versions assume fixed rates and no additional fees for simplicity. Some tools allow you to adjust parameters like interest rates or include extra contributions. For comprehensive financial modeling with variable rates, inflation adjustments, and fee structures, consider using dedicated financial planning software. The {name} is best for quick 'what-if' scenarios."
        },
    ],
    "Convert": [
        {
            "q": "How precise are the conversion results from the {name}?",
            "a": "The {name} uses internationally recognized conversion factors with up to 15 significant digits of precision. This is more than sufficient for engineering, scientific, and everyday applications. Results are rounded to a reasonable number of decimal places for readability, but the underlying calculation maintains full floating-point precision."
        },
        {
            "q": "What units does the {name} support, and can I add custom ones?",
            "a": "The {name} supports all standard units in its category—metric, imperial, and specialized units where applicable. You can convert between any supported pair. Custom unit definitions are not supported, but the range of built-in units covers the vast majority of real-world conversion needs across science, engineering, cooking, and daily life."
        },
        {
            "q": "Why might my conversion result differ slightly from another online converter?",
            "a": "Minor differences (usually in the last decimal place) can occur due to different rounding strategies, the number of significant digits used in conversion factors, or floating-point arithmetic differences between JavaScript engines. For practical purposes, these differences are negligible—the underlying conversion factors are standardized internationally."
        },
    ],
    "Math": [
        {
            "q": "What algorithm does the {name} use behind the scenes?",
            "a": "The {name} implements well-established mathematical algorithms taught in standard math curricula. These are the same formulas used in scientific calculators, mathematical software like MATLAB and Mathematica, and educational platforms. The implementation is in pure JavaScript running directly in your browser for instant results."
        },
        {
            "q": "Can the {name} handle very large numbers or edge cases?",
            "a": "Yes, the {name} uses JavaScript's built-in number type which handles values up to approximately 1.8 × 10^308. For even larger numbers (big integers), some tools support BigInt. Edge cases like zero, negative numbers, and special values are handled gracefully with clear error messages when inputs fall outside valid ranges."
        },
        {
            "q": "Is the {name} suitable for academic or homework use?",
            "a": "Absolutely. The {name} is excellent for checking your work, exploring mathematical concepts, and speeding up repetitive calculations. However, students should understand the underlying math before relying on tools—use it to verify your manual calculations, not replace learning the concepts. Teachers often recommend such tools for self-checking."
        },
    ],
    "Generator": [
        {
            "q": "Are the results from the {name} truly random?",
            "a": "Browser-based generators use cryptographically secure pseudo-random number generators (CSPRNG) via the Web Crypto API (`crypto.getRandomValues()`), which produces values indistinguishable from true randomness for all practical purposes. This is the same standard used for generating encryption keys and secure tokens."
        },
        {
            "q": "Is my generated data private? Does it get stored anywhere?",
            "a": "All generation happens entirely in your browser using client-side JavaScript. Generated data is never transmitted to any server, never stored in any database, and never logged. Once you close the page, the generated data is gone. For sensitive use cases, this local-only architecture provides maximum privacy."
        },
        {
            "q": "How many unique combinations can the {name} produce?",
            "a": "The number of possible outputs depends on the configuration parameters you set. For most generators, the combinatorial space is astronomically large—far exceeding the number of atoms in the observable universe. This means collision probability (getting the same result twice) is practically zero, making the {name} suitable for generating unique identifiers."
        },
    ],
    "Dev Tools": [
        {
            "q": "Does the {name} follow the latest standards and best practices?",
            "a": "Yes, the {name} is designed to follow current web standards, RFC specifications, and industry best practices. When generating configuration files or code snippets, it adheres to the latest stable specifications. For standards that evolve (like security protocols), the tool targets the most recent widely-adopted version."
        },
        {
            "q": "Can I use the {name} in my CI/CD pipeline or development workflow?",
            "a": "The {name} is a browser-based tool best suited for quick lookups, ad-hoc generation, and learning. For CI/CD integration, consider command-line equivalents or programmatic libraries that can be called from build scripts. However, the tool is excellent for prototyping, debugging, and exploring configuration options before committing to code."
        },
        {
            "q": "How does the {name} compare to the equivalent command-line tool?",
            "a": "Browser-based tools offer instant access without installation, making them ideal for quick tasks on any device. Command-line tools typically offer more advanced features, batch processing, and automation capabilities. The {name} is optimized for the 80% use case—fast, accessible, and zero-setup—while CLI tools serve power users and automated workflows."
        },
    ],
    "Text": [
        {
            "q": "How does the {name} handle Unicode, emoji, and special characters?",
            "a": "The {name} fully supports Unicode text including emoji, CJK characters, accented letters, and right-to-left scripts. It processes text as UTF-8 and handles multi-byte characters correctly. However, for operations like counting or transformation, note that what appears as one character may actually be multiple Unicode code points (e.g., emoji with skin tone modifiers)."
        },
        {
            "q": "Is there a limit on how much text I can process with the {name}?",
            "a": "Browser-based tools are limited by available memory and JavaScript performance. For typical use (articles, essays, code files up to a few megabytes), the {name} processes instantly. For very large texts (novels, logs exceeding 10 MB), performance may degrade. In such cases, consider splitting the text or using a desktop tool."
        },
        {
            "q": "Does the {name} preserve the original formatting and line endings?",
            "a": "The {name} preserves all original text including line endings (LF/CRLF), whitespace, and special characters unless the specific operation requires modification. When the tool modifies text, it clearly indicates what changed. Original formatting is maintained wherever possible to prevent unintended corruption."
        },
    ],
    "SEO": [
        {
            "q": "How does the {name} help improve my Google search rankings?",
            "a": "The {name} helps you follow SEO best practices that Google explicitly recommends in their documentation. Proper structured data, optimized meta tags, clean heading hierarchy, and fast-loading pages are all ranking signals. While no single tool guarantees higher rankings, using these tools to fix technical SEO issues removes barriers that could be holding your pages back."
        },
        {
            "q": "Is the {name} compliant with the latest Google Search guidelines?",
            "a": "Yes, the {name} follows current Google Search Central guidelines and schema.org specifications. However, search algorithms evolve, and what's compliant today may change. Always cross-reference with Google's official documentation. The tool helps you implement technical SEO correctly; content quality and backlinks remain the strongest ranking factors."
        },
        {
            "q": "Can the {name} guarantee my page will appear in featured snippets?",
            "a": "No tool can guarantee featured snippet placement, as Google's algorithm decides this algorithmically. However, the {name} helps you structure content in ways that are snippet-friendly: clear headings, concise answers, proper schema markup, and well-formatted lists. These practices significantly increase your chances of being selected for rich results."
        },
    ],
    "Security": [
        {
            "q": "Is it safe to generate security credentials using an online tool?",
            "a": "Yes, the {name} runs entirely in your browser using client-side JavaScript. Keys, hashes, and credentials are generated locally and never transmitted to any server. For maximum security, use tools that are open-source (so you can inspect the code) and operate offline-capable. Always generate sensitive credentials on trusted devices."
        },
        {
            "q": "What security standards does the {name} implement?",
            "a": "The {name} implements industry-standard cryptographic algorithms and security protocols as defined by NIST, IETF RFCs, and OWASP guidelines. Where applicable, it uses the Web Crypto API for cryptographic operations, which is FIPS 140-2 compliant. The specific standard depends on the tool purpose—encryption, hashing, or credential generation."
        },
        {
            "q": "How often should I rotate or regenerate credentials created with the {name}?",
            "a": "Follow your organization's security policy for credential rotation. As a general guideline: passwords every 90 days, API keys and tokens upon suspected compromise, SSH keys every 6-12 months, and hashed values only when the underlying data changes. The {name} makes regeneration quick and easy whenever rotation is needed."
        },
    ],
    "Health": [
        {
            "q": "How accurate is the {name}? Should I trust it for medical decisions?",
            "a": "The {name} uses widely accepted formulas from medical and fitness research (e.g., Mifflin-St Jeor, Epley, Harris-Benedict). These provide reasonable estimates for the general population but may not account for individual variations in metabolism, body composition, or medical conditions. Always consult healthcare professionals for medical decisions."
        },
        {
            "q": "What data do I need to use the {name} accurately?",
            "a": "The {name} requires basic body measurements and lifestyle information such as age, weight, height, gender (for formula selection), and activity level. More accurate inputs produce more accurate estimates. For fitness calculations, using actual measured values (body fat percentage, resting heart rate) rather than estimates further improves precision."
        },
        {
            "q": "Can the {name} replace a consultation with a doctor or dietitian?",
            "a": "No. The {name} provides educational estimates based on population averages and published formulas. It cannot account for your unique medical history, medications, metabolic conditions, or specific health goals. Use it for general awareness and goal-setting, but always involve qualified healthcare professionals for personalized advice."
        },
    ],
    "Fun": [
        {
            "q": "How random and fair is the {name}?",
            "a": "The {name} uses JavaScript's cryptographic random number generator (`crypto.getRandomValues()`) for all random selections. This ensures statistically uniform distribution—every possible outcome has an equal probability. The randomness is indistinguishable from true randomness and is not biased toward any particular result."
        },
        {
            "q": "Can I customize the {name} for my specific needs?",
            "a": "The {name} provides configurable parameters that let you adjust the output to your preferences—such as setting categories, themes, difficulty levels, or participant lists. These customization options make the tool flexible for different scenarios, from party games to classroom activities to creative brainstorming."
        },
        {
            "q": "Is the {name} appropriate for all ages and settings?",
            "a": "The {name} is designed to be family-friendly and suitable for general audiences. Content is kept PG-rated by default. For tools like truth-or-dare or story prompts, options are curated to be fun without being offensive. Always review generated content before using it in sensitive settings like classrooms or with children."
        },
    ],
    "Color": [
        {
            "q": "How does the {name} help with web accessibility (WCAG compliance)?",
            "a": "The {name} helps you evaluate and improve color contrast ratios against WCAG 2.1 standards. It can identify color combinations that meet AA (4.5:1 for normal text) and AAA (7:1) contrast requirements. Some tools simulate various types of color blindness to ensure your designs are perceivable by users with visual impairments."
        },
        {
            "q": "What color spaces and formats does the {name} support?",
            "a": "The {name} supports all major color spaces and formats: HEX (#RRGGBB), RGB, RGBA, HSL, HSLA, HSV, and CMYK. It automatically converts between these formats when you change parameters. For web development, it can also generate CSS-compatible color values and gradient declarations."
        },
        {
            "q": "Can the {name} generate accessible color palettes for my brand?",
            "a": "Yes, the {name} can generate harmonious color palettes using color theory principles like complementary, analogous, triadic, and monochromatic schemes. For brand use, you can lock a primary brand color and let the tool suggest complementary colors that meet accessibility contrast requirements, ensuring your palette is both beautiful and inclusive."
        },
    ],
    "Time": [
        {
            "q": "How does the {name} handle timezone differences and daylight saving?",
            "a": "The {name} uses the IANA timezone database (via the browser's Intl API) to handle all timezone conversions, including daylight saving time (DST) transitions. It automatically adjusts for DST based on each location's current rules. When planning across DST change dates, results account for the offset shift correctly."
        },
        {
            "q": "Can the {name} handle recurring events and exclude weekends/holidays?",
            "a": "The {name} can calculate durations excluding weekends by default. Some tools let you specify custom non-working days. For holiday exclusions, you may need to manually account for specific dates since holiday calendars vary by country and year. The tool focuses on standard work-week calculations."
        },
        {
            "q": "Why does the {name} show a different time than my phone or computer?",
            "a": "Differences can occur if your device's timezone settings are incorrect, if you're comparing across timezones without accounting for the offset, or if your device hasn't synchronized with a time server recently. The {name} uses your browser's timezone setting—verify it matches your actual location in system preferences."
        },
    ],
    "Hash": [
        {
            "q": "Is the {name} cryptographically secure? Can it be reversed?",
            "a": "Cryptographic hash functions like SHA-256 and SHA-3 are designed to be one-way—computationally infeasible to reverse. The {name} produces a fixed-length hash from any input, and even a single bit change in the input produces a completely different hash (avalanche effect). SHA-2 and SHA-3 family hashes remain cryptographically secure as of 2025."
        },
        {
            "q": "What's the difference between the {name} and other hash algorithms like MD5 or SHA-1?",
            "a": "Different hash algorithms offer different security guarantees and output lengths. SHA-256 (32 bytes) provides 128-bit collision resistance and is widely trusted. SHA-512/384 offer stronger security margins. MD5 and SHA-1 are broken—they have known collision attacks and should never be used for security purposes. Choose based on your security requirements and compatibility needs."
        },
        {
            "q": "Can I hash files with the {name}, not just text strings?",
            "a": "Yes, the {name} can hash files directly in your browser. Simply upload the file and the hash is computed locally—the file never leaves your device. This is useful for verifying file integrity after downloads, detecting duplicate files, or generating checksums for distribution. For very large files (hundreds of MB), processing may take a few seconds."
        },
    ],
    "Image": [
        {
            "q": "Does the {name} process images on my device or upload them to a server?",
            "a": "The {name} processes all images entirely in your browser using the HTML5 Canvas API and modern JavaScript. Your images never leave your device—no uploads, no server processing, no storage. This makes it both private and fast, as there's no network latency. You can even use it offline once the page is loaded."
        },
        {
            "q": "What image formats does the {name} support?",
            "a": "The {name} supports all major web image formats: JPEG, PNG, WebP, GIF (static), BMP, and TIFF. Output formats depend on the specific tool—compression tools typically output JPEG or WebP for best file size reduction. SVG vector images are supported for some operations. Browser support for newer formats like AVIF varies."
        },
        {
            "q": "Will the {name} reduce the quality of my images?",
            "a": "For tools like resizers and compressors, some quality reduction is inherent in the process. The {name} gives you control over quality settings (typically a slider from 1-100%) so you can balance file size against visual quality. For information-reading tools like metadata viewers, no quality is lost since the image is only read, not modified."
        },
    ],
}

# ── DeepDive Templates by Category ──
DEEPDIVE_TEMPLATES: Dict[str, str] = {
    "Finance": "{name} is a practical financial tool that helps you make informed money decisions through clear, calculation-based insights. In personal finance, small differences in interest rates, loan terms, or savings rates can compound into thousands of dollars over time—having a quick, accurate calculator removes the guesswork. The {name} implements standard financial formulas (present value, future value, amortization schedules, compound interest) that are identical to those used in Excel, Google Sheets, and professional financial software. All calculations run client-side in your browser using JavaScript, meaning your financial data—loan amounts, savings goals, interest rates—stays completely private on your device. Whether you're comparing mortgage options, planning retirement contributions, calculating investment returns, or splitting a dinner bill, having instant access to accurate financial math empowers better decisions. The tool is designed for quick 'what-if' analysis: adjust one variable and immediately see how it affects the outcome, helping you understand the relationships between principal, rate, time, and payments.",

    "Convert": "{name} eliminates the friction of unit conversion—one of those small but persistent annoyances in daily life and professional work. Whether you're following an international recipe that uses grams instead of cups, reading a European weather report in Celsius, or converting engineering specifications between metric and imperial, quick access to accurate conversion factors saves time and prevents costly mistakes. The {name} uses internationally standardized conversion factors maintained by organizations like NIST and BIPM, with precision far exceeding practical needs. All conversions happen instantly in your browser, and the tool supports bidirectional conversion—enter a value in either unit and get the equivalent. Beyond basic conversion, many unit converter tools handle compound units (like km/h to m/s), temperature offsets (Celsius and Fahrenheit have different zero points), and historical or regional unit variants. For professionals who regularly switch between measurement systems—scientists, engineers, chefs, travelers—having a reliable converter bookmarked is an essential productivity boost.",

    "Math": "{name} brings mathematical problem-solving to your fingertips, handling the computational heavy lifting so you can focus on understanding concepts and interpreting results. Mathematics underpins everything from engineering and physics to finance and data science, yet many useful calculations are tedious to perform by hand. The {name} automates these calculations using well-established algorithms and formulas, delivering instant, accurate results. The implementation uses JavaScript's IEEE 754 double-precision floating-point arithmetic, which provides approximately 15-17 significant digits of precision—more than sufficient for virtually all practical applications. Beyond basic arithmetic, the tool handles special cases (division by zero, negative square roots, overflow conditions) gracefully with clear error messages rather than cryptic NaN outputs. For students, it serves as a learning aid for checking manual work; for professionals, it's a productivity tool that eliminates calculator fumbling; for everyone, it makes advanced mathematical operations accessible without specialized software.",

    "Generator": "{name} automates the creation of structured, randomized data—saving you from the tedious task of making up test data, placeholder content, or unique identifiers by hand. In software development, testing, design, and content creation, you constantly need sample data that looks realistic but isn't real. The {name} fills this gap by programmatically generating data that follows real-world patterns and constraints. All generation happens client-side using your browser's cryptographic random number generator (CSPRNG via `crypto.getRandomValues()`), ensuring both randomness and privacy—no data leaves your device. The generator is configurable: you control the output format, length, character sets, or other domain-specific parameters to match your exact requirements. Whether populating a database with test users, creating wireframe content for a design mockup, generating unique identifiers for a distributed system, or coming up with creative prompts, having a reliable data generator in your toolkit saves hours of manual data creation.",

    "Dev Tools": "{name} is a developer utility that streamlines common programming and DevOps tasks—the kind of small but frequent operations that eat into productive coding time. Every developer has experienced the friction of switching contexts: opening a terminal, remembering the exact command syntax, installing a CLI tool, or searching Stack Overflow for a one-liner. The {name} eliminates this friction by providing instant, browser-based access to specialized development functions. It follows current web standards, RFC specifications, and industry best practices, generating output that's ready to use in production environments. All processing happens client-side, so proprietary code, API keys, or sensitive configuration never leaves your machine. The tool is designed for the most common use case—quick, ad-hoc operations—while acknowledging that complex workflows and automation scenarios are better served by CLI tools and CI/CD integration. For learning, prototyping, debugging, and one-off tasks, a good browser-based dev tool is often faster than installing and configuring a command-line equivalent.",

    "Text": "{name} is a versatile text processing utility that handles the manipulation, analysis, and transformation of written content. Text is the universal format—code, articles, data, messages, documentation—and being able to quickly process it programmatically saves enormous time compared to manual editing. The {name} operates on plain text with full Unicode support, correctly handling multi-byte characters, right-to-left scripts, emoji, and special whitespace. All processing happens instantly in your browser with no server round-trips, making it suitable for sensitive documents that shouldn't leave your device. The tool addresses a specific text operation that's tedious to do by hand but trivial for a computer: counting, sorting, transforming case, checking properties, or converting between formats. For writers checking readability scores, developers formatting code comments, data analysts cleaning CSV exports, or anyone who works extensively with text, having a collection of focused text tools dramatically improves workflow efficiency.",

    "SEO": "{name} is an SEO utility that helps you optimize web pages for search engine visibility by checking technical factors, generating proper markup, and validating best practices. Search engine optimization is a multi-billion-dollar industry, yet many of the highest-impact improvements are technical basics that can be validated automatically: proper heading hierarchy, valid structured data, optimized meta tags, mobile-friendly design, and fast page speed. The {name} automates one specific aspect of technical SEO, giving you actionable feedback without requiring deep SEO expertise. It follows Google Search Central guidelines and schema.org specifications, so the output is aligned with what search engines actually look for. All analysis happens client-side—you can check pages, validate markup, and generate structured data without sending your URL or content to a third party. While technical SEO alone won't guarantee rankings (content quality and backlinks are the primary drivers), it removes barriers that could prevent your great content from being discovered.",

    "Security": "{name} is a security tool that helps protect digital assets through cryptographic operations, credential generation, and security configuration—bringing enterprise-grade security practices to everyday users and developers. In an era of constant data breaches, ransomware attacks, and credential theft, good security hygiene is no longer optional. The {name} implements industry-standard algorithms and protocols (NIST, IETF RFCs, OWASP guidelines) using the browser's Web Crypto API where possible for FIPS 140-2 compliant operations. Critically, all cryptographic operations happen entirely client-side—keys, hashes, and credentials are generated in your browser and never transmitted to any server. This zero-trust architecture means you can generate SSH keys, create certificate signing requests, compute hashes, or encrypt messages without exposing sensitive material to third-party infrastructure. For developers setting up server security, system administrators managing access controls, or anyone who needs to generate secure credentials, having these capabilities instantly available in a browser dramatically lowers the barrier to good security practices.",

    "Health": "{name} is a health and fitness calculator that provides science-based estimates to help you understand your body, set realistic goals, and track progress. The tool implements formulas from peer-reviewed research in exercise science, nutrition, and medicine—the same equations used by fitness professionals, dietitians, and medical practitioners. Important caveat: these are population-average estimates, not personalized medical assessments. Individual factors like genetics, medical conditions, medication effects, and body composition variations mean your actual values may differ. The {name} is best used as an educational and motivational tool: understand the principles behind the calculations, use the estimates as baselines, and adjust based on your real-world results. All calculations happen locally in your browser—your health data stays private. For serious health concerns, medical conditions, or personalized nutrition plans, always consult qualified healthcare professionals who can account for your complete medical history.",

    "Fun": "{name} is a lighthearted utility that adds an element of chance, creativity, or entertainment to everyday situations. Sometimes you need a coin flip to break a tie, a random name for a character, a silly meme caption to lighten the mood, or a story prompt to spark creativity. The {name} fills these moments with genuinely random, unbiased outputs generated by your browser's cryptographic random number generator—no patterns, no favoritism, just pure chance. All generation is client-side and ephemeral: nothing is stored, logged, or tracked. The tool is designed to be family-friendly and appropriate for all settings, from classroom activities to party games to solo creative brainstorming. While the purpose is entertainment, the underlying implementation is rigorous—proper randomization, clean UI, and configurable parameters that let you tailor the output to your specific scenario. Sometimes the most useful tool is the one that makes you smile.",

    "Color": "{name} is a design utility that helps you work with color—one of the most impactful yet challenging aspects of visual design. Color choices affect aesthetics, usability, brand perception, and accessibility, and getting them right requires understanding color theory, contrast ratios, and human perception. The {name} automates the technical aspects so you can focus on creative decisions. It supports all major color spaces (HEX, RGB, HSL, HSV, CMYK) with instant conversion between formats, and applies color theory principles (complementary, analogous, triadic, monochromatic) to generate harmonious palettes. Crucially, it includes accessibility features: contrast ratio checking against WCAG 2.1 AA/AAA standards, and color blindness simulation for the most common types (protanopia, deuteranopia, tritanopia). All processing is client-side—uploaded images for color extraction never leave your device. Whether you're designing a website, creating a brand identity, or just exploring color combinations, having sophisticated color tools in your browser eliminates the need for expensive design software for color work.",

    "Time": "{name} is a time management utility that helps you navigate the complexities of dates, timezones, and scheduling—problems that appear simple but hide surprising depth. Time calculations are notoriously tricky in programming: months have different lengths, leap years add an extra day every four years (except century years not divisible by 400), daylight saving time shifts by one hour on different dates in different jurisdictions, and timezone offsets range from UTC-12 to UTC+14. The {name} handles all these edge cases correctly using the browser's Internationalization API, which draws from the IANA timezone database—the gold standard for timezone data maintained by the internet engineering community. Whether you're scheduling meetings across continents, calculating project deadlines that span DST changes, tracking countdowns to important events, or computing work hours with weekend exclusions, the tool delivers accurate results without requiring you to remember all the edge cases. For remote teams, international businesses, and anyone coordinating across timezones, reliable time tools prevent the costly mistakes that come from timezone confusion.",

    "Image": "{name} is a browser-based image processing tool that performs common image operations without requiring you to install heavy desktop software like Photoshop or GIMP. Image manipulation used to require powerful native applications, but modern browsers with the HTML5 Canvas API and high-performance JavaScript engines can now handle most common image tasks instantly. The {name} processes images entirely on your device—your photos, screenshots, and graphics never leave your computer, ensuring complete privacy. Supported operations include resizing, format conversion, compression, metadata extraction, and basic adjustments. The tool handles all common web formats (JPEG, PNG, WebP, GIF, BMP) and provides quality controls so you can balance file size against visual fidelity. For web developers optimizing images for page speed, content creators preparing visuals for social media, or anyone who needs quick image adjustments without launching Photoshop, browser-based image tools offer a frictionless, privacy-respecting alternative to uploading files to third-party servers.",

    "Hash": "{name} computes cryptographic hash values—fixed-length digital fingerprints of data—that are essential for verifying file integrity, storing passwords securely, and ensuring data hasn't been tampered with. A hash function takes any input (a password, a file, a message) and produces a unique, fixed-size output. The key properties that make hashes useful: determinism (same input always produces same output), avalanche effect (tiny input change produces completely different hash), and one-way (computationally infeasible to reverse). The {name} implements these functions using the browser's SubtleCrypto API where available, providing hardware-accelerated, side-channel-resistant hashing. All computation happens locally—your data, files, and resulting hashes never leave your device. Use cases span security (password storage, file integrity verification), data deduplication (finding duplicate files by hash comparison), blockchain (transaction verification), and digital signatures. Understanding which hash algorithm to use for which purpose is important: SHA-256 and SHA-3 for security, MD5 only for non-security checksums.",

    "Encode/Decode": "{name} transforms data between different representation formats—an essential operation in computing that bridges the gap between how humans read information and how computers process it. Encoding converts data into a standardized format suitable for storage or transmission; decoding reverses the process. Unlike encryption (which requires keys and aims for secrecy), encoding is designed for compatibility and is fully reversible by anyone who knows the scheme. The {name} handles common encoding formats used across the internet and computing: Base64 for embedding binary data in text protocols, URL encoding for safe web addresses, HTML entities for special characters in markup, and various numeric base conversions (binary, octal, decimal, hexadecimal). All processing is client-side JavaScript with no server involvement—your data stays private. For developers debugging API responses, webmasters fixing broken URLs, or anyone working with data interchange formats, understanding and being able to quickly encode/decode data is a fundamental technical skill that this tool makes accessible.",
}

# ── Tips Templates by Category ──
TIPS_TEMPLATES: Dict[str, List[str]] = {
    "Finance": [
        "Always compare multiple scenarios side by side—slight differences in interest rates compound dramatically over long periods",
        "Double-check your inputs: a misplaced decimal or extra zero can change results by orders of magnitude",
        "Use the Rule of 72 for quick mental estimates: divide 72 by your interest rate to get years to double your money",
    ],
    "Convert": [
        "Bookmark the converter for units you use frequently—it's faster than searching each time",
        "When precision matters (engineering, science), note the number of significant figures in your input and match them in output",
        "For cooking, use weight (grams) rather than volume (cups) for more consistent results",
    ],
    "Math": [
        "Use the tool to check your manual calculations—it catches arithmetic errors instantly",
        "For large or repetitive calculations, jot down intermediate results to trace errors if outputs seem wrong",
        "Understand the formula behind the calculation, not just the result—it builds deeper mathematical intuition",
    ],
    "Generator": [
        "Regenerate multiple times if you need variety—each click produces a completely independent random result",
        "For test data, generate large batches and save to a file rather than regenerating each time",
        "When generating security credentials, close the page after copying your result to clear it from browser memory",
    ],
    "Dev Tools": [
        "Keep a browser tab with your most-used dev tools open during coding sessions for quick access",
        "Cross-reference generated output with official documentation when using for production systems",
        "Save commonly used configurations as snippets in your code editor for even faster access",
    ],
    "Text": [
        "For large texts, process in sections if the tool becomes slow—most handle up to several MB smoothly",
        "When comparing texts or checking properties, normalize whitespace first for more meaningful results",
        "Use the tool as a quick sanity check before running complex text processing scripts",
    ],
    "SEO": [
        "Run SEO checks before publishing new content, not after—it's easier to fix issues pre-launch",
        "Combine multiple SEO tools: use a heading checker, structured data validator, and SERP preview together",
        "Re-check your pages periodically—Google's guidelines evolve and what was optimal last year may need updating",
    ],
    "Security": [
        "Never share private keys or passwords generated by the tool via email or messaging apps",
        "Verify the cryptographic parameters (key length, algorithm version) match your organization's security policy",
        "After generating credentials, test them immediately to ensure they work before deploying to production",
    ],
    "Health": [
        "Track your numbers over time rather than focusing on a single measurement—trends matter more than snapshots",
        "Use the tool's estimates as a starting point, then adjust based on your actual results and how your body responds",
        "Recalculate periodically as your weight, age, or activity level changes—your targets should evolve with you",
    ],
    "Fun": [
        "Use the tool to break decision paralysis—when you can't choose, let randomness decide",
        "Combine outputs from multiple fun tools for creative mashups: random name + story prompt + meme text",
        "Save or screenshot your favorite results—random outputs can be surprisingly perfect",
    ],
    "Color": [
        "Always check contrast ratios against WCAG standards before finalizing any color combination",
        "Test your palette under color blindness simulation—about 8% of males have some form of color vision deficiency",
        "Generate 5-10 palettes and compare them side by side before committing to one",
    ],
    "Time": [
        "When scheduling across timezones, always specify the timezone in the meeting invite, not just the time",
        "For countdowns, add one extra day as a buffer—things rarely finish exactly on schedule",
        "Use UTC as your reference point when coordinating across more than two timezones",
    ],
    "Image": [
        "Always keep the original image before compressing or resizing—you can't recover lost quality",
        "Use WebP format for web images—it provides 25-35% better compression than JPEG at the same quality",
        "Batch process images for consistency: apply the same settings to all photos in a gallery or product listing",
    ],
    "Hash": [
        "Always verify downloaded files against published hash values to detect corruption or tampering",
        "Use SHA-256 or stronger for security-critical applications—MD5 and SHA-1 are broken",
        "When hashing passwords, use dedicated password hashing functions (bcrypt, Argon2), not general-purpose hashes",
    ],
    "Encode/Decode": [
        "When debugging encoded strings, decode step by step—accidental double-encoding is a common mistake",
        "Use the appropriate encoding for your context: URL encoding for query strings, HTML entities for markup",
        "Test your encoded output by decoding it back—if you don't get the original, there's a problem",
    ],
}

# ── Common Mistakes Templates by Category ──
MISTAKES_TEMPLATES: Dict[str, List[str]] = {
    "Finance": [
        "Confusing monthly and annual interest rates—always check which rate the tool expects",
        "Forgetting to account for fees (origination, maintenance, early repayment) that significantly affect total cost",
    ],
    "Convert": [
        "Mixing up similar units—ounces (weight) vs fluid ounces (volume), or short tons vs metric tons",
        "Using approximate mental conversions for precise work—always use the tool for accuracy-critical calculations",
    ],
    "Math": [
        "Misunderstanding order of operations—the tool follows PEMDAS, double-check your expression grouping",
        "Forgetting to specify units or precision requirements when interpreting results",
    ],
    "Generator": [
        "Using generated test data in production—always replace placeholder data with real content before deploying",
        "Assuming generated data is unique without checking—while collision probability is tiny, verify for critical applications",
    ],
    "Dev Tools": [
        "Copying generated configuration without understanding each setting—know what each line does",
        "Using development-oriented configurations in production without hardening (enabling debug mode, exposing ports, etc.)",
    ],
    "Text": [
        "Not checking the output encoding—some operations may change character encoding or introduce artifacts",
        "Processing text with invisible control characters without noticing—these can corrupt output silently",
    ],
    "SEO": [
        "Obsessing over technical SEO while neglecting content quality—great content with average SEO beats average content with perfect SEO",
        "Keyword stuffing meta tags—Google penalizes this; write for humans first, search engines second",
    ],
    "Security": [
        "Storing generated credentials in plain text files or sharing them over unencrypted channels",
        "Using weak parameters (short key lengths, outdated algorithms) because they generate faster",
    ],
    "Health": [
        "Taking calculator estimates as medical advice—these are educational tools, not diagnostic devices",
        "Comparing your numbers to professional athletes or fitness models rather than to your own baseline",
    ],
    "Fun": [
        "Overthinking the randomness—if you don't like the first result, just click again",
        "Using humor tools in contexts where the humor might be misinterpreted or cause offense",
    ],
    "Color": [
        "Choosing colors that look great on your calibrated monitor but terrible on common consumer displays",
        "Forgetting that brand colors need to work on both light and dark backgrounds",
    ],
    "Time": [
        "Assuming all countries observe daylight saving time—many equatorial and Asian countries do not",
        "Scheduling meetings at midnight UTC without checking what local time that is for participants",
    ],
    "Image": [
        "Over-compressing images to save bytes—the visual degradation may hurt user experience more than the performance gain helps",
        "Resizing small images larger—this creates pixelation; always start with the highest resolution source available",
    ],
    "Hash": [
        "Using fast hashes (MD5, SHA-1) for password storage—these are designed for speed, which helps attackers brute-force",
        "Assuming a matching hash means the files are identical—hash collisions, while rare, are possible with broken algorithms",
    ],
    "Encode/Decode": [
        "Confusing encoding with encryption—Base64 and URL encoding provide zero security, they just change representation",
        "Double-encoding data accidentally—URLs with pre-encoded components get corrupted when encoded again",
    ],
}


def generate_faq(tool: Dict[str, str]) -> List[Dict[str, str]]:
    """Generate 3 FAQ entries for a tool based on category templates."""
    cat = tool["cat"]
    templates = FAQ_TEMPLATES.get(cat, FAQ_TEMPLATES["Dev Tools"])
    return [
        {"q": t["q"].format(name=tool["name"]), "a": t["a"].format(name=tool["name"])}
        for t in templates
    ]


def generate_content(tool: Dict[str, str]) -> Dict[str, Any]:
    """Generate DeepDive, Tips, and Mistakes for a tool."""
    cat = tool["cat"]
    deepdive_template = DEEPDIVE_TEMPLATES.get(cat, DEEPDIVE_TEMPLATES["Dev Tools"])
    tips = TIPS_TEMPLATES.get(cat, TIPS_TEMPLATES["Dev Tools"])
    mistakes = MISTAKES_TEMPLATES.get(cat, MISTAKES_TEMPLATES["Dev Tools"])
    
    return {
        "deepDive": deepdive_template.format(name=tool["name"]),
        "tips": tips,
        "commonMistakes": mistakes,
    }


def main():
    with open(TOOLS_PATH) as f:
        tools = json.load(f)
    
    with open(FAQ_PATH) as f:
        faq = json.load(f)
    
    with open(CONTENT_PATH) as f:
        content = json.load(f)
    
    # Find missing tools
    existing_faq = set(faq.keys())
    existing_content = set(content.keys())
    
    new_faq_count = 0
    new_content_count = 0
    
    for tool in tools:
        tid = tool["id"]
        if tid not in existing_faq:
            faq[tid] = generate_faq(tool)
            new_faq_count += 1
        if tid not in existing_content:
            content[tid] = generate_content(tool)
            new_content_count += 1
    
    # Write back
    with open(FAQ_PATH, "w") as f:
        json.dump(faq, f, indent=2, ensure_ascii=False)
    
    with open(CONTENT_PATH, "w") as f:
        json.dump(content, f, indent=2, ensure_ascii=False)
    
    print(f"✅ FAQ: {new_faq_count} tools added (total: {len(faq)})")
    print(f"✅ Content: {new_content_count} tools added (total: {len(content)})")


if __name__ == "__main__":
    main()
