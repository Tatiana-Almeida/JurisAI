import { formatDistanceToNow } from "date-fns";
import type { Document } from "@/types/documents";
import type { OCRJob } from "@/types/ocr";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type ActivityFeedProps = {
  documents: Document[];
  jobs: OCRJob[];
};

export function ActivityFeed({ documents, jobs }: ActivityFeedProps) {
  const activities = [
    ...documents.slice(0, 3).map((document) => ({
      id: document.id,
      title: `Documento ${document.type ?? "jurídico"} atualizado`,
      timestamp: document.updated_at ?? document.created_at,
    })),
    ...jobs.slice(0, 3).map((job) => ({
      id: job.id,
      title: `Job de OCR em estado ${job.status}`,
      timestamp: job.updated_at ?? job.created_at,
    })),
  ].sort((left, right) => String(right.timestamp ?? "").localeCompare(String(left.timestamp ?? "")));

  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader>
        <CardTitle>Atividade recente</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {activities.length === 0 ? (
          <p className="text-sm text-muted-foreground">A atividade operacional ainda não foi populada.</p>
        ) : (
          activities.map((activity) => (
            <div key={activity.id} className="rounded-2xl border border-border/60 p-4">
              <div className="font-medium">{activity.title}</div>
              <div className="mt-1 text-sm text-muted-foreground">
                {activity.timestamp
                  ? formatDistanceToNow(new Date(activity.timestamp), { addSuffix: true })
                  : "Sem timestamp"}
              </div>
            </div>
          ))
        )}
      </CardContent>
    </Card>
  );
}
