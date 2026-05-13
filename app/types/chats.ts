export interface TaskTypes{
    id: number;
    title: string;
    updated_at: string;
    conversation: ChatTypes[];
}

export interface OnlyTaskTypes{
    id: number;
    title: string;
    updated_at: string;
}



export interface ChatTypes{
    id: number;
    prompt: string;
    response: string;
    task_id: number;
    is_revised: boolean;
    revised_prompt: string;
    revised_response: string;
    created_at: string;
    updated_at: string;
}
