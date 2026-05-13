"use client"
import Mobile from "@/components/layout/Mobile";
import { WrapperModel } from "@/components/ui/modal/Modal";
import { setLoading } from "@/store/functions/temp";
import { useAppDispatch, useAppSelector } from "@/store/hook";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function Home() {

  const disp = useAppDispatch()
  const open = useAppSelector(state => state.temp.loading)

  return (
    <>
      <WrapperModel open={open} onClose={() => disp(setLoading({ toggle: false }))} />
      <Mobile />
    </>
  );
}
