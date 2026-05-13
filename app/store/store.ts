import { configureStore } from "@reduxjs/toolkit";
import tempSlice from "./functions/temp";
import authSlice from "./functions/auth";
import chatSlice from "./functions/chat";


export const store = configureStore({
    reducer: {
        temp: tempSlice,
        auth: authSlice,
        chat: chatSlice,
    }
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;