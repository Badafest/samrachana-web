import { useState, useRef, useEffect } from "react";
import { useAppSelector } from "../../store";
import { getRounded } from "../Elements/Graph/functions";

export default function FrameAnalysisTable({
  current,
}: {
  current: "reactions" | "action" | "response";
}) {
  const [width, setWidth] = useState<number>(0);
  const [height, setHeight] = useState<number>(0);

  const tableRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = tableRef.current?.parentElement;
    if (container) {
      const rect = container.getBoundingClientRect();
      setWidth(rect.width);
      setHeight(rect.height);
    }
  }, []);

  return (
    <div
      ref={tableRef}
      className="absolute px-6 py-12 bg-primary_light overflow-auto"
      style={{ width, height }}
    >
      {current === "reactions" ? (
        <ReactionTable />
      ) : current === "action" ? (
        <ActionTable />
      ) : (
        <ResponseTable />
      )}
    </div>
  );
}

function ReactionTable() {
  const { reactions } = useAppSelector(
    (state) => state.structure.data.analysis.data
  );
  const { precision } = useAppSelector((state) => state.settings.data);
  return (
    <>
      {reactions.length ? (
        <div className="flex flex-col bg-primary rounded p-2 text-secondary">
          <div className="grid grid-cols-5 text-center bg-primary_light text-sm border border-secondary rounded-t">
            <span className="px-4 py-2">Node</span>
            <span className="border-l border-secondary px-4 py-2">X, Y</span>
            <span className="border-x border-secondary px-4 py-2">
              Horizontal Force
            </span>
            <span className="border-r border-secondary px-4 py-2">
              Vertical Force
            </span>
            <span className="px-4 py-2">Moment</span>
          </div>
          {reactions.map((rxn, index) => (
            <div
              key={index}
              className={`grid grid-cols-5 border-x border-secondary border-b bg-primary_light ${
                index === reactions.length - 1 ? "rounded-b" : ""
              }`}
            >
              <span className="px-4 py-2">{index}</span>
              <span className="border-l border-secondary px-4 py-1">
                {getRounded(rxn[0], precision)}, {getRounded(rxn[1], precision)}
              </span>

              <span className="border-x border-secondary px-4 py-1">
                {getRounded(rxn[2], precision)}
              </span>
              <span className="border-r border-secondary px-4 py-1">
                {getRounded(rxn[3], precision)}
              </span>
              <span className="px-4 py-2">{getRounded(rxn[4], precision)}</span>
            </div>
          ))}
        </div>
      ) : (
        <div className="flex items-center justify-center h-48">
          Data not available. Analyse the structure first.
        </div>
      )}
    </>
  );
}

function ActionTable() {
  const { action } = useAppSelector(
    (state) => state.structure.data.analysis.data
  );
  const { nodes } = useAppSelector((state) => state.structure.data.analysis);
  const { precision } = useAppSelector((state) => state.settings.data);
  return (
    <>
      {action.length ? (
        <div className="flex flex-col bg-primary rounded p-2 text-secondary">
          <div className="grid grid-cols-4 text-center bg-primary_light border text-sm border-secondary rounded-t">
            <span className="px-4 py-2">Node</span>
            <span className="border-x border-secondary px-4 py-2">
              Axial Force
            </span>
            <span className="border-r border-secondary px-4 py-2">
              Shear Force
            </span>
            <span className="px-4 py-2">Bending Moment</span>
          </div>
          {action.map((rxn, index) => (
            <div
              key={index}
              className={`grid grid-cols-4 border-x border-secondary border-b bg-primary_light ${
                index === action.length - 1 ? "rounded-b" : ""
              }`}
            >
              <span className="px-4 py-2">
                {nodes.findIndex((x) => x[0] === rxn[0] && x[1] === rxn[1])}
              </span>

              <span className="border-x border-secondary px-4 py-1">
                {getRounded(rxn[2], precision)}
              </span>
              <span className="border-r border-secondary px-4 py-1">
                {getRounded(rxn[3], precision)}
              </span>
              <span className="px-4 py-2">{getRounded(rxn[4], precision)}</span>
            </div>
          ))}
        </div>
      ) : (
        <div className="flex items-center justify-center h-48">
          Data not available. Analyse the structure first.
        </div>
      )}
    </>
  );
}

function ResponseTable() {
  const { response } = useAppSelector(
    (state) => state.structure.data.analysis.data
  );
  const { nodes } = useAppSelector((state) => state.structure.data.analysis);

  const { precision } = useAppSelector((state) => state.settings.data);
  return (
    <>
      {response.length ? (
        <div className="flex flex-col bg-primary rounded p-2 text-secondary ">
          <div className="grid grid-cols-5 text-center bg-primary_light border text-sm border-secondary rounded-t">
            <span className="px-4 py-2">Node</span>
            <span className="border-l border-secondary p-2">X, Y</span>
            <span className="border-x border-secondary p-2">
              Horizontal Displacement
            </span>
            <span className="border-r border-secondary p-2">
              Vertical Displacement
            </span>
            <span className="px-4 py-2">Slope</span>
          </div>
          {response.map((rxn, index) => (
            <div
              key={index}
              className={`grid grid-cols-5 border-x border-secondary border-b bg-primary_light ${
                index === response.length - 1 ? "rounded-b" : ""
              }`}
            >
              <span className="px-4 py-2">
                {nodes.findIndex((x) => x[0] === rxn[0] && x[1] === rxn[1])}
              </span>
              <span className="px-4 py-2 border-l border-secondary ">
                {rxn[0]}, {rxn[1]}
              </span>

              <span className="border-x border-secondary px-4 py-1">
                {getRounded(rxn[2], precision)}
              </span>
              <span className="border-r border-secondary px-4 py-1">
                {getRounded(rxn[3], precision)}
              </span>
              <span className="px-4 py-2">{getRounded(rxn[4], precision)}</span>
            </div>
          ))}
        </div>
      ) : (
        <div className="flex items-center justify-center h-48">
          Data not available. Analyse the structure first.
        </div>
      )}
    </>
  );
}
