import { ErrorState } from "@/components/shared/error-state";

export function ForbiddenState() {
  return (
    <ErrorState
      title="Acesso negado"
      description="A sua sessão está autenticada, mas não tem permissões para aceder a esta área."
    />
  );
}
