import { categories } from "@/lib/tools-data"

const toolLinks = [
  "Base64 Encoder",
  "JSON Formatter",
  "Password Generator",
  "Regex Tester",
  "SHA-256 Hash",
]

const companyLinks = ["About", "Contact", "Privacy", "Terms"]

export function SiteFooter() {
  return (
    <footer className="border-t border-border bg-card/30">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
          <div className="col-span-2 md:col-span-1">
            <a href="#" className="flex items-center gap-2 text-lg font-bold">
              <span className="flex size-8 items-center justify-center rounded-lg bg-gradient-to-br from-primary to-accent text-sm font-black text-primary-foreground">
                4
              </span>
              4uses
            </a>
            <p className="mt-3 max-w-xs text-sm leading-relaxed text-muted-foreground">
              50+ free online utilities for everyday tasks. No sign-up, no
              limits, fully private in your browser.
            </p>
          </div>

          <FooterColumn title="Tools" items={toolLinks} />
          <FooterColumn
            title="Categories"
            items={categories.slice(0, 6).map((c) => c.label)}
          />
          <FooterColumn title="Company" items={companyLinks} />
        </div>

        <div className="mt-10 border-t border-border pt-6 text-center text-sm text-muted-foreground">
          © {new Date().getFullYear()} 4uses. All rights reserved.
        </div>
      </div>
    </footer>
  )
}

function FooterColumn({ title, items }: { title: string; items: string[] }) {
  return (
    <div>
      <h3 className="text-sm font-semibold text-foreground">{title}</h3>
      <ul className="mt-3 space-y-2">
        {items.map((item) => (
          <li key={item}>
            <a
              href="#"
              className="text-sm text-muted-foreground transition-colors hover:text-foreground"
            >
              {item}
            </a>
          </li>
        ))}
      </ul>
    </div>
  )
}
