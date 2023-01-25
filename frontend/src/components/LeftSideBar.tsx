import { changeAppData } from "../slices/app.slice";
import { useAppDispatch, useAppSelector } from "../store";
import Icon from "./Elements/Icon";
import themes from "../themes/themes.json";
import { useState, useRef } from "react";
import { changeSetting } from "../slices/settings.slice";
import { loadJson } from "../slices/structure.slice";

export default function LeftSideBar() {
  return (
    <div className="flex flex-col justify-between min-w-max bg-primary_dark ">
      <div className="flex flex-col gap-1 p-1">
        <SetViewIcon choose="1" icon="&#xe910;" />
        <SetViewIcon choose="2H" icon="&#xe91d;" />
        <SetViewIcon choose="2V" icon="&#xe91e;" />
        <SetViewIcon choose="3H" icon="&#xe91a;" />
        <SetViewIcon choose="3V" icon="&#xe91b;" />
        <SetViewIcon choose="4" icon="&#xe906;" />
      </div>
      <div className="flex flex-col gap-1 p-1">
        <OpenIcon />
        <JsonIcon />
        <SettingsIcon />
      </div>
    </div>
  );
}

function SetViewIcon({
  choose,
  icon,
}: {
  choose: "1" | "2H" | "2V" | "3H" | "3V" | "4";
  icon: string;
}) {
  const dispatch = useAppDispatch();
  const { layout } = useAppSelector((state) => state.app.data);
  return (
    <Icon
      className={`bg-primary_light border text-secondary ${
        layout === choose ? "border-secondary" : ""
      }`}
      onClick={() => dispatch(changeAppData({ layout: choose }))}
    >
      <span className="icon">{icon}</span>
    </Icon>
  );
}

function SettingsIcon() {
  const [show, setShow] = useState<boolean>(false);
  return (
    <>
      <Icon
        className={`bg-primary_light border text-secondary ${
          show ? "border-secondary" : ""
        }`}
        onClick={() => {
          setShow((prev) => !prev);
        }}
      >
        <span className="icon">&#xe918;</span>
      </Icon>
      {show && <SettingsForm />}
    </>
  );
}

function JsonIcon() {
  const { structure } = useAppSelector((state) => state);
  const download =
    "data:application/json;charset=utf-8," +
    encodeURIComponent(JSON.stringify(structure));
  return (
    <a href={download} download="structure.json">
      <Icon
        className="bg-primary_light border text-secondary active-border-secondary"
        onClick={() => {}}
      >
        <span className="icon">&#xe909;</span>
      </Icon>
    </a>
  );
}

function OpenIcon() {
  const fileInput = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<string>("");
  const dispatch = useAppDispatch();

  const handleFileUpload = () => {
    const files = fileInput.current?.files;
    if (files?.length) {
      const file = files[0];
      const reader = new FileReader();
      reader.readAsText(file);
      reader.onload = () => {
        if (reader.result) {
          const json = JSON.parse(reader.result.toString());
          dispatch(loadJson(json));
          localStorage.setItem("structure", reader.result.toString());
        }
        setFile("");
      };
    }
  };

  return (
    <Icon
      className={`bg-primary_light border text-secondary active-border-secondary`}
      onClick={() => {
        fileInput.current && fileInput.current.click();
      }}
    >
      <span className="icon">&#xe911;</span>
      <input
        type="file"
        accept="application/json"
        className="hidden"
        ref={fileInput}
        value={file}
        onChange={handleFileUpload}
      />
    </Icon>
  );
}

function SettingsForm() {
  return (
    <form className="absolute left-[48px] bottom-[32px] bg-primary px-4 py-2 rounded z-10 max-h-[70vh] overflow-auto">
      <ThemeOption />
      <div className="h-[1px] bg-primary_dark my-1" />
      <label htmlFor="theme" className="text-sm my-1">
        Member Plot Colors
      </label>
      {["seg_plot_color", "load_plot_color", "support_plot_color"].map(
        (plot_color: string, index) => (
          <ColorInput plot_color={plot_color} key={index} />
        )
      )}
      <div className="h-[1px] bg-primary_dark my-1" />
      <label htmlFor="theme" className="text-sm text-center my-1">
        Diagram Plot Colors
      </label>
      {[
        "afd_plot_color",
        "sfd_plot_color",
        "bmd_plot_color",
        "rfd_plot_color",
        "add_plot_color",
        "sdd_plot_color",
        "slp_plot_color",
        "rdd_plot_color",
      ].map((plot_color: string, index) => (
        <ColorInput plot_color={plot_color} key={index} />
      ))}
    </form>
  );
}

function ThemeOption() {
  const { data } = useAppSelector((state) => state.settings);
  const dispatch = useAppDispatch();

  return (
    <div className="flex gap-2 items-center my-1">
      <label htmlFor="theme" className="text-sm">
        Theme
      </label>
      <select
        name="theme"
        id="theme"
        value={data.theme}
        className="bg-primary_light rounded px-2 py-1 text-secondary cursor-pointer outline-none border focus-border-secondary"
        onChange={(e) => dispatch(changeSetting({ theme: e.target.value }))}
      >
        {Object.keys(themes).map((theme, index) => (
          <option key={index} value={theme}>
            {theme}
          </option>
        ))}
      </select>
    </div>
  );
}

function ColorInput({ plot_color }: { plot_color: string }) {
  const { data } = useAppSelector((state) => state.settings);
  const dispatch = useAppDispatch();

  const labels: { [key: string]: string } = {
    seg: "Segment",
    load: "Load",
    support: "Support",
    afd: "Axial Force",
    sfd: "Shear Force",
    bmd: "Bending Moment",
    rfd: "Resultant Force",
    add: "Axial Displacement",
    sdd: "Shear Displacement",
    slp: "Slope",
    rdd: "Resultant Displacement",
  };
  return (
    <div className="flex gap-2 items-center px-2 py-1 rounded bg-primary_light my-1">
      <input
        value={data[plot_color]}
        type="color"
        id={plot_color}
        className="w-8 h-8 outline-none cursor-pointer"
        onChange={(e) =>
          dispatch(changeSetting({ [plot_color]: e.target.value }))
        }
      />
      <label htmlFor="seg_plot_color" className="text-sm">
        {labels[plot_color.split("_")[0]]}
      </label>
    </div>
  );
}
