import Link from "next/link";
import { Button } from "@/components/ui/button";
import { EmptyState } from "@/components/shared/empty-state";

export function UnauthorizedState() {
  return (
    <div className="space-y-4">
      <EmptyState
        title="Sessão necessária"
        description="Esta área do JurisAI requer autenticação antes de carregar dados do tenant."
      />
      <div className="flex justify-center">
        <Button asChild>
          <Link href="/login">Ir para login</Link>
        </Button>
      </div>
    </div>
  );
}
