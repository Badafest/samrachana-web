import { useState, useRef, useEffect } from "react";
import { ILoad, ISegment, ISupport } from "../slices/structure.slice";
import { useAppSelector } from "../store";
import { loadTypes } from "./forms/AddLoadForm";

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
  return (
    <details className="bg-primary_light rounded px-2 py-1">
      <summary>{segment.name}</summary>
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
            <span>{segment.P1[0]}</span>, <span>{segment.P1[1]}</span>
          </div>
          <div>
            <span>{segment.P3[0]}</span>, <span>{segment.P3[1]}</span>
          </div>
          <div>
            <span>{segment.P2[0]}</span>, <span>{segment.P2[1]}</span>
          </div>
          <div>{segment.area}</div>
          <div>{segment.I}</div>
          <div>{segment.youngsModulus}</div>
          <div>{segment.shearModulus}</div>
          <div>{segment.shapeFactor}</div>
          <div>{segment.alpha}</div>
          <div>{segment.density}</div>
        </div>
      </div>
    </details>
  );
}

function LoadTable({ load }: { load: ILoad }) {
  return (
    <details className="bg-primary_light rounded px-2 py-1">
      <summary>{load.name}</summary>
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
          <div>{load.peak}</div>
          <div>
            <span>{load.P1[0]}</span>, <span>{load.P1[1]}</span>
          </div>
          <div>
            <span>{load.P3[0]}</span>, <span>{load.P3[1]}</span>
          </div>
          <div>
            <span>{load.normal[0]}</span>, <span>{load.normal[1]}</span>
          </div>
        </div>
      </div>
    </details>
  );
}

function SupportTable({ support }: { support: ISupport }) {
  return (
    <details className="bg-primary_light rounded px-2 py-1">
      <summary>{support.name}</summary>
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
            <span>{support.location[0]}</span>,{" "}
            <span>{support.location[1]}</span>
          </div>
          <div>
            <span>{support.normal[0]}</span>, <span>{support.normal[1]}</span>
          </div>
          <div>
            <span>{support.settlement[0]}</span>,{" "}
            <span>{support.settlement[1]}</span>,{" "}
            <span>{support.settlement[2]}</span>
          </div>
        </div>
      </div>
    </details>
  );
}
