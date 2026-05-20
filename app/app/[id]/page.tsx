"use client"

import Desktop from "@/components/layout/Desktop";
import Mobile from "@/components/layout/Mobile";
import { WrapperModel } from "@/components/ui/modal/Modal";
import { AppContext } from "@/context/AppContext";
import { setLoading } from "@/store/functions/temp";
import { useAppDispatch, useAppSelector } from "@/store/hook";
import { useParams } from "next/navigation";
import { useContext, useEffect } from "react";

export default function ChatTaskPage() {
  const params = useParams<{ id: string }>()
  const context = useContext(AppContext)
  const dispatch = useAppDispatch()
  const open = useAppSelector((state) => state.temp.loading)
  const selectedTaskId = useAppSelector((state) => state.chat.selectedTaskId)

  useEffect(() => {
    const id = Number(params.id)

    if (!id || selectedTaskId === id || !context) return

    void context.load_task(id)
  }, [context, params.id, selectedTaskId])

  return (
    <>
      <WrapperModel open={open} onClose={() => dispatch(setLoading({ toggle: false }))} />
      <div className="md:hidden">
        <Mobile />
      </div>
      <div className="hidden md:block">
        <Desktop />
      </div>
    </>
  )
}
