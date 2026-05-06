type DataToolbarProps = {
  title: string;
  subtitle?: string;
  actions?: React.ReactNode;
};

export function DataToolbar({ title, subtitle, actions }: DataToolbarProps) {
  return (
    <div className="flex flex-col gap-4 rounded-3xl border border-border/60 bg-background/70 p-4 md:flex-row md:items-center md:justify-between">
      <div>
        <h3 className="font-semibold">{title}</h3>
        {subtitle ? <p className="text-sm text-muted-foreground">{subtitle}</p> : null}
      </div>
      {actions ? <div className="flex items-center gap-2">{actions}</div> : null}
    </div>
  );
}
