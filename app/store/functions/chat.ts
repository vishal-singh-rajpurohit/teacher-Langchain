import { TaskTypes, ChatTypes, OnlyTaskTypes } from "@/types/chats";
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface initialStateTypes{
    tasks: TaskTypes[]
}

const initialState: initialStateTypes = {
    tasks: []
}

function initialLoadFunc(state: initialStateTypes, action: PayloadAction<{data: [OnlyTaskTypes]}>){
    for(let item of action.payload.data){
        state.tasks.push({
            ...item,
            conversation: []
        })
    }
}

export const chatSlice = createSlice({
    name: 'chat',
    initialState: initialState,
    reducers: {
        initialLoad: initialLoadFunc
    }
})

export const { initialLoad, } = chatSlice.actions
export default chatSlice.reducer