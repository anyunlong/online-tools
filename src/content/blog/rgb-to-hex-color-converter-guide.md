---
title: "RGB to HEX Color Converter: How to Convert Colors Between Formats"
date: 2026-06-21
description: "Learn how to convert RGB to HEX and HEX to RGB color codes. Understand color formats used in CSS, HTML, and design tools — with a free online converter."
tags: ["color", "rgb", "hex", "converter", "css", "web design"]
---

## What Are RGB and HEX Color Codes?

RGB (Red, Green, Blue) and HEX (hexadecimal) are the two most common ways to represent colors on screens. Every color on a monitor is a mix of red, green, and blue light at different intensities.

**RGB** uses three numbers (0-255): `rgb(255, 87, 51)`. **HEX** uses a six-char code starting with `#`: `#FF5733`. The first two hex digits are red, middle two are green, last two are blue.

## How to Convert RGB to HEX

Each RGB value from 0–255 converts to two hex digits. Divide by 16: the quotient is the first digit, the remainder is the second. For 255, that’s 15 and 15 = FF. For 87, that’s 5 and 7 = 57. Combine: `#FF5733`.

## How to Convert HEX to RGB

Split the six digits into three pairs (FF, 57, 33). Convert each from base-16 to base-10: FF = 255, 57 = 87, 33 = 51. Result: `rgb(255, 87, 51)`.

## When to Use Each

HEX is compact and ideal for CSS. RGB is better when you need transparency with `rgba()`. For color palettes, try HSL instead.

Experiment with our [HEX Color Generator](https://www.4uses.com/hex-color-gen/) or build palettes with the [Color Shades Generator](https://www.4uses.com/color-shades/).
