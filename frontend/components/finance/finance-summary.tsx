import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { Expense, FinanceSummary, Invoice } from "@/types/finance";

type FinanceSummaryProps = {
  summary?: FinanceSummary;
  invoices: Invoice[];
  expenses: Expense[];
};

export function FinanceSummaryCard({
  summary,
  invoices,
  expenses,
}: FinanceSummaryProps) {
  return (
    <Card className="jurisai-panel rounded-3xl">
      <CardHeader>
        <CardTitle>Financeiro</CardTitle>
      </CardHeader>
      <CardContent className="grid gap-4 md:grid-cols-3">
        <div className="rounded-2xl border border-border/60 p-4">
          <div className="text-sm text-muted-foreground">Pending invoices</div>
          <div className="mt-2 text-2xl font-semibold">{summary?.pending_invoices ?? invoices.length}</div>
        </div>
        <div className="rounded-2xl border border-border/60 p-4">
          <div className="text-sm text-muted-foreground">Paid invoices</div>
          <div className="mt-2 text-2xl font-semibold">{summary?.paid_invoices ?? 0}</div>
        </div>
        <div className="rounded-2xl border border-border/60 p-4">
          <div className="text-sm text-muted-foreground">Expenses registadas</div>
          <div className="mt-2 text-2xl font-semibold">{expenses.length}</div>
        </div>
      </CardContent>
    </Card>
  );
}
