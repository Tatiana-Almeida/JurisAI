"use client";

import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { Expense, FinanceSummary, Invoice } from "@/types/finance";

type FinanceSummaryProps = {
  summary?: FinanceSummary;
  invoices: Invoice[];
  expenses: Expense[];
};

function toNumber(value: number | string | undefined) {
  if (typeof value === "number") {
    return value;
  }
  if (!value) {
    return 0;
  }
  return Number(value);
}

export function FinanceSummaryCard({ summary, invoices, expenses }: FinanceSummaryProps) {
  const chartData = [
    { name: "Faturas abertas", value: summary?.open_invoices ?? 0 },
    { name: "Faturas pagas", value: summary?.paid_invoices ?? 0 },
    { name: "Pagamentos", value: summary?.total_payments ?? 0 },
  ];

  return (
    <div className="grid gap-6">
      <Card className="jurisai-panel rounded-3xl">
        <CardHeader>
          <CardTitle>Resumo financeiro</CardTitle>
        </CardHeader>
        <CardContent className="grid gap-4 md:grid-cols-3">
          <div className="rounded-2xl border border-border/60 p-4">
            <div className="text-sm text-muted-foreground">Total de faturas</div>
            <div className="mt-2 text-2xl font-semibold">{summary?.total_invoices ?? invoices.length}</div>
          </div>
          <div className="rounded-2xl border border-border/60 p-4">
            <div className="text-sm text-muted-foreground">Montante de pagamentos</div>
            <div className="mt-2 text-2xl font-semibold">{toNumber(summary?.payments_amount)}</div>
          </div>
          <div className="rounded-2xl border border-border/60 p-4">
            <div className="text-sm text-muted-foreground">Montante de despesas</div>
            <div className="mt-2 text-2xl font-semibold">{toNumber(summary?.expenses_amount)}</div>
          </div>
        </CardContent>
      </Card>

      <Card className="jurisai-panel rounded-3xl">
        <CardHeader>
          <CardTitle>Indicadores</CardTitle>
        </CardHeader>
        <CardContent className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
              <XAxis dataKey="name" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="value" fill="#1d4ed8" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <div className="grid gap-6 xl:grid-cols-2">
        <Card className="jurisai-panel rounded-3xl">
          <CardHeader>
            <CardTitle>Ultimas faturas</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 text-sm">
            {invoices.slice(0, 5).map((invoice) => (
              <div key={invoice.id} className="rounded-2xl border border-border/60 p-4">
                <div className="font-medium">{invoice.invoice_number ?? invoice.id.slice(0, 8)}</div>
                <div className="mt-1 text-muted-foreground">
                  status={invoice.status ?? "n/d"} · amount={invoice.amount} · due_date={invoice.due_date ?? "n/d"}
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card className="jurisai-panel rounded-3xl">
          <CardHeader>
            <CardTitle>Ultimas despesas</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 text-sm">
            {expenses.slice(0, 5).map((expense) => (
              <div key={expense.id} className="rounded-2xl border border-border/60 p-4">
                <div className="font-medium">{expense.description ?? "Despesa"}</div>
                <div className="mt-1 text-muted-foreground">
                  amount={expense.amount} · reimbursable={String(expense.reimbursable ?? false)} · expense_date=
                  {expense.expense_date ?? "n/d"}
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
