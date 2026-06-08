import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { categoryMap, popularTools } from "@/lib/tools-data"
import { ArrowRight } from "lucide-react"

export function FeaturedTools() {
  return (
    <section id="featured" className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
      <div className="mb-6">
        <h2 className="text-2xl font-bold tracking-tight">Most Popular</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          The tools our users reach for the most.
        </p>
      </div>

      <div className="no-scrollbar -mx-4 flex snap-x snap-mandatory gap-4 overflow-x-auto px-4 pb-2">
        {popularTools.map((tool) => (
          <Card
            key={tool.name}
            className="flex w-72 shrink-0 snap-start flex-col gap-4 border-border bg-gradient-to-b from-card to-card/40 p-6"
          >
            <span
              aria-hidden="true"
              className="flex size-14 items-center justify-center rounded-xl bg-primary/15 text-3xl"
            >
              {tool.emoji}
            </span>
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-foreground">{tool.name}</h3>
              <p className="mt-1.5 text-sm leading-relaxed text-muted-foreground">
                {tool.description}. Fast, private and free to use right in your browser.
              </p>
            </div>
            <Button variant="secondary" className="w-full">
              Use Now
              <ArrowRight className="size-4" />
            </Button>
            <span className="text-xs text-muted-foreground">
              {categoryMap[tool.categoryId]?.emoji} {categoryMap[tool.categoryId]?.label}
            </span>
          </Card>
        ))}
      </div>
    </section>
  )
}
