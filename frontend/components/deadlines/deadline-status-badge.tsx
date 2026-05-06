import { Badge } from "@/components/ui/badge";

type DeadlineStatusBadgeProps = {
  completed?: boolean;
  isOverdue?: boolean;
};

export function DeadlineStatusBadge({
  completed = false,
  isOverdue = false,
}: DeadlineStatusBadgeProps) {
  const label = completed ? "completed" : isOverdue ? "overdue" : "pending";
  return (
    <Badge variant="secondary" className="rounded-full">
      {label}
    </Badge>
  );
}
