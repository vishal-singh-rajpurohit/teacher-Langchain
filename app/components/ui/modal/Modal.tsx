import { Spinner } from "@/components/ui/spinner";

export const WrapperModel = ({ open, onClose }: { open: boolean; onClose(): void }) => {
    return (
        <section className={`${open ? '' : 'hidden'} fixed w-full h-full z-50 bg-gray-400/30`}>
            <div className="w-full h-full flex items-center justify-center">
                <Spinner className="w-8 h-8" />
            </div>
        </section>
    )
}