import { format } from "date-fns";
import type { Deadline } from "@/types/deadlines";
import { EmptyState } from "@/components/shared/empty-state";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type UpcomingDeadlinesProps = {
  deadlines: Deadline[];
};

export function UpcomingDeadlines({ deadlines }: UpcomingDeadlinesProps) {
  if (deadlines.length === 0) {
    return (
      <EmptyState
        title="Sem prazos próximos"
        description="Os prazos pendentes desta organização vão aparecer aqui."
      />
    );
  }

  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader>
        <CardTitle>Prazos próximos</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {deadlines.slice(0, 5).map((deadline) => (
          <div key={deadline.id} className="rounded-2xl border border-border/60 p-4">
            <div className="font-medium">
              Caso {deadline.law_case_id ? deadline.law_case_id.slice(0, 8) : "sem vínculo"}
            </div>
            <div className="mt-1 text-sm text-muted-foreground">
              {deadline.due_date ? format(new Date(deadline.due_date), "dd/MM/yyyy HH:mm") : "Sem data"}
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
