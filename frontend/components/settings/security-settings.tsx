import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function SecuritySettings() {
  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader>
        <CardTitle>Segurança</CardTitle>
      </CardHeader>
      <CardContent className="space-y-2 text-sm text-muted-foreground">
        <div>JWT via Authorization Bearer.</div>
        <div>LocalStorage é temporário até hardening com cookies httpOnly.</div>
        <div>Cache multi-tenant é limpo ao trocar organização.</div>
      </CardContent>
    </Card>
  );
}
