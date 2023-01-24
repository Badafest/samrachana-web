from lib import _app2d
from json import loads, dump
import sys
from numpy import array

import warnings

warnings.filterwarnings("ignore")


def vectorize(vector):
    return array(vector, "float")


def stdOutArray(output):
    sys.stdout.writelines([str(x) for x in output])


def stdOut(output):
    sys.stdout.write(str(output))


def convertListsToArray(dict):
    return {
        key: (vectorize(value) if type(value) == type([]) else value)
        for (key, value) in dict.items()
    }


def main():
    func = sys.argv[1]
    param = loads(sys.argv[2])
    output = "function or parameter invalid"

    if func == "plot-seg":
        output = _app2d["_segments"]["_plot"](param["type"],
                                              vectorize(param["P1"]),
                                              vectorize(param["P3"]),
                                              float(param["scale"]),
                                              vectorize(param["P2"]),
                                              int(param["no"]))
        stdOutArray(output)

    elif func == "plot-sup":
        output = _app2d["_supports"]["_plot"](param["type"],
                                              vectorize(param["location"]),
                                              float(param["scale"]),
                                              vectorize(param["normal"]))
        stdOutArray(output)

    elif func == "plot-lod":
        if int(param["degree"]) > -3:
            output = _app2d["_loads"]["_plot_normal"](vectorize(param["X"]),
                                                      vectorize(param["Y"]),
                                                      vectorize(param["A"]),
                                                      vectorize(param["B"]),
                                                      vectorize(param["C"]),
                                                      int(param["degree"]),
                                                      float(param["peak"]),
                                                      vectorize(
                                                          param["normal"]),
                                                      param["type"],
                                                      float(param["scale"]),
                                                      int(param["log_plot"]))
        else:
            output = _app2d["_loads"]["_plot_extra"](vectorize(param["A"]),
                                                     vectorize(param["B"]),
                                                     vectorize(param["C"]),
                                                     param["type"],
                                                     int(param["degree"]),
                                                     float(param["peak"]),
                                                     float(param["scale"]))
        stdOutArray(output)

    elif func == "frame":
        structure = _app2d["_format"]["_structify"](param["elements"])

        output = _app2d["_structure"]["_frame"](structure, param["shear"],
                                                param["inextensible"],
                                                param["simplify"],
                                                float(param["accuracy"]))
        stdOut(output)

    elif func == "truss":
        structure = _app2d["_format"]["_structify"](param["elements"])

        output = _app2d["_structure"]["_truss"](structure, param["shear"],
                                                param["inextensible"],
                                                param["simplify"],
                                                float(param["accuracy"]))
        stdOut(output)

    elif func == "vec-diag":
        data = convertListsToArray(param["data"])

        data["memLoc"] = data["memLoc"].astype(int)

        data["simplified"]["segments"] = array([
            convertListsToArray(segment)
            for segment in data["simplified"]["segments"]
        ])

        for segment in data["simplified"]["segments"]:
            if segment["parent"] != "None":
                segment["parent"] = convertListsToArray(segment["parent"])

        data["simplified"]["loads"] = array([
            convertListsToArray(load) for load in data["simplified"]["loads"]
        ])

        for load in data["simplified"]["loads"]:
            load["parentSegment"] = convertListsToArray(load["parentSegment"])
            if load["parentSegment"]["parent"] != "None":
                load["parentSegment"]["parent"] = convertListsToArray(
                    load["parentSegment"]["parent"])

        data["simplified"]["supports"] = array([
            convertListsToArray(support)
            for support in data["simplified"]["supports"]
        ])

        segments = _app2d["_format"]["_structify"](
            param["segments"])["segments"]

        for segment in segments:
            segment["parent"] = "None"

        structure = "_frame" if param["structure"] == "frame" else "_truss"

        output = {}

        plotTypes = {
            "_force_comp.x": "axialForce",
            "_force_comp.y": "shearForce",
            "_force_comp": "force",
            "_moment": "moment",
            "_delta_comp.x": "axialDisplacement",
            "_delta_comp.y": "shearDisplacement",
            "_delta_comp": "displacement",
            "_slope": "slope"
        }

        for plot in param["plots"]:

            splitted = plot.split(".")
            main = splitted[0]
            component = splitted[1] if len(splitted) == 2 else None

            lineDataType = "_action" if main == "_force_comp" or main == "_moment" else "_response"

            default = [
                _app2d["_simulation"][structure][lineDataType][main](segment,
                                                                     data,
                                                                     component,
                                                                     scale=1)
                for segment in segments
            ]

            _, plotData = _app2d["_simulation"]["_utils"]["_rescale"](
                segments,
                default,
                maxPlot=param["maxPlot"],
                precision=param["precision"])

            output[plotTypes[plot]] = plotData.tolist()

        stdOut(output)

    elif func == "snap-seg":
        segment = param["segment"]
        segment["P1"] = vectorize(segment["P1"])
        segment["P3"] = vectorize(segment["P3"])
        segment["P2"] = vectorize(segment["P2"])
        output = _app2d["_segments"]["_snap"](segment,
                                              vectorize(param["point"]))
        stdOut(output)

    else:
        stdOutArray(output)


main()
