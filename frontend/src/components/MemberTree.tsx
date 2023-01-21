import { useState, useRef, useEffect } from "react";
import { changeAppData } from "../slices/app.slice";
import { ILoad, ISegment, ISupport } from "../slices/structure.slice";
import { useAppDispatch, useAppSelector } from "../store";
import { getRounded } from "./Elements/Graph/functions";
import Icon from "./Elements/Icon";
import { loadTypes } from "./forms/LoadForm";

export default function MemberTree() {
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

  const { segments, loads, supports } = useAppSelector(
    (state) => state.structure.members
  );

  return (
    <div
      ref={tableRef}
      className="absolute bg-primary_light pt-10 px-4 overflow-auto"
      style={{ width, height }}
    >
      <div className="flex flex-col gap-1 px-4 py-2 bg-primary rounded">
        <div className="border-b border-secondary px-2 py-1">Segments</div>
        {segments.map((segment, index) => (
          <SegmentTable key={index} segment={segment} />
        ))}
        <div className="border-b border-secondary px-2 py-1">Loads</div>
        {loads.map((load, index) => (
          <LoadTable key={index} load={load} />
        ))}
        <div className="border-b border-secondary px-2 py-1">Supports</div>
        {supports.map((support, index) => (
          <SupportTable key={index} support={support} />
        ))}
      </div>
    </div>
  );
}

function SegmentTable({ segment }: { segment: ISegment }) {
  const { precision } = useAppSelector((state) => state.settings.data);
  const dispatch = useAppDispatch();
  return (
    <details className="bg-primary_light rounded px-2 py-1">
      <summary className="flex items-center justify-between">
        {segment.name}{" "}
        <Icon
          className="border border-secondary rounded"
          onClick={() => {
            dispatch(
              changeAppData({ active_tool: "select", selected: segment.name })
            );
          }}
        >
          edit_delete_tool
        </Icon>
      </summary>
      <div className="grid grid-cols-4 px-4 py-1">
        <div className="col-span-2">
          <div>Type</div>
          <div>Initial Coordinates</div>
          <div>Final Coordinates</div>
          <div>Mid Coordinates</div>
          <div>Area</div>
          <div>Moment of Inertia</div>
          <div>Elastic Modulus</div>
          <div>Shear Modulus</div>
          <div>Shape Factor</div>
          <div>Temperature Coefficient</div>
          <div>Density</div>
        </div>
        <div className="col-span-2">
          <div>{segment.type}</div>
          <div>
            <span>{getRounded(segment.P1[0], precision)}</span>,{" "}
            <span>{getRounded(segment.P1[1], precision)}</span>
          </div>
          <div>
            <span>{getRounded(segment.P3[0], precision)}</span>,{" "}
            <span>{getRounded(segment.P3[1], precision)}</span>
          </div>
          <div>
            <span>{getRounded(segment.P2[0], precision)}</span>,{" "}
            <span>{getRounded(segment.P2[1], precision)}</span>
          </div>
          <div>{getRounded(segment.area, precision)}</div>
          <div>{getRounded(segment.I, precision)}</div>
          <div>{getRounded(segment.youngsModulus, precision)}</div>
          <div>{getRounded(segment.shearModulus, precision)}</div>
          <div>{getRounded(segment.shapeFactor, precision)}</div>
          <div>{getRounded(segment.alpha, precision)}</div>
          <div>{getRounded(segment.density, precision)}</div>
        </div>
      </div>
    </details>
  );
}

function LoadTable({ load }: { load: ILoad }) {
  const { precision } = useAppSelector((state) => state.settings.data);
  const dispatch = useAppDispatch();
  return (
    <details className="bg-primary_light rounded px-2 py-1">
      <summary className="flex justify-between items-center">
        {load.name}
        <Icon
          className="border border-secondary rounded"
          onClick={() => {
            dispatch(
              changeAppData({ active_tool: "select", selected: load.name })
            );
          }}
        >
          edit_delete_tool
        </Icon>
      </summary>
      <div className="grid grid-cols-4 px-4 py-1">
        <div className="col-span-2">
          <div>Type</div>
          <div>Parent Segment</div>
          <div>Peak Value</div>
          <div>Initial Coordinates</div>
          <div>Final Coordinates</div>
          <div>Normal</div>
        </div>
        <div className="col-span-2">
          <div>{loadTypes[load.degree + 4]}</div>
          <div>{load.psName}</div>
          <div>{getRounded(load.peak, precision)}</div>
          <div>
            <span>{getRounded(load.P1[0], precision)}</span>,{" "}
            <span>{getRounded(load.P1[1], precision)}</span>
          </div>
          <div>
            <span>{getRounded(load.P3[0], precision)}</span>,{" "}
            <span>{getRounded(load.P3[1], precision)}</span>
          </div>
          <div>
            <span>{getRounded(load.normal[0], precision)}</span>,{" "}
            <span>{getRounded(load.normal[1], precision)}</span>
          </div>
        </div>
      </div>
    </details>
  );
}

function SupportTable({ support }: { support: ISupport }) {
  const { precision } = useAppSelector((state) => state.settings.data);
  const dispatch = useAppDispatch();
  return (
    <details className="bg-primary_light rounded px-2 py-1">
      <summary className="flex items-center justify-between">
        {support.name}
        <Icon
          className="border border-secondary rounded"
          onClick={() => {
            dispatch(
              changeAppData({ active_tool: "select", selected: support.name })
            );
          }}
        >
          edit_delete_tool
        </Icon>
      </summary>
      <div className="grid grid-cols-4 px-4 py-1">
        <div className="col-span-2">
          <div>Type</div>
          <div>Location</div>
          <div>Normal</div>
          <div>Settlement</div>
        </div>
        <div className="col-span-2">
          <div>{support.type}</div>
          <div>
            <span>{getRounded(support.location[0], precision)}</span>,{" "}
            <span>{getRounded(support.location[1], precision)}</span>
          </div>
          <div>
            <span>{getRounded(support.normal[0], precision)}</span>,{" "}
            <span>{getRounded(support.normal[1], precision)}</span>
          </div>
          <div>
            <span>{getRounded(support.settlement[0], precision)}</span>,{" "}
            <span>{getRounded(support.settlement[1], precision)}</span>,{" "}
            <span>{getRounded(support.settlement[2], precision)}</span>
          </div>
        </div>
      </div>
    </details>
  );
}
