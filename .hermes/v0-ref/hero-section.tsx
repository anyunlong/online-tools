import { buttonVariants } from "@/components/ui/button"
import { ArrowRight, Flame } from "lucide-react"
import { cn } from "@/lib/utils"

const stats = [
  { value: "50+", label: "Tools" },
  { value: "100%", label: "Free" },
  { value: "No", label: "Registration" },
]

export function HeroSection() {
  return (
    <section className="relative overflow-hidden">
      {/* subtle background glow */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 -z-10"
        style={{
          backgroundImage:
            "radial-gradient(60% 50% at 50% 0%, oklch(0.62 0.21 285 / 0.18), transparent 70%)",
        }}
      />
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 -z-10 opacity-[0.04]"
        style={{
          backgroundImage:
            "linear-gradient(to right, white 1px, transparent 1px), linear-gradient(to bottom, white 1px, transparent 1px)",
          backgroundSize: "48px 48px",
        }}
      />

      <div className="mx-auto max-w-4xl px-4 py-20 text-center sm:px-6 sm:py-28 lg:px-8">
        <span className="inline-flex items-center gap-2 rounded-full border border-border bg-secondary/60 px-3 py-1 text-xs font-medium text-muted-foreground">
          <Flame className="size-3.5 text-accent" />
          50+ free utilities, always growing
        </span>

        <h1 className="mt-6 text-balance text-4xl font-bold tracking-tight sm:text-5xl lg:text-6xl">
          <span className="gradient-text">Free Online Tools</span>
          <br />
          for Everyday Tasks
        </h1>

        <p className="mx-auto mt-5 max-w-xl text-pretty text-lg leading-relaxed text-muted-foreground">
          50+ free utilities — no sign-up, no limits. Encode, format, convert
          and generate, all in your browser.
        </p>

        <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
          <a
            href="#tools"
            className={cn(
              buttonVariants({ size: "lg" }),
              "h-12 w-full px-6 text-base sm:w-auto",
            )}
          >
            Explore Tools
            <ArrowRight className="size-4" />
          </a>
          <a
            href="#featured"
            className={cn(
              buttonVariants({ size: "lg", variant: "secondary" }),
              "h-12 w-full px-6 text-base sm:w-auto",
            )}
          >
            Popular Tools
          </a>
        </div>

        <dl className="mx-auto mt-14 grid max-w-lg grid-cols-3 gap-4">
          {stats.map((s) => (
            <div
              key={s.label}
              className="rounded-xl border border-border bg-card/50 px-4 py-5 backdrop-blur-sm"
            >
              <dt className="text-2xl font-bold text-foreground sm:text-3xl">{s.value}</dt>
              <dd className="mt-1 text-sm text-muted-foreground">{s.label}</dd>
            </div>
          ))}
        </dl>
      </div>
    </section>
  )
}
