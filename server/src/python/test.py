from lib.structureMethods import frame2d
from lib.functionDefinitions import structify2d
from lib.simulationMethods import vectorDiagramDataForces2Dcomp, getRescaledData
from numpy import array

elements = [{
    "type": "line",
    "name": "line#1",
    "P1": [0, 0],
    "P3": [0, 5],
    "P2": [0, 2.5],
    "I": 1,
    "area": 1,
    "alpha": 1,
    "density": 1,
    "shapeFactor": 1,
    "youngsModulus": 1,
    "shearModulus": 1,
    "class": "segment",
}, {
    "type": "line",
    "name": "line#2",
    "P1": [0, 5],
    "P3": [10, 5],
    "P2": [5, 5],
    "I": 1,
    "area": 1,
    "alpha": 1,
    "density": 1,
    "shapeFactor": 1,
    "youngsModulus": 1,
    "shearModulus": 1,
    "class": "segment",
}, {
    "type": "line",
    "name": "line#3",
    "P1": [10, 5],
    "P3": [10, 0],
    "P2": [5, 2.5],
    "I": 1,
    "area": 1,
    "alpha": 1,
    "density": 1,
    "shapeFactor": 1,
    "youngsModulus": 1,
    "shearModulus": 1,
    "class": "segment",
}, {
    "degree": 0,
    "P1": [0, 5],
    "P3": [10, 5],
    "psName": "line#2",
    "parentSegment": {
        "type": "line",
        "name": "line#2",
        "P1": [0, 5],
        "P3": [10, 5],
        "P2": [5, 5],
        "I": 1,
        "area": 1,
        "alpha": 1,
        "density": 1,
        "shapeFactor": 1,
        "youngsModulus": 1,
        "shearModulus": 1,
        "class": "segment"
    },
    "peak": 1,
    "normal": [0, -1],
    "class": "load"
}, {
    "type": "Hinge",
    "location": [0, 0],
    "normal": [0, 1],
    "settlement": [0, 0, 0],
    "class": "support"
}, {
    "type": "Roller",
    "location": [10, 0],
    "normal": [0, 1],
    "settlement": [0, 0, 0],
    "class": "support"
}]

# segments = [convertTo3D(seg) for seg in structure["segments"]]
# loads = [convertTo3D(lod) for lod in structure["loads"]]
# supports = [convertTo3D(sup) for sup in structure["supports"]]
structure = structify2d(elements)

data = frame2d(structure)

segments = structure["segments"]

default = [
    vectorDiagramDataForces2Dcomp(segment, data, "y") for segment in segments
]

scaled = getRescaledData(segments, default, maxPlot=2)
