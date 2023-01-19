import { FC } from "react";

export default function ThreeViewsVt({
  ViewTop,
  ViewBottomLeft,
  ViewBottomRight,
}: {
  ViewTop: FC;
  ViewBottomLeft: FC;
  ViewBottomRight: FC;
}) {
  return (
    <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-1">
      <div className="relative col-span-2 row-span-1 outline outline-primary">
        <ViewTop />
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
