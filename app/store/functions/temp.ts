import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface initialTypes {
    loading: boolean;
    searching: boolean;
    email: string;
    contextModalOpen: boolean;
    composerContext: string;
    webSearchEnabled: boolean;
}

const initialState: initialTypes = {
    loading: false,
    searching: false,
    email: "",
    contextModalOpen: false,
    composerContext: "",
    webSearchEnabled: false,
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

function setContextModalFunc(state: initialTypes, action: PayloadAction<{ toggle: boolean }>) {
    state.contextModalOpen = action.payload.toggle
}

function setComposerContextFunc(state: initialTypes, action: PayloadAction<{ context: string }>) {
    state.composerContext = action.payload.context
}

function clearComposerContextFunc(state: initialTypes) {
    state.composerContext = ""
}

function setWebSearchFunc(state: initialTypes, action: PayloadAction<{ enabled: boolean }>) {
    state.webSearchEnabled = action.payload.enabled
}




export const tempSlice = createSlice({
    name: 'temp',
    initialState: initialState,
    reducers: {
        setLoading: setLoadingState,
        setSearch: setSearchState,
        setTempEmail: setEmailFunc,
        setContextModal: setContextModalFunc,
        setComposerContext: setComposerContextFunc,
        clearComposerContext: clearComposerContextFunc,
        setWebSearch: setWebSearchFunc,
    }
})

export const {
    clearComposerContext,
    setComposerContext,
    setContextModal,
    setLoading,
    setSearch,
    setTempEmail,
    setWebSearch,
} = tempSlice.actions;
export default tempSlice.reducer;
