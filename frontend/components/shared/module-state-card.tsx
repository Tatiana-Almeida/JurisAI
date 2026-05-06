import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { StatusBadge } from "@/components/shared/status-badge";

type ModuleStateCardProps = {
  title: string;
  status: "active" | "partial" | "pending";
  description: string;
  bullets: string[];
};

export function ModuleStateCard({
  title,
  status,
  description,
  bullets,
}: ModuleStateCardProps) {
  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader className="space-y-3">
        <div className="flex items-center justify-between gap-3">
          <CardTitle>{title}</CardTitle>
          <StatusBadge status={status} />
        </div>
        <p className="text-sm leading-6 text-muted-foreground">{description}</p>
      </CardHeader>
      <CardContent>
        <ul className="space-y-2 text-sm text-muted-foreground">
          {bullets.map((bullet) => (
            <li key={bullet} className="flex gap-2">
              <span className="mt-2 size-1.5 rounded-full bg-primary/70" />
              <span>{bullet}</span>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}
