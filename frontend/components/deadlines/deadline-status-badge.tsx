import { Badge } from "@/components/ui/badge";

type DeadlineStatusBadgeProps = {
  completed?: boolean;
  isOverdue?: boolean;
  daysRemaining?: number;
};

export function DeadlineStatusBadge({
  completed = false,
  isOverdue = false,
  daysRemaining,
}: DeadlineStatusBadgeProps) {
  const isCritical =
    !completed && !isOverdue && typeof daysRemaining === "number" && daysRemaining <= 3;

  const label = completed
    ? "Concluido"
    : isOverdue
      ? "Em atraso"
      : isCritical
        ? "Critico"
        : "Pendente";

  return (
    <Badge
      variant="secondary"
      className={
        completed
          ? "rounded-full bg-emerald-100 text-emerald-700 dark:bg-emerald-500/15 dark:text-emerald-300"
          : isOverdue
            ? "rounded-full bg-rose-100 text-rose-700 dark:bg-rose-500/15 dark:text-rose-300"
            : isCritical
              ? "rounded-full bg-amber-100 text-amber-700 dark:bg-amber-500/15 dark:text-amber-300"
              : "rounded-full"
      }
    >
      {label}
    </Badge>
  );
}
