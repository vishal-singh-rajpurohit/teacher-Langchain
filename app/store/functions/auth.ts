import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface initialStateTypes{
    name: string;
    email: string;
    is_verified: boolean;
    credits_token: number;
    joinedAt: string;
}

const initialState: initialStateTypes = {
    email: "",
    name: "",
    credits_token: 0,
    is_verified: false,
    joinedAt: ""
}

function loginFunc(state: initialStateTypes, action: PayloadAction<{data: initialStateTypes}>){
    state.name = action.payload.data.name;
    state.email = action.payload.data.email;
    state.credits_token = action.payload.data.credits_token;
    state.is_verified = action.payload.data.is_verified;
    state.joinedAt = action.payload.data.joinedAt;
}

export const authSlice = createSlice({
    initialState: initialState,
    name: 'auth',
    reducers: {
        login: loginFunc
    }
})

export const { login, } = authSlice.actions;

export default authSlice.reducer;