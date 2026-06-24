export function Hero() {
  return (
    <section id="top" className="relative pt-36 pb-24 md:pt-44 md:pb-32 overflow-hidden bg-[#faf9f6] dark:bg-[#1a1918]">
      <div className="absolute inset-0 grid-bg pointer-events-none" aria-hidden />
      <div className="relative max-w-5xl mx-auto px-6 lg:px-10 text-center">
        <div className="inline-flex items-center gap-2 rounded-full border border-border bg-muted/60 px-3 py-1 text-xs text-muted-foreground animate-fade-up">
          <span className="relative flex h-1.5 w-1.5">
            <span className="absolute inset-0 rounded-full bg-signal animate-ping opacity-60" />
            <span className="relative inline-flex h-1.5 w-1.5 rounded-full bg-signal" />
          </span>
          Engenharia de Processos &amp; Hiperautomação de Processos
        </div>

        <h1 className="mt-8 text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-semibold tracking-tight text-foreground leading-[1.05] animate-fade-up [animation-delay:80ms]">
          Sua empresa não precisa de
          <br className="hidden sm:block" />{" "}
          <span className="text-muted-foreground">mais sistemas.</span>
          <br />
          Ela precisa de{" "}
          <span className="relative inline-block">
            processos integrados.
            <span className="absolute -bottom-1 left-0 right-0 h-[3px] bg-brand/70 rounded-full" />
          </span>
        </h1>

        <p className="mt-8 max-w-2xl mx-auto text-base md:text-lg text-muted-foreground leading-relaxed animate-fade-up [animation-delay:160ms]">
          O desperdício invisível está sangrando a margem do seu negócio através de planilhas
          paralelas, digitação manual e falhas de comunicação. Nós desenhamos a transformação
          digital da sua operação e implementamos motores de automação sob medida via n8n e IA. Sem
          travar sua equipe, sem licenças abusivas.
        </p>

        <div className="mt-10 flex flex-col items-center gap-3 animate-fade-up [animation-delay:240ms]">
          <a
            href="#contato"
            className="group inline-flex items-center gap-2 rounded-md bg-foreground text-background px-6 py-3.5 text-sm md:text-base font-medium hover:bg-foreground/90 transition shadow-[0_8px_30px_-12px_color-mix(in_oklab,var(--brand)_50%,transparent)]"
          >
            🟢 Solicitar Diagnóstico Operacional Sem Custo
            <span className="transition group-hover:translate-x-0.5">→</span>
          </a>
          <p className="text-xs text-muted-foreground">
            Uma análise estratégica de 30 minutos focada em gargalos e ROI real.
          </p>
        </div>

        <div className="mt-16 md:mt-20 w-full max-w-5xl mx-auto px-2 sm:px-0 animate-fade-up [animation-delay:320ms]">
          <div className="relative rounded-xl p-1.5 md:p-2.5 bg-foreground/5 border border-border/40 shadow-[0_10px_25px_rgba(0,0,0,0.05)] backdrop-blur-sm">
            <img 
              src="/hero-dashboard.png" 
              alt="Sistema de Gestão Operacional e Dashboard de Construção em funcionamento num monitor"
              className="w-full h-auto rounded-md shadow-sm object-cover"
            />
          </div>
        </div>
      </div>
    </section>
  );
}
