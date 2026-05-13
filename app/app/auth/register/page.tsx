"use client"
import { Eye, EyeOff, Lock, Mail, User } from "lucide-react"
import Link from "next/link"
import { FormEvent, useEffect, useState } from "react"
import api from '@/config/axios.config'
import { RegisterAPITypes } from "@/types/apiRequest.types"
import { AxiosResponse } from "axios"
import { RegisterAPIRespTypes } from "@/types/apiResponse.types"
import { useAppDispatch } from "@/store/hook"
import { login } from "@/store/functions/auth"
import { useRouter } from "next/navigation"

export default function RegisterPage() {

    const disp = useAppDispatch()
    const router = useRouter()

    const [showPassword, setShowPassword] = useState(false)
    const [showConfirm, setShowConfirm] = useState(false)

    const [errors, setErrors] = useState<{
        name?: string
        email?: string
        password?: string
        conform_password?: string
    }>({})

    const [checkingEmail, setCheckingEmail] = useState(false)

    const [userDet, setUserDet] = useState<RegisterAPITypes>({
        email: '',
        name: '',
        password: '',
        conform_password: '',
    })

    async function register(e: FormEvent<HTMLFormElement>) {
        try {
            e.preventDefault()
            const resp: AxiosResponse<RegisterAPIRespTypes> = await api.post('/auth/register', userDet, {
                withCredentials: true
            })

            disp(login({
                data: {
                    name: resp.data.name,
                    email: resp.data.email,
                    credits_token: resp.data.credits_token,
                    is_verified: resp.data.is_verified,
                    joinedAt: resp.data.updated_at
                }
            }))

            setUserDet({
                email: '',
                name: '',
                password: '',
                conform_password: '',
            })

            router.replace('/auth/verify')

        } catch (error) {
            console.log('Error in register: ', error)
        }
    }



    useEffect(() => {
        if (!userDet.email.trim()) return

        const timer = setTimeout(async () => {
            try {
                setCheckingEmail(true)

                await api.post("/auth/is-email-avilable", {
                    email: userDet.email,
                })

                setErrors((prev) => ({
                    ...prev,
                    email: "",
                }))
            } catch (error) {
                setErrors((prev) => ({
                    ...prev,
                    email: "Email already exists",
                }))
            } finally {
                setCheckingEmail(false)
            }
        }, 600)

        return () => clearTimeout(timer)
    }, [userDet.email])

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

                <form className="space-y-4" onSubmit={register}>
                    <div className="relative">
                        <User className="absolute left-4 top-1/2 -translate-y-1/2 text-neutral-400" size={18} />
                        <input
                            type="text"
                            placeholder="Full name"
                            onChange={(e) => setUserDet({ ...userDet, name: e.target.value })}
                            className="w-full rounded-2xl border border-neutral-200 bg-neutral-50 py-3 pl-11 pr-4 text-sm outline-none transition focus:border-black focus:bg-white"
                        />
                    </div>

                    <div className="relative">
                        <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-neutral-400" size={18} />
                        <input
                            type="email"
                            value={userDet.email}
                            placeholder="Email address"
                            onChange={(e) =>
                                setUserDet({ ...userDet, email: e.target.value })
                            }
                            className={`w-full rounded-2xl border bg-neutral-50 py-3 pl-11 pr-4 text-sm outline-none transition focus:bg-white ${errors.email
                                    ? "border-red-400 focus:border-red-500"
                                    : "border-neutral-200 focus:border-black"
                                }`}
                        />

                        {checkingEmail && (
                            <p className="mt-1 text-xs text-neutral-400">Checking email...</p>
                        )}

                        {errors.email && (
                            <p className="mt-1 text-xs text-red-500">{errors.email}</p>
                        )}
                    </div>

                    <div className="relative">
                        <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-neutral-400" size={18} />
                        <input
                            type={showPassword ? "text" : "password"}
                            placeholder="Password"
                            onChange={(e) => setUserDet({ ...userDet, password: e.target.value })}
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
                            onChange={(e) => setUserDet({ ...userDet, conform_password: e.target.value })}
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