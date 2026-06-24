# Mapa de Arquitetura: Página Web Martines

Este documento mapeia exclusivamente o site institucional de Produtos Digitais (Landing Page), seu Motor SEO de Blog e Ferramentas Internas.

## 1. Landing Page (Frontend e Backend Integrado)

- **Tecnologia:** React com TanStack Start (SSR/SSG), TailwindCSS e Shadcn UI.
- **Repositório Base:** `Pagina web`
- **Porta no Servidor:** `:8082` (ou porta exclusiva destinada à Institucional).
- **Hospedagem:** VPS `216.22.43.39` gerenciado via Nginx Proxy Manager.
- **Páginas Principais:**
  - `/` -> Página de Vendas focada em captação de Leads B2B.
  - `/blog/$slug` -> Rota Dinâmica que puxa e renderiza matérias automaticamente sem banco de dados complexo (apenas via JSON).

## 2. A Máquina de Conteúdo: A "Agência Fantasma" (Automação n8n)

A Landing Page possui um braço de Inteligência Artificial avançado que funciona como uma agência de marketing autônoma.

- **Arquitetura Desacoplada:** Todo o workflow de curadoria (Google News), redação (Groq/LLaMA3), design (Leonardo AI + n8n) e distribuição omnichannel (Site, LinkedIn e Instagram) foi documentado separadamente.
- **Documentação Exclusiva:** Veja o arquivo `../Agencia fantasma/mapa_do_fantasma.md` para o passo a passo de como clonar, ajustar credenciais e gerenciar a API da Meta (Instagram Graph API) e ImgBB para novos clientes.

## 3. Painel Administrativo (Área Restrita)

Ao acessar a rota de Dashboard no site, temos uma torre de controle:

### Motor de Analytics

- **Mecanismo:** Script nativo de RPC (Remote Procedure Call) no TanStack que aciona na rota raiz (`__root.tsx`). Registra os IPs e datas no arquivo `/opt/blog_data/analytics.json`.
- **Gráficos (Recharts):** Demonstra de forma fluida os últimos 30 dias de tráfego (visitas acumuladas) e o horário de maior pico do site.

### Gestor de Blog e IA

- **Deleção Expressa:** O administrador visualiza todas as matérias criadas pela Inteligência Artificial e, com um botão, pode limpar o JSON e excluir a página do site (sem precisar entrar no servidor Linux).
- **Atalho de Ecossistema:** Links rápidos para o N8N da empresa, Proxy Manager, Evolution API e portais RDO.
