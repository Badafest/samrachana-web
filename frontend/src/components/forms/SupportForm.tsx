import { useAppDispatch, useAppSelector } from "../../store";
import { useState, useEffect } from "react";

import {
  addSupport,
  deletePlotData,
  deleteSupport,
  ISegment,
  ISupport,
} from "../../slices/structure.slice";
import { changeAppData, clearToolCoords } from "../../slices/app.slice";

import { getSupportPlotData } from "../../controller/plot.controller";
import { snapToSegment } from "../../utils/snapFunctions";

const supportTypes = {
  fixed: "Fixed",
  hinge: "Hinge",
  roller: "Roller",
  internal_hinge: "Internal Hinge",
  node: "Node",
  custom: {
    Fx: "100",
    M: "001",
    FyM: "011",
    FxM: "101",
  },
};

type TSupportTypes =
  | "Fixed"
  | "Hinge"
  | "Roller"
  | "Internal Hinge"
  | "Node"
  | "100"
  | "001"
  | "011"
  | "101";

export default function SupportForm({ edit }: { edit?: ISupport }) {
  const { active_tool, tool_coords } = useAppSelector(
    (state) => state.app.data
  );

  const { supports, segments } = useAppSelector(
    (state) => state.structure.members
  );
  const { socket_id } = useAppSelector((state) => state.app.data);
  const dispatch = useAppDispatch();

  const [type, setType] = useState<TSupportTypes>(edit?.type || "Fixed");

  const [name, setName] = useState<string>(
    edit?.name || `support#${supports.length + 1}`
  );

  const [location, setLocation] = useState<[number, number]>(
    edit?.location || [0, 0]
  );
  const [normal, setNormal] = useState<[number, number]>(
    edit?.normal || [0, 1]
  );
  const [normalAngle, setNormalAngle] = useState<number>(
    Math.round((180 * Math.atan2(normal[1], normal[0])) / Math.PI)
  );
  const [settlement, setSettlement] = useState<[number, number, number]>(
    edit?.settlement || [0, 0, 0]
  );

  const [snapTo, setSnapTo] = useState<string>("");

  useEffect(() => {
    if (!edit) {
      dispatch(clearToolCoords());
      setType(
        supportTypes[
          active_tool as
            | "fixed"
            | "hinge"
            | "internal_hinge"
            | "roller"
            | "node"
        ] as TSupportTypes
      );
    }
  }, [active_tool]);

  useEffect(() => {
    if (!edit) {
      if (tool_coords.length === 1) {
        setLocation(tool_coords[0]);
      }
    }
  }, [tool_coords]);

  useEffect(() => {
    if (!edit) {
      if (tool_coords.length === 1) {
        handleAddSupport();
        dispatch(clearToolCoords());
      }
    }
  }, [location]);

  const handleAddSupport = async () => {
    const isNameTaken = supports.find((item) => item.name === name);

    const newName = `support#${supports.length + (isNameTaken ? 1 : 2)}`;
    if (!edit) {
      setName(newName);
    }

    const snapParent = segments.find((item) => item.name === snapTo);
    const snappedLocation = snapParent
      ? snapToSegment(snapParent?.P1, snapParent?.P3, location)
      : location;

    const newSupport: ISupport = {
      name: edit ? name : isNameTaken ? newName : name,
      class: "support",
      type,
      location: snappedLocation,
      normal,
      settlement,
    };

    dispatch(deleteSupport(edit?.name || ""));
    try {
      await getSupportPlotData(newSupport, socket_id);
      dispatch(addSupport(newSupport));
      dispatch(changeAppData({ status: `${name} added to structure!` }));
      if (edit?.name !== name) {
        dispatch(deletePlotData(edit?.name || ""));
      }
    } catch (error: any) {
      edit && dispatch(addSupport(edit));
      dispatch(
        changeAppData({
          status: error.message || error,
        })
      );
    }
  };

  const handleDelete = (event: any) => {
    event.preventDefault();
    dispatch(deleteSupport(edit?.name || ""));
    dispatch(deletePlotData(edit?.name || ""));
  };

  const handleFormSubmit = (event: any) => {
    event.preventDefault();
    handleAddSupport();
  };

  return (
    <div className="bg-primary_light text-contrast1 rounded p-2">
      <form onSubmit={handleFormSubmit} className="flex flex-col gap-1 text-sm">
        <label htmlFor="type">Type</label>
        <select
          name="type"
          id="type"
          className="bg-primary cursor-pointer rounded px-2 py-1  text-secondary outline-none border focus-border-secondary"
          value={type}
          onChange={(e) => setType(e.target.value as TSupportTypes)}
        >
          {["Fixed", "Hinge", "Roller", "Internal Hinge", "Node"].map(
            (type, index) => (
              <option value={type} key={index}>
                {type}
              </option>
            )
          )}
          <option value="100">Resist Fx</option>
          <option value="101">Resist Fx+M</option>
          <option value="001">Resist M</option>
          <option value="011">Resist Fy+M</option>
        </select>
        <div className="h-[1px] w-full bg-primary_dark">ss</div>
        <label htmlFor="name">Name</label>
        <input
          name="name"
          id="name"
          className="bg-primary rounded px-2 py-1  text-secondary outline-none border focus-border-secondary"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <div className="h-[1px] w-full bg-primary_dark" />
        <label>Location</label>
        <div className="flex gap-1">
          <input
            name="locationX"
            id="locationX"
            type="number"
            placeholder="X"
            className="bg-primary rounded py-1 px-2 text-secondary outline-none border focus-border-secondary"
            value={location[0]}
            onChange={(e) => {
              setLocation((prev) => [parseFloat(e.target.value), prev[1]]);
            }}
          />
          <input
            name="locationY"
            id="locationY"
            type="number"
            placeholder="Y"
            className="bg-primary rounded py-1 px-2 text-secondary outline-none border focus-border-secondary"
            value={location[1]}
            onChange={(e) => {
              setLocation((prev) => [prev[0], parseFloat(e.target.value)]);
            }}
          />
        </div>
        <label>Snap To</label>
        <select
          name="type"
          id="type"
          className="bg-primary cursor-pointer rounded px-2 py-1  text-secondary outline-none border focus-border-secondary"
          value={snapTo}
          onChange={(e) => setSnapTo(e.target.value)}
        >
          <option value="">None</option>
          {segments.map((segment, index) => (
            <option value={segment.name} key={index}>
              {segment.name}
            </option>
          ))}
        </select>

        <label>Normal</label>
        <div className="flex gap-1 flex-col">
          <input
            name="normal"
            id="normal"
            type="number"
            placeholder="theta"
            min="-90"
            max="90"
            step="5"
            className="bg-primary rounded py-1 px-2 text-secondary outline-none border focus-border-secondary"
            value={normalAngle}
            onChange={(e) => {
              const degrees = parseFloat(e.target.value);
              const radians = (Math.PI * degrees) / 180;
              setNormalAngle(degrees);
              setNormal(
                !isNaN(radians)
                  ? [Math.cos(radians), Math.sin(radians)]
                  : [0, 1]
              );
            }}
          />
          <span className="bg-primary rounded py-1 px-2 text-secondary">
            {Math.round(normal[0] * 1000) / 1000},{" "}
            {Math.round(normal[1] * 1000) / 1000}
          </span>
        </div>

        <label>Settlement</label>
        <div className="flex gap-1">
          <input
            name="settlementX"
            id="settlementX"
            type="number"
            placeholder="X"
            className="bg-primary rounded py-1 px-2 text-secondary outline-none border focus-border-secondary"
            value={settlement[0]}
            onChange={(e) => {
              setSettlement((prev) => [
                parseFloat(e.target.value),
                prev[1],
                prev[2],
              ]);
            }}
          />
          <input
            name="settlementY"
            id="settlementY"
            type="number"
            placeholder="Y"
            className="bg-primary rounded py-1 px-2 text-secondary outline-none border focus-border-secondary"
            value={settlement[1]}
            onChange={(e) => {
              setSettlement((prev) => [
                prev[0],
                parseFloat(e.target.value),
                prev[2],
              ]);
            }}
          />
          <input
            name="settlementTheta"
            id="settlementThea"
            type="number"
            placeholder="theta"
            className="bg-primary rounded py-1 px-2 text-secondary outline-none border focus-border-secondary"
            value={settlement[0]}
            onChange={(e) => {
              setSettlement((prev) => [
                prev[0],
                prev[1],
                parseFloat(e.target.value),
              ]);
            }}
          />
        </div>

        <div className="h-[1px] w-full bg-primary_dark" />
        <button className="bg-secondary text-primary_light rounded px-2 py-1 border hover-border-contrast1">
          {edit ? "Edit" : "Add"} Support
        </button>
        {edit && (
          <>
            <div className="h-[1px] w-full bg-primary_dark" />
            <button
              className="bg-secondary text-primary_light rounded px-2 py-1 border hover-border-contrast1"
              onClick={handleDelete}
            >
              Delete Support
            </button>
          </>
        )}
      </form>
    </div>
  );
}
