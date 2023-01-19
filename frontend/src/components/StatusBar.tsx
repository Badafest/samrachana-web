import { useAppSelector } from "../store";

export default function StatusBar() {
  const { status } = useAppSelector((state) => state.app.data);
  const { material, section, units, precision } = useAppSelector(
    (state) => state.settings.data
  );
  const { segments, loads, supports } = useAppSelector(
    (state) => state.structure.members
  );
  return (
    <div className="h-[24px] px-2 flex justify-between items-center text-contrast1 text-sm bg-primary">
      <span>{status}</span>
      <span>
        {segments.length} segments | {loads.length} loads | {supports.length}{" "}
        supports | {material} | {section} | {units} | {precision}
      </span>
    </div>
  );
}
