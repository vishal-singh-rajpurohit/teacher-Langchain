"use client"

import { ChatTypes } from "@/types/chats"
import { cleanAssistantResponse } from "@/lib/assistant-response"
import { Bot, UserRound } from "lucide-react"
import dynamic from "next/dynamic"
import { memo, useEffect, useRef } from "react"
import remarkGfm from "remark-gfm"

const ReactMarkdown = dynamic(() => import("react-markdown"), {
  ssr: false,
})

export const ChatBox = memo(function ChatBox({ messages }: { messages: ChatTypes[] }) {
  const bottomRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  if (!messages.length) {
    return (
      <section className="flex h-full items-center justify-center px-4 py-6 text-center text-sm text-neutral-400">
        Ask a question to start this PDF chat.
      </section>
    )
  }

  return (
    <section className="flex-1 bg-white px-3 py-6 sm:px-4">
      <div className="mx-auto max-w-4xl space-y-8">
        {messages.map((item, idx) => (
          <MessageCycle key={item.id ?? idx} message={item} />
        ))}
        <div ref={bottomRef} />
      </div>
    </section>
  )
})

const MessageCycle = memo(function MessageCycle({ message }: { message: ChatTypes }) {
  return (
    <>
      <ChatMessage message={message.prompt} isUser />
      <ChatMessage
        message={message.response}
        isUser={false}
        streaming={message.status === "streaming"}
        error={message.error}
      />
    </>
  )
})

interface ChatMessageProps {
  isUser: boolean
  message: string
  streaming?: boolean
  error?: string
}

const ChatMessage = memo(function ChatMessage(props: ChatMessageProps) {
  const {
    message,
    isUser,
    streaming = false,
    error,
  } = props
  const displayMessage = isUser ? message : cleanAssistantResponse(message)
  const assistantMessage = displayMessage || (streaming ? "Thinking..." : "")

  return (
    <div className={`flex gap-3 ${isUser ? "justify-end" : "justify-start"}`}>
      {!isUser && (
        <div className="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-teal-50 text-teal-700 ring-1 ring-teal-100">
          <Bot size={17} />
        </div>
      )}
      <div
        className={`
          max-w-[86%] rounded-lg px-4 py-3 text-sm leading-7 shadow-sm md:max-w-[78%] md:px-5 md:py-4
          ${isUser
            ? "bg-neutral-950 text-white"
            : "border border-neutral-200 bg-neutral-50 text-neutral-800"
          }
        `}
      >
        {isUser ? (
          <p className="whitespace-pre-wrap break-words">{displayMessage}</p>
        ) : (
          <div className="prose prose-sm max-w-none break-words prose-neutral">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {assistantMessage}
            </ReactMarkdown>
            {streaming && (
              <span className="mt-1 inline-block h-4 w-1 animate-pulse rounded-full bg-teal-600 align-middle" />
            )}
            {error && (
              <p className="mt-3 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-600">
                {error}
              </p>
            )}
          </div>
        )}
      </div>
      {isUser && (
        <div className="mt-1 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-neutral-900 text-white">
          <UserRound size={16} />
        </div>
      )}
    </div>
  )
})
