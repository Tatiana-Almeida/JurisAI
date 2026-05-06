import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type KBSearchProps = {
  retrievalMethod?: string;
  sourcesCount?: number;
};

export function KBSearch({ retrievalMethod, sourcesCount }: KBSearchProps) {
  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader>
        <CardTitle>Search foundation</CardTitle>
      </CardHeader>
      <CardContent className="text-sm text-muted-foreground">
        retrieval_method={retrievalMethod ?? "pending"} · sources_count={sourcesCount ?? 0}
      </CardContent>
    </Card>
  );
}
