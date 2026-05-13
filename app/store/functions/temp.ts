import { TaskTypes } from "@/types/chats";
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface initialTypes {
    loading: boolean;
    searching: boolean;
    email: string;
    chat_id: string;
    selected_chat: TaskTypes
}

const initialState: initialTypes = {
    loading: false,
    searching: false,
    email: "",
    chat_id: "",
    selected_chat: {
        id: 0,
        title: '',
        updated_at: '',
        conversation: []
    }
}

function setLoadingState(state: initialTypes, action: PayloadAction<{ toggle: boolean }>) {
    state.loading = action.payload.toggle;
}

function setSearchState(state: initialTypes, action: PayloadAction<{ toggle: boolean }>) {
    state.searching = action.payload.toggle;
}

function setEmailFunc(state: initialTypes, action: PayloadAction<{email: string}>){
    state.email = action.payload.email
}

function setSelectChatFunc(state: initialTypes, action: PayloadAction<{
    id: string;
    task: TaskTypes;
}>){
    state.chat_id = action.payload.id;
    state.selected_chat = action.payload.task;
}




export const tempSlice = createSlice({
    name: 'temp',
    initialState: initialState,
    reducers: {
        setLoading: setLoadingState,
        setSearch: setSearchState,
        setTempEmail: setEmailFunc,
        setSelectChat: setSelectChatFunc
    }
})

export const { setLoading, setSearch, setTempEmail, setSelectChat } = tempSlice.actions;
export default tempSlice.reducer;