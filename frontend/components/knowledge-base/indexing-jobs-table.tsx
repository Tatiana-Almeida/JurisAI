import type { IndexingJob } from "@/types/knowledge-base";
import { EmptyState } from "@/components/shared/empty-state";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type IndexingJobsTableProps = {
  jobs: IndexingJob[];
};

export function IndexingJobsTable({ jobs }: IndexingJobsTableProps) {
  if (jobs.length === 0) {
    return (
      <EmptyState
        title="Sem jobs de indexação"
        description="Os jobs de indexação aparecem aqui quando documentos forem preparados para embeddings."
      />
    );
  }

  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader>
        <CardTitle>Jobs de indexação</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {jobs.map((job) => (
          <div key={job.id} className="rounded-2xl border border-border/60 p-4 text-sm">
            <div className="font-medium">{job.status}</div>
            <div className="mt-1 text-muted-foreground">
              chunks_created={job.chunks_created ?? 0} · chunks_deleted={job.chunks_deleted ?? 0}
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
