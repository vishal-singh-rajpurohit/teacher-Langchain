"use client"
import { CircleEllipsis, MessageCirclePlus, Sparkles } from "lucide-react"
import { ChatOptions } from "../options/Chat"
import {ChatBox, type Message} from './Messages'
import ContextModal from "../modal/ContextModel"
import { useSelector } from "react-redux"
import { useAppSelector } from "@/store/hook"

const InitialteCmp = () => { 
    return (
        <section className="flex h-full items-center justify-center px-4">
            <div className="max-w-md text-center">
                <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-neutral-100">
                    <Sparkles size={26} className="text-neutral-700" />
                </div>

                <h1 className="text-2xl font-semibold text-neutral-900">
                    Start by asking questions
                </h1>

                <p className="mt-2 text-sm leading-6 text-neutral-500">
                    Upload PDFs, search the web, and ask anything from your documents.
                </p>

                <div className="mt-6 grid gap-3 text-left text-sm">
                    <button className="rounded-2xl border bg-white px-4 py-3 text-neutral-700 shadow-sm transition hover:bg-neutral-50">
                        Summarize this PDF
                    </button>

                    <button className="rounded-2xl border bg-white px-4 py-3 text-neutral-700 shadow-sm transition hover:bg-neutral-50">
                        Find important points from my document
                    </button>

                    <button className="rounded-2xl border bg-white px-4 py-3 text-neutral-700 shadow-sm transition hover:bg-neutral-50">
                        Search answer from uploaded files
                    </button>
                </div>
            </div>
        </section>
    )
}

// const messages: Message[] = [
//     { id: "1", role: "user", content: "Hi!" },
//     { id: "2", role: "assistant", content: "Hello! How can I help you?" },
//     { id: "3", role: "user", content: "Tell me a joke." },
//     { id: "4", role: "assistant", content: "Why don’t programmers like nature? Too many bugs." },
//     { id: "5", role: "user", content: "Haha nice." },
//     { id: "6", role: "assistant", content: "Glad you liked it!" },
//     { id: "7", role: "user", content: "What is TypeScript?" },
//     { id: "8", role: "assistant", content: "TypeScript is a typed superset of JavaScript." },
//     { id: "9", role: "user", content: "Is it hard to learn?" },
//     { id: "10", role: "assistant", content: "Not really, especially if you know JavaScript." },
//     { id: "11", role: "user", content: "Cool." },
//     { id: "12", role: "assistant", content: "Anything else you'd like to know?" },
//     { id: "13", role: "user", content: "Explain interfaces." },
//     { id: "14", role: "assistant", content: "Interfaces define the shape of objects." },
//     { id: "15", role: "user", content: "Give example." },
//     { id: "16", role: "assistant", content: "Sure! interface User { name: string; age: number; }" },
//     { id: "17", role: "user", content: "Nice." },
//     { id: "18", role: "assistant", content: "Happy to help!" },
//     { id: "19", role: "user", content: "What about types?" },
//     { id: "20", role: "assistant", content: "Types are similar but more flexible than interfaces." },
//     { id: "21", role: "user", content: "Thanks!" },
//     { id: "22", role: "assistant", content: "You're welcome!" }
// ]


interface MainProps {
    onOpenTasks?: () => void
}

const Main = ({ onOpenTasks }: MainProps) => {

    const selected_chat = useAppSelector(state=>state.temp.selected_chat)
    
    return (
        <section className="relative flex h-screen w-full flex-col overflow-hidden bg-white">
            {/* Top Bar */}
            <header className="flex h-14 shrink-0 items-center justify-between border-b px-4">
                <button className="rounded-xl p-2 text-neutral-600 transition hover:bg-neutral-100">
                    <CircleEllipsis onClick={onOpenTasks} size={22} />
                </button>

                <h2 className="text-sm font-medium text-neutral-700">
                    New RAG Chat
                </h2>

                <button className="rounded-xl p-2 text-neutral-600 transition hover:bg-neutral-100">
                    <MessageCirclePlus size={22} />
                </button>
            </header>

            {/* Main Content */}
            <main className="flex-1 overflow-y-auto pb-28">
                {
                    selected_chat.id ? (
                        <ChatBox messages={selected_chat.conversation} />
                    ): (
                        <InitialteCmp />
                    )
                }
                
                {/* <ContextModal onClose={()=>{}} open={true} /> */}
            </main>

            {/* Chat Input */}
            <div className="absolute bottom-0 left-0 right-0 border-t bg-white">
                <ChatOptions />
            </div>
        </section>
    )
}

export default Main