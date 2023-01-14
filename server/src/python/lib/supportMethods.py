from numpy import (add, arange, array, cos, cross, diag, hstack, ones, pi, sin,
                   vstack, zeros)
from numpy.linalg import norm

from lib.functionDefinitions import apply, unit


def arrowsPlotData(scale):
    pt1 = array([0, 0, 0])
    pt2 = scale*array([1, 0, 0])
    pt3 = scale*array([0.9, 0, 0.05])
    pt4 = array([pt3[0], pt3[1], -pt3[2]])
    xArrow = vstack((pt1, pt2, pt3, pt4, pt2))
    yArrow = apply(lambda x: array([x[1], x[0], x[2]]), xArrow)
    zArrow = apply(lambda x: array([x[2], x[1], x[0]]), xArrow)
    return vstack((xArrow, yArrow, zArrow, pt1))


def curvesPlotData(scale):
    pt1 = array([0, 0, 0])
    pt5 = scale*array([0.4, 0, 0])
    pt6 = scale*array([0.3, 0, 0.3])
    pt7 = scale*array([0, 0, 0.4])
    xzCurve = vstack((pt1, pt5, pt6, pt7))
    yzCurve = apply(lambda x: array([x[1], x[0], x[2]]), xzCurve)
    xyCurve = apply(lambda x: array([x[0], x[2], x[1]]), xzCurve)
    return vstack((xzCurve, yzCurve, xyCurve, pt1))


def rollerPlotData(location, scale=1, normal=array([0, 0, 1])):
    pt1 = array([0, 0, 0])
    pt2 = scale*array([1, 0, 0])
    xArrow = 0.5*vstack((pt1, pt2, pt1))
    yArrow = apply(lambda x: array([x[1], x[0], x[2]]), xArrow)
    zArrow = apply(lambda x: array([x[2], x[1], x[0]]), xArrow)
    v1 = cross(normal, array([1, 0, 0]))
    v2 = cross(normal, array([0, 1, 0]))
    npt = scale*normal
    pt = 0.9*scale*normal
    nptx = unit(v2 if norm(v1) == 0 else v1)
    npty = cross(normal, nptx)
    th = (2*pi)/3
    npt120 = cos(th)*nptx+sin(th)*npty
    npt240 = cos(2*th)*nptx+sin(2*th)*npty
    basic = vstack((xArrow, yArrow, zArrow, pt, pt+0.05*scale*nptx,
                   npt, pt+0.05*scale*npt120, pt, pt+0.05*scale*npt240, npt, pt))
    basic = add(basic, location)
    return basic


def fixedPlotData(location, scale=1):
    arrows = arrowsPlotData(scale)
    curves = curvesPlotData(scale)
    return add(vstack((arrows, curves)), location)


def hingePlotData(location, scale=1):
    return add(arrowsPlotData(scale), location)


def internalHingePlotData(location, scale=1):
    return add(curvesPlotData2(scale), location)


def customPlotData(location, scale=1, types='001000'):
    types = array(list(types)).astype(int)
    fd = fixedPlotData(location, scale)
    xArrow = fd[0:5] if types[0] else location
    yArrow = fd[5:10] if types[1] else location
    zArrow = fd[10:15] if types[2] else location
    yzCurve = fd[20:24] if types[3] else location
    xzCurve = fd[16:20] if types[4] else location
    xyCurve = fd[24:28] if types[5] else location
    return vstack((xArrow, yArrow, zArrow, yzCurve, xzCurve, xyCurve, location))


def supportPlotData(types, location, scale=2, normal=array([0, 0, 1])):
    if types == 'Fixed':
        return fixedPlotData(location, 1/scale)
    elif types == 'Hinge':
        return hingePlotData(location, 1/scale)
    elif types == 'Roller':
        return rollerPlotData(location, 1/scale, normal)
    elif types == 'Internal Hinge':
        return internalHingePlotData(location, 1/scale)
    else:
        return customPlotData(location, 1/scale, types)


def arrowsPlotData2(scale):
    pt1 = array([0, 0])
    pt2 = scale*array([0.5, 0])
    pt3 = scale*array([0.1, 0.1])
    pt4 = array([pt3[0], -pt3[1]])
    pt5 = scale*array([0.1, 0])
    xArrow = vstack((pt1, pt3, pt2, pt4, pt1))
    yArrow = apply(lambda x: array([x[1], 2*x[0]]), xArrow)
    return vstack((xArrow, yArrow, -xArrow))


def curvesPlotData2(scale):
    pt1 = array([-0.3, 0.3])
    pt5 = array([-0.3, -0.3])
    pt6 = array([0.3, -0.3])
    pt7 = array([0.3, 0.3])
    xyCurve = vstack((pt6, pt5, array([0, 0])))
    return scale*vstack((xyCurve, pt6))


def rollerPlotData2(location, scale=1, normal=array([0, 1])):
    normal = unit(normal)
    pt1 = array([0, 0])
    pt2 = scale*array([1, 0])
    xArrow = 0.4*vstack((pt1, pt2))
    yArrow = apply(lambda x: array([x[1], x[0]]), xArrow)
    perp = scale*array([normal[1], -normal[0]])
    pt3 = scale*normal*0.3
    pt4 = pt3 + perp*0.15
    pt5 = scale*normal
    pt6 = pt3 - perp*0.15
    basic = vstack((xArrow, yArrow, -xArrow, -yArrow, pt1, pt4, pt5, pt6, pt1))
    basic = add(basic, location)
    return basic


def fixedPlotData2(location, scale=1):
    arrows = arrowsPlotData2(scale)
    curves = curvesPlotData2(scale)
    return add(vstack((arrows, curves)), location)


def hingePlotData2(location, scale=1):
    return add(arrowsPlotData2(scale), location)


def internalHingePlotData2(location, scale=1):
    curve = vstack((curvesPlotData2(scale), -1*curvesPlotData2(scale)))
    return add(curve, location)


def customPlotData2(location, scale=1, types='010'):
    if types == '000' or types == 'Node':
        return vstack((location-5,
                       location+5,
                       location,
                       location+array([-5, 5]),
                       location+array([5, -5])))
    types = array(list(types)).astype(int)
    fd = fixedPlotData2(location, scale)
    xArrow = vstack((fd[0:5], fd[10:15])) if types[0] else location
    yArrow = fd[5:10] if types[1] else location
    xyCurve = fd[15:19] if types[2] else location
    return vstack((xArrow, yArrow, xyCurve, location))


def supportPlotData2(types, location, scale=50, normal=array([0, 0, -1])):
    if location.size == 3:
        location = location[1:3]
    if normal.size == 3:
        normal = normal[1:3]
    if types == 'Fixed':
        return fixedPlotData2(location, 50)
    elif types == 'Hinge':
        return hingePlotData2(location, 50)
    elif types == 'Roller':
        return rollerPlotData2(location, 50, normal)
    elif types == 'Internal Hinge':
        return internalHingePlotData2(location, 50)
    else:
        return customPlotData2(location, 50, types)


def rxn(types):
    if types == 'Fixed':
        rxn = ones(6).astype(int)
    elif types == 'Hinge':
        rxn = array([1, 1, 1, 0, 0, 0], dtype=int)
    elif types == 'Roller':
        rxn = array([0, 0, 1, 0, 0, 0], dtype=int)
    else:
        try:
            rxn = apply(lambda x: types[x], arange(6)).astype(int)
        except:
            rxn = zeros(6).astype(int)
    return rxn
