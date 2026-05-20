"use client"
import Main from "@/components/ui/chat/Main";
import { TasksMain } from "../ui/tasks/Tasks";
import { useState } from "react";

export default function Mobile() {

  const [openTasks, setOpenTasks] = useState(false)

  return (
    <section className="h-svh w-full overflow-hidden bg-white">
      <TasksMain open={openTasks} onClose={() => setOpenTasks(false)} />
      <Main onOpenTasks={() => setOpenTasks(true)} />
    </section>
  )
}
