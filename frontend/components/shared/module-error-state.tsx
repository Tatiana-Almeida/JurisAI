import { ErrorState } from "@/components/shared/error-state";

type ModuleErrorStateProps = {
  moduleName: string;
  title?: string;
  description?: string;
};

export function ModuleErrorState({
  moduleName,
  title,
  description = "O modulo nao pode ser carregado com os dados atuais do backend.",
}: ModuleErrorStateProps) {
  return <ErrorState title={title ?? `Falha no modulo ${moduleName}`} description={description} />;
}
