import { useState } from "react";
import LineView from "../LineView";
import MainView from "../MainView";
import SimView from "../SimView";
import TableView from "../TableView";
import TreeView from "../TreeView";

type TViewOption = "main" | "line" | "sim" | "tree" | "table";
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
        <option value="line">Actions and Responses</option>
        <option value="sim">Vector Diagrams</option>
      </select>
      <ViewRenderer selected={selected} />
    </>
  );
}

function ViewRenderer({ selected }: { selected: TViewOption | undefined }) {
  if (selected === "main") {
    return <MainView />;
  } else if (selected === "line") {
    return <LineView />;
  } else if (selected === "sim") {
    return <SimView />;
  } else if (selected === "table") {
    return <TableView />;
  } else if (selected === "tree") {
    return <TreeView />;
  } else {
    return <div>View not Found</div>;
  }
}
