import { ChatTypes, OnlyTaskTypes, PdfFileTypes, TaskTypes } from "@/types/chats";
import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { cleanAssistantResponse } from "@/lib/assistant-response";

interface InitialStateTypes {
    tasks: TaskTypes[];
    selectedTaskId: number | null;
    sending: boolean;
    streamError: string;
}

const initialState: InitialStateTypes = {
    tasks: [],
    selectedTaskId: null,
    sending: false,
    streamError: "",
}

function findTask(state: InitialStateTypes, taskId: number) {
    return state.tasks.find((task) => task.id === taskId)
}

function initialLoadFunc(state: InitialStateTypes, action: PayloadAction<{ data: OnlyTaskTypes[] }>) {
    state.tasks = action.payload.data.map((item) => {
        const existing = findTask(state, item.id)

        return {
            ...item,
            conversation: existing?.conversation ?? [],
            pdf_files: existing?.pdf_files ?? [],
        }
    })
}

function loadConversationChatFunc(state: InitialStateTypes, action: PayloadAction<{
    task_id: number;
    conversations: ChatTypes[];
}>) {
    const currentTask = findTask(state, action.payload.task_id)

    if (!currentTask) return

    currentTask.conversation = action.payload.conversations.map((message) => ({
        ...message,
        response: cleanAssistantResponse(message.response),
        revised_response: message.revised_response
            ? cleanAssistantResponse(message.revised_response)
            : message.revised_response,
        status: message.status ?? "complete",
    }))

    state.tasks = [
        currentTask,
        ...state.tasks.filter((task) => task.id !== action.payload.task_id),
    ]
}

function pushNewChatFunc(state: InitialStateTypes, action: PayloadAction<{ data: TaskTypes | OnlyTaskTypes }>) {
    const newTask: TaskTypes = {
        id: action.payload.data.id,
        title: action.payload.data.title,
        conversation: "conversation" in action.payload.data ? action.payload.data.conversation : [],
        updated_at: action.payload.data.updated_at,
        pdf_files: "pdf_files" in action.payload.data ? action.payload.data.pdf_files : [],
    }

    state.tasks = [
        newTask,
        ...state.tasks.filter((task) => task.id !== newTask.id),
    ]
    state.selectedTaskId = newTask.id
}

function setSelectedTaskFunc(state: InitialStateTypes, action: PayloadAction<{ taskId: number }>) {
    state.selectedTaskId = action.payload.taskId
}

function clearSelectedTaskFunc(state: InitialStateTypes) {
    state.selectedTaskId = null
    state.streamError = ""
}

function setSendingFunc(state: InitialStateTypes, action: PayloadAction<{ sending: boolean }>) {
    state.sending = action.payload.sending
}

function setTaskFilesFunc(state: InitialStateTypes, action: PayloadAction<{ taskId: number; files: PdfFileTypes[] }>) {
    const currentTask = findTask(state, action.payload.taskId)
    if (!currentTask) return

    currentTask.pdf_files = action.payload.files
}

function addTaskFilesFunc(state: InitialStateTypes, action: PayloadAction<{ taskId: number; files: PdfFileTypes[] }>) {
    const currentTask = findTask(state, action.payload.taskId)
    if (!currentTask) return

    const incomingIds = new Set(action.payload.files.map((file) => file.id))
    currentTask.pdf_files = [
        ...action.payload.files,
        ...currentTask.pdf_files.filter((file) => !incomingIds.has(file.id)),
    ]
}

function removeTaskFileFunc(state: InitialStateTypes, action: PayloadAction<{ taskId: number; fileId: number }>) {
    const currentTask = findTask(state, action.payload.taskId)
    if (!currentTask) return

    currentTask.pdf_files = currentTask.pdf_files.filter((file) => file.id !== action.payload.fileId)
}

function appendChatMessageFunc(state: InitialStateTypes, action: PayloadAction<{ taskId: number; message: ChatTypes }>) {
    const currentTask = findTask(state, action.payload.taskId)
    if (!currentTask) return

    currentTask.conversation.push(action.payload.message)
    currentTask.updated_at = new Date().toISOString()
}

function appendAssistantDeltaFunc(state: InitialStateTypes, action: PayloadAction<{
    taskId: number;
    messageId: number;
    delta: string;
}>) {
    const currentTask = findTask(state, action.payload.taskId)
    const currentMessage = currentTask?.conversation.find((message) => message.id === action.payload.messageId)

    if (!currentMessage) return

    currentMessage.response += action.payload.delta
    currentMessage.status = "streaming"
}

function finalizeChatMessageFunc(state: InitialStateTypes, action: PayloadAction<{
    taskId: number;
    localMessageId: number;
    message: ChatTypes;
}>) {
    const currentTask = findTask(state, action.payload.taskId)
    if (!currentTask) return

    const messageIndex = currentTask.conversation.findIndex((message) => message.id === action.payload.localMessageId)
    const finalMessage = {
        ...action.payload.message,
        response: cleanAssistantResponse(action.payload.message.response),
        revised_response: action.payload.message.revised_response
            ? cleanAssistantResponse(action.payload.message.revised_response)
            : action.payload.message.revised_response,
        status: "complete" as const,
        local: false,
    }

    if (messageIndex >= 0) {
        currentTask.conversation[messageIndex] = finalMessage
    } else {
        currentTask.conversation.push(finalMessage)
    }
}

function markChatMessageErrorFunc(state: InitialStateTypes, action: PayloadAction<{
    taskId: number;
    messageId: number;
    error: string;
}>) {
    const currentTask = findTask(state, action.payload.taskId)
    const currentMessage = currentTask?.conversation.find((message) => message.id === action.payload.messageId)

    if (!currentMessage) return

    currentMessage.status = "error"
    currentMessage.error = action.payload.error
    state.streamError = action.payload.error
}

export const chatSlice = createSlice({
    name: 'chat',
    initialState: initialState,
    reducers: {
        initialLoad: initialLoadFunc,
        load_conversation_chat: loadConversationChatFunc,
        push_new_chat: pushNewChatFunc,
        setSelectedTask: setSelectedTaskFunc,
        clearSelectedTask: clearSelectedTaskFunc,
        setSending: setSendingFunc,
        setTaskFiles: setTaskFilesFunc,
        addTaskFiles: addTaskFilesFunc,
        removeTaskFile: removeTaskFileFunc,
        appendChatMessage: appendChatMessageFunc,
        appendAssistantDelta: appendAssistantDeltaFunc,
        finalizeChatMessage: finalizeChatMessageFunc,
        markChatMessageError: markChatMessageErrorFunc,
    }
})

export const {
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
} = chatSlice.actions
export default chatSlice.reducer
