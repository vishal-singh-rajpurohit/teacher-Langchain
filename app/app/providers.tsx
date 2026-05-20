"use client"

import { AppProvider } from "@/context/AppContext"
import { store } from "@/store/store"
import { Provider } from "react-redux"

export function Providers({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <Provider store={store}>
      <AppProvider>{children}</AppProvider>
    </Provider>
  )
}
