import { useEffect, useState } from "react";
import { Menu, X, Moon, Sun } from "lucide-react";
import { useTheme } from "@/hooks/use-theme";

const links = [
  { href: "#diagnostico", label: "O Diagnóstico" },
  { href: "#sistemas", label: "Sistemas Desenvolvidos" },
  { href: "#lideranca", label: "Liderança de Pensamento" },
  { href: "#blog", label: "Blog" },
];

export function Navbar({ onOpenRestricted }: { onOpenRestricted: () => void }) {
  const { theme, toggle } = useTheme();
  const [open, setOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12);
    onScroll();
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header
      className={`fixed top-0 inset-x-0 z-40 transition-all duration-300 ${
        scrolled ? "backdrop-blur-xl bg-background/75 border-b border-border" : "bg-transparent"
      }`}
    >
      <nav className="max-w-7xl mx-auto px-6 lg:px-10 h-16 flex items-center justify-between">
        <a href="#top" className="flex items-center gap-2 tracking-tight">
          <img src="/logo.png" alt="Martines Produtos Digitais" className="h-9 w-auto" />
        </a>

        <ul className="hidden md:flex items-center gap-9 text-sm text-muted-foreground">
          {links.map((l) => (
            <li key={l.href}>
              <a href={l.href} className="hover:text-foreground transition-colors">
                {l.label}
              </a>
            </li>
          ))}
        </ul>

        <div className="flex items-center gap-1.5">
          <button
            onClick={toggle}
            aria-label="Alternar tema"
            className="h-9 w-9 grid place-items-center rounded-md hover:bg-accent text-muted-foreground hover:text-foreground transition"
          >
            {theme === "light" ? <Moon className="h-4 w-4" /> : <Sun className="h-4 w-4" />}
          </button>
          <button
            onClick={onOpenRestricted}
            className="hidden md:inline-flex h-9 px-3 items-center text-sm text-foreground hover:text-brand transition"
          >
            Área Restrita
          </button>
          <button
            onClick={() => setOpen((v) => !v)}
            aria-label="Abrir menu"
            className="md:hidden h-9 w-9 grid place-items-center rounded-md hover:bg-accent text-foreground"
          >
            {open ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>
        </div>
      </nav>

      {open && (
        <div className="md:hidden border-t border-border bg-background">
          <ul className="px-6 py-4 space-y-3">
            {links.map((l) => (
              <li key={l.href}>
                <a
                  href={l.href}
                  onClick={() => setOpen(false)}
                  className="block py-1.5 text-sm text-foreground"
                >
                  {l.label}
                </a>
              </li>
            ))}
            <li>
              <button
                onClick={() => {
                  setOpen(false);
                  onOpenRestricted();
                }}
                className="block py-1.5 text-sm text-foreground"
              >
                Área Restrita
              </button>
            </li>
          </ul>
        </div>
      )}
    </header>
  );
}
