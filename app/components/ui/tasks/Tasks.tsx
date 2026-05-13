"use client"
import { AppContext } from "@/context/AppContext"
import { setSearch } from "@/store/functions/temp"
import { useAppDispatch, useAppSelector } from "@/store/hook"
import { CircleUser, Search, X } from "lucide-react"
import { useRouter } from "next/navigation"
import { useContext, useState } from "react"

// const Tasks = [
//     { id: "1", title: "Finish project report", updatedAt: new Date().toISOString() },
//     { id: "2", title: "Buy groceries", updatedAt: new Date().toISOString() },
//     { id: "3", title: "Call client for feedback", updatedAt: new Date().toISOString() },
//     { id: "4", title: "Prepare presentation slides", updatedAt: new Date().toISOString() },
//     { id: "5", title: "Fix login bug", updatedAt: new Date().toISOString() },
//     { id: "6", title: "Read new tech article", updatedAt: new Date().toISOString() },
//     { id: "7", title: "Workout session", updatedAt: new Date().toISOString() },
//     { id: "8", title: "Plan weekend trip", updatedAt: new Date().toISOString() },
//     { id: "9", title: "Clean workspace", updatedAt: new Date().toISOString() },
//     { id: "10", title: "Update resume", updatedAt: new Date().toISOString() },
// ]

interface TasksMainProps {
    open: boolean
    onClose: () => void
}

export function TasksMain({ open, onClose }: TasksMainProps) {
    const router = useRouter()
    const disp = useAppDispatch();
    const searchOpen = useAppSelector(state => state.temp.searching);
    
    const tasks = useAppSelector(state => state.chat.tasks)

    const [searchValue, setSearchValue] = useState("")

    const filteredTasks = tasks.filter((task) =>
        task.title.toLowerCase().includes(searchValue.toLowerCase())
    )

    const context = useContext(AppContext)

    if (!context) {
        throw new Error('Context not found')
    }

    const { startNewChat } = context;

    return (
        <section
            className={`absolute inset-0 z-50 h-full w-full bg-white transition-transform duration-300 ease-in-out ${open ? "translate-x-0" : "-translate-x-full"
                }`}
        >
            <div className="flex h-full flex-col">
                <div className="flex h-16 items-center justify-between border-b px-4">
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
                                    disp(setSearch({ toggle: !searchOpen }))
                                    setSearchValue("")
                                }}
                                className="rounded-xl p-2 text-neutral-600 hover:bg-neutral-100"
                            >
                                <X size={20} />
                            </button>
                        </div>
                    ) : (
                        <>
                            <div className="text-lg font-semibold text-neutral-900">
                                Vishal&apos;s
                            </div>

                            <div className="flex items-center gap-2">
                                <button
                                    onClick={() => disp(setSearch({ toggle: !searchOpen }))}
                                    className="rounded-xl p-2 text-neutral-600 hover:bg-neutral-100"
                                >
                                    <Search size={21} />
                                </button>

                                <button className="rounded-xl p-2 text-neutral-600 hover:bg-neutral-100">
                                    <CircleUser onClick={() => router.push('/user/profile')} size={21} />
                                </button>

                                <button
                                    onClick={onClose}
                                    className="rounded-xl p-2 text-neutral-600 hover:bg-neutral-100"
                                >
                                    <X size={21} />
                                </button>
                            </div>
                        </>
                    )}
                </div>

                <div className="flex-1 overflow-y-auto px-4 py-4">
                    <p className="mb-3 text-xs font-semibold uppercase tracking-wide text-neutral-400">
                        {searchValue ? "Search Results" : "Recent"}
                    </p>

                    <div className="space-y-2">
                        {filteredTasks.length > 0 ? (
                            filteredTasks.map((item) => (
                                <TaskList
                                    key={item.id}
                                    id={item.id}
                                    title={item.title}
                                    updatedAt={item.updated_at}
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
        </section>
    )
}

interface TaskListType {
    id: number
    title: string
    updatedAt: string
}

export function TaskList(props: TaskListType) {
    const context = useContext(AppContext)

    if (!context) {
        throw new Error('Context not found')
    }

    const { startNewChat } = context;
    return (
        <button onClick={() => startNewChat(props.id)} className="w-full rounded-2xl px-4 py-3 text-left text-sm text-neutral-700 transition hover:bg-neutral-100">
            {props.title}
        </button>
    )
}