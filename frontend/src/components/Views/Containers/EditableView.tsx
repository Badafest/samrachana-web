import { useState } from "react";
import AnimView from "../AnimView";
import MainView from "../MainView";
import VecView from "../VecView";
import TableView from "../TableView";
import TreeView from "../TreeView";

type TViewOption = "main" | "line" | "vec" | "tree" | "table";
export default function EditableView(
  props: { default: TViewOption } = { default: "main" }
) {
  const [selected, setSelected] = useState<TViewOption>(props.default);

  return (
    <>
      <select
        defaultValue={selected}
        onChange={(evt) => setSelected(evt.target.value as TViewOption)}
        className="absolute z-10 cursor-pointer top-1 left-4 bg-primary rounded px-2 py-1 text-xs text-secondary outline-none border focus-border-secondary"
      >
        <option value="main">Structure</option>
        <option value="tree">Members</option>
        <option value="table">Analysis Result</option>
        <option value="vec">Vector Diagrams</option>
        <option value="line">Animated Diagrams</option>
      </select>
      <ViewRenderer selected={selected} />
    </>
  );
}

function ViewRenderer({ selected }: { selected: TViewOption | undefined }) {
  if (selected === "main") {
    return <MainView />;
  } else if (selected === "line") {
    return <AnimView />;
  } else if (selected === "vec") {
    return <VecView />;
  } else if (selected === "table") {
    return <TableView />;
  } else if (selected === "tree") {
    return <TreeView />;
  } else {
    return <div>View not Found</div>;
  }
}
