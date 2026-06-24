import { useEffect, useState } from "react";
import { MessageCircle } from "lucide-react";

export function WhatsappFab() {
  const [showTip, setShowTip] = useState(false);
  useEffect(() => {
    const t = setTimeout(() => setShowTip(true), 2000);
    return () => clearTimeout(t);
  }, []);
  return (
    <a
      href="http://wa.me/5511954210088"
      target="_blank"
      rel="noopener noreferrer"
      aria-label="Fale com o especialista no WhatsApp"
      className="group fixed bottom-6 right-6 z-30 flex items-center gap-3"
    >
      <span
        className={`hidden md:inline-block text-xs font-medium px-3 py-2 rounded-lg bg-foreground text-background shadow-lg transition-all duration-300 ${
          showTip ? "opacity-100 translate-x-0" : "opacity-0 translate-x-2 pointer-events-none"
        }`}
      >
        Fale direto com o Especialista
      </span>
      <span className="relative h-14 w-14 rounded-full bg-[#25D366] text-white grid place-items-center shadow-xl animate-pulse-ring">
        <MessageCircle className="h-6 w-6" strokeWidth={2} />
      </span>
    </a>
  );
}
