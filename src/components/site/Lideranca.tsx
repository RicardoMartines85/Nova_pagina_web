import { useEffect, useState } from "react";
import { Link } from "@tanstack/react-router";

const staticPosts = [
  {
    title: "Por que 87% dos projetos de IA corporativa falham no terceiro mês",
    excerpt:
      "Não é o modelo. É o processo. Um framework para evitar a armadilha do POC eterno.",
    meta: "8 min de leitura · Estratégia",
    link: "#"
  },
  {
    title: "De 14 planilhas a um único fluxo: redução de 72% no ciclo de aprovação",
    excerpt:
      "Estudo de caso real: indústria de médio porte, integração ERP legado + n8n + IA.",
    meta: "12 min de leitura · Caso",
    link: "#"
  },
  {
    title: "As-Is, To-Be e o erro de pular o mapeamento operacional",
    excerpt:
      "Como Business Translators traduzem o caos invisível em arquitetura executável.",
    meta: "6 min de leitura · Método",
    link: "#"
  },
];

interface Post {
  slug?: string;
  title: string;
  excerpt: string;
  meta?: string;
  link?: string;
  image?: string;
  date?: string;
}

export function Lideranca() {
  const [posts, setPosts] = useState<Post[]>(staticPosts);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await fetch("/blog_data/posts.json");
        if (response.ok) {
          const data = await response.json();
          if (Array.isArray(data) && data.length > 0) {
            setPosts(data);
          } else if (data.posts && Array.isArray(data.posts) && data.posts.length > 0) {
             setPosts(data.posts);
          }
        }
      } catch (error) {
        console.error("Erro ao carregar posts do N8N. Usando fallback.", error);
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();
  }, []);

  return (
    <section id="lideranca" className="py-24 md:py-32 border-t border-border">
      <div className="max-w-7xl mx-auto px-6 lg:px-10">
        <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-6">
          <div className="max-w-2xl">
            <p className="text-xs uppercase tracking-[0.18em] text-brand font-medium">
              Insights
            </p>
            <h2 className="mt-4 text-3xl md:text-5xl font-semibold tracking-tight text-foreground leading-[1.1]">
              Liderança de Pensamento
            </h2>
            <p className="mt-4 text-muted-foreground text-base md:text-lg">
              Insights práticos sobre eficiência, tecnologia e processos.
            </p>
          </div>
        </div>

        <div className="mt-14 grid md:grid-cols-3 gap-6">
          {posts.map((p, index) => {
            const isInternal = !!p.slug;
            
            const cardContent = (
              <>
              <div className="aspect-[16/10] bg-gradient-to-br from-muted to-accent relative overflow-hidden">
                {p.image ? (
                  <img src={p.image} alt={p.title} className="absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" />
                ) : (
                  <div className="absolute inset-0 grid-bg opacity-60" />
                )}
                <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              </div>
              <div className="p-6 flex-1 flex flex-col">
                <div className="mb-2 text-[11px] font-medium text-muted-foreground uppercase tracking-wider">
                  {p.date ? new Date(p.date).toLocaleDateString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' }).replace(',', ' às') : "Post recente"}
                </div>
                <h3 className="text-lg font-semibold text-foreground tracking-tight leading-snug group-hover:text-brand transition">
                  {p.title}
                </h3>
                <p className="mt-3 text-sm text-muted-foreground leading-relaxed flex-1">
                  {p.excerpt}
                </p>

                <div className="mt-6 pt-4 border-t border-border text-xs text-brand font-medium group-hover:underline">
                  {isInternal ? "Ler material completo →" : (p.link && p.link !== "#" ? "Ler notícia externa →" : (p.meta || "Em breve"))}
                </div>
              </div>
              </>
            );

            return isInternal ? (
              <Link
                key={index}
                to={`/blog/${p.slug}`}
                className="group bg-card border border-border rounded-xl overflow-hidden flex flex-col transition hover:border-brand/40"
              >
                {cardContent}
              </Link>
            ) : (
              <a
                key={index}
                href={p.link || "#"}
                target={p.link && p.link !== "#" ? "_blank" : "_self"}
                rel="noreferrer"
                className="group bg-card border border-border rounded-xl overflow-hidden flex flex-col transition hover:border-brand/40"
              >
                {cardContent}
              </a>
            );
          })}
        </div>
      </div>
    </section>
  );
}
