type LoadingScreenProps = {
  title?: string;
  description?: string;
};

export function LoadingScreen({
  title = "A preparar sessao",
  description = "A autenticacao e o contexto da organizacao estao a ser inicializados.",
}: LoadingScreenProps) {
  return (
    <div className="flex min-h-[50vh] items-center justify-center">
      <div className="jurisai-panel w-full max-w-md rounded-3xl p-8 text-center">
        <div className="mx-auto mb-4 size-10 animate-spin rounded-full border-2 border-primary/25 border-t-primary" />
        <h2 className="text-lg font-semibold">{title}</h2>
        <p className="mt-2 text-sm text-muted-foreground">{description}</p>
      </div>
    </div>
  );
}
