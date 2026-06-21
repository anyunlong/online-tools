---
title: "URL Encoding Explained: What is %20 and How to Encode URLs"
date: 2026-06-21
description: "Learn what URL encoding (percent encoding) is, why %20 represents a space, and how to encode and decode URLs — with practical examples."
tags: ["url", "encoding", "percent encoding", "web development", "guide"]
---

## What is URL Encoding?

URL encoding converts special characters in URLs to percent-sign notation so they can be transmitted safely. Characters like `/`, `?`, `&`, and spaces have special meanings in URLs and must be encoded when used as literal data.

## Why %20 is a Space

The ASCII code for space is 32 decimal = 20 hexadecimal. So a space becomes `%20`. Similarly:
- `&` = `%26`, `=` = `%3D`, `#` = `%23`, `?` = `%3F`, `/` = `%2F`

## When You Need URL Encoding

**Query parameters**: A search for "rock & roll" becomes `?q=rock%20%26%20roll`.

**File names**: "report (final).pdf" becomes `report%20%28final%29.pdf`.

**International text**: Chinese, Japanese, and other non-ASCII characters are first encoded as UTF-8 bytes, then percent-encoded. "中文" becomes `%E4%B8%AD%E6%96%87`.

Use our free [URL Encoder / Decoder](https://www.4uses.com/url-encode/) to quickly encode or decode any text for use in URLs and API calls.
