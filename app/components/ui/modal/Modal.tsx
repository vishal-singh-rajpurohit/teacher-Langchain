import { Spinner } from "@/components/ui/spinner";

export const WrapperModel = ({ open, onClose }: { open: boolean; onClose(): void }) => {
    return (
        <section
            className={`${open ? '' : 'hidden'} fixed inset-0 z-50 h-full w-full bg-gray-400/30`}
            onClick={onClose}
        >
            <div className="flex h-full w-full items-center justify-center" onClick={(event) => event.stopPropagation()}>
                <Spinner className="w-8 h-8" />
            </div>
        </section>
    )
}
