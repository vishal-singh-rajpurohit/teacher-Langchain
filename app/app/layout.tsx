import "./globals.css";
import { Geist } from "next/font/google";
import type { Metadata } from "next";
import { cn } from "@/lib/utils";
import { Providers } from "./providers";

const geist = Geist({ subsets: ['latin'], variable: '--font-sans', display: "swap" });

export const metadata: Metadata = {
  title: "PDF AI Agent",
  description: "Analyze, summarize, and chat with PDF documents.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode; }>) {
  return (
    <html lang="en" className={cn("font-sans", geist.variable)} >
      <body className="">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
