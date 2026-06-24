import { HardHat, Boxes, MessageSquare, Plug } from "lucide-react";

const solutions = [
  {
    icon: HardHat,
    title: "RDO 100% Automatizado (Operacional)",
    desc: "O aplicativo definitivo para controle de campo. Preenchimento via celular, sincronização automática em nuvem e painéis gerenciais em tempo real. Esqueça o papel na sua operação.",
  },
  {
    icon: Boxes,
    title: "Máquina de Conteúdo com IA (Marketing)",
    desc: "Seu ecossistema de postagens 100% autônomo. Uma IA que pesquisa tendências do seu setor e publica artigos no seu blog, LinkedIn e Instagram automaticamente.",
  },
  {
    icon: MessageSquare,
    title: "Extração Inteligente de Dados (Backoffice)",
    desc: "Automação que lê documentos complexos (como projetos em PDF ou faturas) e extrai os dados exatos direto para o seu ERP, eliminando dias de digitação manual.",
  },
  {
    icon: Plug,
    title: "Integrações de Sistemas Legados (TI)",
    desc: "Conexão invisível entre seus softwares atuais (Protheus, SAP, CRMs) e fluxos modernos ágeis via integração de APIs.",
  },
];

export function Sistemas() {
  return (
    <section id="sistemas" className="py-24 md:py-32 border-t border-border bg-muted/30">
      <div className="max-w-7xl mx-auto px-6 lg:px-10">
        <div className="max-w-3xl">
          <p className="text-xs uppercase tracking-[0.18em] text-brand font-medium">
            Catálogo
          </p>
          <h2 className="mt-4 text-3xl md:text-5xl font-semibold tracking-tight text-foreground leading-[1.1]">
            Soluções Digitais "Plug and Play"{" "}
            <span className="text-muted-foreground">prontas para tracionar o seu negócio.</span>
          </h2>
          <p className="mt-4 text-base md:text-lg text-muted-foreground">
            Além de projetos sob medida, oferecemos ecossistemas validados para implementação imediata.
          </p>
        </div>

        <div className="mt-14 grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {solutions.map((s, i) => (
            <article
              key={s.title}
              className="group relative bg-background border border-border rounded-xl p-6 transition-all duration-300 hover:-translate-y-1 hover:border-brand/40 hover:shadow-[0_20px_40px_-20px_color-mix(in_oklab,var(--brand)_35%,transparent)]"
            >
              <div className="absolute top-6 right-6 text-xs text-muted-foreground/60 tabular-nums">
                0{i + 1}
              </div>
              <div className="h-11 w-11 rounded-lg bg-brand/10 text-brand grid place-items-center group-hover:bg-brand group-hover:text-brand-foreground transition">
                <s.icon className="h-5 w-5" strokeWidth={1.5} />
              </div>
              <h3 className="mt-6 text-lg font-semibold text-foreground tracking-tight">
                {s.title}
              </h3>
              <p className="mt-3 text-sm text-muted-foreground leading-relaxed">
                {s.desc}
              </p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
