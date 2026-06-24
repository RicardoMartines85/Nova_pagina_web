import { useEffect, useState } from "react";
import { X, Lock } from "lucide-react";

export function RestrictedModal({
  open,
  onClose,
}: {
  open: boolean;
  onClose: () => void;
}) {
  const [pwd, setPwd] = useState("");
  const [error, setError] = useState(false);

  useEffect(() => {
    if (!open) {
      setPwd("");
      setError(false);
    }
  }, [open]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    if (open) window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  if (!open) return null;

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    if (pwd === "RyCo@2501") {
      window.location.href = "/area_restrita";
    } else {
      setError(true);
    }
  };

  return (
    <div className="fixed inset-0 z-50 grid place-items-center p-4">
      <div
        className="absolute inset-0 bg-background/60 backdrop-blur-md"
        onClick={onClose}
      />
      <div className="relative w-full max-w-md bg-card border border-border rounded-2xl shadow-2xl p-7 md:p-8 animate-fade-up">
        <button
          onClick={onClose}
          aria-label="Fechar"
          className="absolute top-4 right-4 h-8 w-8 grid place-items-center rounded-md hover:bg-accent text-muted-foreground"
        >
          <X className="h-4 w-4" />
        </button>
        <div className="h-11 w-11 rounded-lg bg-brand/10 text-brand grid place-items-center">
          <Lock className="h-5 w-5" strokeWidth={1.5} />
        </div>
        <h3 className="mt-5 text-xl font-semibold tracking-tight text-foreground">
          Área Restrita
        </h3>
        <p className="mt-1.5 text-sm text-muted-foreground">
          Acesso reservado a clientes ativos e operação interna.
        </p>
        <form onSubmit={submit} className="mt-6 space-y-3">
          <input
            type="password"
            autoFocus
            value={pwd}
            onChange={(e) => {
              setPwd(e.target.value);
              setError(false);
            }}
            placeholder="Credencial"
            className="w-full rounded-lg border border-input bg-background px-4 py-3 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-brand/40 focus:border-brand"
          />
          {error && (
            <p className="text-xs text-destructive">
              Acesso negado. Credencial incorreta.
            </p>
          )}
          <button
            type="submit"
            className="w-full inline-flex justify-center items-center rounded-md bg-foreground text-background px-4 py-3 text-sm font-medium hover:bg-foreground/90 transition"
          >
            Acessar
          </button>
        </form>
      </div>
    </div>
  );
}
