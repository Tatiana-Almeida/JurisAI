"use client";

import Link from "next/link";
import { createColumnHelper, flexRender, getCoreRowModel, useReactTable } from "@tanstack/react-table";
import type { Document } from "@/types/documents";
import { EmptyState } from "@/components/shared/empty-state";
import { DocumentTypeBadge } from "@/components/documents/document-type-badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

const columnHelper = createColumnHelper<Document>();

const columns = [
  columnHelper.accessor("id", {
    header: "Documento",
    cell: ({ row }) => <Link href={`/documents/${row.original.id}`}>{row.original.id.slice(0, 8)}</Link>,
  }),
  columnHelper.accessor("type", {
    header: "Tipo",
    cell: ({ getValue }) => <DocumentTypeBadge type={getValue()} />,
  }),
  columnHelper.accessor("version", {
    header: "Versão",
  }),
  columnHelper.accessor("law_case_id", {
    header: "Caso",
    cell: ({ getValue }) => getValue()?.slice(0, 8) ?? "Sem caso",
  }),
];

type DocumentsTableProps = {
  documents: Document[];
};

export function DocumentsTable({ documents }: DocumentsTableProps) {
  const table = useReactTable({
    data: documents,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  if (documents.length === 0) {
    return (
      <EmptyState
        title="Sem documentos"
        description="Os documentos jurídicos desta organização vão aparecer aqui após o primeiro upload."
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
