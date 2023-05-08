import { setSessionStorage } from "@/lib/session-storage"
import { Router, useRouter } from "next/router"
import React from "react"

const Login = function () {

    const emailRef = React.useRef<any>()
    const authKeyRef = React.useRef<any>()
    const [error, setError] = React.useState("")
    const router = useRouter()

    const onFormSubmit = async function (e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault()
        try {
            setError('')
            const res = await fetch("/api/auth", {
                method: "POST",
                body: JSON.stringify({
                    email: emailRef.current.value,
                    authKey: authKeyRef.current.value
                })
            })
            const data = await res.json()
            if (!res.ok) {
                throw data.message
            }

            setSessionStorage("user", data)
            router.push("/")
        } catch (error: any) {
            // show watrinng in tthe client
            setError(error)
        }

    }

    return <>
        <section className="bg-gray-50 dark:bg-gray-900">
        <div className="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">

            <div className="px-5">
                <form onSubmit={onFormSubmit}>
                    <label htmlFor="email">Email</label>
                    <input ref={emailRef} id="email" type="email" defaultValue="Noam@test.com" required />
                    <br />
                    <label htmlFor="email">Authentication Key</label>
                    <input ref={authKeyRef} id="auth" type="string" defaultValue="GVF54" required />
                    <br />
                    <input type="submit" value="Login" />
                    {/* Errors */}
                    <p style={{ color: "red" }}>  {error}</p>
                </form>
            </div>
            </div>
        </section>
    </>
}



export default Login