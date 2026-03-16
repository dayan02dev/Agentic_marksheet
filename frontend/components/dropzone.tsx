"use client"

import React, { useCallback, useState } from "react"
import { useDropzone } from "react-dropzone"
import { Upload, File, X, AlertCircle } from "lucide-react"
import { cn } from "@/lib/utils"

const MAX_FILE_SIZE = 100 * 1024 * 1024 // 100MB total
const MAX_SINGLE_FILE_SIZE = 25 * 1024 * 1024 // 25MB per file

interface FileWithPreview extends File {
  preview?: string
}

interface DropzoneProps {
  onFilesSelected: (files: File[]) => void
  maxFiles?: number
  disabled?: boolean
  accept?: Record<string, string[]>
}

export function Dropzone({
  onFilesSelected,
  maxFiles = 20,
  disabled = false,
  accept = {
    "image/*": [".jpg", ".jpeg", ".png"],
    "application/pdf": [".pdf"],
    "application/zip": [".zip"],
  },
}: DropzoneProps) {
  const [files, setFiles] = React.useState<FileWithPreview[]>([])
  const [validationError, setValidationError] = useState<string | null>(null)

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      setValidationError(null)

      // Validate individual file sizes
      const oversized = acceptedFiles.filter(f => f.size > MAX_SINGLE_FILE_SIZE)
      if (oversized.length > 0) {
        setValidationError(
          `${oversized.map(f => f.name).join(", ")} exceed${oversized.length === 1 ? "s" : ""} the 25MB per-file limit.`
        )
        return
      }

      const newFiles = [...files, ...acceptedFiles].slice(0, maxFiles)

      // Validate total size
      const totalSize = newFiles.reduce((sum, f) => sum + f.size, 0)
      if (totalSize > MAX_FILE_SIZE) {
        setValidationError(
          `Total upload size (${(totalSize / 1024 / 1024).toFixed(1)}MB) exceeds the 100MB limit.`
        )
        return
      }

      setFiles(newFiles)
      onFilesSelected(newFiles)
    },
    [files, maxFiles, onFilesSelected]
  )

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    maxFiles,
    accept,
    disabled,
    noClick: disabled,
  })

  const removeFile = (index: number) => {
    const newFiles = files.filter((_, i) => i !== index)
    setFiles(newFiles)
    onFilesSelected(newFiles)
  }

  return (
    <div className="space-y-4">
      <div
        {...getRootProps()}
        className={cn(
          "flex flex-col items-center justify-center rounded-lg border-2 border-dashed p-12 text-center transition-colors",
          isDragActive
            ? "border-primary bg-primary/5"
            : "border-muted-foreground/25 hover:border-muted-foreground/50",
          disabled && "cursor-not-allowed opacity-50"
        )}
      >
        <input {...getInputProps()} />
        <Upload className="mb-4 h-12 w-12 text-muted-foreground" />
        <p className="text-lg font-medium">
          {isDragActive ? "Drop files here" : "Drag & drop marksheets here"}
        </p>
        <p className="text-sm text-muted-foreground">
          or click to browse (JPG, PNG, PDF, or ZIP)
        </p>
        <p className="mt-2 text-xs text-muted-foreground">
          Max {maxFiles} files per batch
        </p>
      </div>

      {validationError && (
        <div className="flex items-start gap-2 rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-700">
          <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
          <span>{validationError}</span>
        </div>
      )}

      {files.length > 0 && (
        <div className="space-y-2">
          <p className="text-sm font-medium">
            Selected files ({files.length}/{maxFiles})
          </p>
          <div className="max-h-48 space-y-1 overflow-y-auto">
            {files.map((file, index) => (
              <div
                key={index}
                className="flex items-center justify-between rounded-md bg-muted px-3 py-2 text-sm"
              >
                <div className="flex items-center gap-2 overflow-hidden">
                  <File className="h-4 w-4 shrink-0" />
                  <span className="truncate">{file.name}</span>
                  <span className="text-xs text-muted-foreground">
                    ({(file.size / 1024).toFixed(0)} KB)
                  </span>
                </div>
                <button
                  type="button"
                  onClick={() => removeFile(index)}
                  className="shrink-0 rounded-full p-1 hover:bg-destructive hover:text-destructive-foreground"
                  disabled={disabled}
                >
                  <X className="h-4 w-4" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
