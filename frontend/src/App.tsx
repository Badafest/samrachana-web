import Graph from "./components/Graph";
import TitleBar from "./components/TitleBar";

function App() {
  return (
    <div className="flex flex-col h-screen">
      <div className="px-4 py-2">
        <TitleBar />
      </div>
      <div className="flex-grow h-1 flex">
        <div className="w-10 border resize"></div>
        <div className="flex-grow overflow-hidden border">
          <Graph name="main_graph" width={9999} height={9999} />
        </div>
        <div className="w-10 border"></div>
      </div>
      <div className="px-2 py-1 flex justify-end"></div>
    </div>
  );
}

export default App;
