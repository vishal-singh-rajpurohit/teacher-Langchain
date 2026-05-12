"use client"

import { FileText, X } from "lucide-react"
import { useState } from "react"

interface ContextModalProps {
    open: boolean
    onClose: () => void
}

export default function ContextModal({ open, onClose }: ContextModalProps) {
    const [helpWith, setHelpWith] = useState("")
    const [description, setDescription] = useState("")
    const [knowledgeLevel, setKnowledgeLevel] = useState("beginner")
    const [files, setFiles] = useState<FileList | null>(null)

    if (!open) return null

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()

        console.log({
            helpWith,
            description,
            knowledgeLevel,
            files,
        })

        onClose()
    }

    return (
        <section className="fixed inset-0 z-50 flex items-end justify-center bg-black/40 px-3 sm:items-center">
            <div className="w-full max-w-lg rounded-t-3xl bg-white p-5 shadow-2xl sm:rounded-3xl">
                <div className="mb-5 flex items-center justify-between">
                    <div>
                        <h2 className="text-lg font-semibold text-neutral-900">
                            Set Chat Context
                        </h2>
                        <p className="text-sm text-neutral-500">
                            Tell AI how it should help you.
                        </p>
                    </div>

                    <button
                        onClick={onClose}
                        className="rounded-xl p-2 text-neutral-500 hover:bg-neutral-100"
                    >
                        <X size={20} />
                    </button>
                </div>

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="mb-1 block text-sm font-medium text-neutral-700">
                            Help with
                        </label>
                        <input
                            type="text"
                            value={helpWith}
                            onChange={(e) => setHelpWith(e.target.value)}
                            placeholder="Example: Research paper, coding, business plan..."
                            className="w-full rounded-2xl border border-neutral-200 bg-neutral-50 px-4 py-3 text-sm outline-none focus:border-black focus:bg-white"
                        />
                    </div>

                    <div>
                        <label className="mb-1 block text-sm font-medium text-neutral-700">
                            Description
                        </label>
                        <textarea
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            placeholder="Write full context about your task..."
                            rows={4}
                            className="w-full resize-none rounded-2xl border border-neutral-200 bg-neutral-50 px-4 py-3 text-sm outline-none focus:border-black focus:bg-white"
                        />
                    </div>

                    <div>
                        <label className="mb-1 block text-sm font-medium text-neutral-700">
                            PDFs Upload File
                        </label>

                        <label className="flex cursor-pointer flex-col items-center justify-center rounded-2xl border border-dashed border-neutral-300 bg-neutral-50 px-4 py-6 text-center hover:bg-neutral-100">
                            <FileText className="mb-2 text-neutral-500" size={28} />
                            <span className="text-sm font-medium text-neutral-700">
                                Click to upload PDFs
                            </span>
                            <span className="mt-1 text-xs text-neutral-400">
                                You can select multiple PDF files
                            </span>

                            <input
                                type="file"
                                accept="application/pdf"
                                multiple
                                onChange={(e) => setFiles(e.target.files)}
                                className="hidden"
                            />
                        </label>

                        {files && (
                            <p className="mt-2 text-xs text-neutral-500">
                                {files.length} file selected
                            </p>
                        )}
                    </div>

                    <div>
                        <label className="mb-1 block text-sm font-medium text-neutral-700">
                            How much you know?
                        </label>

                        <select
                            value={knowledgeLevel}
                            onChange={(e) => setKnowledgeLevel(e.target.value)}
                            className="w-full rounded-2xl border border-neutral-200 bg-neutral-50 px-4 py-3 text-sm outline-none focus:border-black focus:bg-white"
                        >
                            <option value="beginner">Beginner - Explain simply</option>
                            <option value="intermediate">Intermediate - Give practical details</option>
                            <option value="advanced">Advanced - Give deep technical answer</option>
                            <option value="expert">Expert - Direct and professional</option>
                        </select>
                    </div>

                    <button
                        type="submit"
                        className="w-full rounded-2xl bg-black py-3 text-sm font-semibold text-white transition hover:bg-neutral-800"
                    >
                        Save Context
                    </button>
                </form>
            </div>
        </section>
    )
}