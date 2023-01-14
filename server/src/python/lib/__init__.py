from lib.structureMethods import frame2d, frame3d, truss2d, truss3d
from lib.segmentMethods import segPlotData, segPlotData2, actionData, responseData, trussActionData, trussResponseData
from lib.loadMethods import loadPlotData, loadPlotData2, loadPlotData3, loadPlotData4
from lib.supportMethods import supportPlotData, supportPlotData2
from lib.simulationMethods import vectorDiagramDataForces2D, vectorDiagramDataForces2Dcomp, vectorDiagramDataTrussForces2Dcomp,\
    vectorDiagramDataMoments2D, vectorDiagramDataAngles2Dcomp, vectorDiagramDataDisps2Dcomp, vectorDiagramDataTrussDisps2Dcomp, \
        simulateFrameMotion2D, simulateTrussMotion2, simulateFrameMotion3D, simulateTrussMotion, timeGraphData,\
        vectorDiagramDataForces3D, vectorDiagramDataForces3Dcomp, vectorDiagramDataTrussForces3Dcomp,vectorDiagramDataMoments3D, \
            vectorDiagramDataMoments3Dcomp, vectorDiagramDataAngles3Dcomp, vectorDiagramDataDisps3Dcomp, vectorDiagramDataTrussDisps3Dcomp,\
                fillAnimationFrames, getRescaledData, makeFunData
from lib.functionDefinitions import make, make2d, structify, structify2d

_app2d = {
    "_format": {
        "_make": make2d,
        "_structify": structify2d
    },
    "_structure": {
        "_frame": frame2d,
        "_truss": truss2d
    },
    "_segments": {
        "_plot": segPlotData2,
        "_frame_data": {
            "_action": actionData,
            "_response": responseData,
        },
        "_truss_data": {
            "_action": trussActionData,
            "_response": trussResponseData
        }
    },
    "_loads": {
        "_plot": {
            "_others": loadPlotData2,
            "_moment": loadPlotData4
        }
    },
    "_supports": {
        "_plot": supportPlotData2
    },
    "_simulation": {
        "_frame": {
            "_action": {
                "_force": vectorDiagramDataForces2D,
                "_force_comp": vectorDiagramDataForces2Dcomp,
                "_moment": vectorDiagramDataMoments2D
            },
            "_response": {
                "_slope": vectorDiagramDataAngles2Dcomp,
                "_delta_comp": vectorDiagramDataDisps2Dcomp
            },
            "_motion": simulateFrameMotion2D
        },
        "_truss": {
            "_action_comp": vectorDiagramDataTrussForces2Dcomp,
            "_response_comp": vectorDiagramDataTrussDisps2Dcomp,
            "_motion": simulateTrussMotion2
        },
        "_timegraph": timeGraphData,
        "_uitls": {
            "_make_data": makeFunData,
            "_rescale": getRescaledData,
            "_fill": fillAnimationFrames
        }
    }
}

_app3d = {
    "_format": {
        "_make": make,
        "_structify": structify
    },
    "_structure": {
        "_frame": frame3d,
        "_truss": truss3d
    },
    "_segments": {
        "_plot": segPlotData,
        "_frame_data": {
            "_action": actionData,
            "_response": responseData,
        },
        "_truss_data": {
            "_action": trussActionData,
            "_response": trussResponseData
        }
    },
    "_loads": {
        "_plot": {
            "_others": loadPlotData,
            "_moment": loadPlotData3
        }
    },
    "_supports": {
        "_plot": supportPlotData
    },
    "_simulation": {
        "_frame": {
            "_action": {
                "_force": vectorDiagramDataForces3D,
                "_force_comp": vectorDiagramDataForces3Dcomp,
                "_moment": vectorDiagramDataMoments3D,
                "_moment_comp": vectorDiagramDataMoments3Dcomp
            },
            "_response": {
                "_angle_comp": vectorDiagramDataAngles3Dcomp,
                "_delta_comp": vectorDiagramDataDisps3Dcomp
            },
            "_motion": simulateFrameMotion3D
        },
        "_truss": {
            "_action_comp": vectorDiagramDataTrussForces3Dcomp,
            "_response_comp": vectorDiagramDataTrussDisps3Dcomp,
            "_motion": simulateTrussMotion
        },
        "_timegraph": timeGraphData,
        "_uitls": {
            "_make_data": makeFunData,
            "_rescale": getRescaledData,
            "_fill": fillAnimationFrames
        }
    }
}
