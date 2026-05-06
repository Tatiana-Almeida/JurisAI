import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { User } from "@/types/auth";

type ProfileSettingsProps = {
  user?: User | null;
};

export function ProfileSettings({ user }: ProfileSettingsProps) {
  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader>
        <CardTitle>Conta</CardTitle>
      </CardHeader>
      <CardContent className="space-y-2 text-sm text-muted-foreground">
        <div>Nome: {user?.name ?? "N/D"}</div>
        <div>Email: {user?.email ?? "N/D"}</div>
        <div>Role: {user?.role ?? "N/D"}</div>
      </CardContent>
    </Card>
  );
}
