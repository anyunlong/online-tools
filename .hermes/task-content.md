Add SEO-rich content to ALL 51 tool pages. Do NOT stop until every page is done.

## HOW TO ADD CONTENT

Each tool page (.astro file in src/pages/) uses ToolLayout which has an `<slot name="info">` area. Add content there like this:

<div slot="info">
  <h2 class="text-base font-semibold text-surface-100 mb-2">What is [Tool Name]?</h2>
  <p class="mb-3">[2-3 sentence plain English explanation]</p>
  <h2 class="text-base font-semibold text-surface-100 mb-2">When to Use</h2>
  <ul class="list-disc pl-5 mb-3 space-y-1">
    <li>[Scenario 1]</li>
    <li>[Scenario 2]</li>
  </ul>
  <h2 class="text-base font-semibold text-surface-100 mb-2">How to Use</h2>
  <p class="mb-3">[1-2 sentences]</p>
  <h2 class="text-base font-semibold text-surface-100 mb-2">Related Tools</h2>
  <p>Try our <a href="/[related-tool]/" class="text-primary hover:underline">[Related Tool Name]</a> for similar tasks.</p>
</div>

## REQUIREMENTS
- Each page: 150-250 words
- One internal link to a related tool per page
- Unique content per tool (no copy-paste)
- Don't touch existing <script> or widget code
- Preserve all existing Astro imports and markup

## ALSO: Update i18n
- Read src/i18n/utils.js - many tools already have "howto" text. Add howto for any tools that are missing it.
- Read src/i18n/zh.json - add matching Chinese howto translations.

## VERIFY
Run `npm run build` at the end. All 54 pages must build clean.
