"use client"

import { AppContext } from "@/context/AppContext"
import { setContextModal } from "@/store/functions/temp"
import { useAppDispatch } from "@/store/hook"
import { useAppSelector } from "@/store/hook"
import { Bot, FileUp, MessageCirclePlus, PanelLeft, Sparkles } from "lucide-react"
import { useContext } from "react"
import { ChatOptions } from "../options/Chat"
import { ChatBox } from "./Messages"

const starterPrompts = [
    "Summarize this PDF",
    "Find the key risks and recommendations",
    "Create study notes from this document",
]

const InitialteCmp = ({ onPrompt }: { onPrompt: (prompt: string) => void }) => {
    const dispatch = useAppDispatch()

    return (
        <section className="flex min-h-full items-center justify-center px-4 py-10">
            <div className="w-full max-w-3xl">
                <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-teal-50 text-teal-700 ring-1 ring-teal-100">
                    <Bot size={30} />
                </div>

                <h1 className="mt-5 text-center text-3xl font-semibold tracking-tight text-neutral-950 sm:text-4xl">
                    PDF AI Agent
                </h1>

                <p className="mx-auto mt-3 max-w-xl text-center text-sm leading-6 text-neutral-500 sm:text-base">
                    Upload a PDF, then ask for summaries, explanations, tables, citations, or document-aware answers.
                </p>

                <div className="mt-8 grid gap-3 sm:grid-cols-3">
                    <button
                        onClick={() => dispatch(setContextModal({ toggle: true }))}
                        className="flex min-h-28 flex-col justify-between rounded-lg border border-teal-200 bg-teal-50 p-4 text-left text-teal-950 transition hover:bg-teal-100"
                    >
                        <FileUp size={22} />
                        <span className="text-sm font-semibold">Upload PDF</span>
                    </button>

                    {starterPrompts.map((prompt) => (
                        <button
                            key={prompt}
                            onClick={() => onPrompt(prompt)}
                            className="flex min-h-28 flex-col justify-between rounded-lg border border-neutral-200 bg-white p-4 text-left text-neutral-800 shadow-sm transition hover:border-neutral-300 hover:bg-neutral-50"
                        >
                            <Sparkles size={20} className="text-amber-600" />
                            <span className="text-sm font-medium">{prompt}</span>
                        </button>
                    ))}
                </div>
            </div>
        </section>
    )
}

interface MainProps {
    onOpenTasks?: () => void
}

const Main = ({ onOpenTasks }: MainProps) => {
    const selectedTaskId = useAppSelector((state) => state.chat.selectedTaskId)
    const selectedChat = useAppSelector((state) => state.chat.tasks.find((task) => task.id === state.chat.selectedTaskId))
    const sending = useAppSelector((state) => state.chat.sending)

    const context = useContext(AppContext)

    if (!context) {
        throw new Error("Context not found")
    }

    const { clear_chats, send_message } = context
    const title = selectedChat?.title || "New PDF Chat"
    const fileCount = selectedChat?.pdf_files.length ?? 0

    return (
        <section className="relative flex h-svh w-full flex-col overflow-hidden bg-white">
            <header className="flex h-16 shrink-0 items-center justify-between border-b border-neutral-200 bg-white px-3 sm:px-4">
                {onOpenTasks ? (
                    <button
                        onClick={onOpenTasks}
                        className="rounded-lg p-2 text-neutral-600 transition hover:bg-neutral-100"
                        aria-label="Open chats"
                    >
                        <PanelLeft size={22} />
                    </button>
                ) : (
                    <div className="w-10" />
                )}

                <div className="min-w-0 text-center">
                    <h2 className="mx-auto max-w-[54vw] truncate text-sm font-semibold text-neutral-900 md:max-w-xl">
                        {title}
                    </h2>
                    <div className="mt-1 flex items-center justify-center gap-2 text-xs text-neutral-500">
                        <span>{fileCount} PDF{fileCount === 1 ? "" : "s"}</span>
                        {sending && (
                            <>
                                <span className="h-1 w-1 rounded-full bg-neutral-300" />
                                <span>Thinking</span>
                            </>
                        )}
                    </div>
                </div>

                <button
                    className="rounded-lg p-2 text-neutral-600 transition hover:bg-neutral-100"
                    onClick={clear_chats}
                    aria-label="Start new chat"
                >
                    <MessageCirclePlus size={22} />
                </button>
            </header>

            <main className="flex-1 overflow-y-auto pb-36">
                {selectedTaskId && selectedChat ? (
                    <ChatBox messages={selectedChat.conversation} />
                ) : (
                    <InitialteCmp
                        onPrompt={(prompt) => {
                            void send_message({
                                prompt,
                                useWebSearch: false,
                                context: null,
                            })
                        }}
                    />
                )}
            </main>

            <div className="absolute bottom-0 left-0 right-0 border-t bg-white">
                <ChatOptions disabled={sending} />
            </div>
        </section>
    )
}

export default Main
