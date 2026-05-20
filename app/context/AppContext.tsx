"use client"
import { usePathname, useRouter } from "next/navigation";
import { AppContextTypes } from "./ContextTypes";
import { createContext, ReactNode, useCallback, useEffect } from "react";
import api from "@/config/axios.config";
import { API_BASE_URL } from "@/config/api-base";
import { useAppDispatch, useAppSelector } from "@/store/hook";
import {
    ListPdfAPIRespTypes,
    LoadTaskAPIRespTypes,
    RegisterAPIRespTypes,
    CreateTaskAPIRespTypes,
    SendChatStreamEventTypes,
    UploadPdfAPIRespTypes,
} from "@/types/apiResponse.types";
import { AxiosResponse } from "axios";
import { login } from "@/store/functions/auth";
import {
    addTaskFiles,
    appendAssistantDelta,
    appendChatMessage,
    clearSelectedTask,
    finalizeChatMessage,
    initialLoad,
    load_conversation_chat,
    markChatMessageError,
    push_new_chat,
    removeTaskFile,
    setSelectedTask,
    setSending,
    setTaskFiles,
} from "@/store/functions/chat";
import { setLoading } from "@/store/functions/temp";
import { TaskTypes } from "@/types/chats";
import { SendChatStreamRequestTypes } from "@/types/apiRequest.types";
import { cleanAssistantResponse } from "@/lib/assistant-response";

export const AppContext = createContext<AppContextTypes | null>(null);

function parseStreamLine(line: string): SendChatStreamEventTypes | null {
    const trimmed = line.trim()
    if (!trimmed) return null

    const payload = trimmed.startsWith("data:")
        ? trimmed.slice(5).trim()
        : trimmed

    if (!payload || payload === "[DONE]") return null

    return JSON.parse(payload) as SendChatStreamEventTypes
}

