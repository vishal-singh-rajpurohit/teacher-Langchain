"use client"

import { FileText, Trash2, UploadCloud, X } from "lucide-react"
import type { FormEvent } from "react"
import { useState } from "react"

export interface ContextModalSubmit {
    context: string;
    files: File[];
}

interface ContextModalProps {
    open: boolean;
    onClose: () => void;
    onSubmit: (data: ContextModalSubmit) => Promise<void> | void;
    uploading?: boolean;
}

export default function ContextModal({ open, onClose, onSubmit, uploading = false }: ContextModalProps) {
    const [helpWith, setHelpWith] = useState("")
    const [description, setDescription] = useState("")
    const [knowledgeLevel, setKnowledgeLevel] = useState("beginner")
    const [files, setFiles] = useState<File[]>([])

    if (!open) return null

    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault()

        const contextParts = [
            helpWith.trim() ? `Help with: ${helpWith.trim()}` : "",
            description.trim() ? `Description: ${description.trim()}` : "",
            `Knowledge level: ${knowledgeLevel}`,
        ].filter(Boolean)

        await onSubmit({
            context: contextParts.join("\n"),
            files,
        })

        setHelpWith("")
        setDescription("")
        setKnowledgeLevel("beginner")
        setFiles([])
    }

    return (
        <section className="fixed inset-0 z-50 flex items-end justify-center bg-black/45 px-3 sm:items-center">
            <div className="max-h-[92svh] w-full max-w-2xl overflow-y-auto rounded-t-lg bg-white p-5 shadow-2xl sm:rounded-lg sm:p-6">
                <div className="mb-5 flex items-start justify-between gap-4">
                    <div>
                        <h2 className="text-lg font-semibold text-neutral-900">
                            Add PDFs and Context
                        </h2>
                        <p className="text-sm text-neutral-500">
                            Attach documents and set the answer style for this chat.
                        </p>
                    </div>

                    <button
                        onClick={onClose}
                        className="rounded-md p-2 text-neutral-500 hover:bg-neutral-100"
                        disabled={uploading}
                        aria-label="Close context modal"
                    >
                        <X size={20} />
                    </button>
                </div>

                <form onSubmit={handleSubmit} className="space-y-5">
                    <div className="grid gap-4 sm:grid-cols-2">
                        <div>
                            <label className="mb-1 block text-sm font-medium text-neutral-700">
                                Help with
                            </label>
                            <input
                                type="text"
                                value={helpWith}
                                onChange={(e) => setHelpWith(e.target.value)}
                                placeholder="Research, legal review, study notes..."
                                className="w-full rounded-lg border border-neutral-200 bg-neutral-50 px-4 py-3 text-sm outline-none focus:border-neutral-900 focus:bg-white"
                            />
                        </div>

                        <div>
                            <label className="mb-1 block text-sm font-medium text-neutral-700">
                                Response style
                            </label>

                            <div className="grid grid-cols-2 gap-2">
                                {[
                                    ["beginner", "Simple"],
                                    ["intermediate", "Practical"],
                                    ["advanced", "Detailed"],
                                    ["expert", "Direct"],
                                ].map(([value, label]) => (
                                    <button
                                        key={value}
                                        type="button"
                                        onClick={() => setKnowledgeLevel(value)}
                                        className={`rounded-lg border px-3 py-2 text-sm transition ${knowledgeLevel === value
                                            ? "border-neutral-950 bg-neutral-950 text-white"
                                            : "border-neutral-200 bg-white text-neutral-700 hover:bg-neutral-50"
                                            }`}
                                    >
                                        {label}
                                    </button>
                                ))}
                            </div>
                        </div>
                    </div>

                    <div>
                        <label className="mb-1 block text-sm font-medium text-neutral-700">
                            PDFs
                        </label>

                        <label className="flex cursor-pointer flex-col items-center justify-center rounded-lg border border-dashed border-teal-300 bg-teal-50/60 px-4 py-7 text-center hover:bg-teal-50">
                            <UploadCloud className="mb-2 text-teal-700" size={30} />
                            <span className="text-sm font-medium text-neutral-700">
                                Select PDF files
                            </span>
                            <span className="mt-1 text-xs text-neutral-400">
                                Multiple files are supported
                            </span>

                            <input
                                type="file"
                                accept="application/pdf"
                                multiple
                                onChange={(e) => setFiles(Array.from(e.target.files ?? []))}
                                className="hidden"
                            />
                        </label>

                        {files.length > 0 && (
                            <div className="mt-3 space-y-2">
                                {files.map((file, index) => (
                                    <div
                                        key={`${file.name}-${file.size}`}
                                        className="flex items-center gap-2 rounded-lg border border-neutral-200 bg-white px-3 py-2 text-sm"
                                    >
                                        <FileText size={16} className="shrink-0 text-teal-700" />
                                        <span className="min-w-0 flex-1 truncate text-neutral-700">{file.name}</span>
                                        <span className="text-xs text-neutral-400">{formatFileSize(file.size)}</span>
                                        <button
                                            type="button"
                                            onClick={() => setFiles((current) => current.filter((_, fileIndex) => fileIndex !== index))}
                                            className="rounded-md p-1 text-neutral-500 hover:bg-neutral-100 hover:text-red-600"
                                            aria-label={`Remove ${file.name}`}
                                        >
                                            <Trash2 size={15} />
                                        </button>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>

                    <div>
                        <label className="mb-1 block text-sm font-medium text-neutral-700">
                            Instructions
                        </label>
                        <textarea
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            placeholder="Add focus areas, sections, preferred format, or constraints..."
                            rows={4}
                            className="w-full resize-none rounded-lg border border-neutral-200 bg-neutral-50 px-4 py-3 text-sm outline-none focus:border-neutral-900 focus:bg-white"
                        />
                    </div>

                    <button
                        type="submit"
                        disabled={uploading || (!files.length && !helpWith.trim() && !description.trim())}
                        className="w-full rounded-lg bg-neutral-950 py-3 text-sm font-semibold text-white transition hover:bg-neutral-800 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                        {uploading ? "Saving..." : "Save to Chat"}
                    </button>
                </form>
            </div>
        </section>
    )
}

function formatFileSize(size: number) {
    if (size < 1024 * 1024) return `${Math.max(1, Math.round(size / 1024))} KB`
    return `${(size / (1024 * 1024)).toFixed(1)} MB`
}
