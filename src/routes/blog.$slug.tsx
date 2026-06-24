import { createFileRoute, Link, notFound } from "@tanstack/react-router";
import { ArrowLeft, Share2 } from "lucide-react";
import { getPostsAdmin } from "../api/posts";

export const Route = createFileRoute("/blog/$slug")({
  loader: async ({ params }) => {
    try {
      const { posts } = await getPostsAdmin();
      const post = posts.find((p: any) => p.slug === params.slug);
      if (!post) {
        throw notFound();
      }
      return { post };
    } catch (e) {
      throw notFound();
    }
  },
  head: ({ loaderData }) => {
    const post = loaderData?.post;
    if (!post) return {};
    return {
      meta: [
        { title: `${post.title} | Blog Martines` },
        { name: "description", content: post.excerpt },
        { property: "og:title", content: post.title },
        { property: "og:description", content: post.excerpt },
        ...(post.image ? [{ property: "og:image", content: post.image }] : []),
        { name: "twitter:card", content: "summary_large_image" },
      ],
    };
  },
  component: BlogPost,
});

interface Post {
  slug: string;
  title: string;
  excerpt: string;
  content: string;
  meta?: string;
  link?: string;
  image?: string;
  date?: string;
}

function BlogPost() {
  const { post } = Route.useLoaderData();

  if (!post) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-background px-4">
        <h1 className="text-4xl font-bold text-foreground">Post não encontrado</h1>
        <p className="mt-2 text-muted-foreground">O artigo que você está procurando não existe.</p>
        <Link to="/" className="mt-6 text-brand hover:underline flex items-center gap-2">
          <ArrowLeft className="w-4 h-4" /> Voltar para o início
        </Link>
      </div>
    );
  }

  // Como o conteúdo pode vir como markdown ou texto plano da IA, uma abordagem simples
  // é quebrar em parágrafos se não tiver tags HTML, ou usar dangerouslySetInnerHTML
  const renderContent = () => {
    if (!post.content) return null;
    // Se o N8N mandou com HTML/Markdown básico
    if (post.content.includes("<h2") || post.content.includes("<strong>")) {
      return (
        <div
          className="prose prose-invert max-w-none prose-brand text-muted-foreground leading-loose"
          dangerouslySetInnerHTML={{ __html: post.content }}
        />
      );
    }
    // Tratamento de quebra de linhas para texto puro com double newline
    return (
      <div className="text-lg text-muted-foreground leading-relaxed space-y-6">
        {post.content.split("\n\n").map((paragraph, i) => {
          if (paragraph.startsWith("# ")) {
            return (
              <h2 key={i} className="text-3xl font-bold text-foreground mt-12 mb-6">
                {paragraph.replace("# ", "")}
              </h2>
            );
          }
          if (paragraph.startsWith("## ")) {
            return (
              <h3 key={i} className="text-2xl font-bold text-foreground mt-10 mb-4">
                {paragraph.replace("## ", "")}
              </h3>
            );
          }
          return <p key={i}>{paragraph}</p>;
        })}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-background pb-24">
      {/* Navbar Minimalista */}
      <nav className="w-full border-b border-border bg-background/80 backdrop-blur sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-6 h-16 flex items-center justify-between">
          <Link
            to="/"
            className="text-muted-foreground hover:text-foreground transition flex items-center gap-2 text-sm font-medium"
          >
            <ArrowLeft className="w-4 h-4" /> Voltar
          </Link>
          <div className="flex gap-4">
            <button className="text-muted-foreground hover:text-brand transition">
              <Share2 className="w-4 h-4" />
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-4xl mx-auto px-6 mt-12 md:mt-20">
        {/* Header */}
        <header className="mb-12">
          <div className="flex items-center gap-3 mb-6">
            <span className="text-sm text-muted-foreground flex items-center gap-2">
              {post.date
                ? new Date(post.date).toLocaleDateString("pt-BR", {
                    day: "2-digit",
                    month: "long",
                    year: "numeric",
                    hour: "2-digit",
                    minute: "2-digit",
                  })
                : "Post recente"}
            </span>
          </div>
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-foreground tracking-tight leading-[1.1] mb-6">
            {post.title}
          </h1>
          <p className="text-xl text-muted-foreground leading-relaxed border-l-4 border-brand/50 pl-4">
            {post.excerpt}
          </p>
        </header>

        {/* Hero Image */}
        {post.image && (
          <div className="w-full aspect-video md:aspect-[21/9] rounded-2xl overflow-hidden mb-16 relative border border-border shadow-2xl">
            <img src={post.image} alt={post.title} className="w-full h-full object-cover" />
            <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
          </div>
        )}

        {/* Artigo */}
        <article className="max-w-3xl mx-auto">
          {renderContent()}

          {/* Fonte ABNT */}
          {post.link && post.link !== "#" && (
            <div className="mt-12 pt-6 border-t border-border/50">
              <h4 className="text-sm font-semibold text-foreground mb-2">Referências e Fontes</h4>
              <p className="text-xs text-muted-foreground leading-relaxed break-all">
                AUTOR DESCONHECIDO. <strong>{post.title}</strong>. Disponível em: &lt;
                <a
                  href={post.link}
                  target="_blank"
                  rel="noreferrer"
                  className="text-brand hover:underline"
                >
                  {post.link}
                </a>
                &gt;. Acesso em:{" "}
                {post.date
                  ? new Date(post.date).toLocaleDateString("pt-BR")
                  : new Date().toLocaleDateString("pt-BR")}
                .
              </p>
            </div>
          )}

          {/* Disclaimer IA */}
          <div className="mt-8 p-4 border-l-2 border-muted-foreground/30 bg-muted/20 text-muted-foreground text-sm flex items-start gap-3 rounded-r-lg">
            <span className="text-xl">🤖</span>
            <p>
              <strong>Transparência de Conteúdo:</strong> Esta reportagem foi rastreada, lida e
              roteirizada de forma 100% autônoma por nossos{" "}
              <em>Agentes de Inteligência Artificial</em>. A automação no centro da informação.
            </p>
          </div>

          {/* CTA OBRIGATÓRIO (Fallback de SEO) */}
          <div className="mt-20 p-8 rounded-2xl bg-brand/5 border border-brand/20 text-center relative overflow-hidden">
            <div className="absolute top-0 right-0 w-64 h-64 bg-brand/10 blur-[100px] rounded-full translate-x-1/2 -translate-y-1/2" />
            <h3 className="text-2xl font-bold text-foreground mb-4 relative z-10">
              Sua empresa ainda perde dinheiro com operações manuais?
            </h3>
            <p className="text-muted-foreground mb-8 relative z-10">
              A <strong>Martines Produtos Digitais</strong> cria hiperautomações inteligentes que
              acabam com a ineficiência. Agende uma consultoria e veja a IA trabalhar para você.
            </p>
            <a
              href="https://wa.me/5511954210088"
              target="_blank"
              rel="noreferrer"
              className="relative z-10 inline-flex h-12 items-center justify-center rounded-md bg-brand px-8 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-brand/90"
            >
              Falar com um Especialista
            </a>
          </div>
        </article>
      </main>
    </div>
  );
}