export const AppProvider = ({ children }: Readonly<{ children: ReactNode }>) => {

    const router = useRouter()
    const pathname = usePathname()
    const disp = useAppDispatch()
    const selectedTaskId = useAppSelector((state) => state.chat.selectedTaskId)
    const tasks = useAppSelector((state) => state.chat.tasks)

    const normalizeFiles = (data: UploadPdfAPIRespTypes | ListPdfAPIRespTypes) => {
        return Array.isArray(data) ? data : data.files
    }

    const startNewChat = useCallback((id: number) => {
        disp(setSelectedTask({ taskId: id }))
        router.replace(`/?id=${id}`)
    }, [disp, router])

    const clear_chats = useCallback(() => {
        router.replace(`/`)
        disp(clearSelectedTask())
    }, [disp, router])

    const load_chat_files = useCallback(async (taskId: number) => {
        try {
            const resp: AxiosResponse<ListPdfAPIRespTypes> = await api.get(`/llm/${taskId}/files`, { withCredentials: true })
            disp(setTaskFiles({
                taskId,
                files: normalizeFiles(resp.data),
            }))
        } catch (error) {
            console.log('Error in loading files: ', error)
        }
    }, [disp])

    const load_task = useCallback(async (id: number) => {
        try {
            disp(setLoading({ toggle: true }))
            const resp: AxiosResponse<LoadTaskAPIRespTypes> = await api.get(`/llm/get-chats/?id=${id}`, { withCredentials: true })

            disp(load_conversation_chat({
                task_id: resp.data.task_id,
                conversations: resp.data.result
            }))
            disp(setSelectedTask({ taskId: resp.data.task_id }))
            await load_chat_files(resp.data.task_id)
        } catch (error) {
            console.log('Error in load: ', error)
        } finally {
            disp(setLoading({ toggle: false }))
        }
    }, [disp, load_chat_files])

    const create_new_conversation = useCallback(async (prompt = "New PDF chat") => {
        try {
            const resp: AxiosResponse<CreateTaskAPIRespTypes> = await api.post('/llm/new', { prompt }, { withCredentials: true })
            const taskId = resp.data.id ?? resp.data.task_id
            const data: TaskTypes = {
                id: taskId,
                title: resp.data.title,
                updated_at: resp.data.updated_at,
                conversation: [],
                pdf_files: [],
            }

            disp(push_new_chat({
                data
            }))
            startNewChat(data.id)

            return data
        } catch (error) {
            console.log('Error in creating: ', error)
            return null
        }
    }, [disp, startNewChat])

    const getOrCreateSelectedTask = useCallback(async (prompt?: string) => {
        if (selectedTaskId) {
            return tasks.find((task) => task.id === selectedTaskId) ?? null
        }

        return create_new_conversation(prompt)
    }, [create_new_conversation, selectedTaskId, tasks])

    const upload_chat_files = useCallback(async (files: File[], taskId?: number) => {
        if (!files.length) {
            return taskId ? tasks.find((task) => task.id === taskId) ?? null : getOrCreateSelectedTask()
        }

        const targetTask = taskId
            ? tasks.find((task) => task.id === taskId) ?? null
            : await getOrCreateSelectedTask("New PDF chat")

        if (!targetTask) return null

        const formData = new FormData()
        files.forEach((file) => formData.append("files[]", file))

        try {
            const resp: AxiosResponse<UploadPdfAPIRespTypes> = await api.post(`/llm/${targetTask.id}/files`, formData, {
                withCredentials: true,
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            })

            disp(addTaskFiles({
                taskId: targetTask.id,
                files: normalizeFiles(resp.data),
            }))

            return targetTask
        } catch (error) {
            console.log('Error in uploading files: ', error)
            return targetTask
        }
    }, [disp, getOrCreateSelectedTask, tasks])

    const delete_chat_file = useCallback(async (taskId: number, fileId: number) => {
        try {
            await api.delete(`/llm/${taskId}/files/${fileId}`, { withCredentials: true })
            disp(removeTaskFile({ taskId, fileId }))
        } catch (error) {
            console.log('Error in deleting file: ', error)
        }
    }, [disp])

    const send_message = useCallback(async (input: SendChatStreamRequestTypes) => {
        const targetTask = await getOrCreateSelectedTask(input.prompt)
        if (!targetTask) return

        const localMessageId = -Date.now()
        const now = new Date().toISOString()

        disp(setSending({ sending: true }))
        disp(appendChatMessage({
            taskId: targetTask.id,
            message: {
                id: localMessageId,
                prompt: input.prompt,
                response: "",
                task_id: targetTask.id,
                is_revised: false,
                revised_prompt: "",
                revised_response: "",
                created_at: now,
                updated_at: now,
                status: "streaming",
                local: true,
            },
        }))

        try {
            const resp = await fetch(`${API_BASE_URL}/llm/${targetTask.id}/chat/stream`, {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(input),
            })

            if (!resp.ok || !resp.body) {
                throw new Error("Unable to stream the assistant response.")
            }

            const reader = resp.body.getReader()
            const decoder = new TextDecoder()
            let buffer = ""

            while (true) {
                const { done, value } = await reader.read()
                if (done) break

                buffer += decoder.decode(value, { stream: true })
                const lines = buffer.split("\n")
                buffer = lines.pop() ?? ""

                for (const line of lines) {
                    const event = parseStreamLine(line)
                    if (!event) continue

                    if ("type" in event && event.type === "delta") {
                        disp(appendAssistantDelta({
                            taskId: targetTask.id,
                            messageId: localMessageId,
                            delta: cleanAssistantResponse(event.delta),
                        }))
                    }

                    if ("token" in event) {
                        disp(appendAssistantDelta({
                            taskId: targetTask.id,
                            messageId: localMessageId,
                            delta: cleanAssistantResponse(event.token),
                        }))
                    }

                    if ("type" in event && event.type === "done") {
                        disp(finalizeChatMessage({
                            taskId: targetTask.id,
                            localMessageId,
                            message: event.message,
                        }))
                    }

                    if ("type" in event && event.type === "error") {
                        throw new Error(event.message)
                    }

                    if ("error" in event && event.error) {
                        throw new Error(event.message)
                    }
                }
            }
        } catch (error) {
            const message = error instanceof Error ? error.message : "Something went wrong while streaming."
            disp(markChatMessageError({
                taskId: targetTask.id,
                messageId: localMessageId,
                error: message,
            }))
        } finally {
            disp(setSending({ sending: false }))
        }
    }, [disp, getOrCreateSelectedTask])

    useEffect(() => {
        const timer = setTimeout(async () => {
            try {
                const resp: AxiosResponse<RegisterAPIRespTypes> = await api.get("/auth/", {
                    withCredentials: true
                })

                disp(login({
                    data: {
                        name: resp.data.name,
                        email: resp.data.email,
                        credits_token: resp.data.credits_token,
                        is_verified: resp.data.is_verified,
                        joinedAt: resp.data.updated_at
                    }
                }))

                disp(initialLoad({ data: resp.data.tasks }))

                if (!resp.data.is_verified && pathname !== '/auth/verify') {
                    router.replace('/auth/verify')
                } else if (resp.data.is_verified && pathname.startsWith('/auth')) {
                    router.replace('/')
                }

            } catch {
                if (!pathname.startsWith('/auth')) {
                    router.replace('/auth/login')
                }
            }
        }, 600)

        return () => clearTimeout(timer)
    }, [disp, pathname, router])

    const data: AppContextTypes = {
        startNewChat,
        load_task,
        create_new_conversation,
        clear_chats,
        delete_chat_file,
        load_chat_files,
        send_message,
        upload_chat_files,
    }

    return (
        <AppContext.Provider value={data} >{children}</AppContext.Provider>
    )
}
