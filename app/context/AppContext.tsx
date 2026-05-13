"use client"
import { useRouter } from "next/navigation";
import { AppContextTypes } from "./ContextTypes";
import { createContext, ReactNode, useEffect } from "react";
import api from "@/config/axios.config";
import { useAppDispatch } from "@/store/hook";
import { LoadTaskAPIRespTypes, RegisterAPIRespTypes } from "@/types/apiResponse.types";
import { AxiosResponse } from "axios";
import { login } from "@/store/functions/auth";
import { initialLoad, load_conversation_chat } from "@/store/functions/chat";
import { setSelectChat } from "@/store/functions/temp";

export const AppContext = createContext<AppContextTypes | null>(null);

export const AppProvider = ({ children }: Readonly<{ children: ReactNode }>) => {

    const router = useRouter()
    const disp = useAppDispatch()

    async function startNewChat(id: number) {
        router.replace(`/?id=${id}`)
        // Make Requrest
    }

    function clear_chats(){
        disp(setSelectChat({
            id: '',
            task: {
                id: 0,
                title: '',
                updated_at: '',
                conversation: []
            }
        }))
    }

    async function load_task(id: number){
        try {
            const resp: AxiosResponse<LoadTaskAPIRespTypes> = await api.get(`/llm/get-chats/?id=${id}`, {withCredentials: true})

            disp(load_conversation_chat({
                task_id: resp.data.task_id,
                conversations: resp.data.result
            }))
            disp(setSelectChat({
                id: String(id),
                task: {
                    id: resp.data.task_id,
                    title: "",
                    updated_at: "",
                    conversation: resp.data.result
                }
            }))
        } catch (error) {
            console.log('Error in load: ', error)
        }
    }

    async function create_new_conversation(){
        try {
            const resp = await api.post('/llm/new', {}, {withCredentials: true})
        } catch (error) {
            console.log('Error in creating: ', error)
        }
    }

    useEffect(() => {
        const timer = setTimeout(async () => {
            try {
                const resp: AxiosResponse<RegisterAPIRespTypes> = await api.get("/auth", {
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

                

                if (!resp.data.is_verified) router.replace('/auth/verify')
                else router.replace('/')

            } catch (error) {
                router.replace('/auth/login')
            }
        }, 600)

        return () => clearTimeout(timer)
    }, [])

    const data: AppContextTypes = {
        startNewChat,
        load_task
    }

    return (
        <AppContext.Provider value={data} >{children}</AppContext.Provider>
    )
}