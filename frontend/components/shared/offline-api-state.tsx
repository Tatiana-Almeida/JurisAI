import { ErrorState } from "@/components/shared/error-state";

type OfflineApiStateProps = {
  apiUrl: string;
};

export function OfflineApiState({ apiUrl }: OfflineApiStateProps) {
  return (
    <ErrorState
      title="API indisponivel"
      description={`Nao foi possivel contactar a API configurada em ${apiUrl}. Verifique staging, CORS, rede ou autenticacao.`}
    />
  );
}
