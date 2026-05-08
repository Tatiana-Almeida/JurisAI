"use client";

import Link from "next/link";
import { createColumnHelper, flexRender, getCoreRowModel, useReactTable } from "@tanstack/react-table";
import type { LawCase } from "@/types/cases";
import { CaseStatusBadge } from "@/components/cases/case-status-badge";
import { EmptyState } from "@/components/shared/empty-state";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

const columnHelper = createColumnHelper<LawCase>();

const columns = [
  columnHelper.accessor("title", {
    header: "Processo",
    cell: ({ row }) => <Link href={`/cases/${row.original.id}`}>{row.original.title}</Link>,
  }),
  columnHelper.accessor("client.name", {
    id: "client",
    header: "Cliente",
    cell: ({ row }) => row.original.client?.name ?? "Sem cliente",
  }),
  columnHelper.accessor("lawyer.name", {
    id: "lawyer",
    header: "Advogado",
    cell: ({ row }) => row.original.lawyer?.name ?? "Sem advogado",
  }),
  columnHelper.accessor("status", {
    header: "Estado",
    cell: ({ getValue }) => <CaseStatusBadge status={getValue()} />,
  }),
];

type CasesTableProps = {
  cases: LawCase[];
};

export function CasesTable({ cases }: CasesTableProps) {
  const table = useReactTable({
    data: cases,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  if (cases.length === 0) {
    return (
      <EmptyState
        title="Sem processos"
        description="Crie o primeiro processo desta organização para começar a operar o Frontend MVP."
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
