"use client"
import { useRouter } from "next/navigation";
import { AppContextTypes } from "./ContextTypes";
import { createContext, ReactNode } from "react";

export const AppContext = createContext<AppContextTypes | null>(null);

export const AppProvider =({children}: Readonly<{children: ReactNode}>)=>{

    const router = useRouter()

    async function startNewChat(id: string){
        router.replace(`/?id=${id}`)
        // Make Requrest
    }

    const data: AppContextTypes = {
        startNewChat,
    }

    return(
        <AppContext.Provider value={data} >{children}</AppContext.Provider>
    )
}