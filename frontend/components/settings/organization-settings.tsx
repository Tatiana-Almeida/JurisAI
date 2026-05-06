import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { Organization } from "@/types/organization";

type OrganizationSettingsProps = {
  organization?: Organization | null;
};

export function OrganizationSettings({ organization }: OrganizationSettingsProps) {
  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader>
        <CardTitle>Organização ativa</CardTitle>
      </CardHeader>
      <CardContent className="space-y-2 text-sm text-muted-foreground">
        <div>Nome: {organization?.name ?? "Sem organização ativa"}</div>
        <div>Plano: {organization?.plan ?? "N/D"}</div>
      </CardContent>
    </Card>
  );
}
