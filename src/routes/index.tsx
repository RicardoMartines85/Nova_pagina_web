import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { Navbar } from "@/components/site/Navbar";
import { Hero } from "@/components/site/Hero";
import { Diagnostico } from "@/components/site/Diagnostico";
import { Sistemas } from "@/components/site/Sistemas";
import { Lideranca } from "@/components/site/Lideranca";
import { Contato } from "@/components/site/Contato";
import { Footer } from "@/components/site/Footer";
import { WhatsappFab } from "@/components/site/WhatsappFab";
import { RestrictedModal } from "@/components/site/RestrictedModal";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      {
        title:
          "Consultoria em Transformação Digital e Hiperautomação B2B | Martines",
      },
      {
        name: "description",
        content:
          "Elimine o trabalho manual e integre seus sistemas. Consultoria em transformação digital, hiperautomação de processos e soluções em IA para empresas.",
      },
      {
        property: "og:title",
        content:
          "Consultoria em Transformação Digital e Hiperautomação B2B | Martines",
      },
      {
        property: "og:description",
        content:
          "Elimine o trabalho manual e integre seus sistemas. Consultoria em transformação digital, hiperautomação de processos e soluções em IA para empresas.",
      },
      { property: "og:type", content: "website" },
    ],
    links: [
      { rel: "canonical", href: "/" },
      {
        rel: "preconnect",
        href: "https://fonts.googleapis.com",
      },
      {
        rel: "preconnect",
        href: "https://fonts.gstatic.com",
        crossOrigin: "anonymous",
      },
      {
        rel: "stylesheet",
        href: "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
      },
    ],
  }),
  component: Index,
});

function Index() {
  const [restrictedOpen, setRestrictedOpen] = useState(false);
  return (
    <main className="min-h-screen bg-background text-foreground antialiased">
      <Navbar onOpenRestricted={() => setRestrictedOpen(true)} />
      <Hero />
      <Diagnostico />
      <Sistemas />
      <Lideranca />
      <Contato />
      <Footer />
      <WhatsappFab />
      <RestrictedModal
        open={restrictedOpen}
        onClose={() => setRestrictedOpen(false)}
      />
    </main>
  );
}
