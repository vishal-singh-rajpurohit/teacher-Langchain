"use client"

import ContextModal, { ContextModalSubmit } from "@/components/ui/modal/ContextModel"
import { AppContext } from "@/context/AppContext"
import {
    clearComposerContext,
    setComposerContext,
    setContextModal,
    setWebSearch,
} from "@/store/functions/temp"
import { useAppDispatch, useAppSelector } from "@/store/hook"
import {
    FileText,
    Globe,
    LayersPlus,
    Loader2,
    SendHorizontal,
    TextQuote,
    X,
} from "lucide-react"
import type { ReactNode } from "react"
import { useContext, useState } from "react"

export const ChatOptions = ({ disabled = false }: { disabled?: boolean }) => {
    const dispatch = useAppDispatch()
    const [message, setMessage] = useState("")
    const [openLayers, setOpenLayers] = useState(false)
    const [uploading, setUploading] = useState(false)

    const selectedChat = useAppSelector((state) => state.chat.tasks.find((task) => task.id === state.chat.selectedTaskId))
    const openContext = useAppSelector((state) => state.temp.contextModalOpen)
    const savedContext = useAppSelector((state) => state.temp.composerContext)
    const useWebSearch = useAppSelector((state) => state.temp.webSearchEnabled)
    const appContext = useContext(AppContext)

    if (!appContext) {
        throw new Error("Context not found")
    }

    const { delete_chat_file, send_message, upload_chat_files } = appContext

    const handleSend = async () => {
        if (!message.trim() || disabled) return

        const prompt = message.trim()
        setMessage("")

        await send_message({
            prompt,
            useWebSearch,
            context: savedContext.trim() || null,
        })
    }

    const handleContextSubmit = async ({ context, files }: ContextModalSubmit) => {
        setUploading(true)
        try {
            if (context.trim()) dispatch(setComposerContext({ context: context.trim() }))
            await upload_chat_files(files)
            dispatch(setContextModal({ toggle: false }))
        } finally {
            setUploading(false)
        }
    }

    return (
        <>
            <ContextModal
                open={openContext}
                onClose={() => dispatch(setContextModal({ toggle: false }))}
                onSubmit={handleContextSubmit}
                uploading={uploading}
            />

            <section className="w-full border-t border-neutral-200 bg-white/95 px-3 py-3 backdrop-blur-md md:px-4">
                <div className="relative mx-auto max-w-4xl space-y-3">
                    <LayerOptions
                        open={openLayers}
                        useWebSearch={useWebSearch}
                        onOpenContext={() => {
                            setOpenLayers(false)
                            dispatch(setContextModal({ toggle: true }))
                        }}
                        onToggleWeb={() => dispatch(setWebSearch({ enabled: !useWebSearch }))}
                    />

                    {(selectedChat?.pdf_files.length || savedContext || useWebSearch) ? (
                        <div className="flex flex-wrap items-center gap-2 text-xs">
                            {useWebSearch && (
                                <Pill icon={<Globe size={14} />} label="Web search" onRemove={() => dispatch(setWebSearch({ enabled: false }))} />
                            )}

                            {savedContext && (
                                <Pill icon={<TextQuote size={14} />} label="Context added" onRemove={() => dispatch(clearComposerContext())} />
                            )}

                            {selectedChat?.pdf_files.map((file) => (
                                <Pill
                                    key={file.id}
                                    icon={<FileText size={14} />}
                                    label={file.name}
                                    onRemove={() => {
                                        void delete_chat_file(selectedChat.id, file.id)
                                    }}
                                />
                            ))}
                        </div>
                    ) : null}

                    <div className="flex items-end gap-2 md:gap-3">
                        <div className="flex min-h-12 w-full items-end rounded-lg border border-neutral-200 bg-neutral-50 px-2 transition focus-within:border-neutral-400 focus-within:bg-white md:px-3">
                            <button
                                type="button"
                                onClick={() => setOpenLayers((prev) => !prev)}
                                className="mb-1 shrink-0 rounded-md p-2 text-neutral-600 transition hover:bg-neutral-200"
                                aria-label="Add tools or files"
                            >
                                <LayersPlus size={20} />
                            </button>

                            <textarea
                                rows={1}
                                placeholder="Ask anything about your PDF..."
                                value={message}
                                onChange={(e) => setMessage(e.target.value)}
                                onKeyDown={(e) => {
                                    if (e.key === "Enter" && !e.shiftKey) {
                                        e.preventDefault()
                                        void handleSend()
                                    }
                                }}
                                className="max-h-32 min-h-11 flex-1 resize-none bg-transparent px-2 py-3 text-sm leading-6 text-neutral-900 outline-none placeholder:text-neutral-400"
                            />
                        </div>

                        <button
                            onClick={() => void handleSend()}
                            className="flex h-12 w-12 shrink-0 items-center justify-center rounded-lg bg-neutral-950 text-white transition hover:bg-neutral-800 disabled:cursor-not-allowed disabled:opacity-50"
                            disabled={!message.trim() || disabled}
                            aria-label="Send message"
                        >
                            {disabled ? <Loader2 size={18} className="animate-spin" /> : <SendHorizontal size={18} />}
                        </button>
                    </div>
                </div>
            </section>
        </>
    )
}

interface LayerOptionsProps {
    open: boolean
    useWebSearch: boolean
    onOpenContext: () => void
    onToggleWeb: () => void
}

const LayerOptions = ({ open, useWebSearch, onOpenContext, onToggleWeb }: LayerOptionsProps) => {
    if (!open) return null

    return (
        <div className="absolute bottom-16 left-0 z-40 w-64 rounded-lg border border-neutral-200 bg-white p-2 shadow-xl">
            <LayerOptionItem
                icon={<Globe size={18} />}
                title={useWebSearch ? "Web Search On" : "Web Search"}
                desc="Search latest information"
                onClick={onToggleWeb}
            />

            <LayerOptionItem
                icon={<FileText size={18} />}
                title="Add PDF"
                desc="Upload document"
                onClick={onOpenContext}
            />

            <LayerOptionItem
                icon={<TextQuote size={18} />}
                title="Add Context"
                desc="Paste custom context"
                onClick={onOpenContext}
            />
        </div>
    )
}

interface LayerOptionItemProps {
    icon: ReactNode
    title: string
    desc: string
    onClick: () => void
}

const LayerOptionItem = ({ icon, title, desc, onClick }: LayerOptionItemProps) => {
    return (
        <button
            onClick={onClick}
            className="flex w-full items-center gap-3 rounded-md px-3 py-2 text-left transition hover:bg-neutral-100"
        >
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-md bg-neutral-100 text-neutral-700">
                {icon}
            </div>

            <div>
                <p className="text-sm font-medium text-neutral-800">{title}</p>
                <p className="text-xs text-neutral-500">{desc}</p>
            </div>
        </button>
    )
}

const Pill = ({ icon, label, onRemove }: { icon: ReactNode; label: string; onRemove: () => void }) => {
    return (
        <span className="inline-flex max-w-full items-center gap-1 rounded-md border border-neutral-200 bg-white px-2 py-1 text-neutral-600 shadow-sm">
            {icon}
            <span className="max-w-40 truncate">{label}</span>
            <button onClick={onRemove} className="rounded p-0.5 hover:bg-neutral-100" aria-label={`Remove ${label}`}>
                <X size={13} />
            </button>
        </span>
    )
}
