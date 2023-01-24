from lib.structureMethods import frame2d
from lib.functionDefinitions import structify2d
from lib.simulationMethods import vectorDiagramDataForces2Dcomp, getRescaledData
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
        "class": "segment",
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
}, {
    "type": "Node",
    "location": [5, 0],
    "normal": [0, 1],
    "settlement": [0, 0, 0],
    "class": "support"
}]

# segments = [convertTo3D(seg) for seg in structure["segments"]]
# loads = [convertTo3D(lod) for lod in structure["loads"]]
# supports = [convertTo3D(sup) for sup in structure["supports"]]
# structure = structify2d(elements)

# data = frame2d(structure)

myData = {
    "simplified": {
        "segments":
        array([{
            "type": "line",
            "P1": array([0, 2, 4]),
            "P3": array([0, 6, 4]),
            "P2": array([0, 4, 4]),
            "youngsModulus": 1,
            "shearModulus": 1,
            "area": 1,
            "Iyy": 1,
            "Izz": 1,
            "J": 2,
            "shapeFactor": array([1, 1]),
            "axisVector": array([1, 0, 0]),
            "class": "segment",
            "parent": {
                "name": "segment#1",
                "class": "segment",
                "type": "line",
                "P1": array([0, 2, 4]),
                "P3": array([0, 10, 4]),
                "P2": array([0, 6, 4]),
                "area": 1,
                "youngsModulus": 1,
                "shearModulus": 1,
                "alpha": 1,
                "density": 1,
                "shapeFactor": array([1, 1]),
                "Iyy": 1,
                "Izz": 1,
                "J": 2,
                "axisVector": array([1, 0, 0]),
                "parent": "None"
            }
        }, {
            "type": "line",
            "P1": array([0, 6, 4]),
            "P3": array([0, 10, 4]),
            "P2": array([0, 8, 4]),
            "youngsModulus": 1,
            "shearModulus": 1,
            "area": 1,
            "Iyy": 1,
            "Izz": 1,
            "J": 2,
            "shapeFactor": array([1, 1]),
            "axisVector": array([1, 0, 0]),
            "class": "segment",
            "parent": {
                "name": "segment#1",
                "class": "segment",
                "type": "line",
                "P1": array([0, 2, 4]),
                "P3": array([0, 10, 4]),
                "P2": array([0, 6, 4]),
                "area": 1,
                "youngsModulus": 1,
                "shearModulus": 1,
                "alpha": 1,
                "density": 1,
                "shapeFactor": array([1, 1]),
                "Iyy": 1,
                "Izz": 1,
                "J": 2,
                "axisVector": array([1, 0, 0]),
                "parent": "None"
            }
        }]),
        "loads":
        array([{
            "degree": 0,
            "parentSegment": {
                "type": "line",
                "P1": array([0, 2, 4]),
                "P3": array([0, 6, 4]),
                "P2": array([0, 4, 4]),
                "youngsModulus": 1,
                "shearModulus": 1,
                "area": 1,
                "Iyy": 1,
                "Izz": 1,
                "J": 2,
                "shapeFactor": array([1, 1]),
                "axisVector": array([1, 0, 0]),
                "class": "segment",
                "parent": {
                    "name": "segment#1",
                    "class": "segment",
                    "type": "line",
                    "P1": array([0, 2, 4]),
                    "P3": array([0, 10, 4]),
                    "P2": array([0, 6, 4]),
                    "area": 1,
                    "youngsModulus": 1,
                    "shearModulus": 1,
                    "alpha": 1,
                    "density": 1,
                    "shapeFactor": array([1, 1]),
                    "Iyy": 1,
                    "Izz": 1,
                    "J": 2,
                    "axisVector": array([1, 0, 0]),
                    "parent": "None"
                }
            },
            "P1": array([0, 2, 4]),
            "P3": array([0, 6, 4]),
            "normal": array([0, 0, -1]),
            "peak": 1,
            "class": "load"
        }, {
            "degree": 0,
            "parentSegment": {
                "type": "line",
                "P1": array([0, 6, 4]),
                "P3": array([0, 10, 4]),
                "P2": array([0, 8, 4]),
                "youngsModulus": 1,
                "shearModulus": 1,
                "area": 1,
                "Iyy": 1,
                "Izz": 1,
                "J": 2,
                "shapeFactor": array([1, 1]),
                "axisVector": array([1, 0, 0]),
                "class": "segment",
                "parent": {
                    "name": "segment#1",
                    "class": "segment",
                    "type": "line",
                    "P1": array([0, 2, 4]),
                    "P3": array([0, 10, 4]),
                    "P2": array([0, 6, 4]),
                    "area": 1,
                    "youngsModulus": 1,
                    "shearModulus": 1,
                    "alpha": 1,
                    "density": 1,
                    "shapeFactor": array([1, 1]),
                    "Iyy": 1,
                    "Izz": 1,
                    "J": 2,
                    "axisVector": array([1, 0, 0]),
                    "parent": "None"
                }
            },
            "P1": array([0, 6, 4]),
            "P3": array([0, 10, 4]),
            "normal": array([0, 0, -1]),
            "peak": 1,
            "class": "load"
        }]),
        "supports":
        array([{
            "name": "support#2",
            "class": "support",
            "type": "Hinge",
            "location": array([0, 2, 4]),
            "normal": array([0, 0, 1]),
            "settlement": array([0, 0, 0, 0, 0, 0])
        }, {
            "name": "support#3",
            "class": "support",
            "type": "Roller",
            "location": array([0, 10, 4]),
            "normal": array([0, 0, 1]),
            "settlement": array([0, 0, 0, 0, 0, 0])
        }, {
            "name": "support#1",
            "class": "support",
            "type": "Node",
            "location": array([0, 6, 4]),
            "normal": array([0, 0, 1]),
            "settlement": array([0, 0, 0, 0, 0, 0])
        }, {
            "type": "Node",
            "location": array([0, 2, 4]),
            "settlement": array([0, 0, 0, 0, 0, 0]),
            "normal": array([0, 0, 1]),
            "class": "support"
        }, {
            "type": "Node",
            "location": array([0, 10, 4]),
            "settlement": array([0, 0, 0, 0, 0, 0]),
            "normal": array([0, 0, 1]),
            "class": "support"
        }])
    },
    "responseRaw":
    array([[0, 2, 4, 0, 0, 0, -21.3333333, 0, 0],
           [0, 6, 4, 0, 0, -53.3333333, -2.77555756e-16, 0, 0],
           [0, 10, 4, 0, 0, 0, 21.3333333, 0, 0]]),
    "response":
    array([[2, 4, 0, 0, -21.33333333], [10, 4, 0, 0, 21.33333333]]),
    "actionRaw":
    array([[0, 2, 4, 0, 4, 0, 0, 0, -5.32907052e-15],
           [0, 6, 4, 0, -1.55431223e-15, 0, 0, 0, -8],
           [0, 6, 4, 0, 0, 0, 0, 0, -8],
           [0, 10, 4, 0, -4, 0, 0, 0, 8.8817842e-16]]),
    "action":
    array([[2, 4, 0, 4, -5.32907052e-15], [10, 4, 0, -4, 8.8817842e-16]]),
    "memLoc":
    array([[0, 1], [1, 2]]),
    "reactions":
    array([[2, 4, 0, 4, -5.32907052e-15], [10, 4, 0, 4, -8.8817842e-16]]),
    "time":
    0.006011009216308594
}

segments = array([{
    "name": "segment#1",
    "class": "segment",
    "type": "line",
    "P1": array([0, 2, 4]),
    "P3": array([0, 10, 4]),
    "P2": array([0, 6, 4]),
    "area": 1,
    "youngsModulus": 1,
    "shearModulus": 1,
    "alpha": 1,
    "density": 1,
    "shapeFactor": array([1, 1]),
    "Iyy": 1,
    "Izz": 1,
    "J": 2,
    "axisVector": array([1, 0, 0]),
    "parent": "None"
}])

default = [
    vectorDiagramDataForces2Dcomp(segment, myData, "y") for segment in segments
]

scaled = getRescaledData(segments, default, maxPlot=2)
print(scaled)
