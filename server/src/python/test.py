from lib.structureMethods import frame2d
from lib.functionDefinitions import structify2d
from numpy import array

elements = [{
    "type": "line",
    "name": "line#1",
    "P1": [0, 0],
    "P3": [10, 0],
    "P2": [5, 0],
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
    "P1": [0, 0],
    "P3": [10, 0],
    "psName": "line#1",
    "parentSegment": {
        "type": "line",
        "name": "line#1",
        "P1": [0, 0],
        "P3": [10, 0],
        "P2": [5, 0],
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
    "type": "Fixed",
    "location": [0, 0],
    "normal": [0, 1],
    "settlement": [0, 0, 0],
    "class": "support"
}]

# segments = [convertTo3D(seg) for seg in structure["segments"]]
# loads = [convertTo3D(lod) for lod in structure["loads"]]
# supports = [convertTo3D(sup) for sup in structure["supports"]]
structure = structify2d(elements)

frame2d(structure)