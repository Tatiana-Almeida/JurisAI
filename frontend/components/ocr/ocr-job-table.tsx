"use client";

import { createColumnHelper, flexRender, getCoreRowModel, useReactTable } from "@tanstack/react-table";
import type { OCRJob } from "@/types/ocr";
import { OCRStatusBadge } from "@/components/ocr/ocr-status-badge";
import { EmptyState } from "@/components/shared/empty-state";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

const columnHelper = createColumnHelper<OCRJob>();

const columns = [
  columnHelper.accessor("document", {
    header: "Documento",
    cell: ({ getValue }) => getValue()?.slice(0, 8) ?? "Sem documento",
  }),
  columnHelper.accessor("extraction_method", {
    header: "Método",
    cell: ({ getValue }) => getValue() ?? "local",
  }),
  columnHelper.accessor("status", {
    header: "Estado",
    cell: ({ getValue }) => <OCRStatusBadge status={getValue()} />,
  }),
  columnHelper.accessor("error_message", {
    header: "Falha",
    cell: ({ getValue }) => getValue() ?? "—",
  }),
];

type OCRJobTableProps = {
  jobs: OCRJob[];
};

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
        description="Assim que o OCR for acionado sobre um documento, os jobs vão aparecer aqui com polling automático."
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
