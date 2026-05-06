"use client";

import { format } from "date-fns";
import { createColumnHelper, flexRender, getCoreRowModel, useReactTable } from "@tanstack/react-table";
import type { Deadline } from "@/types/deadlines";
import { DeadlineStatusBadge } from "@/components/deadlines/deadline-status-badge";
import { EmptyState } from "@/components/shared/empty-state";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

const columnHelper = createColumnHelper<Deadline>();

const columns = [
  columnHelper.accessor("law_case_id", {
    header: "Caso",
    cell: ({ getValue }) => getValue()?.slice(0, 8) ?? "Sem caso",
  }),
  columnHelper.accessor("due_date", {
    header: "Vencimento",
    cell: ({ getValue }) =>
      getValue() ? format(new Date(getValue()!), "dd/MM/yyyy HH:mm") : "Sem data",
  }),
  columnHelper.accessor("days_remaining", {
    header: "Dias",
  }),
  columnHelper.display({
    id: "status",
    header: "Estado",
    cell: ({ row }) => (
      <DeadlineStatusBadge
        completed={row.original.completed}
        isOverdue={row.original.is_overdue}
      />
    ),
  }),
];

type DeadlinesTableProps = {
  deadlines: Deadline[];
};

export function DeadlinesTable({ deadlines }: DeadlinesTableProps) {
  const table = useReactTable({
    data: deadlines,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  if (deadlines.length === 0) {
    return (
      <EmptyState
        title="Sem prazos"
        description="Os prazos desta organização vão aparecer aqui com destaque visual para risco e atraso."
      />
    );
  }

  return (
    <div className="jurisai-panel rounded-3xl p-4">
      <Table>
        <TableHeader>
          {table.getHeaderGroups().map((headerGroup) => (
            <TableRow key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <TableHead key={header.id}>
                  {header.isPlaceholder
                    ? null
                    : flexRender(header.column.columnDef.header, header.getContext())}
                </TableHead>
              ))}
            </TableRow>
          ))}
        </TableHeader>
        <TableBody>
          {table.getRowModel().rows.map((row) => (
            <TableRow key={row.id}>
              {row.getVisibleCells().map((cell) => (
                <TableCell key={cell.id}>
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
