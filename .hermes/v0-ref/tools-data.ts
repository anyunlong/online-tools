export type Category = {
  id: string
  label: string
  emoji: string
}

export type Tool = {
  name: string
  description: string
  categoryId: string
  emoji: string
  popular?: boolean
}

export const categories: Category[] = [
  { id: "encode", label: "Encode/Decode", emoji: "🔐" },
  { id: "hash", label: "Hash", emoji: "🔒" },
  { id: "text", label: "Text", emoji: "📝" },
  { id: "time", label: "Time", emoji: "⏰" },
  { id: "dev", label: "Dev Tools", emoji: "🛠" },
  { id: "convert", label: "Convert", emoji: "🔄" },
  { id: "formatter", label: "Formatter", emoji: "📋" },
  { id: "generator", label: "Generator", emoji: "✨" },
  { id: "security", label: "Security", emoji: "🛡" },
  { id: "design", label: "Design", emoji: "🎨" },
  { id: "image", label: "Image", emoji: "🖼" },
  { id: "math", label: "Math", emoji: "🔢" },
]

export const categoryMap = Object.fromEntries(
  categories.map((c) => [c.id, c]),
) as Record<string, Category>

export const tools: Tool[] = [
  // Encode/Decode
  { name: "Base64 Encoder", description: "Encode and decode Base64 strings", categoryId: "encode", emoji: "🔐", popular: true },
  { name: "URL Encoder", description: "Encode and decode URL components", categoryId: "encode", emoji: "🌐" },
  { name: "HTML Entity Encoder", description: "Convert characters to HTML entities", categoryId: "encode", emoji: "📄" },
  { name: "JWT Decoder", description: "Decode and inspect JSON Web Tokens", categoryId: "encode", emoji: "🎫", popular: true },

  // Hash
  { name: "MD5 Hash", description: "Generate MD5 hashes from text", categoryId: "hash", emoji: "🔑" },
  { name: "SHA-256 Hash", description: "Generate secure SHA-256 hashes", categoryId: "hash", emoji: "🔒", popular: true },
  { name: "Bcrypt Generator", description: "Hash passwords with bcrypt", categoryId: "hash", emoji: "🛡" },

  // Text
  { name: "Word Counter", description: "Count words, characters and lines", categoryId: "text", emoji: "📝" },
  { name: "Case Converter", description: "Convert between text cases instantly", categoryId: "text", emoji: "🔤" },
  { name: "Lorem Ipsum", description: "Generate placeholder dummy text", categoryId: "text", emoji: "📃" },
  { name: "Text Diff", description: "Compare two text blocks side by side", categoryId: "text", emoji: "🔍" },
  { name: "Remove Duplicates", description: "Remove duplicate lines from text", categoryId: "text", emoji: "🧹" },

  // Time
  { name: "Unix Timestamp", description: "Convert Unix timestamps to dates", categoryId: "time", emoji: "⏰", popular: true },
  { name: "Cron Parser", description: "Explain cron expressions in plain English", categoryId: "time", emoji: "📅" },
  { name: "Time Zone Converter", description: "Convert times across time zones", categoryId: "time", emoji: "🌍" },

  // Dev Tools
  { name: "Regex Tester", description: "Test and debug regular expressions", categoryId: "dev", emoji: "🛠", popular: true },
  { name: "UUID Generator", description: "Generate v4 UUIDs in bulk", categoryId: "dev", emoji: "🆔" },
  { name: "Diff Checker", description: "Compare code and files line by line", categoryId: "dev", emoji: "📊" },
  { name: "Cron Builder", description: "Build cron schedules visually", categoryId: "dev", emoji: "⚙️" },

  // Convert
  { name: "JSON to CSV", description: "Convert JSON data to CSV format", categoryId: "convert", emoji: "🔄" },
  { name: "YAML to JSON", description: "Convert YAML into JSON and back", categoryId: "convert", emoji: "📑" },
  { name: "Unit Converter", description: "Convert length, weight and volume", categoryId: "convert", emoji: "📏" },
  { name: "Color Converter", description: "Convert HEX, RGB, HSL color values", categoryId: "convert", emoji: "🎯" },

  // Formatter
  { name: "JSON Formatter", description: "Format and validate JSON beautifully", categoryId: "formatter", emoji: "📋", popular: true },
  { name: "SQL Formatter", description: "Beautify and indent SQL queries", categoryId: "formatter", emoji: "🗄" },
  { name: "XML Formatter", description: "Format and prettify XML documents", categoryId: "formatter", emoji: "📰" },
  { name: "CSS Beautifier", description: "Format and minify CSS code", categoryId: "formatter", emoji: "🎨" },

  // Generator
  { name: "Password Generator", description: "Create strong random passwords", categoryId: "generator", emoji: "✨", popular: true },
  { name: "QR Code Generator", description: "Generate QR codes from text or URLs", categoryId: "generator", emoji: "📱" },
  { name: "Fake Data Generator", description: "Generate realistic test data", categoryId: "generator", emoji: "🎲" },

  // Security
  { name: "Password Strength", description: "Check how strong your password is", categoryId: "security", emoji: "🛡" },
  { name: "SSL Checker", description: "Inspect SSL certificate details", categoryId: "security", emoji: "🔐" },
  { name: "Hash Identifier", description: "Identify hash types automatically", categoryId: "security", emoji: "🕵️" },

  // Design
  { name: "Color Picker", description: "Pick colors and copy values", categoryId: "design", emoji: "🎨" },
  { name: "Gradient Generator", description: "Create CSS gradients visually", categoryId: "design", emoji: "🌈" },
  { name: "Shadow Generator", description: "Build CSS box shadows with preview", categoryId: "design", emoji: "🪟" },
  { name: "Palette Generator", description: "Generate harmonious color palettes", categoryId: "design", emoji: "🖌" },

  // Image
  { name: "Image Compressor", description: "Compress images without quality loss", categoryId: "image", emoji: "🖼", popular: true },
  { name: "Image Resizer", description: "Resize images to exact dimensions", categoryId: "image", emoji: "📐" },
  { name: "Image to Base64", description: "Convert images to Base64 strings", categoryId: "image", emoji: "🔗" },
  { name: "Favicon Generator", description: "Generate favicons from any image", categoryId: "image", emoji: "⭐" },

  // Math
  { name: "Percentage Calculator", description: "Calculate percentages quickly", categoryId: "math", emoji: "🔢" },
  { name: "Number Base Converter", description: "Convert between binary, hex, decimal", categoryId: "math", emoji: "🧮" },
  { name: "Random Number", description: "Generate random numbers in a range", categoryId: "math", emoji: "🎰" },
  { name: "Scientific Calculator", description: "Advanced calculations made easy", categoryId: "math", emoji: "📐" },
]

export const popularTools = tools.filter((t) => t.popular)
