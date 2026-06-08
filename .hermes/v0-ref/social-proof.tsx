const stats = [
  { value: "100K+", label: "Monthly Users" },
  { value: "50+", label: "Tools Available" },
  { value: "4.9★", label: "Average Rating" },
]

export function SocialProof() {
  return (
    <section id="about" className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
      <div className="rounded-2xl border border-border bg-card/40 p-8 text-center sm:p-12">
        <p className="text-sm font-medium uppercase tracking-wider text-muted-foreground">
          Trusted by developers worldwide
        </p>
        <div className="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-3">
          {stats.map((s) => (
            <div key={s.label}>
              <div className="gradient-text text-4xl font-bold tracking-tight sm:text-5xl">
                {s.value}
              </div>
              <div className="mt-2 text-sm text-muted-foreground">{s.label}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
