import { CSSProperties } from "react";
import { useTheme } from "./themes/useTheme";

import "./themes/theme.css";
import { useAppSelector } from "./store";

import TitleBar from "./components/TitleBar";

import EditableView from "./components/Views/Containers/EditableView";

import OneView from "./components/Views/Containers/one";
import TwoViewsHz from "./components/Views/Containers/twoHz";
import TwoViewsVt from "./components/Views/Containers/twoVt";
import ThreeViewsHz from "./components/Views/Containers/threeHz";
import FourViews from "./components/Views/Containers/four";
import ThreeViewsVt from "./components/Views/Containers/threeVt";

import LeftSideBar from "./components/LeftSideBar";
import RightSideBar from "./components/RightSideBar";

import StatusBar from "./components/StatusBar";

function App() {
  const theme = useTheme();

  return (
    <div
      className="flex flex-col h-screen bg-none items-stretch"
      style={theme as CSSProperties}
    >
      <TitleBar />
      <div className="flex flex-grow">
        <LeftSideBar />
        <MultiViews />
        <RightSideBar />
      </div>
      <StatusBar />
    </div>
  );
}

function DefaultMainView() {
  return <EditableView default="main" />;
}

function DefaultTreeView() {
  return <EditableView default="tree" />;
}

function DefaultTableView() {
  return <EditableView default="table" />;
}

function DefaultLineView() {
  return <EditableView default="line" />;
}

function DefaultSimView() {
  return <EditableView default="sim" />;
}

function MultiViews() {
  const { layout } = useAppSelector((state) => state.app.data);
  switch (layout) {
    case "1":
      return <OneView View={DefaultMainView} />;
    case "2H":
      return (
        <TwoViewsHz ViewLeft={DefaultMainView} ViewRight={DefaultTreeView} />
      );
    case "2V":
      return (
        <TwoViewsVt ViewTop={DefaultMainView} ViewBottom={DefaultTableView} />
      );
    case "3H":
      return (
        <ThreeViewsHz
          ViewLeft={DefaultMainView}
          ViewRightTop={DefaultTableView}
          ViewRightBottom={DefaultLineView}
        />
      );
    case "3V":
      return (
        <ThreeViewsVt
          ViewTop={DefaultMainView}
          ViewBottomLeft={DefaultTableView}
          ViewBottomRight={DefaultLineView}
        />
      );
    case "4":
      return (
        <FourViews
          ViewTopLeft={DefaultMainView}
          ViewTopRight={DefaultTreeView}
          ViewBottomLeft={DefaultTableView}
          ViewBottomRight={DefaultLineView}
        />
      );
    default:
      return <OneView View={DefaultMainView} />;
  }
}

export default App;
