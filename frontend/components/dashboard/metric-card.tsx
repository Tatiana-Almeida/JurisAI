import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

type MetricCardProps = {
  title: string;
  value: string | number;
  hint?: string;
};

export function MetricCard({ title, value, hint }: MetricCardProps) {
  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-3xl font-semibold tracking-tight">{value}</div>
        {hint ? <p className="mt-2 text-sm text-muted-foreground">{hint}</p> : null}
      </CardContent>
    </Card>
  );
}
