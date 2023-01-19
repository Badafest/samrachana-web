import { PropsWithChildren } from "react";

export default function ViewTopBar({ children }: PropsWithChildren) {
  return (
    <div className="absolute z-10 right-2 text-secondary text-xs px-4 py-1 flex items-center justify-end gap-2">
      {children}
    </div>
  );
}
