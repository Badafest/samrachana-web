import { CSSProperties, useEffect, useState } from "react";
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

import useMessageHandler from "./hooks/useMessageHandler";
import useKeypressHandler from "./hooks/useKeypressHandler";

function App() {
  const theme = useTheme();
  const [socket, setSocket] = useState<WebSocket>();

  const keypressHandler = useKeypressHandler();

  useEffect(() => {
    if (!socket) {
      const ws = new WebSocket(import.meta.env.VITE_WS_URL);
      setSocket(ws);
    }
    addEventListener("keypress", keypressHandler);
  }, []);

  const socketMessageHandler = useMessageHandler();

  useEffect(() => {
    socket?.addEventListener("message", socketMessageHandler);
    return () => {
      socket?.removeEventListener("message", socketMessageHandler);
    };
  }, [socket]);

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
