export interface RegisterAPITypes{
    email: string;
    name: string;
    password: string;
    conform_password: string;
}

export interface LoginAPITypes{
    email: string;
    password: string;
}

export interface SendChatStreamRequestTypes {
    prompt: string;
    useWebSearch: boolean;
    context: string | null;
}

