import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

type OCRStatusBadgeProps = {
  status?: string;
};

const statusStyles: Record<string, string> = {
  pending: "bg-slate-200 text-slate-800 dark:bg-slate-500/20 dark:text-slate-200",
  running: "bg-amber-100 text-amber-800 dark:bg-amber-500/15 dark:text-amber-200",
  completed: "bg-emerald-100 text-emerald-800 dark:bg-emerald-500/15 dark:text-emerald-200",
  failed: "bg-rose-100 text-rose-800 dark:bg-rose-500/15 dark:text-rose-200",
  skipped: "bg-cyan-100 text-cyan-800 dark:bg-cyan-500/15 dark:text-cyan-200",
};

export function OCRStatusBadge({ status = "pending" }: OCRStatusBadgeProps) {
  return (
    <Badge variant="secondary" className={cn("rounded-full", statusStyles[status] ?? statusStyles.pending)}>
      {status}
    </Badge>
  );
}
