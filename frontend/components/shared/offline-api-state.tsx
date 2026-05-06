import { ErrorState } from "@/components/shared/error-state";

type OfflineApiStateProps = {
  apiUrl: string;
};

export function OfflineApiState({ apiUrl }: OfflineApiStateProps) {
  return (
    <ErrorState
      title="API indisponível"
      description={`Não foi possível contactar a API configurada em ${apiUrl}. Verifique staging, CORS, rede ou autenticação.`}
    />
  );
}
