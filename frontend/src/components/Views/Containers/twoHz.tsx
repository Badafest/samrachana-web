import { FC } from "react";
import OneView from "./one";

export default function TwoViewsHz({
  ViewLeft,
  ViewRight,
}: {
  ViewLeft: FC;
  ViewRight: FC;
}) {
  return (
    <div className="relative flex-grow flex gap-1">
      <OneView View={ViewLeft} />
      <OneView View={ViewRight} />
    </div>
  );
}
