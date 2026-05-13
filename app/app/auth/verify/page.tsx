"use client"

import api from "@/config/axios.config"
import { ArrowLeft, ShieldCheck } from "lucide-react"
import { useRouter } from "next/navigation"
import { useRef, useState } from "react"

export default function VerifyOtpPage() {
    const [otp, setOtp] = useState<string[]>(Array(6).fill(""))
    const inputsRef = useRef<Array<HTMLInputElement | null>>([])
    const router = useRouter()

    const handleChange = (value: string, index: number) => {
        if (!/^\d?$/.test(value)) return

        const newOtp = [...otp]
        newOtp[index] = value
        setOtp(newOtp)

        if (value && index < 5) {
            inputsRef.current[index + 1]?.focus()
        }
    }

    const handleKeyDown = (
        e: React.KeyboardEvent<HTMLInputElement>,
        index: number
    ) => {
        if (e.key === "Backspace" && !otp[index] && index > 0) {
            inputsRef.current[index - 1]?.focus()
        }
    }

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()

        const code = otp.join("")

        if (code.length !== 6) {
            alert("Please enter 6 digit OTP")
            return
        }

        try {
            const resp = await api.post('/auth/verify-account', {
                otp: code
            }, {
                withCredentials: true
            })

            console.log('Submition done: ', resp)

            router.replace('/')
        } catch (error) {
            console.log('Error in Submit OTP: ', error)
        }
    }

    return (
        <section className="flex min-h-screen items-center justify-center bg-neutral-950 px-4 py-8">
            <div className="w-full max-w-md rounded-3xl bg-white p-6 shadow-2xl">
                <button className="mb-6 rounded-xl p-2 text-neutral-600 hover:bg-neutral-100">
                    <ArrowLeft size={22} />
                </button>

                <div className="mb-7 text-center">
                    <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-black text-white">
                        <ShieldCheck size={25} />
                    </div>

                    <h1 className="text-2xl font-bold text-neutral-900">
                        Verify Account
                    </h1>

                    <p className="mt-2 text-sm leading-6 text-neutral-500">
                        Enter the 6 digit OTP sent to your email address.
                    </p>
                </div>

                <form onSubmit={handleSubmit}>
                    <div className="mb-5 flex justify-center gap-2">
                        {otp.map((digit, index) => (
                            <input
                                key={index}
                                ref={(el) => {
                                    inputsRef.current[index] = el
                                }}
                                type="text"
                                inputMode="numeric"
                                maxLength={1}
                                value={digit}
                                onChange={(e) =>
                                    handleChange(e.target.value, index)
                                }
                                onKeyDown={(e) => handleKeyDown(e, index)}
                                className="h-12 w-12 rounded-2xl border border-neutral-200 bg-neutral-50 text-center text-lg font-semibold outline-none transition focus:border-black focus:bg-white"
                            />
                        ))}
                    </div>

                    <button
                        type="submit"
                        className="w-full rounded-2xl bg-black py-3 text-sm font-semibold text-white transition hover:bg-neutral-800"
                    >
                        Verify OTP
                    </button>
                </form>

                <p className="mt-5 text-center text-sm text-neutral-500">
                    Didn&apos;t receive code?{" "}
                    <button className="font-medium text-black">
                        Resend OTP
                    </button>
                </p>
            </div>
        </section>
    )
}