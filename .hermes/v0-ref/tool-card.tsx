import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { categoryMap, type Tool } from "@/lib/tools-data"

export function ToolCard({ tool }: { tool: Tool }) {
  const category = categoryMap[tool.categoryId]
  return (
    <Card className="group flex flex-col gap-3 border-border bg-card/60 p-5 transition-all duration-200 hover:-translate-y-1 hover:border-primary/40 hover:bg-card hover:shadow-lg hover:shadow-primary/10">
      <div className="flex items-start justify-between gap-3">
        <span
          aria-hidden="true"
          className="flex size-11 items-center justify-center rounded-lg bg-secondary text-xl transition-colors group-hover:bg-primary/15"
        >
          {tool.emoji}
        </span>
        <Badge
          variant="secondary"
          className="bg-secondary/80 text-xs font-normal text-muted-foreground"
        >
          {category?.label}
        </Badge>
      </div>
      <div>
        <h3 className="text-base font-semibold text-foreground transition-colors group-hover:text-primary">
          {tool.name}
        </h3>
        <p className="mt-1 text-sm leading-relaxed text-muted-foreground">
          {tool.description}
        </p>
      </div>
    </Card>
  )
}
