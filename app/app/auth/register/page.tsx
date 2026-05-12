"use client"

import { Eye, EyeOff, Lock, Mail, User } from "lucide-react"
import Link from "next/link"
import { useState } from "react"

export default function RegisterPage() {
    const [showPassword, setShowPassword] = useState(false)
    const [showConfirm, setShowConfirm] = useState(false)

    return (
        <section className="flex min-h-screen items-center justify-center bg-neutral-950 px-4 py-8">
            <div className="w-full max-w-md rounded-3xl border border-white/10 bg-white p-6 shadow-2xl">
                <div className="mb-7 text-center">
                    <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-black text-white">
                        <Lock size={24} />
                    </div>

                    <h1 className="text-2xl font-bold text-neutral-900">
                        Create Account
                    </h1>

                    <p className="mt-2 text-sm text-neutral-500">
                        Register to start using your RAG chat app.
                    </p>
                </div>

                <form className="space-y-4">
                    <div className="relative">
                        <User className="absolute left-4 top-1/2 -translate-y-1/2 text-neutral-400" size={18} />
                        <input
                            type="text"
                            placeholder="Full name"
                            className="w-full rounded-2xl border border-neutral-200 bg-neutral-50 py-3 pl-11 pr-4 text-sm outline-none transition focus:border-black focus:bg-white"
                        />
                    </div>

                    <div className="relative">
                        <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-neutral-400" size={18} />
                        <input
                            type="email"
                            placeholder="Email address"
                            className="w-full rounded-2xl border border-neutral-200 bg-neutral-50 py-3 pl-11 pr-4 text-sm outline-none transition focus:border-black focus:bg-white"
                        />
                    </div>

                    <div className="relative">
                        <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-neutral-400" size={18} />
                        <input
                            type={showPassword ? "text" : "password"}
                            placeholder="Password"
                            className="w-full rounded-2xl border border-neutral-200 bg-neutral-50 py-3 pl-11 pr-12 text-sm outline-none transition focus:border-black focus:bg-white"
                        />
                        <button
                            type="button"
                            onClick={() => setShowPassword(!showPassword)}
                            className="absolute right-4 top-1/2 -translate-y-1/2 text-neutral-400"
                        >
                            {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                        </button>
                    </div>

                    <div className="relative">
                        <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-neutral-400" size={18} />
                        <input
                            type={showConfirm ? "text" : "password"}
                            placeholder="Confirm password"
                            className="w-full rounded-2xl border border-neutral-200 bg-neutral-50 py-3 pl-11 pr-12 text-sm outline-none transition focus:border-black focus:bg-white"
                        />
                        <button
                            type="button"
                            onClick={() => setShowConfirm(!showConfirm)}
                            className="absolute right-4 top-1/2 -translate-y-1/2 text-neutral-400"
                        >
                            {showConfirm ? <EyeOff size={18} /> : <Eye size={18} />}
                        </button>
                    </div>

                    <button
                        type="submit"
                        className="w-full rounded-2xl bg-black py-3 text-sm font-semibold text-white transition hover:bg-neutral-800"
                    >
                        Create Account
                    </button>
                </form>

                <p className="mt-6 text-center text-sm text-neutral-500">
                    Already have an account?{" "}
                    <Link href={'/auth/login'} className="font-medium text-black">Login</Link>
                </p>
            </div>
        </section>
    )
}