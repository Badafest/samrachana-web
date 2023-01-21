import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export interface ISegment {
  name: string;
  class: "segment";
  type: "line" | "arc" | "quad";
  P1: [number, number];
  P2: [number, number];
  P3: [number, number];
  I: number;
  area: number;
  youngsModulus: number;
  shearModulus: number;
  alpha: number;
  density: number;
  shapeFactor: number;
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

export interface IStructure {
  members: { segments: ISegment[]; loads: ILoad[]; supports: ISupport[] };
  data: {
    plot: {
      [name: string]: [number, number][];
    };
  };
}

const initialState: IStructure = {
  members: {
    segments: [],
    loads: [],
    supports: [],
  },
  data: {
    plot: {},
  },
};

export const structureSlice = createSlice({
  name: "structure",
  initialState,
  reducers: {
    addSegment: (state, { payload }: PayloadAction<ISegment>) => {
      const segment = state.members.segments.find(
        (x) => x.name === payload.name
      );
      if (segment) {
        throw new Error("Name is already taken");
      }
      state.members.segments = [...state.members.segments, payload];
    },
    addLoad: (state, { payload }: PayloadAction<ILoad>) => {
      const load = state.members.loads.find((x) => x.name === payload.name);
      if (load) {
        throw new Error("Name is already taken");
      }
      state.members.loads = [...state.members.loads, payload];
    },
    addSupport: (state, { payload }: PayloadAction<ISupport>) => {
      const support = state.members.supports.find(
        (x) => x.name === payload.name
      );
      if (support) {
        throw new Error("Name is already taken");
      }
      state.members.supports = [...state.members.supports, payload];
    },

    deleteSegment: (state, { payload }: PayloadAction<string>) => {
      state.members.segments = state.members.segments.filter(
        (segment) => segment.name !== payload
      );
    },
    deleteLoad: (state, { payload }: PayloadAction<string>) => {
      state.members.loads = state.members.loads.filter(
        (load) => load.name !== payload
      );
    },
    deleteSupport: (state, { payload }: PayloadAction<string>) => {
      state.members.supports = state.members.supports.filter(
        (support) => support.name !== payload
      );
    },
    addPlotData: (
      state,
      { payload }: PayloadAction<{ name: string; data: [number, number][] }>
    ) => {
      state.data.plot = {
        ...state.data.plot,
        ...{ [payload.name]: payload.data },
      };
    },
    deletePlotData: (state, { payload }: PayloadAction<string>) => {
      if (state.data.plot[payload]) {
        delete state.data.plot[payload];
      }
    },
  },
});

export const {
  addSegment,
  addLoad,
  addSupport,
  deleteLoad,
  deleteSupport,
  deleteSegment,
  addPlotData,
} = structureSlice.actions;
