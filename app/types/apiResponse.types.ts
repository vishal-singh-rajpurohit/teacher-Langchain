import { ChatTypes } from "./chats";

export interface RegisterAPIRespTypes{
    email: "",
    name: "",
    credits_token: 0,
    is_verified: false,
    updated_at: "",
    tasks: [TaskTypes]
}

export interface TaskTypes{
    id: number;
    title: string;
    updated_at: string;
}

export interface LoadTaskAPIRespTypes{
    message: string;
    success: boolean;
    task_id: number;
    result: ChatTypes[]
}