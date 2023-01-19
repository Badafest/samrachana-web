import { FC } from "react";
import OneView from "./one";

export default function TwoViewsVt({
  ViewTop,
  ViewBottom,
}: {
  ViewTop: FC;
  ViewBottom: FC;
}) {
  return (
    <div className="relative flex flex-col gap-1 flex-grow">
      <OneView View={ViewTop} />
      <OneView View={ViewBottom} />
    </div>
  );
}
