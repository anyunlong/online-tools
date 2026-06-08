"use client"

import { useMemo, useState } from "react"
import { Search } from "lucide-react"
import { Input } from "@/components/ui/input"
import { ToolCard } from "@/components/tool-card"
import { categories, tools } from "@/lib/tools-data"

export function ToolsExplorer() {
  const [query, setQuery] = useState("")
  const [activeCategory, setActiveCategory] = useState<string | null>(null)

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    return tools.filter((tool) => {
      const matchesCategory = !activeCategory || tool.categoryId === activeCategory
      const matchesQuery =
        !q ||
        tool.name.toLowerCase().includes(q) ||
        tool.description.toLowerCase().includes(q)
      return matchesCategory && matchesQuery
    })
  }, [query, activeCategory])

  return (
    <section id="categories" className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      {/* Search */}
      <div className="relative mx-auto max-w-2xl">
        <Search className="pointer-events-none absolute left-4 top-1/2 size-5 -translate-y-1/2 text-muted-foreground" />
        <Input
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search for a tool..."
          aria-label="Search for a tool"
          className="h-14 rounded-xl border-border bg-card/60 pl-12 text-base shadow-sm backdrop-blur-sm focus-visible:ring-primary"
        />
      </div>

      {/* Category pills */}
      <div className="no-scrollbar -mx-4 mt-6 flex gap-2 overflow-x-auto px-4 pb-1">
        <button
          onClick={() => setActiveCategory(null)}
          className={`shrink-0 rounded-full border px-4 py-2 text-sm font-medium transition-colors ${
            activeCategory === null
              ? "border-primary bg-primary text-primary-foreground"
              : "border-border bg-secondary/60 text-muted-foreground hover:text-foreground"
          }`}
        >
          All
        </button>
        {categories.map((cat) => (
          <button
            key={cat.id}
            onClick={() => setActiveCategory(cat.id)}
            className={`flex shrink-0 items-center gap-1.5 rounded-full border px-4 py-2 text-sm font-medium transition-colors ${
              activeCategory === cat.id
                ? "border-primary bg-primary text-primary-foreground"
                : "border-border bg-secondary/60 text-muted-foreground hover:text-foreground"
            }`}
          >
            <span aria-hidden="true">{cat.emoji}</span>
            {cat.label}
          </button>
        ))}
      </div>

      {/* Tool grid */}
      <div id="tools" className="mt-8 scroll-mt-20">
        <div className="mb-5 flex items-baseline justify-between">
          <h2 className="text-2xl font-bold tracking-tight">All Tools</h2>
          <span className="text-sm text-muted-foreground">
            {filtered.length} {filtered.length === 1 ? "tool" : "tools"}
          </span>
        </div>

        {filtered.length > 0 ? (
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
            {filtered.map((tool) => (
              <ToolCard key={tool.name} tool={tool} />
            ))}
          </div>
        ) : (
          <div className="rounded-xl border border-dashed border-border py-16 text-center text-muted-foreground">
            No tools found for{" "}
            <span className="font-medium text-foreground">&ldquo;{query}&rdquo;</span>
          </div>
        )}
      </div>
    </section>
  )
}
