import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function SecuritySettings() {
  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader>
        <CardTitle>Seguranca</CardTitle>
      </CardHeader>
      <CardContent className="space-y-2 text-sm text-muted-foreground">
        <div>JWT via Authorization Bearer.</div>
        <div>LocalStorage continua temporario ate hardening com cookies httpOnly.</div>
        <div>Cache multi-tenant e limpo ao trocar organizacao.</div>
        <div>Sem segredos persistidos no repositório frontend.</div>
      </CardContent>
    </Card>
  );
}
