import { useState } from "react";
import { useAppSelector } from "../../store";
import drawPath from "../../utils/drawing";
import Graph from "../Elements/Graph";

export default function SimGraph() {
  const {
    sim_grid_color,
    sim_grid_dots,
    sim_grid_opacity,
    seg_plot_color,
    seg_plot_width,
    afd_plot_color,
    sfd_plot_color,
    rfd_plot_color,
    bmd_plot_color,
    add_plot_color,
    sdd_plot_color,
    rdd_plot_color,
    slp_plot_color,
  } = useAppSelector((state) => state.settings.data);

  const { segments } = useAppSelector((state) => state.structure.members);

  const { plot, diagrams } = useAppSelector((state) => state.structure.data);

  interface IShowOptions {
    axialForce: boolean;
    shearForce: boolean;
    force: boolean;
    moment: boolean;
    axialDisplacement: boolean;
    shearDisplacement: boolean;
    displacement: boolean;
    slope: boolean;
  }

  const [show, setShow] = useState<IShowOptions>({
    axialForce: false,
    shearForce: false,
    force: false,
    moment: true,
    axialDisplacement: false,
    shearDisplacement: false,
    displacement: false,
    slope: false,
  });

  const updateFunction = (
    context: CanvasRenderingContext2D | null,
    zoom: number,
    origin: [number, number]
  ) => {
    if (context) {
      context.clearRect(0, 0, context?.canvas.width, context?.canvas.height);
      segments.forEach((segment) => {
        const data = plot[segment.name];
        data &&
          drawPath(
            context,
            data,
            origin,
            zoom,
            seg_plot_color,
            seg_plot_width / 2
          );
      });
      show.axialForce &&
        diagrams.axialForce &&
        diagrams.axialForce.forEach((diagram) => {
          const data = diagram.map((x) => x.slice(1, 3)) as [number, number][];
          drawPath(context, data, origin, zoom, afd_plot_color, seg_plot_width);
        });
      show.shearForce &&
        diagrams.shearForce &&
        diagrams.shearForce.forEach((diagram) => {
          const data = diagram.map((x) => x.slice(1, 3)) as [number, number][];
          drawPath(context, data, origin, zoom, sfd_plot_color, seg_plot_width);
        });
      show.force &&
        diagrams.force &&
        diagrams.force.forEach((diagram) => {
          const data = diagram.map((x) => x.slice(1, 3)) as [number, number][];
          drawPath(context, data, origin, zoom, rfd_plot_color, seg_plot_width);
        });
      show.moment &&
        diagrams.moment &&
        diagrams.moment.forEach((diagram) => {
          const data = diagram.map((x) => x.slice(1, 3)) as [number, number][];
          drawPath(context, data, origin, zoom, bmd_plot_color, seg_plot_width);
        });
      show.axialDisplacement &&
        diagrams.axialDisplacement &&
        diagrams.axialDisplacement.forEach((diagram) => {
          const data = diagram.map((x) => x.slice(1, 3)) as [number, number][];
          drawPath(context, data, origin, zoom, add_plot_color, seg_plot_width);
        });
      show.shearDisplacement &&
        diagrams.shearDisplacement &&
        diagrams.shearDisplacement.forEach((diagram) => {
          const data = diagram.map((x) => x.slice(1, 3)) as [number, number][];
          drawPath(context, data, origin, zoom, sdd_plot_color, seg_plot_width);
        });
      show.displacement &&
        diagrams.displacement &&
        diagrams.displacement.forEach((diagram) => {
          const data = diagram.map((x) => x.slice(1, 3)) as [number, number][];
          drawPath(
            context,
            data.slice(1, -1),
            origin,
            zoom,
            rdd_plot_color,
            seg_plot_width
          );
        });
      show.slope &&
        diagrams.slope &&
        diagrams.slope.forEach((diagram) => {
          const data = diagram.map((x) => x.slice(1, 3)) as [number, number][];
          drawPath(context, data, origin, zoom, slp_plot_color, seg_plot_width);
        });
    }
  };

  return (
    <>
      <Graph
        color={sim_grid_color}
        dots={sim_grid_dots}
        opacity={sim_grid_opacity}
        updateFunction={updateFunction}
        updateDependency={[Object.values(show)]}
      />
      <div className="absolute left-2 bottom-2 bg-primary rounded p-2 flex gap-2 text-xs">
        <div className="flex flex-col gap-2">
          <div className="bg-primary_light rounded px-4 py-2 flex gap-2">
            <input
              type="checkbox"
              id="axialForce"
              name="axialForce"
              className="cursor-pointer"
              checked={show.axialForce}
              onChange={(e) =>
                setShow((prev) => ({ ...prev, axialForce: e.target.checked }))
              }
            />
            <label className="cursor-pointer" htmlFor="axialForce">
              Axial Force
            </label>
          </div>
          <div className="bg-primary_light rounded px-4 py-2 flex gap-2">
            <input
              type="checkbox"
              id="shearForce"
              name="shearForce"
              className="cursor-pointer"
              checked={show.shearForce}
              onChange={(e) =>
                setShow((prev) => ({ ...prev, shearForce: e.target.checked }))
              }
            />
            <label className="cursor-pointer" htmlFor="shearForce">
              Shear Force
            </label>
          </div>
          <div className="bg-primary_light rounded px-4 py-2 flex gap-2">
            <input
              type="checkbox"
              id="moment"
              name="moment"
              className="cursor-pointer"
              checked={show.moment}
              onChange={(e) =>
                setShow((prev) => ({ ...prev, moment: e.target.checked }))
              }
            />
            <label className="cursor-pointer" htmlFor="moment">
              Bending Moment
            </label>
          </div>
          <div className="bg-primary_light rounded px-4 py-2 flex gap-2">
            <input
              type="checkbox"
              id="force"
              name="force"
              className="cursor-pointer"
              checked={show.force}
              onChange={(e) =>
                setShow((prev) => ({ ...prev, force: e.target.checked }))
              }
            />
            <label className="cursor-pointer" htmlFor="force">
              Resultant Force
            </label>
          </div>
        </div>
        <div className="flex flex-col gap-2">
          <div className="bg-primary_light rounded px-4 py-2 flex gap-2">
            <input
              type="checkbox"
              id="axialDisplacement"
              name="axialDisplacement"
              className="cursor-pointer"
              checked={show.axialDisplacement}
              onChange={(e) =>
                setShow((prev) => ({
                  ...prev,
                  axialDisplacement: e.target.checked,
                }))
              }
            />
            <label className="cursor-pointer" htmlFor="axialDisplacement">
              Axial Displacement
            </label>
          </div>
          <div className="bg-primary_light rounded px-4 py-2 flex gap-2">
            <input
              type="checkbox"
              id="shearDisplacement"
              name="shearDisplacement"
              className="cursor-pointer"
              checked={show.shearDisplacement}
              onChange={(e) =>
                setShow((prev) => ({
                  ...prev,
                  shearDisplacement: e.target.checked,
                }))
              }
            />
            <label className="cursor-pointer" htmlFor="shearDisplacement">
              Shear Displacement
            </label>
          </div>
          <div className="bg-primary_light rounded px-4 py-2 flex gap-2">
            <input
              type="checkbox"
              id="slope"
              name="slope"
              className="cursor-pointer"
              checked={show.slope}
              onChange={(e) =>
                setShow((prev) => ({ ...prev, slope: e.target.checked }))
              }
            />
            <label className="cursor-pointer" htmlFor="slope">
              Slope
            </label>
          </div>
          <div className="bg-primary_light rounded px-4 py-2 flex gap-2">
            <input
              type="checkbox"
              id="displacement"
              name="displacement"
              className="cursor-pointer"
              checked={show.displacement}
              onChange={(e) =>
                setShow((prev) => ({ ...prev, displacement: e.target.checked }))
              }
            />
            <label className="cursor-pointer" htmlFor="displacement">
              Resultant Displacement
            </label>
          </div>
        </div>
      </div>
    </>
  );
}
