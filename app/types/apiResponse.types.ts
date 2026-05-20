import { ChatTypes, OnlyTaskTypes, PdfFileTypes } from "./chats";

export interface RegisterAPIRespTypes{
    email: string;
    name: string;
    credits_token: number;
    is_verified: boolean;
    updated_at: string;
    tasks: OnlyTaskTypes[];
}

export interface LoadTaskAPIRespTypes{
    message: string;
    success: boolean;
    task_id: number;
    result: ChatTypes[]
}

export interface CreateTaskAPIRespTypes{
    id?: number;
    task_id: number;
    title: string;
    updated_at: string;
}

export type UploadPdfAPIRespTypes = PdfFileTypes[] | { files: PdfFileTypes[] };

export type ListPdfAPIRespTypes = PdfFileTypes[] | { files: PdfFileTypes[] };

export type SendChatStreamEventTypes =
    | { type: "delta"; delta: string }
    | { type: "done"; message: ChatTypes }
    | { type: "error"; message: string }
    | { token: string }
    | { done: true; chat_id: number; task_id: number }
    | { error: true; message: string };
