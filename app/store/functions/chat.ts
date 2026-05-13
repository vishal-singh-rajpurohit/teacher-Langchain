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

function load_conversation_chat_Func(state: initialStateTypes, action: PayloadAction<{
    task_id: number;
    conversations: ChatTypes[];
}>){
    const current_task = state.tasks.filter(task => task.id === action.payload.task_id)[0];
    current_task.conversation = action.payload.conversations;

    const filtered = state.tasks.filter(task => task.id !== action.payload.task_id);

    state.tasks = [
        current_task,
        ...filtered
    ]
}

export const chatSlice = createSlice({
    name: 'chat',
    initialState: initialState,
    reducers: {
        initialLoad: initialLoadFunc,
        load_conversation_chat: load_conversation_chat_Func
    }
})

export const { initialLoad, load_conversation_chat } = chatSlice.actions
export default chatSlice.reducer