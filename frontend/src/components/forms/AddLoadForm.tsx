import { useAppDispatch, useAppSelector } from "../../store";
import { useState, useEffect } from "react";

import { addLoad, ILoad } from "../../slices/structure.slice";
import { changeAppData, clearToolCoords } from "../../slices/app.slice";

export const loadTypes = [
  "Misfit",
  "Temperature",
  "Moment",
  "Point",
  "Uniform",
  "Linear",
  "Quadratic",
  "Cubic",
];

import { getLoadPlotData } from "../../controller/plot.controller";
import { snapToSegment } from "../../utils/snapFunctions";

export default function AddLoadForm() {
  const { active_tool, tool_coords } = useAppSelector(
    (state) => state.app.data
  );

  const { loads } = useAppSelector((state) => state.structure.members);
  const { segments } = useAppSelector((state) => state.structure.members);

  const { socket_id } = useAppSelector((state) => state.app.data);
  const dispatch = useAppDispatch();

  const [name, setName] = useState<string>(`load#${loads.length + 1}`);
  const [type, setType] = useState<string>("");
  const [peak, setPeak] = useState<number>(1);

  const [P1, setP1] = useState<[number, number]>([0, 0]);
  const [P3, setP3] = useState<[number, number]>([0, 0]);
  const [normal, setNormal] = useState<[number, number]>([0, -1]);
  const [normalAngle, setNormalAngle] = useState<number>(-90);

  const [psName, setPsName] = useState<string>(segments.at(-1)?.name || "");

  useEffect(() => {
    dispatch(clearToolCoords());
    setType(active_tool[0].toUpperCase() + active_tool.slice(1));
  }, [active_tool]);

  useEffect(() => {
    if (tool_coords.length === 1) {
      setP1(tool_coords[0]);
    } else if (tool_coords.length === 2) {
      setP3(tool_coords[1]);
    } else {
      setP1([0, 0]);
      setP3([0, 0]);
    }
  }, [tool_coords]);

  useEffect(() => {
    if (tool_coords.length === 1 && loadTypes.indexOf(type) <= 3) {
      handleAddLoad();
      dispatch(clearToolCoords());
    }
    if (tool_coords.length === 2 && loadTypes.indexOf(type) > 3) {
      handleAddLoad();
      dispatch(clearToolCoords());
    }
  }, [P1, P3]);

  const handleAddLoad = async () => {
    const isNameTaken = loads.find((item) => item.name === name);

    const newName = `load#${loads.length + (isNameTaken ? 1 : 2)}`;
    setName(newName);

    const parentSegment = segments.find((segment) => segment.name === psName);
    if (parentSegment) {
      const degree = loadTypes.indexOf(type) - 4;
      const newLoad: ILoad = {
        name: isNameTaken ? newName : name,
        class:
          degree === -4 ? "misfitLoad" : degree === -3 ? "temprLoad" : "load",
        degree,
        peak,
        normal,
        psName,
        parentSegment,
        P1: snapToSegment(parentSegment.P1, parentSegment.P3, P1),
        P3: snapToSegment(parentSegment.P1, parentSegment.P3, P3),
      };

      console.log(newLoad);

      await getLoadPlotData(newLoad, socket_id);

      dispatch(addLoad(newLoad));
      dispatch(changeAppData({ status: `${name} added to structure!` }));
    }
  };

  const handleFormSubmit = (event: any) => {
    event.preventDefault();
    handleAddLoad();
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
          onChange={(e) => {
            setType(e.target.value);
          }}
        >
          {loadTypes.map((type, index) => (
            <option value={type} key={index}>
              {type}
            </option>
          ))}
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
        <label htmlFor="psName">Parent Segment</label>
        <select
          name="psName"
          id="psName"
          className="bg-primary cursor-pointer rounded px-2 py-1  text-secondary outline-none border focus-border-secondary"
          value={psName}
          onChange={(e) => {
            setPsName(e.target.value);
          }}
        >
          {segments.map((segment, index) => (
            <option value={segment.name} key={index}>
              {segment.name}
            </option>
          ))}
        </select>
        <div className="h-[1px] w-full bg-primary_dark">ss</div>
        <label htmlFor="peak">Peak Value</label>
        <input
          name="peak"
          id="peak"
          type="number"
          placeholder="peak"
          className="bg-primary rounded py-1 px-2 text-secondary outline-none border focus-border-secondary"
          value={peak}
          onChange={(e) => {
            setPeak((prev) => parseFloat(e.target.value));
          }}
        />
        <div className="h-[1px] w-full bg-primary_dark">ss</div>
        <label>Initial Coordinates</label>
        <div className="flex gap-1">
          <input
            name="P1x"
            id="P1x"
            type="number"
            placeholder="X"
            className="bg-primary rounded py-1 px-2 text-secondary outline-none border focus-border-secondary"
            value={P1[0]}
            onChange={(e) => {
              setP1((prev) => [parseFloat(e.target.value), prev[1]]);
            }}
          />
          <input
            name="P1y"
            id="P1y"
            type="number"
            placeholder="Y"
            className="bg-primary rounded py-1 px-2 text-secondary outline-none border focus-border-secondary"
            value={P1[1]}
            onChange={(e) => {
              setP3((prev) => [prev[0], parseFloat(e.target.value)]);
            }}
          />
        </div>

        <label>Final Coordinates</label>
        <div className="flex gap-1">
          <input
            name="P3x"
            id="P3x"
            type="number"
            placeholder="X"
            className="bg-primary rounded py-1 px-2 text-secondary outline-none border focus-border-secondary"
            value={P3[0]}
            onChange={(e) => {
              setP3((prev) => [parseFloat(e.target.value), prev[1]]);
            }}
          />
          <input
            name="P3y"
            id="P3y"
            type="number"
            placeholder="Y"
            className="bg-primary rounded py-1 px-2 text-secondary outline-none border focus-border-secondary"
            value={P3[1]}
            onChange={(e) => {
              setP3((prev) => [prev[0], parseFloat(e.target.value)]);
            }}
          />
        </div>

        <div className="h-[1px] w-full bg-primary_dark" />
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

        <div className="h-[1px] w-full bg-primary_dark" />
        <button className="bg-secondary text-primary_light rounded px-2 py-1 border hover-border-contrast1">
          Add Load
        </button>
      </form>
    </div>
  );
}
