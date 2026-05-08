import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

type StatusBadgeProps = {
  status: "active" | "partial" | "pending" | "implemented" | "missing";
  className?: string;
};

const statusLabelMap: Record<StatusBadgeProps["status"], string> = {
  active: "Ativo",
  partial: "Parcial",
  pending: "Pendente",
  implemented: "Implementado",
  missing: "Em falta",
};

export function StatusBadge({ status, className }: StatusBadgeProps) {
  return (
    <Badge
      variant="secondary"
      className={cn(
        "rounded-full px-3 py-1 text-xs font-medium",
        status === "active" && "bg-emerald-100 text-emerald-700 dark:bg-emerald-500/15 dark:text-emerald-300",
        status === "partial" && "bg-amber-100 text-amber-700 dark:bg-amber-500/15 dark:text-amber-300",
        status === "pending" && "bg-slate-200 text-slate-700 dark:bg-slate-500/20 dark:text-slate-200",
        status === "implemented" && "bg-cyan-100 text-cyan-700 dark:bg-cyan-500/15 dark:text-cyan-300",
        status === "missing" && "bg-rose-100 text-rose-700 dark:bg-rose-500/15 dark:text-rose-300",
        className,
      )}
    >
      {statusLabelMap[status]}
    </Badge>
  );
}
