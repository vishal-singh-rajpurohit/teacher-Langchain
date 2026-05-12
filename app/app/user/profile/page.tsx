"use client"

import { useAppSelector } from "@/store/hook"
import { ArrowLeft, LogOut, Mail, User } from "lucide-react"
import { useRouter } from "next/navigation"



export default function ProfilePage() {

    const router = useRouter()

    function onBack(){
        router.back()
    }

    function onLogout(){}

    const {email, joinedAt, name} = useAppSelector(state=>state.auth)

    return (
        <section className="flex h-screen w-full flex-col bg-white">
            
            {/* Header */}
            <div className="flex h-14 items-center justify-between border-b px-4">
                <button
                    onClick={onBack}
                    className="rounded-xl p-2 text-neutral-600 hover:bg-neutral-100"
                >
                    <ArrowLeft size={22} />
                </button>

                <h2 className="text-sm font-medium text-neutral-700">
                    Profile
                </h2>

                <div className="w-10" /> {/* spacing balance */}
            </div>

            {/* Content */}
            <div className="flex flex-1 flex-col items-center px-4 py-8">

                {/* Avatar */}
                <div className="flex h-20 w-20 items-center justify-center rounded-2xl bg-neutral-100">
                    <User size={32} className="text-neutral-600" />
                </div>

                {/* Name */}
                <h1 className="mt-4 text-lg font-semibold text-neutral-900">
                    {name}
                </h1>

                {/* Info Cards */}
                <div className="mt-6 w-full max-w-md space-y-3">

                    <InfoCard icon={<Mail size={18} />} label="Email" value={email} />

                    <InfoCard
                        icon={<User size={18} />}
                        label="Joined"
                        value={joinedAt}
                    />
                </div>

                {/* Logout */}
                <button
                    onClick={onLogout}
                    className="mt-8 flex w-full max-w-md items-center justify-center gap-2 rounded-2xl bg-black py-3 text-sm font-semibold text-white transition hover:bg-neutral-800"
                >
                    <LogOut size={18} />
                    Logout
                </button>
            </div>
        </section>
    )
}

interface InfoCardProps {
    icon: React.ReactNode
    label: string
    value: string
}

const InfoCard = ({ icon, label, value }: InfoCardProps) => {
    return (
        <div className="flex items-center gap-3 rounded-2xl border bg-neutral-50 px-4 py-3">
            <div className="text-neutral-600">{icon}</div>

            <div>
                <p className="text-xs text-neutral-400">{label}</p>
                <p className="text-sm font-medium text-neutral-800">{value}</p>
            </div>
        </div>
    )
}