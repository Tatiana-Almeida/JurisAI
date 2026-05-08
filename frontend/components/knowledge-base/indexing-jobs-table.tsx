"use client";

import Link from "next/link";
import { createColumnHelper, flexRender, getCoreRowModel, useReactTable } from "@tanstack/react-table";
import type { IndexingJob } from "@/types/knowledge-base";
import { EmptyState } from "@/components/shared/empty-state";
import { OCRStatusBadge } from "@/components/ocr/ocr-status-badge";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

type IndexingJobsTableProps = {
  jobs: IndexingJob[];
};

const columnHelper = createColumnHelper<IndexingJob>();

const columns = [
  columnHelper.accessor("status", {
    header: "Estado",
    cell: ({ getValue }) => <OCRStatusBadge status={getValue()} />,
  }),
  columnHelper.accessor("document", {
    header: "Documento",
    cell: ({ getValue }) => getValue() ?? "n/d",
  }),
  columnHelper.accessor("knowledge_base", {
    header: "Base",
    cell: ({ getValue }) => getValue() ?? "n/d",
  }),
  columnHelper.accessor("chunks_created", {
    header: "Chunks",
    cell: ({ row }) => `${row.original.chunks_created ?? 0}/${row.original.chunks_deleted ?? 0}`,
  }),
  columnHelper.accessor("error_message", {
    header: "Erro",
    cell: ({ getValue }) => getValue() ?? "—",
  }),
  columnHelper.display({
    id: "actions",
    header: "Acoes",
    cell: ({ row }) => (
      <div className="flex flex-wrap gap-2">
        {row.original.document ? (
          <Button asChild size="sm" variant="outline">
            <Link href={`/documents/${row.original.document}`}>Documento</Link>
          </Button>
        ) : null}
        {row.original.knowledge_base ? (
          <Button asChild size="sm" variant="ghost">
            <Link href={`/knowledge-base/${row.original.knowledge_base}`}>Base</Link>
          </Button>
        ) : null}
      </div>
    ),
  }),
];

export function IndexingJobsTable({ jobs }: IndexingJobsTableProps) {
  const table = useReactTable({
    data: jobs,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  if (jobs.length === 0) {
    return (
      <EmptyState
        title="Sem jobs de indexacao"
        description="Os jobs de indexacao aparecem aqui quando documentos forem preparados para embeddings."
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
