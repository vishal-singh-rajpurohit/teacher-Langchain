"use client"

import { Eye, EyeOff, Lock, Mail } from "lucide-react"
import Link from "next/link"
import { useState } from "react"

export default function LoginPage() {
    const [showPassword, setShowPassword] = useState(false)
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [errors, setErrors] = useState<{ email?: string; password?: string }>({})

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()

        const newErrors: { email?: string; password?: string } = {}

        if (!email.trim()) newErrors.email = "Email is required"
        else if (!/\S+@\S+\.\S+/.test(email)) newErrors.email = "Enter a valid email"

        if (!password.trim()) newErrors.password = "Password is required"
        else if (password.length < 6) newErrors.password = "Password must be at least 6 characters"

        setErrors(newErrors)

        if (Object.keys(newErrors).length > 0) return

        console.log({ email, password })
    }

    return (
        <section className="flex min-h-screen items-center justify-center bg-neutral-950 px-4 py-8">
            <div className="w-full max-w-md rounded-3xl border border-white/10 bg-white p-6 shadow-2xl">
                <div className="mb-7 text-center">
                    <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-black text-white">
                        <Lock size={24} />
                    </div>

                    <h1 className="text-2xl font-bold text-neutral-900">
                        Welcome Back
                    </h1>

                    <p className="mt-2 text-sm text-neutral-500">
                        Login to continue your RAG chat.
                    </p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <div className="relative">
                            <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-neutral-400" size={18} />
                            <input
                                type="email"
                                placeholder="Email address"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className={`w-full rounded-2xl border bg-neutral-50 py-3 pl-11 pr-4 text-sm outline-none transition focus:bg-white ${
                                    errors.email
                                        ? "border-red-400 focus:border-red-500"
                                        : "border-neutral-200 focus:border-black"
                                }`}
                            />
                        </div>
                        {errors.email && (
                            <p className="mt-1.5 px-1 text-xs text-red-500">
                                {errors.email}
                            </p>
                        )}
                    </div>

                    <div>
                        <div className="relative">
                            <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-neutral-400" size={18} />
                            <input
                                type={showPassword ? "text" : "password"}
                                placeholder="Password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className={`w-full rounded-2xl border bg-neutral-50 py-3 pl-11 pr-12 text-sm outline-none transition focus:bg-white ${
                                    errors.password
                                        ? "border-red-400 focus:border-red-500"
                                        : "border-neutral-200 focus:border-black"
                                }`}
                            />

                            <button
                                type="button"
                                onClick={() => setShowPassword(!showPassword)}
                                className="absolute right-4 top-1/2 -translate-y-1/2 text-neutral-400"
                            >
                                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                            </button>
                        </div>

                        {errors.password && (
                            <p className="mt-1.5 px-1 text-xs text-red-500">
                                {errors.password}
                            </p>
                        )}
                    </div>

                    <button
                        type="submit"
                        className="w-full rounded-2xl bg-black py-3 text-sm font-semibold text-white transition hover:bg-neutral-800"
                    >
                        Login
                    </button>
                </form>

                <p className="mt-6 text-center text-sm text-neutral-500">
                    Don&apos;t have an account?{" "}
                    <Link href={'/auth/register'} className="font-medium text-black">Register</Link>
                </p>
            </div>
        </section>
    )
}