import { MouseEventHandler, PropsWithChildren } from "react";

interface IIconProps extends PropsWithChildren {
  className: string;
  onClick: MouseEventHandler;
}

export default function Icon({ className, onClick, ...rest }: IIconProps) {
  return (
    <div
      className={
        "text-lg flex justify-center items-center rounded w-8 h-8 cursor-pointer select-none " +
        className
      }
      onClick={onClick}
    >
      {rest.children}
    </div>
  );
}
