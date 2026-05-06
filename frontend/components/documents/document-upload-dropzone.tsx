"use client";

import { useMemo } from "react";
import { UploadCloud } from "lucide-react";
import { useDropzone } from "react-dropzone";
import { cn } from "@/lib/utils";

const acceptedMimeTypes = {
  "application/pdf": [".pdf"],
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
  "text/plain": [".txt"],
  "image/png": [".png"],
  "image/jpeg": [".jpg", ".jpeg"],
};

type DocumentUploadDropzoneProps = {
  maxSizeMb?: number;
  onFilesAccepted?: (files: File[]) => void;
  uploadProgress?: number | null;
  helperText?: string;
};

export function DocumentUploadDropzone({
  maxSizeMb = 10,
  onFilesAccepted,
  uploadProgress,
  helperText,
}: DocumentUploadDropzoneProps) {
  const maxSizeBytes = useMemo(() => maxSizeMb * 1024 * 1024, [maxSizeMb]);

  const dropzone = useDropzone({
    accept: acceptedMimeTypes,
    maxSize: maxSizeBytes,
    onDropAccepted: onFilesAccepted,
  });

  return (
    <div
      {...dropzone.getRootProps()}
      className={cn(
        "jurisai-panel rounded-[1.75rem] border-dashed p-8 text-center transition-colors",
        dropzone.isDragActive && "border-primary bg-primary/5",
      )}
    >
      <input {...dropzone.getInputProps()} />
      <div className="mx-auto mb-4 flex size-14 items-center justify-center rounded-2xl bg-primary/10 text-primary">
        <UploadCloud className="size-6" />
      </div>
      <h3 className="text-lg font-semibold">Upload preparado para documentos jurídicos</h3>
      <p className="mt-2 text-sm text-muted-foreground">
        Aceita PDF, DOCX, TXT, PNG, JPG e JPEG. Limite configurável de {maxSizeMb} MB.
      </p>
      {dropzone.fileRejections.length > 0 ? (
        <div className="mt-4 rounded-2xl bg-destructive/10 p-3 text-sm text-destructive">
          {dropzone.fileRejections[0]?.errors[0]?.message ??
            "Não foi possível aceitar o ficheiro."}
        </div>
      ) : null}
      {typeof uploadProgress === "number" ? (
        <p className="mt-4 text-sm text-muted-foreground">Progresso do upload: {uploadProgress}%</p>
      ) : null}
      <p className="mt-4 text-xs text-muted-foreground">
        {helperText ??
          "O upload já está preparado para integração real com o backend e validações do serializer de documentos."}
      </p>
    </div>
  );
}
