import { TaskTypes } from "@/types/chats";

export interface SendMessageInput {
    prompt: string;
    useWebSearch: boolean;
    context: string | null;
}

export interface AppContextTypes {
    startNewChat: (id: number) => void;
    load_task: (id: number) => Promise<void>;
    clear_chats: () => void;
    create_new_conversation: (prompt?: string) => Promise<TaskTypes | null>;
    send_message: (input: SendMessageInput) => Promise<void>;
    load_chat_files: (taskId: number) => Promise<void>;
    upload_chat_files: (files: File[], taskId?: number) => Promise<TaskTypes | null>;
    delete_chat_file: (taskId: number, fileId: number) => Promise<void>;
}
