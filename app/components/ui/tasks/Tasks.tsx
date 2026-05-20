"use client"

import { AppContext } from "@/context/AppContext"
import { setSearch } from "@/store/functions/temp"
import { useAppDispatch, useAppSelector } from "@/store/hook"
import { Bot, CircleUser, FileText, MessageSquarePlus, Search, X } from "lucide-react"
import { useRouter } from "next/navigation"
import { useContext, useMemo, useState } from "react"

interface TasksMainProps {
    open: boolean
    onClose: () => void
}

export function TasksMain({ open, onClose }: TasksMainProps) {
    return (
        <section
            className={`absolute inset-0 z-50 h-full w-full bg-white transition-transform duration-300 ease-in-out ${open ? "translate-x-0" : "-translate-x-full"
                }`}
        >
            <TaskPanel onClose={onClose} showClose />
        </section>
    )
}

export function TaskSidebar() {
    return (
        <aside className="h-svh border-r border-neutral-200 bg-neutral-50">
            <TaskPanel />
        </aside>
    )
}

function TaskPanel({ onClose, showClose = false }: { onClose?: () => void; showClose?: boolean }) {
    const router = useRouter()
    const disp = useAppDispatch()
    const searchOpen = useAppSelector((state) => state.temp.searching)
    const selectedTaskId = useAppSelector((state) => state.chat.selectedTaskId)
    const tasks = useAppSelector((state) => state.chat.tasks)
    const [searchValue, setSearchValue] = useState("")

    const context = useContext(AppContext)

    if (!context) {
        throw new Error("Context not found")
    }

    const { clear_chats, load_task } = context

    const filteredTasks = useMemo(() => {
        return tasks.filter((task) =>
            task.title.toLowerCase().includes(searchValue.toLowerCase())
        )
    }, [searchValue, tasks])

    async function loadTask(id: number) {
        await load_task(id)
        router.push(`/?id=${id}`)
        onClose?.()
    }

    return (
        <div className="flex h-full flex-col">
            <div className="flex h-16 items-center justify-between border-b border-neutral-200 bg-white px-4">
                {searchOpen ? (
                    <div className="flex w-full items-center gap-2">
                        <Search size={20} className="text-neutral-400" />

                        <input
                            autoFocus
                            value={searchValue}
                            onChange={(e) => setSearchValue(e.target.value)}
                            placeholder="Search chats..."
                            className="flex-1 bg-transparent text-sm outline-none placeholder:text-neutral-400"
                        />

                        <button
                            onClick={() => {
                                disp(setSearch({ toggle: false }))
                                setSearchValue("")
                            }}
                            className="rounded-lg p-2 text-neutral-600 hover:bg-neutral-100"
                        >
                            <X size={20} />
                        </button>
                    </div>
                ) : (
                    <>
                        <div className="flex items-center gap-2 text-base font-semibold text-neutral-900">
                            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-teal-50 text-teal-700 ring-1 ring-teal-100">
                                <Bot size={18} />
                            </span>
                            PDF Agent
                        </div>

                        <div className="flex items-center gap-1">
                            <button
                                onClick={clear_chats}
                                className="rounded-lg p-2 text-neutral-600 hover:bg-neutral-100"
                                title="New chat"
                            >
                                <MessageSquarePlus size={20} />
                            </button>

                            <button
                                onClick={() => disp(setSearch({ toggle: true }))}
                                className="rounded-lg p-2 text-neutral-600 hover:bg-neutral-100"
                                title="Search chats"
                            >
                                <Search size={20} />
                            </button>

                            <button
                                className="rounded-lg p-2 text-neutral-600 hover:bg-neutral-100"
                                onClick={() => router.push("/user/profile")}
                                title="Profile"
                            >
                                <CircleUser size={20} />
                            </button>

                            {showClose && (
                                <button
                                    onClick={onClose}
                                    className="rounded-lg p-2 text-neutral-600 hover:bg-neutral-100"
                                    title="Close"
                                >
                                    <X size={20} />
                                </button>
                            )}
                        </div>
                    </>
                )}
            </div>

            <div className="flex-1 overflow-y-auto px-3 py-4">
                <p className="mb-3 px-2 text-xs font-semibold uppercase tracking-wide text-neutral-400">
                    {searchValue ? "Search Results" : "Recent"}
                </p>

                <div className="space-y-1">
                    {filteredTasks.length > 0 ? (
                        filteredTasks.map((item) => (
                            <TaskList
                                select={loadTask}
                                key={item.id}
                                id={item.id}
                                title={item.title}
                                updatedAt={item.updated_at}
                                fileCount={item.pdf_files?.length ?? 0}
                                active={selectedTaskId === item.id}
                            />
                        ))
                    ) : (
                        <div className="py-10 text-center text-sm text-neutral-400">
                            No chats found
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}

interface TaskListType {
    id: number
    title: string
    updatedAt: string
    fileCount: number
    active: boolean
    select: (id: number) => void
}

export function TaskList(props: TaskListType) {
    return (
        <button
            onClick={() => void props.select(props.id)}
            className={`w-full rounded-lg px-3 py-3 text-left text-sm transition ${props.active
                ? "bg-neutral-900 text-white"
                : "text-neutral-700 hover:bg-neutral-100"
                }`}
        >
            <span className="block truncate">{props.title || "Untitled chat"}</span>
            {(props.updatedAt || props.fileCount > 0) && (
                <span className={`mt-1 flex items-center gap-2 truncate text-xs ${props.active ? "text-neutral-300" : "text-neutral-400"}`}>
                    {props.updatedAt && <span>{new Date(props.updatedAt).toLocaleDateString()}</span>}
                    {props.fileCount > 0 && (
                        <>
                            <span className="h-1 w-1 rounded-full bg-current opacity-50" />
                            <span className="inline-flex items-center gap-1">
                                <FileText size={12} />
                                {props.fileCount}
                            </span>
                        </>
                    )}
                </span>
            )}
        </button>
    )
}
