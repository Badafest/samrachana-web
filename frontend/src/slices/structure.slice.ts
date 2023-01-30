import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export interface ISegmentProps {
  area: number;
  I: number;
  youngsModulus: number;
  shearModulus: number;
  alpha: number;
  density: number;
  shapeFactor: number;
  [key: string]: number | string | [number, number];
}

export interface ISegment extends ISegmentProps {
  name: string;
  class: "segment";
  type: "line" | "arc" | "quad";
  P1: [number, number];
  P2: [number, number];
  P3: [number, number];
}

export interface ILoad {
  name: string;
  class: "load" | "misfitLoad" | "temprLoad";
  degree: number;
  P1: [number, number];
  P3: [number, number];
  peak: number;
  normal: [number, number];
  psName: string;
  parentSegment: ISegment;
}

export interface ISupport {
  name: string;
  class: "support";
  type:
    | "Fixed"
    | "Roller"
    | "Hinge"
    | "Internal Hinge"
    | "Node"
    | "001"
    | "100"
    | "101"
    | "011";
  location: [number, number];
  normal: [number, number];
  settlement: [number, number, number];
}

export interface IAnalysisData {
  simplified: object;
  memLoc: [number, number][];
  actionRaw: number[][];
  action: number[][];
  responseRaw: number[][];
  response: number[][];
  reactions: number[][];
}

export interface IDiagramsData {
  segments: string[];
  axialForce: number[][][];
  shearForce: number[][][];
  force: number[][][];
  moment: number[][][];
  axialDisplacement: number[][][];
  shearDisplacement: number[][][];
  displacement: number[][][];
  slope: number[][][];
  [key: string]: number[][][] | string[];
}

export interface IStructure {
  members: { segments: ISegment[]; loads: ILoad[]; supports: ISupport[] };
  data: {
    plot: {
      [name: string]: [number, number][];
    };
    analysis: {
      nodes: [number, number][];
      options: {
        type: "frame" | "truss";
        inextensible: boolean;
        simplify: boolean;
        accuracy: number;
      };
      data: IAnalysisData;
    };
    diagrams: IDiagramsData;
  };
}

const userStructure = localStorage.getItem("structure");

export const defaultStructure: IStructure = {
  members: {
    segments: [],
    loads: [],
    supports: [],
  },
  data: {
    plot: {},
    analysis: {
      options: {
        type: "frame",
        inextensible: true,
        simplify: true,
        accuracy: 0.995,
      },
      nodes: [],
      data: {
        simplified: {},
        memLoc: [],
        actionRaw: [],
        action: [],
        response: [],
        responseRaw: [],
        reactions: [],
      },
    },
    diagrams: {
      segments: [],
      axialForce: [],
      shearForce: [],
      force: [],
      moment: [],
      axialDisplacement: [],
      shearDisplacement: [],
      displacement: [],
      slope: [],
    },
  },
};

export const initialState: IStructure = userStructure
  ? { ...defaultStructure, ...JSON.parse(userStructure) }
  : defaultStructure;

export const structureSlice = createSlice({
  name: "structure",
  initialState,
  reducers: {
    loadJson: (state, { payload }: PayloadAction<IStructure>) => {
      state.members = { ...payload.members };
      state.data = { ...payload.data };
    },
    addSegment: (state, { payload }: PayloadAction<ISegment>) => {
      const segment = state.members.segments.find(
        (x) => x.name === payload.name
      );
      if (segment) {
        throw new Error("Name is already taken");
      }
      state.members.segments = [...state.members.segments, payload];
      localStorage.setItem("structure", JSON.stringify(state));
    },
    addLoad: (state, { payload }: PayloadAction<ILoad>) => {
      const load = state.members.loads.find((x) => x.name === payload.name);
      if (load) {
        throw new Error("Name is already taken");
      }
      state.members.loads = [...state.members.loads, payload];
      localStorage.setItem("structure", JSON.stringify(state));
    },
    addSupport: (state, { payload }: PayloadAction<ISupport>) => {
      const support = state.members.supports.find(
        (x) => x.name === payload.name
      );
      if (support) {
        throw new Error("Name is already taken");
      }
      state.members.supports = [...state.members.supports, payload];
      localStorage.setItem("structure", JSON.stringify(state));
    },

    deleteSegment: (state, { payload }: PayloadAction<string>) => {
      state.members.segments = state.members.segments.filter(
        (segment) => segment.name !== payload
      );
      localStorage.setItem("structure", JSON.stringify(state));
    },
    segmentProperty: (
      state,
      { payload }: PayloadAction<{ name: string; props: ISegmentProps }>
    ) => {
      state.members.segments = state.members.segments.map((segment) =>
        segment.name === payload.name
          ? { ...segment, ...payload.props }
          : segment
      );
      localStorage.setItem("structure", JSON.stringify(state));
    },
    deleteLoad: (state, { payload }: PayloadAction<string>) => {
      state.members.loads = state.members.loads.filter(
        (load) => load.name !== payload
      );
      localStorage.setItem("structure", JSON.stringify(state));
    },
    deleteSupport: (state, { payload }: PayloadAction<string>) => {
      state.members.supports = state.members.supports.filter(
        (support) => support.name !== payload
      );
      localStorage.setItem("structure", JSON.stringify(state));
    },
    addPlotData: (
      state,
      { payload }: PayloadAction<{ name: string; data: [number, number][] }>
    ) => {
      state.data.plot = {
        ...state.data.plot,
        ...{ [payload.name]: payload.data },
      };
      localStorage.setItem("structure", JSON.stringify(state));
    },
    deletePlotData: (state, { payload }: PayloadAction<string>) => {
      if (state.data.plot[payload]) {
        delete state.data.plot[payload];
      }
      localStorage.setItem("structure", JSON.stringify(state));
    },
    analysisOptions: (
      state,
      {
        payload,
      }: PayloadAction<{
        type: "frame" | "truss";
        inextensible: boolean;
        simplify: boolean;
        accuracy: number;
      }>
    ) => {
      state.data.analysis.options = { ...payload };
      localStorage.setItem("structure", JSON.stringify(state));
    },
    analysisData: (state, { payload }: PayloadAction<IAnalysisData>) => {
      state.data.analysis.data = { ...payload };
      state.data.analysis.nodes = payload.reactions.map((rxn) =>
        state.data.analysis.options.type === "frame"
          ? rxn.slice(0, 2)
          : rxn.slice(1, 3)
      ) as [number, number][];
      localStorage.setItem("structure", JSON.stringify(state));
    },
    diagramsData: (state, { payload }: PayloadAction<IDiagramsData>) => {
      state.data.diagrams = { ...state.data.diagrams, ...payload };
      localStorage.setItem("structure", JSON.stringify(state));
    },
  },
});

export const {
  loadJson,
  addSegment,
  addLoad,
  addSupport,
  deleteLoad,
  deleteSupport,
  deleteSegment,
  segmentProperty,
  addPlotData,
  deletePlotData,
  analysisOptions,
  analysisData,
  diagramsData,
} = structureSlice.actions;
