"use client"

import Main from "@/components/ui/chat/Main";
import { TaskSidebar } from "@/components/ui/tasks/Tasks";

export default function Desktop() {
  return (
    <section className="grid h-svh w-full grid-cols-[300px_1fr] overflow-hidden bg-white">
      <TaskSidebar />
      <Main />
    </section>
  )
}
