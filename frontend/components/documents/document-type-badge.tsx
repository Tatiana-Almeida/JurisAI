import { Badge } from "@/components/ui/badge";

type DocumentTypeBadgeProps = {
  type?: string;
};

export function DocumentTypeBadge({ type }: DocumentTypeBadgeProps) {
  return (
    <Badge variant="secondary" className="rounded-full">
      {type ?? "internal"}
    </Badge>
  );
}
