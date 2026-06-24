import { useState } from "react";

export function Contato() {
  const [sent, setSent] = useState(false);
  return (
    <section id="contato" className="py-24 md:py-32 border-t border-border bg-muted/30">
      <div className="max-w-4xl mx-auto px-6 lg:px-10">
        <div className="text-center max-w-2xl mx-auto">
          <p className="text-xs uppercase tracking-[0.18em] text-brand font-medium">
            Diagnóstico Operacional
          </p>
          <h2 className="mt-4 text-3xl md:text-5xl font-semibold tracking-tight text-foreground leading-[1.1]">
            Onde está o desperdício invisível da sua operação hoje?
          </h2>
          <p className="mt-5 text-muted-foreground text-base md:text-lg">
            30 minutos de call. Sem pitch chato de vendas. Saímos da conversa com um mapa preliminar dos seus gargalos operacionais e o ROI estimado para automatizar a sua empresa.
          </p>
        </div>

        <form
          onSubmit={async (e) => {
            e.preventDefault();
            const formData = new FormData(e.currentTarget);
            const data = Object.fromEntries(formData.entries());
            
            // O botão vira "Recebido" instantaneamente para boa UX
            setSent(true);
            
            try {
              // Webhook Oficial do n8n (Testes)
              await fetch("https://n8n.martines.halftech.com/webhook-test/martines_formulario", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data),
              });
            } catch (error) {
              console.error("Erro ao enviar formulário para o n8n", error);
            }
          }}
          className="mt-12 bg-background border border-border rounded-2xl p-6 md:p-10 grid gap-5"
        >
          <div className="grid md:grid-cols-2 gap-5">
            <Field label="Nome" name="nome" placeholder="Como devemos te chamar" />
            <Field
              label="E-mail Corporativo"
              name="email"
              type="email"
              placeholder="voce@empresa.com.br"
            />
          </div>
          <div className="grid md:grid-cols-2 gap-5">
            <Field label="WhatsApp" name="whatsapp" type="tel" placeholder="(11) 99999-9999" />
            <Field label="Cargo" name="cargo" placeholder="Diretor, C-Level, Sócio…" />
          </div>
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              Onde está o maior gargalo da sua empresa hoje?
            </label>
            <textarea
              rows={4}
              required
              placeholder="Descreva em poucas linhas o processo que mais consome tempo, dinheiro ou atenção."
              className="w-full rounded-lg border border-input bg-background px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-brand/40 focus:border-brand transition"
            />
          </div>
          <button
            type="submit"
            disabled={sent}
            className="mt-2 inline-flex justify-center items-center gap-2 rounded-md bg-foreground text-background px-6 py-3.5 text-sm md:text-base font-medium hover:bg-foreground/90 transition disabled:opacity-60"
          >
            {sent ? "Recebido — entraremos em contato em até 24h" : "🟢 Agendar Diagnóstico Agora"}
          </button>
          <p className="text-xs text-muted-foreground text-center">
            Seus dados são tratados sob LGPD. Sem listas de remarketing. Sem ruído.
          </p>
        </form>
      </div>
    </section>
  );
}

function Field({
  label,
  name,
  type = "text",
  placeholder,
}: {
  label: string;
  name: string;
  type?: string;
  placeholder?: string;
}) {
  return (
    <div>
      <label htmlFor={name} className="block text-sm font-medium text-foreground mb-2">
        {label}
      </label>
      <input
        id={name}
        name={name}
        type={type}
        required
        placeholder={placeholder}
        className="w-full rounded-lg border border-input bg-background px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-brand/40 focus:border-brand transition"
      />
    </div>
  );
}
