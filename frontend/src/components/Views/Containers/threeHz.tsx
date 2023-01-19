import { FC } from "react";

export default function ThreeViewsHz({
  ViewLeft,
  ViewRightTop,
  ViewRightBottom,
}: {
  ViewLeft: FC;
  ViewRightTop: FC;
  ViewRightBottom: FC;
}) {
  return (
    <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-1 ">
      <div className="relative col-span-1 row-span-2 outline outline-primary">
        <ViewLeft />
      </div>
      <div className="relative col-span-1 row-span-1 outline outline-primary">
        <ViewRightTop />
      </div>
      <div className="relative col-span-1 row-span-1 outline outline-primary">
        <ViewRightBottom />
      </div>
    </div>
  );
}
