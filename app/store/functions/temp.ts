import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface initialTypes {
    loading: boolean;
    searching: boolean;
}

const initialState: initialTypes = {
    loading: false,
    searching: false
}

function setLoadingState(state: initialTypes, action: PayloadAction<{ toggle: boolean }>) {
    state.loading = action.payload.toggle;
}

function setSearchState(state: initialTypes, action: PayloadAction<{ toggle: boolean }>) {
    state.searching = action.payload.toggle;
}

export const tempSlice = createSlice({
    name: 'temp',
    initialState: initialState,
    reducers: {
        setLoading: setLoadingState,
        setSearch: setSearchState
    }
})

export const { setLoading, setSearch } = tempSlice.actions;
export default tempSlice.reducer;