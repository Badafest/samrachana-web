import { FC } from "react";

export default function OneView({ View }: { View: FC }) {
  return (
    <div className="relative flex-grow outline outline-primary">
      <View />
    </div>
  );
}
