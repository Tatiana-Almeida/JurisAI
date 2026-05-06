import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

type CaseStatusBadgeProps = {
  status?: string;
};

const statusStyles: Record<string, string> = {
  open: "bg-cyan-100 text-cyan-800 dark:bg-cyan-500/15 dark:text-cyan-200",
  in_progress: "bg-amber-100 text-amber-800 dark:bg-amber-500/15 dark:text-amber-200",
  closed: "bg-emerald-100 text-emerald-800 dark:bg-emerald-500/15 dark:text-emerald-200",
  on_hold: "bg-slate-200 text-slate-800 dark:bg-slate-500/20 dark:text-slate-200",
};

export function CaseStatusBadge({ status = "open" }: CaseStatusBadgeProps) {
  return (
    <Badge variant="secondary" className={cn("rounded-full", statusStyles[status] ?? statusStyles.open)}>
      {status}
    </Badge>
  );
}
