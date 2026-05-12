"use client"
import { useEffect, useRef } from "react"

export type Message = {
    id: string
    role: "user" | "assistant"
    content: string
}

interface ChatBoxProps {
    messages: Message[]
}


export const ChatBox = ({ messages }: ChatBoxProps) => {
    const bottomRef = useRef<HTMLDivElement | null>(null)

    // auto scroll to bottom
    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" })
    }, [messages])

    return (
        <section className="flex-1 overflow-y-auto px-4 py-6">
            <div className="mx-auto max-w-3xl space-y-6">

                {messages.map((msg) => (
                    <ChatMessage key={msg.id} message={msg} />
                ))}

                <div ref={bottomRef} />
            </div>
        </section>
    )
}

interface ChatMessageProps {
    message: {
        role: "user" | "assistant"
        content: string
    }
}



const ChatMessage = ({ message }: ChatMessageProps) => {
    const isUser = message.role === "user"

    return (
        <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>

            <div
                className={`
                    max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-6
                    ${isUser
                        ? "bg-black text-white"
                        : "bg-neutral-100 text-neutral-800"}
                `}
            >
                {message.content}
            </div>

        </div>
    )
}
