"use client"
import { ChatTypes } from "@/types/chats"
import { useEffect, useRef } from "react"

export type Message = {
    id: string
    role: "user" | "assistant"
    content: string
}


export const ChatBox = (props: { messages: ChatTypes[] }) => {
    const bottomRef = useRef<HTMLDivElement | null>(null)

    // auto scroll to bottom
    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" })
    }, [props.messages])

    return (
        <section className="flex-1 overflow-y-auto px-4 py-6">
            <div className="mx-auto max-w-3xl space-y-6">
                {
                    props.messages.map((item, idx)=>(
                        <MessageCycle key={idx} messages={item} />
                    ))
                }
                <div ref={bottomRef} />
            </div>
        </section>
    )
}


const MessageCycle = (props: { messages: ChatTypes }) => {
    return (

        <>
            <ChatMessage key={props.messages.id} message={props.messages.prompt} isUser={true} />
            <ChatMessage key={props.messages.id} message={props.messages.response} isUser={false} />
        </>
    )
}


const ChatMessage = ({ message, isUser }: { isUser: boolean; message: string; }) => {

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
                {message}
            </div>

        </div>
    )
}
