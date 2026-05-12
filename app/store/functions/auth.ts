import { createSlice } from "@reduxjs/toolkit";

interface initialStateTypes{
    name: string;
    email: string;
    joinedAt: string;
}

const initialState: initialStateTypes = {
    email: "gamingwood18@gmail.com",
    name: "Vishal Singh",
    joinedAt: "26 May 2025",
}

export const authSlice = createSlice({
    initialState: initialState,
    name: 'auth',
    reducers: {}
})

export const {} = authSlice.actions;

export default authSlice.reducer;