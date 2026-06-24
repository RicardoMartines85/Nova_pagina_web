export function Footer() {
  const year = new Date().getFullYear();
  return (
    <footer className="border-t border-border bg-background">
      <div className="max-w-7xl mx-auto px-6 lg:px-10 py-14 grid md:grid-cols-4 gap-10">
        <div className="md:col-span-2">
          <img src="/logo.png" alt="Martines Produtos Digitais" className="h-12 w-auto" />
          <p className="mt-3 text-sm text-muted-foreground max-w-sm leading-relaxed">
            Engenharia de processos, hiperautomação e IA aplicada para empresas que já não cabem
            mais em planilhas.
          </p>
        </div>
        <div>
          <h4 className="text-xs uppercase tracking-widest text-foreground font-medium">
            Navegação
          </h4>
          <ul className="mt-4 space-y-2 text-sm text-muted-foreground">
            <li>
              <a href="#diagnostico" className="hover:text-foreground">
                O Diagnóstico
              </a>
            </li>
            <li>
              <a href="#sistemas" className="hover:text-foreground">
                Sistemas
              </a>
            </li>
            <li>
              <a href="#lideranca" className="hover:text-foreground">
                Insights
              </a>
            </li>
            <li>
              <a href="#contato" className="hover:text-foreground">
                Contato
              </a>
            </li>
          </ul>
        </div>
        <div>
          <h4 className="text-xs uppercase tracking-widest text-foreground font-medium">Contato</h4>
          <ul className="mt-4 space-y-2 text-sm text-muted-foreground">
            <li>
              <a href="http://wa.me/5511954210088" className="hover:text-foreground">
                WhatsApp Direto
              </a>
            </li>
            <li>
              <a href="mailto:contato@martines.halftech.com" className="hover:text-foreground">
                contato@martines.halftech.com
              </a>
            </li>
          </ul>
        </div>
      </div>
      <div className="border-t border-border">
        <div className="max-w-7xl mx-auto px-6 lg:px-10 py-6 flex flex-col md:flex-row items-center justify-between gap-3 text-xs text-muted-foreground">
          <p>© {year} Martines Produtos Digitais. Todos os direitos reservados.</p>
          <p>Tratamento de dados em conformidade com a LGPD (Lei 13.709/2018).</p>
        </div>
      </div>
    </footer>
  );
}
