import { createFileRoute } from "@tanstack/react-router";
import {
  Shield,
  ChevronRight,
  Settings,
  Webhook,
  Activity,
  LayoutDashboard,
  Cpu,
  HardDrive,
  Server,
  Folder,
  ShieldCheck,
  BarChart3,
  Trash2,
  FileText,
} from "lucide-react";
import { useState, useEffect } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  CartesianGrid,
} from "recharts";
import { getAnalyticsData } from "../api/tracking";
import { getPostsAdmin, deletePost } from "../api/posts";

export const Route = createFileRoute("/area_restrita")({
  component: AreaRestrita,
});

function AreaRestrita() {
  const [activeFolder, setActiveFolder] = useState<string | null>(null);
  const [dailyData, setDailyData] = useState<any[]>([]);
  const [hourlyData, setHourlyData] = useState<any[]>([]);
  const [postsAdmin, setPostsAdmin] = useState<any[]>([]);

  useEffect(() => {
    const fetchAnalytics = async () => {
      // 1. Fetch Analytics
      const { visits } = await getAnalyticsData();

      const daysMap: Record<string, number> = {};
      const hoursMap: Record<string, number> = {};

      for (let i = 0; i < 24; i++) hoursMap[`${i}h`] = 0;

      visits.forEach((v) => {
        daysMap[v.date] = (daysMap[v.date] || 0) + 1;
        const hour = new Date(v.timestamp).getHours();
        hoursMap[`${hour}h`] += 1;
      });

      const daily = Object.keys(daysMap)
        .sort()
        .slice(-30)
        .map((date) => ({ date: date.split("-").slice(1).join("/"), visitas: daysMap[date] }));

      const hourly = Object.keys(hoursMap).map((hour) => ({ hora: hour, acessos: hoursMap[hour] }));

      if (daily.length === 0) daily.push({ date: "Hoje", visitas: 0 });

      setDailyData(daily);
      setHourlyData(hourly);

      // 2. Fetch Posts Admin
      const { posts } = await getPostsAdmin();
      setPostsAdmin(posts);
    };
    fetchAnalytics();
  }, []);

  const handleDeletePost = async (slug: string) => {
    if (
      confirm("Tem certeza que deseja apagar essa reportagem? Ela sumirá do site imediatamente.")
    ) {
      const res = await deletePost({ data: { slug } });
      if (res.success) {
        setPostsAdmin(postsAdmin.filter((p) => p.slug !== slug));
        alert("Reportagem excluída com sucesso!");
      } else {
        alert("Erro ao excluir: " + res.error);
      }
    }
  };

  return (
    <div className="min-h-screen bg-[#0B1120] text-white flex font-sans">
      {/* Sidebar */}
      <aside className="w-64 bg-[#111827] border-r border-[#1F2937] flex flex-col hidden md:flex">
        <div className="p-6 flex items-center justify-center border-b border-[#1F2937]">
          <img src="/logo.png" alt="Logo" className="h-10" />
        </div>
        <nav className="p-4 flex-1 flex flex-col gap-2">
          <button className="w-full flex items-center gap-3 bg-[#1F2937] text-white px-4 py-3 rounded-lg border-l-4 border-green-500 font-medium">
            <LayoutDashboard className="h-5 w-5" />
            Dashboard
          </button>
        </nav>
        <div className="p-4 border-t border-[#1F2937]">
          <a
            href="/"
            className="w-full flex items-center gap-3 text-gray-400 hover:text-white px-4 py-3 rounded-lg hover:bg-[#1F2937] transition-colors"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="lucide lucide-log-out"
            >
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
              <polyline points="16 17 21 12 16 7" />
              <line x1="21" x2="9" y1="12" y2="12" />
            </svg>
            Sair
          </a>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-6 lg:p-10 overflow-y-auto">
        <div className="max-w-6xl mx-auto space-y-8 animate-fade-up">
          {/* Header */}
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Olá, Ricardo! 👋</h1>
            <p className="text-gray-400 mt-1">
              Aqui está o resumo da sua infraestrutura digital e monitoramento de tráfego.
            </p>
          </div>

          {/* Analytics Dashboard */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <BarChart3 className="h-5 w-5 text-brand" />
              <h2 className="text-xl font-bold">Monitoramento de Tráfego SEO</h2>
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-6">
                <h3 className="text-sm font-medium text-gray-400 mb-6">
                  Visitas Diárias (Últimos 30 dias)
                </h3>
                <div className="h-64 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={dailyData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" vertical={false} />
                      <XAxis
                        dataKey="date"
                        stroke="#6B7280"
                        fontSize={12}
                        tickLine={false}
                        axisLine={false}
                      />
                      <YAxis stroke="#6B7280" fontSize={12} tickLine={false} axisLine={false} />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: "#111827",
                          borderColor: "#1F2937",
                          borderRadius: "8px",
                        }}
                        itemStyle={{ color: "#10B981" }}
                      />
                      <Bar dataKey="visitas" fill="#10B981" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-6">
                <h3 className="text-sm font-medium text-gray-400 mb-6">
                  Pico de Acessos por Horário (24h)
                </h3>
                <div className="h-64 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={hourlyData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" vertical={false} />
                      <XAxis
                        dataKey="hora"
                        stroke="#6B7280"
                        fontSize={12}
                        tickLine={false}
                        axisLine={false}
                      />
                      <YAxis stroke="#6B7280" fontSize={12} tickLine={false} axisLine={false} />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: "#111827",
                          borderColor: "#1F2937",
                          borderRadius: "8px",
                        }}
                        itemStyle={{ color: "#3B82F6" }}
                      />
                      <Line
                        type="monotone"
                        dataKey="acessos"
                        stroke="#3B82F6"
                        strokeWidth={3}
                        dot={{ r: 4, fill: "#3B82F6", strokeWidth: 0 }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          </div>

          {/* Metrics */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-6">
              <div className="flex justify-between items-center mb-4">
                <div className="flex items-center gap-2 text-gray-400">
                  <Cpu className="h-4 w-4" />
                  <span className="text-sm font-medium">CPU</span>
                </div>
                <span className="text-xl font-bold">1.7%</span>
              </div>
              <div className="h-2 w-full bg-gray-800 rounded-full overflow-hidden">
                <div className="h-full bg-blue-500 rounded-full" style={{ width: "1.7%" }}></div>
              </div>
            </div>

            <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-6">
              <div className="flex justify-between items-center mb-4">
                <div className="flex items-center gap-2 text-gray-400">
                  <HardDrive className="h-4 w-4" />
                  <span className="text-sm font-medium">RAM Global</span>
                </div>
                <span className="text-xl font-bold">33.9%</span>
              </div>
              <div className="h-2 w-full bg-gray-800 rounded-full overflow-hidden">
                <div className="h-full bg-green-500 rounded-full" style={{ width: "33.9%" }}></div>
              </div>
            </div>

            <div className="bg-[#111827] border border-[#1F2937] rounded-xl p-6">
              <div className="flex items-center gap-2 text-gray-400 mb-4">
                <Server className="h-4 w-4" />
                <span className="text-sm font-medium">Consumo de Apps</span>
              </div>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-400">rdo-app</span>
                  <span>310.1MiB</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">rdo-mobile</span>
                  <span>4.977MiB</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">n8n</span>
                  <span>349.5MiB</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">evolution-api</span>
                  <span>252.0MiB</span>
                </div>
              </div>
            </div>
          </div>

          {/* Tools */}
          <div>
            <h2 className="text-xl font-bold mb-4">Suas Ferramentas</h2>

            {activeFolder === null ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <a
                  href="https://n8n.martines.halftech.com"
                  target="_blank"
                  rel="noreferrer"
                  className="bg-[#111827] border border-[#1F2937] hover:border-red-500/50 transition-colors rounded-xl p-6 flex flex-col items-center text-center group"
                >
                  <div className="h-14 w-14 rounded-2xl bg-red-500/20 text-red-500 grid place-items-center mb-4 group-hover:scale-110 transition-transform">
                    <Webhook className="h-7 w-7" />
                  </div>
                  <h3 className="font-bold text-lg">n8n</h3>
                  <p className="text-xs text-gray-400 mt-1">Automações e Integrações</p>
                </a>

                <a
                  href="http://216.22.43.39:81/"
                  target="_blank"
                  rel="noreferrer"
                  className="bg-[#111827] border border-[#1F2937] hover:border-blue-500/50 transition-colors rounded-xl p-6 flex flex-col items-center text-center group"
                >
                  <div className="h-14 w-14 rounded-2xl bg-blue-500/20 text-blue-500 grid place-items-center mb-4 group-hover:scale-110 transition-transform">
                    <ShieldCheck className="h-7 w-7" />
                  </div>
                  <h3 className="font-bold text-lg">Proxy Manager</h3>
                  <p className="text-xs text-gray-400 mt-1">Domínios e Segurança SSL</p>
                </a>

                <a
                  href="https://api.martines.halftech.com/manager"
                  target="_blank"
                  rel="noreferrer"
                  className="bg-[#111827] border border-[#1F2937] hover:border-green-500/50 transition-colors rounded-xl p-6 flex flex-col items-center text-center group"
                >
                  <div className="h-14 w-14 rounded-2xl bg-green-500/20 text-green-500 grid place-items-center mb-4 group-hover:scale-110 transition-transform">
                    <Settings className="h-7 w-7" />
                  </div>
                  <h3 className="font-bold text-lg">Evolution API</h3>
                  <p className="text-xs text-gray-400 mt-1">Integração de WhatsApp</p>
                </a>

                <button
                  onClick={() => setActiveFolder("projetos")}
                  className="bg-[#111827] border border-[#1F2937] hover:border-yellow-500/50 transition-colors rounded-xl p-6 flex flex-col items-center text-center group"
                >
                  <div className="h-14 w-14 rounded-2xl bg-yellow-500/20 text-yellow-500 grid place-items-center mb-4 group-hover:scale-110 transition-transform">
                    <Folder className="h-7 w-7" fill="currentColor" />
                  </div>
                  <h3 className="font-bold text-lg">Projetos</h3>
                  <p className="text-xs text-gray-400 mt-1">Sistemas RDO e Apps</p>
                </button>
              </div>
            ) : (
              <div className="animate-fade-in">
                <button
                  onClick={() => setActiveFolder(null)}
                  className="mb-4 text-sm text-gray-400 hover:text-white flex items-center gap-1 transition-colors"
                >
                  <ChevronRight className="h-4 w-4 rotate-180" /> Voltar para Ferramentas
                </button>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                  <a
                    href="http://216.22.43.39:8081/"
                    target="_blank"
                    rel="noreferrer"
                    className="bg-[#111827] border border-[#1F2937] hover:border-cyan-500/50 transition-colors rounded-xl p-6 flex flex-col items-center text-center group"
                  >
                    <div className="h-14 w-14 rounded-2xl bg-cyan-500/20 text-cyan-500 grid place-items-center mb-4 group-hover:scale-110 transition-transform">
                      <Activity className="h-7 w-7" />
                    </div>
                    <h3 className="font-bold text-lg">RDO AppWeb</h3>
                    <p className="text-xs text-gray-400 mt-1">Plataforma Desktop (React)</p>
                  </a>

                  <a
                    href="http://216.22.43.39:8082/"
                    target="_blank"
                    rel="noreferrer"
                    className="bg-[#111827] border border-[#1F2937] hover:border-purple-500/50 transition-colors rounded-xl p-6 flex flex-col items-center text-center group"
                  >
                    <div className="h-14 w-14 rounded-2xl bg-purple-500/20 text-purple-500 grid place-items-center mb-4 group-hover:scale-110 transition-transform">
                      <LayoutDashboard className="h-7 w-7" />
                    </div>
                    <h3 className="font-bold text-lg">RDO Mobile</h3>
                    <p className="text-xs text-gray-400 mt-1">App PWA para Campo</p>
                  </a>
                </div>
              </div>
            )}
          </div>

          {/* Gerenciador de Blog */}
          <div className="mt-12">
            <div className="flex items-center gap-2 mb-4">
              <FileText className="h-5 w-5 text-brand" />
              <h2 className="text-xl font-bold">Gerenciador de Blog (IA)</h2>
            </div>

            <div className="bg-[#111827] border border-[#1F2937] rounded-xl overflow-hidden">
              <table className="w-full text-left text-sm text-gray-400">
                <thead className="bg-[#1F2937] text-xs uppercase text-gray-300">
                  <tr>
                    <th className="px-6 py-4">Matéria</th>
                    <th className="px-6 py-4">Data</th>
                    <th className="px-6 py-4">Slug</th>
                    <th className="px-6 py-4 text-right">Ação</th>
                  </tr>
                </thead>
                <tbody>
                  {postsAdmin.length === 0 ? (
                    <tr>
                      <td colSpan={4} className="px-6 py-8 text-center text-gray-500">
                        Nenhuma reportagem encontrada ou JSON vazio.
                      </td>
                    </tr>
                  ) : (
                    postsAdmin.map((post: any, i) => (
                      <tr
                        key={i}
                        className="border-b border-[#1F2937] hover:bg-[#1F2937]/50 transition-colors"
                      >
                        <td className="px-6 py-4 font-medium text-white max-w-xs">
                          <div className="flex items-center gap-3">
                            {post.image ? (
                              <img
                                src={post.image}
                                alt="Capa"
                                className="w-10 h-10 rounded object-cover border border-[#1F2937] flex-shrink-0"
                              />
                            ) : (
                              <div className="w-10 h-10 rounded bg-[#1F2937] flex items-center justify-center flex-shrink-0 border border-[#374151]">
                                <FileText className="w-4 h-4 text-gray-500" />
                              </div>
                            )}
                            <span className="truncate" title={post.title}>
                              {post.title}
                            </span>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          {post.date
                            ? new Date(post.date).toLocaleDateString("pt-BR")
                            : "Data Indisponível"}
                        </td>
                        <td className="px-6 py-4 text-gray-500 text-xs truncate max-w-[150px]">
                          {post.slug || "Externo"}
                        </td>
                        <td className="px-6 py-4 text-right">
                          <button
                            onClick={() =>
                              post.slug
                                ? handleDeletePost(post.slug)
                                : alert("Posts estáticos ou sem slug não podem ser deletados.")
                            }
                            className="text-red-500 hover:text-white hover:bg-red-600 p-2 rounded-lg transition-all"
                            title="Apagar matéria"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
