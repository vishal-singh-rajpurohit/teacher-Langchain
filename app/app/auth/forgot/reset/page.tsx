"use client"

import api from "@/config/axios.config"
import { ArrowLeft, Eye, EyeOff, LockKeyhole } from "lucide-react"
import { useRouter } from "next/navigation"
import { useState } from "react"

export default function ResetPasswordPage() {
    const [showPassword, setShowPassword] = useState(false)
    const [showConfirm, setShowConfirm] = useState(false)
    const [password, setPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")
    const [errors, setErrors] = useState<{
        password?: string
        confirmPassword?: string
    }>({})

    const router = useRouter()

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()

        const newErrors: typeof errors = {}

        if (!password.trim()) newErrors.password = "New password is required"
        else if (password.length < 6)
            newErrors.password = "Password must be at least 6 characters"

        if (!confirmPassword.trim())
            newErrors.confirmPassword = "Confirm password is required"
        else if (password !== confirmPassword)
            newErrors.confirmPassword = "Passwords do not match"

        setErrors(newErrors)

        if (Object.keys(newErrors).length > 0) return


        await api.post('/auth/reset-password', {
            new_password: password,
            conform_password: confirmPassword
        }, {withCredentials: true})

        router.replace('/auth/login')

    }

    return (
        <section className="flex min-h-screen items-center justify-center bg-neutral-950 px-4 py-8">
            <div className="w-full max-w-md rounded-3xl bg-white p-6 shadow-2xl">
                <button className="mb-6 rounded-xl p-2 text-neutral-600 hover:bg-neutral-100">
                    <ArrowLeft size={22} />
                </button>

                <div className="mb-7 text-center">
                    <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-black text-white">
                        <LockKeyhole size={25} />
                    </div>

                    <h1 className="text-2xl font-bold text-neutral-900">
                        Reset Password
                    </h1>

                    <p className="mt-2 text-sm leading-6 text-neutral-500">
                        Create a new secure password for your account.
                    </p>
                </div>

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <div className="relative">
                            <LockKeyhole
                                className="absolute left-4 top-1/2 -translate-y-1/2 text-neutral-400"
                                size={18}
                            />

                            <input
                                type={showPassword ? "text" : "password"}
                                placeholder="New password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className={`w-full rounded-2xl border bg-neutral-50 py-3 pl-11 pr-12 text-sm outline-none transition focus:bg-white ${errors.password
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

                    <div>
                        <div className="relative">
                            <LockKeyhole
                                className="absolute left-4 top-1/2 -translate-y-1/2 text-neutral-400"
                                size={18}
                            />

                            <input
                                type={showConfirm ? "text" : "password"}
                                placeholder="Confirm password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                className={`w-full rounded-2xl border bg-neutral-50 py-3 pl-11 pr-12 text-sm outline-none transition focus:bg-white ${errors.confirmPassword
                                    ? "border-red-400 focus:border-red-500"
                                    : "border-neutral-200 focus:border-black"
                                    }`}
                            />

                            <button
                                type="button"
                                onClick={() => setShowConfirm(!showConfirm)}
                                className="absolute right-4 top-1/2 -translate-y-1/2 text-neutral-400"
                            >
                                {showConfirm ? <EyeOff size={18} /> : <Eye size={18} />}
                            </button>
                        </div>

                        {errors.confirmPassword && (
                            <p className="mt-1.5 px-1 text-xs text-red-500">
                                {errors.confirmPassword}
                            </p>
                        )}
                    </div>

                    <button
                        type="submit"
                        className="w-full rounded-2xl bg-black py-3 text-sm font-semibold text-white transition hover:bg-neutral-800"
                    >
                        Update Password
                    </button>
                </form>
            </div>
        </section>
    )
}