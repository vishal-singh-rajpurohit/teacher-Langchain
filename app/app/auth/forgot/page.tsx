"use client"

import api from "@/config/axios.config"
import { setTempEmail } from "@/store/functions/temp"
import { useAppDispatch } from "@/store/hook"
import { ArrowLeft, Mail, KeyRound } from "lucide-react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { useState } from "react"

export default function ForgotPasswordPage() {
    const [email, setEmail] = useState("")
    const [error, setError] = useState("")
    const [loading, setLoading] = useState(false)
    const router = useRouter()
    const disp = useAppDispatch()

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        setError("")

        if (!email.trim()) {
            setError("Email is required")
            return
        }

        if (!/\S+@\S+\.\S+/.test(email)) {
            setError("Enter a valid email")
            return
        }

        try {
            setLoading(true)
            await api.post("/auth/forgot-password", { email })
            disp(setTempEmail({email}))
            router.replace("/auth/forgot/verify")
        } catch {
            setError("No account available with this email")
        } finally {
            setLoading(false)
        }
    }

    return (
        <section className="flex min-h-screen items-center justify-center bg-neutral-950 px-4 py-8">
            <div className="w-full max-w-md rounded-3xl border border-white/10 bg-white p-6 shadow-2xl">
                <Link
                    href="/auth/login"
                    className="mb-6 inline-flex rounded-xl p-2 text-neutral-600 hover:bg-neutral-100"
                >
                    <ArrowLeft size={22} />
                </Link>

                <div className="mb-7 text-center">
                    <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-black text-white">
                        <KeyRound size={24} />
                    </div>

                    <h1 className="text-2xl font-bold text-neutral-900">
                        Forgot Password
                    </h1>

                    <p className="mt-2 text-sm leading-6 text-neutral-500">
                        Enter your email address and we&apos;ll send you an OTP to reset your password.
                    </p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <div className="relative">
                            <Mail
                                className="absolute left-4 top-1/2 -translate-y-1/2 text-neutral-400"
                                size={18}
                            />

                            <input
                                type="email"
                                placeholder="Email address"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className={`w-full rounded-2xl border bg-neutral-50 py-3 pl-11 pr-4 text-sm outline-none transition focus:bg-white ${
                                    error
                                        ? "border-red-400 focus:border-red-500"
                                        : "border-neutral-200 focus:border-black"
                                }`}
                            />
                        </div>

                        {error && (
                            <p className="mt-1.5 px-1 text-xs text-red-500">
                                {error}
                            </p>
                        )}
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full rounded-2xl bg-black py-3 text-sm font-semibold text-white transition hover:bg-neutral-800 disabled:cursor-not-allowed disabled:opacity-60"
                    >
                        {loading ? "Sending OTP..." : "Send Reset OTP"}
                    </button>
                </form>

                <p className="mt-6 text-center text-sm text-neutral-500">
                    Remember your password?{" "}
                    <Link href="/auth/login" className="font-medium text-black">
                        Login
                    </Link>
                </p>
            </div>
        </section>
    )
}