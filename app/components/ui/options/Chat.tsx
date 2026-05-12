"use client"

import {
    FileText,
    Globe,
    LayersPlus,
    SendHorizontal,
    TextQuote,
} from "lucide-react"
import { useState } from "react"

export const ChatOptions = () => {
    const [message, setMessage] = useState("")
    const [openLayers, setOpenLayers] = useState(false)

    const handleSend = () => {
        if (!message.trim()) return
        setMessage("")
    }

    return (
        <section className="w-full border-t bg-white/80 px-4 py-3 backdrop-blur-md">
            <div className="relative mx-auto flex max-w-4xl items-center gap-3">
                <LayerOptions open={openLayers} />

                <div className="flex w-full items-center rounded-xl bg-gray-100 px-3 py-2 ring-black/10 transition focus-within:ring-2">
                    <button
                        type="button"
                        onClick={() => setOpenLayers((prev) => !prev)}
                        className="rounded-lg p-2 transition hover:bg-gray-200"
                    >
                        <LayersPlus size={20} className="text-gray-600" />
                    </button>

                    <input
                        type="text"
                        placeholder="Start asking about your PDF or web..."
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        className="flex-1 bg-transparent px-2 text-sm text-gray-800 outline-none placeholder:text-gray-400"
                    />
                </div>

                <button
                    onClick={handleSend}
                    className="rounded-xl bg-black p-3 text-white transition hover:bg-black/90 disabled:opacity-50"
                    disabled={!message.trim()}
                >
                    <SendHorizontal size={18} />
                </button>
            </div>
        </section>
    )
}

interface LayerOptionsProps {
    open: boolean
}

const LayerOptions = ({ open }: LayerOptionsProps) => {
    if (!open) return null

    return (
        <div className="absolute bottom-16 left-0 z-50 w-56 rounded-2xl border bg-white p-2 shadow-xl">
            <LayerOptionItem
                icon={<Globe size={18} />}
                title="Web Search"
                desc="Search latest information"
            />

            <LayerOptionItem
                icon={<FileText size={18} />}
                title="Add PDF"
                desc="Upload document"
            />

            <LayerOptionItem
                icon={<TextQuote size={18} />}
                title="Add Context"
                desc="Paste custom context"
            />
        </div>
    )
}

interface LayerOptionItemProps {
    icon: React.ReactNode
    title: string
    desc: string
}

const LayerOptionItem = ({ icon, title, desc }: LayerOptionItemProps) => {
    return (
        <button className="flex w-full items-center gap-3 rounded-xl px-3 py-2 text-left transition hover:bg-neutral-100">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-neutral-100 text-neutral-700">
                {icon}
            </div>

            <div>
                <p className="text-sm font-medium text-neutral-800">{title}</p>
                <p className="text-xs text-neutral-500">{desc}</p>
            </div>
        </button>
    )
}