from lib import _app2d
from json import loads, dump
import sys
from numpy import array


def vectorize(vector):
    return array(vector, "float")


def stdOutArray(output):
    sys.stdout.writelines([str(x) for x in output])


def stdOut(output):
    sys.stdout.write(str(output))


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

    elif func == "snap-seg":
        segment = param["segment"]
        segment["P1"] = vectorize(segment["P1"])
        segment["P3"] = vectorize(segment["P3"])
        segment["P2"] = vectorize(segment["P2"])
        output = _app2d["_segments"]["_snap"](segment,
                                              vectorize(param["point"]))
        stdOut(dump(output))

    else:
        stdOut(output)

    sys.stdout.flush()


main()
