import { FC } from "react";

export default function FourViews({
  ViewTopLeft,
  ViewTopRight,
  ViewBottomLeft,
  ViewBottomRight,
}: {
  ViewTopLeft: FC;
  ViewTopRight: FC;
  ViewBottomLeft: FC;
  ViewBottomRight: FC;
}) {
  return (
    <div className="flex-grow grid grid-cols-2 grid-rows-2">
      <div className="relative col-span-1 row-span-1 outline outline-primary">
        <ViewTopLeft />
      </div>
      <div className="relative col-span-1 row-span-1 outline outline-primary">
        <ViewTopRight />
      </div>
      <div className="relative col-span-1 row-span-1 outline outline-primary">
        <ViewBottomLeft />
      </div>
      <div className="relative col-span-1 row-span-1 outline outline-primary">
        <ViewBottomRight />
      </div>
    </div>
  );
}
