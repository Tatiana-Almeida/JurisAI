"use client";

import Link from "next/link";
import { createColumnHelper, flexRender, getCoreRowModel, useReactTable } from "@tanstack/react-table";
import type { OCRJob } from "@/types/ocr";
import { OCRStatusBadge } from "@/components/ocr/ocr-status-badge";
import { EmptyState } from "@/components/shared/empty-state";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

const columnHelper = createColumnHelper<OCRJob>();

type OCRJobTableProps = {
  jobs: OCRJob[];
};

const columns = [
  columnHelper.accessor("document", {
    header: "Documento",
    cell: ({ row }) => (
      <div className="space-y-1">
        <div>{row.original.document?.slice(0, 8) ?? "Sem documento"}</div>
        {row.original.status === "pending" || row.original.status === "running" ? (
          <div className="text-xs text-primary">Polling ativo</div>
        ) : null}
      </div>
    ),
  }),
  columnHelper.accessor("extraction_method", {
    header: "Metodo",
    cell: ({ getValue }) => getValue() ?? "local",
  }),
  columnHelper.display({
    id: "provider",
    header: "Provider",
    cell: () => "n/d no serializer",
  }),
  columnHelper.accessor("status", {
    header: "Estado",
    cell: ({ getValue }) => <OCRStatusBadge status={getValue()} />,
  }),
  columnHelper.accessor("created_at", {
    header: "Criado em",
    cell: ({ getValue }) => getValue() ?? "n/d",
  }),
  columnHelper.accessor("updated_at", {
    header: "Atualizado em",
    cell: ({ row }) => row.original.updated_at ?? row.original.finished_at ?? row.original.started_at ?? "n/d",
  }),
  columnHelper.accessor("error_message", {
    header: "Falha",
    cell: ({ getValue }) => getValue() ?? "—",
  }),
  columnHelper.display({
    id: "actions",
    header: "Acoes",
    cell: ({ row }) => (
      <div className="flex flex-wrap gap-2">
        <Button asChild size="sm" variant="outline">
          <Link href={`/documents/${row.original.document}`}>Ver documento</Link>
        </Button>
        <Button asChild size="sm" variant="ghost">
          <Link href={`/ocr?document=${row.original.document ?? ""}`}>Ver resultado</Link>
        </Button>
      </div>
    ),
  }),
];

export function OCRJobTable({ jobs }: OCRJobTableProps) {
  const table = useReactTable({
    data: jobs,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  if (jobs.length === 0) {
    return (
      <EmptyState
        title="Sem jobs de OCR"
        description="Assim que o OCR for acionado sobre um documento, os jobs vao aparecer aqui com polling automatico."
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
