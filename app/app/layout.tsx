"use client"
import "./globals.css";
import { Geist } from "next/font/google";
import { cn } from "@/lib/utils";
import { store } from "@/store/store";
import { Provider } from "react-redux";
import { AppProvider } from "@/context/AppContext";

const geist = Geist({ subsets: ['latin'], variable: '--font-sans' });

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode; }>) {
  return (
    <html lang="en" className={cn("font-sans", geist.variable)} >
      <body className="">
        <Provider store={store} >
          <AppProvider >
            {children}
          </AppProvider>
        </Provider>
      </body>
    </html>
  );
}
