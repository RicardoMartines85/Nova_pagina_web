export function Diagnostico() {
  return (
    <section id="diagnostico" className="py-24 md:py-32 border-t border-border">
      <div className="max-w-7xl mx-auto px-6 lg:px-10 grid lg:grid-cols-2 gap-14 lg:gap-20 items-center">
        <div>
          <p className="text-xs uppercase tracking-[0.18em] text-brand font-medium">
            O Diferencial
          </p>
          <h2 className="mt-4 text-3xl md:text-5xl font-semibold tracking-tight text-foreground leading-[1.1]">
            Entender a pergunta é <span className="text-muted-foreground">50% da resposta.</span>
          </h2>
          <p className="mt-6 text-base md:text-lg text-muted-foreground leading-relaxed">
            Automatizar a bagunça só serve para gerar ineficiência em escala industrial. A
            Inteligência Artificial e a automação são amplificadores potentes, mas exigem direção
            clara. Atuamos como{" "}
            <span className="text-foreground font-medium">Business Translators</span>: entramos na
            sua operação, mapeamos o fluxo atual (As-Is) e desenhamos a transição exata para o
            modelo automatizado (To-Be).
          </p>
          <p className="mt-4 text-base md:text-lg text-muted-foreground leading-relaxed">
            Menos vaidade digital. Mais eficiência raiz.
          </p>

          <div className="mt-10 grid grid-cols-2 gap-6 max-w-md">
            <Stat k="As-Is" v="Mapeamento" />
            <Stat k="To-Be" v="Desenho" />
            <Stat k="ROI" v="Validação" />
            <Stat k="n8n + IA" v="Execução" />
          </div>
        </div>

        <FlowDiagram />
      </div>
    </section>
  );
}

function Stat({ k, v }: { k: string; v: string }) {
  return (
    <div className="border-l-2 border-border pl-4">
      <div className="text-xs text-muted-foreground">{v}</div>
      <div className="text-lg font-semibold text-foreground">{k}</div>
    </div>
  );
}

function FlowDiagram() {
  return (
    <div className="relative aspect-square w-full max-w-lg mx-auto rounded-xl border border-border bg-card p-6 overflow-hidden">
      <div className="absolute inset-0 grid-bg opacity-50" />
      <svg viewBox="0 0 400 400" className="relative h-full w-full">
        {/* Chaos cluster */}
        <g className="text-muted-foreground">
          {[...Array(7)].map((_, i) => (
            <rect
              key={i}
              x={20 + (i % 3) * 22}
              y={40 + Math.floor(i / 3) * 26}
              width={36}
              height={18}
              rx={3}
              fill="none"
              stroke="currentColor"
              strokeWidth={1}
              opacity={0.5}
              transform={`rotate(${((i * 37) % 18) - 9} ${40 + (i % 3) * 22} ${50 + Math.floor(i / 3) * 26})`}
            />
          ))}
        </g>
        <text
          x="20"
          y="170"
          className="fill-muted-foreground text-[10px] uppercase tracking-widest"
        >
          As-Is · Caos
        </text>

        {/* Connecting flow */}
        <path
          d="M 130 100 C 200 100, 200 300, 280 300"
          fill="none"
          stroke="var(--brand)"
          strokeWidth={1.5}
          className="animate-flow"
        />
        <path
          d="M 130 130 C 220 130, 180 270, 280 270"
          fill="none"
          stroke="var(--brand)"
          strokeWidth={1.5}
          className="animate-flow"
          style={{ animationDelay: "0.5s" }}
        />

        {/* Order grid */}
        <g>
          {[0, 1, 2].map((row) =>
            [0, 1, 2].map((col) => (
              <rect
                key={`${row}-${col}`}
                x={260 + col * 38}
                y={240 + row * 38}
                width={30}
                height={30}
                rx={4}
                fill="var(--brand)"
                opacity={0.08 + (row + col) * 0.08}
                stroke="var(--brand)"
                strokeWidth={1}
              />
            )),
          )}
        </g>
        <text
          x="260"
          y="385"
          className="fill-foreground text-[10px] uppercase tracking-widest font-medium"
        >
          To-Be · Ordem
        </text>

        {/* Pulse node */}
        <circle cx="280" cy="285" r="6" fill="var(--brand)">
          <animate attributeName="r" values="6;10;6" dur="2s" repeatCount="indefinite" />
          <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite" />
        </circle>
      </svg>
    </div>
  );
}
