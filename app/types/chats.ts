export interface PdfFileTypes {
    id: number;
    name: string;
    size: number;
    task_id: number;
    created_at: string;
}

export interface TaskTypes {
    id: number;
    title: string;
    updated_at: string;
    conversation: ChatTypes[];
    pdf_files: PdfFileTypes[];
}

export interface OnlyTaskTypes {
    id: number;
    title: string;
    updated_at: string;
}

export type ChatStatus = "complete" | "streaming" | "error";

export interface ChatTypes {
    id: number;
    prompt: string;
    response: string;
    task_id: number;
    is_revised: boolean;
    revised_prompt: string;
    revised_response: string;
    created_at: string;
    updated_at: string;
    status?: ChatStatus;
    error?: string;
    local?: boolean;
}
