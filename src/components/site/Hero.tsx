export function Hero() {
  return (
    <section id="top" className="relative pt-32 pb-20 md:pt-40 md:pb-28 overflow-hidden bg-[#faf9f6] dark:bg-[#1a1918]">
      <div className="absolute inset-0 grid-bg pointer-events-none opacity-40 dark:opacity-20" aria-hidden />
      
      <div className="relative max-w-7xl mx-auto px-6 lg:px-10">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-8 items-center">
          
          {/* Coluna 1: Texto e CTA */}
          <div className="text-center lg:text-left max-w-2xl mx-auto lg:mx-0">
            <div className="inline-flex items-center gap-2 rounded-full border border-border bg-background/60 px-3 py-1 text-xs text-muted-foreground animate-fade-up">
              <span className="relative flex h-1.5 w-1.5">
                <span className="absolute inset-0 rounded-full bg-signal animate-ping opacity-60" />
                <span className="relative inline-flex h-1.5 w-1.5 rounded-full bg-signal" />
              </span>
              Engenharia de Processos & Hiperautomação B2B
            </div>

            <h1 className="mt-8 text-4xl sm:text-5xl lg:text-6xl font-semibold tracking-tight text-foreground leading-[1.1] animate-fade-up [animation-delay:80ms]">
              Sua empresa não precisa de
              <br className="hidden sm:block" />{" "}
              <span className="text-muted-foreground">mais sistemas.</span>
              <br />
              Ela precisa de{" "}
              <span className="text-brand font-bold">
                processos integrados.
              </span>
            </h1>

            <p className="mt-6 text-base md:text-lg text-muted-foreground leading-relaxed animate-fade-up [animation-delay:160ms]">
              O desperdício invisível está sangrando a margem do seu negócio através de planilhas
              paralelas, digitação manual e falhas de comunicação. Nós desenhamos a transformação
              digital da sua operação e implementamos motores de automação sob medida.
            </p>

            <div className="mt-10 flex flex-col lg:flex-row items-center lg:items-start gap-4 animate-fade-up [animation-delay:240ms]">
              <a
                href="#contato"
                className="group inline-flex items-center gap-2 rounded-md bg-brand text-brand-foreground px-6 py-3.5 text-sm md:text-base font-medium hover:bg-brand/90 transition shadow-[0_8px_30px_-12px_color-mix(in_oklab,var(--brand)_50%,transparent)]"
              >
                🟢 Solicitar Diagnóstico Operacional Sem Custo
                <span className="transition group-hover:translate-x-0.5">→</span>
              </a>
            </div>
            <p className="mt-3 text-xs text-muted-foreground text-center lg:text-left animate-fade-up [animation-delay:280ms]">
              Uma análise estratégica de 30 minutos focada em gargalos e ROI real.
            </p>
          </div>

          {/* Coluna 2: Imagem do Dashboard na Mesa */}
          <div className="w-full relative animate-fade-up [animation-delay:320ms]">
            <img 
              src="/hero-dashboard.png" 
              alt="Sistema de Gestão Operacional e Dashboard de Construção em funcionamento num monitor"
              className="w-full h-auto rounded-lg shadow-[0_10px_25px_rgba(0,0,0,0.05)] object-cover"
            />
          </div>

        </div>
      </div>
    </section>
  );
}
