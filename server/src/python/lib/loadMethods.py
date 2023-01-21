from lib.numbaFunctions import linePointGlobalFEA, lineMomentGlobalFEA, linePolyGlobalFEA
from lib.numbaFunctions import linePointAngleX, linePointDisplaceX, lineMomentAngleX, lineMomentDisplaceX, linePolyAngleX, linePolyAngleXNeg, linePolyDisplaceX, linePolyDisplaceXNeg
from lib.numbaFunctions import lineMomentForceX, lineMomentMomentX, linePointForceX, linePointMomentX, linePolyForceX, linePolyForceXNeg, linePolyMomentX, linePolyMomentXNeg
from lib.functionDefinitions import unit, apply, make, tolClose
from lib.segmentMethods import lineTransformation, segEqn
from numpy import dot, array, cross, hstack, zeros, log10, arange, linspace, ceil, vstack, int, pi, sin, cos, add, min
from numpy.linalg import norm

# Plotting Functions


def polyPlotData(A,
                 B,
                 X,
                 Y,
                 degree=0,
                 peak=1,
                 normal=array([0, 0, -1]),
                 types='line',
                 dummy=1,
                 C=None,
                 peakPlot=0):
    normal = unit(normal)
    if peak < 0:
        peak = -peak
        normal = -normal
    scale = peakPlot if peakPlot else ((log10(peak / 50) + 1) /
                                       peak if peak >= 50 else 1)
    l = norm(Y - X)
    a = dot(X - A, unit(B - A))
    b = dot(Y - A, unit(B - A))

    def eSeg(x):
        return segEqn(types, A, B, x, C)

    def eLoad(x):        return eSeg(x) - \
(scale*(peak/(l**degree))*(x-a)**degree)*normal

    noOfpts = int((ceil(l) / 50) + 2) if peakPlot else int(ceil(l) + 2)
    goodXs = linspace(a, b, noOfpts)
    xv = unit(Y - X)

    def giveMePoints(x):
        p0 = eLoad(x)
        p1 = eSeg(x)
        h = norm(p0 - p1)
        f = min([0.2 * h, 15]) if peakPlot else min([0.2 * h, 0.5])
        p2 = p1 + f * xv - f * normal
        p3 = p2 - 2 * f * xv
        return vstack((p0, p1, p2, p3, p1, p0))

    return (apply(giveMePoints, goodXs).reshape((noOfpts * 6), 3)) / dummy


def pointPlotData(X, peak=1, normal=array([0, 0, -1]), dummy=1, peakPlot=0):
    normal = unit(normal)
    if peak < 0:
        peak = -peak
        normal = -normal
    scale = peakPlot if peakPlot else ((log10(peak / 50) + 1) /
                                       peak if peak >= 50 else 1)
    v1 = cross(normal, array([1, 0, 0]))
    v2 = cross(normal, array([0, 1, 0]))
    o = array([0, 0, 0])
    npt = -0.2 * dummy * scale * peak * normal
    nptx = unit(v2) if norm(v1) == 0 else unit(v1)
    npty = cross(normal, nptx)
    th = (2 * pi) / 3
    npt120 = cos(th) * nptx + sin(th) * npty
    npt240 = cos(2 * th) * nptx + sin(2 * th) * npty
    basic = vstack(
        (o, npt, npt + 0.1 * dummy * nptx, o, npt, npt + 0.1 * dummy * npt120,
         o, npt, npt + 0.1 * dummy * npt240, o, npt / 0.2))
    basic = add(basic, X)
    return (basic)


def momentPlotData(X, peak=1, normal=array([1, 0, 0]), dummy=1, peakPlot=0):
    normal = unit(normal)
    if peak < 0:
        peak = -peak
        normal = -normal
    scale = peakPlot if peakPlot else ((log10(peak / 50) + 1) /
                                       peak if peak >= 50 else 1)
    v1 = cross(normal, array([1, 0, 0]))
    v2 = cross(normal, array([0, 1, 0]))
    o = array([0, 0, 0])

    nptx = unit(v2) if (norm(v1) == 0) else unit(v1)
    npty = cross(normal, nptx)
    th = arange(0, 3 * pi / 2, pi / 16)
    pts = scale * peak * apply(lambda t: nptx * cos(t) + npty * sin(t), th)
    arrowOrigin = pts[-1]
    arrowEnd = -scale * peak * npty
    f = min([0.5, 0.2 * scale * peak])
    pt1 = arrowOrigin + f * npty
    pt2 = arrowOrigin - f * npty
    arrow = vstack((arrowOrigin, pt1, arrowEnd, pt2, arrowOrigin))
    pts = vstack((o, pts, arrow))
    basic = add(pts, X)
    return (basic / dummy)


def polyPlotData2(A,
                  B,
                  X,
                  Y,
                  degree=0,
                  peak=1,
                  normal=array([0, -1]),
                  types='line',
                  scale=1,
                  C=None,
                  peakPlot=0):
    normal = unit(normal)
    xv = array([-normal[1], normal[0]])
    if peak < 0:
        peak = -peak
        normal = -normal

    if any(C == None):
        C = array([0, 0])

    a = dot(X - A, unit(B - A))
    b = dot(Y - A, unit(B - A))

    if a < 0:
        a = 0
    elif a > norm(B - A):
        a = norm(B - A)
    else:
        a = a

    if b < 0:
        b = 0
    elif b > norm(B - A):
        b = norm(B - A)
    else:
        b = b

    # if a>b:
    # a,b = b,a

    def eSeg(x):
        return segEqn(types, hstack((0, A)), hstack((0, B)), x, hstack(
            (0, C)))[1:3]

    X = eSeg(a)
    Y = eSeg(b)
    l = norm(Y - X)

    def eLoad(x):
        return eSeg(x) - ((abs(x - a) / l)**degree) * peak * normal * scale

    noOfpts = int((ceil(l) * 2) + 2)
    goodXs = linspace(a, b, noOfpts)

    def giveMePoints(x):
        p0 = eLoad(x)
        p1 = eSeg(x)
        h = norm(p0 - p1)
        f = min([0.15 * h, 0.15])
        p2 = p1 + f * xv - f * normal
        p3 = p2 - 2 * f * xv
        return vstack((p0, p1, p2, p3, p1, p0))

    return apply(giveMePoints, goodXs).reshape((noOfpts * 6), 2)


def pointPlotData2(A,
                   B,
                   X,
                   peak=1,
                   normal=array([0, -1]),
                   types='line',
                   dummy=1,
                   C=None,
                   peakPlot=0):
    normal = -unit(normal)
    if peak < 0:
        peak = -peak
        normal = -normal

    if any(C == None):
        C = array([0, 0])
    a = dot(X - A, unit(B - A))

    if a < 0:
        a = 0
    elif a > norm(B - A):
        a = norm(B - A)
    else:
        a = a

    def eSeg(x):
        return segEqn(types, hstack((0, A)), hstack((0, B)), x, hstack(
            (0, C)))[1:3]

    X = eSeg(a)

    f = max([min([0.15, 0.15 * peak]), 0.05])
    vec = array([-normal[1], normal[0]])
    lineOrigin = normal * peak
    lineEnd = f * normal
    arrowEnd = array([0, 0])
    pt1 = lineEnd + f * vec
    pt2 = lineEnd - f * vec
    arrow = vstack((lineOrigin, lineEnd, pt1, arrowEnd, pt2, lineEnd)) * dummy
    basic = add(arrow, X)
    return basic


def momentPlotData2(A,
                    B,
                    X,
                    peak=1,
                    types='line',
                    dummy=1,
                    C=None,
                    peakPlot=0):
    if any(C == None):
        C = array([0, 0])

    a = dot(X - A, unit(B - A))

    if a < 0.0:
        a = 0
    elif a > norm(B - A):
        a = norm(B - A)
    else:
        a = a

    def eSeg(x):
        return segEqn(types, hstack((0, A)), hstack((0, B)), x, hstack(
            (0, C)))[1:3]

    X = eSeg(a)

    f = 0.3 * peak
    o = array([0, 0])
    th = arange(0, 3 * pi / 2, pi / 20) * (abs(peak) / peak)
    pts = peak * apply(lambda t: array([cos(t), sin(t)]), th)
    arrowOrigin = pts[-1]
    arrowEnd = peak * (array([0, -1]) if peak == abs(peak) else array([0, 1]))
    pt1 = arrowOrigin + array([0, f / 2])
    pt2 = arrowOrigin - array([0, f / 2])
    arrow = vstack((arrowOrigin, pt1, arrowEnd, pt2, arrowOrigin))
    pts = vstack((o, pts, arrow)) * dummy / 2
    basic = add(pts, X)
    return basic


def loadPlotData(X,
                 Y=None,
                 A=None,
                 B=None,
                 C='None',
                 degree=0,
                 peak=1,
                 normal=array([0, 0, -1]),
                 types='line',
                 scale=2,
                 peakPlot=0):
    peakPlot = not peakPlot
    if degree == -2.0:
        return momentPlotData(X, peak, normal, scale, peakPlot)
    elif degree == -1.0:
        return pointPlotData(X, peak, normal, scale, peakPlot)
    else:
        return polyPlotData(A, B, X, Y, degree, peak, normal, types, scale, C,
                            peakPlot)


def loadPlotData2(X,
                  Y=None,
                  A=None,
                  B=None,
                  C='None',
                  degree=0,
                  peak=1,
                  normal=array([0, 0, -1]),
                  types='line',
                  scale=1,
                  peakPlot=0):
    if peakPlot and abs(peak) >= 1:
        peak = (abs(peak) / peak) * (log10(abs(peak)) + 1)
    if peak == 0:
        peak = 1e-10
    if degree == -2.0:
        return momentPlotData2(A, B, X, peak, types, scale, C, peakPlot)
    elif degree == -1.0:
        return pointPlotData2(A, B, X, peak, normal, types, scale, C, peakPlot)
    else:
        return polyPlotData2(A, B, X, Y, degree, peak, normal, types, scale, C,
                             peakPlot)


def loadPlotData3(A, B, C, types, degree, peak=None):

    def eSeg(x):
        return segEqn(types, A, B, x, C)

    riseFall = max(0.1 * norm(B - A), 0.25)
    xv = unit(B - A)
    yv = cross(ps['axisVector', xv])
    C = eSeg(norm(B - A) / 2)
    if degree == -3:
        return array([
            A + yv * riseFall, C + yv * riseFall, B + yv * riseFall, B,
            B - yv * riseFall, C - yv * riseFall, A - yv * riseFall, A,
            A + yv * riseFall
        ])
    else:
        if peak == abs(peak):
            return array([
                C + yv * riseFall, C - xv * riseFall, C - yv * riseFall,
                C + xv * riseFall, C + yv * riseFall
            ])
        else:
            return array([
                C - xv * riseFall + yv * riseFall, C,
                C - xv * riseFall - yv * riseFall,
                C + xv * riseFall - yv * riseFall, C,
                C + xv * riseFall + yv * riseFall,
                C - xv * riseFall + yv * riseFall
            ])


def loadPlotData4(A, B, C, types, degree, peak=None, scale=1):

    def eSeg(x):
        return segEqn(types, hstack((0, A)), hstack((0, B)), x, hstack(
            (0, C)))[1:3]

    riseFall = min([0.1 * norm(B - A), 0.25]) * scale
    xv = unit(B - A)
    yv, xv = riseFall * unit(array([-xv[1], xv[0]])), riseFall * xv
    C = eSeg(norm(B - A) / 2)
    if degree == -3:
        if types == 'line':
            pt1 = eSeg(0.45 * norm(B - A))
            pt2 = eSeg(0.55 * norm(B - A))
            return array([pt1 + yv, pt2 + yv, pt2 - yv, pt1 - yv, pt1 + yv])
        else:
            pts1 = [eSeg(f * norm(B - A)) for f in linspace(0.25, 0.75, 50)]
            pts2 = [eSeg(f * norm(B - A)) for f in linspace(0.75, 0.25, 50)]
            return vstack((pts1 + yv, pts2 - yv, pts1[0] + yv))
    else:
        if peak == abs(peak):
            return array([
                C - xv, C - xv - yv, C - 2 * xv, C - xv + yv, C - xv, C + xv,
                C + xv - yv, C + 2 * xv, C + xv + yv, C + xv
            ])
        else:
            return array([
                C - xv, C - 2 * xv - yv, C - 2 * xv + yv, C - xv, C + xv,
                C + 2 * xv - yv, C + 2 * xv + yv, C + xv
            ])


# Action breakdown
def lineForceX(A, B, X, Y, degree, peak, normal):
    if degree == -2:
        return lambda x: lineMomentForceX(float(x))
    elif degree == -1:
        return lambda x: linePointForceX(A.astype(float), B.astype(float),
                                         X.astype(float), float(peak),
                                         normal.astype(float), float(x))
    else:
        if dot(unit(Y - X), unit(B - A)) > 0:
            return lambda x: linePolyForceX(A.astype(float), B.astype(
                float), X.astype(float), Y.astype(float), degree, float(peak),
                                            normal.astype(float), float(x))
        else:
            return lambda x: linePolyForceXNeg(A.astype(float), B.astype(
                float), X.astype(float), Y.astype(float), degree, float(peak),
                                               normal.astype(float), float(x))


def lineMomentX(A, B, X, Y, degree, peak, normal):
    if degree == -2:
        return lambda x: lineMomentMomentX(A.astype(float), B.astype(float),
                                           X.astype(float), float(peak),
                                           normal.astype(float), float(x))
    elif degree == -1:
        return lambda x: linePointMomentX(A.astype(float), B.astype(float),
                                          X.astype(float), float(peak),
                                          normal.astype(float), float(x))
    else:
        if dot(unit(Y - X), unit(B - A)) > 0:
            return lambda x: linePolyMomentX(A.astype(float), B.astype(
                float), X.astype(float), Y.astype(float), degree, float(peak),
                                             normal.astype(float), float(x))
        else:
            return lambda x: linePolyMomentXNeg(A.astype(float), B.astype(
                float), X.astype(float), Y.astype(float), degree, float(peak),
                                                normal.astype(float), float(x))


# Response breakdowm


def lineAngleX(A, B, X, Y, degree, peak, normal, youngsModulus, shearModulus,
               Iyy, Izz, J, axisVector):
    if degree == -2:
        return lambda x: lineMomentAngleX(
            A.astype(float), B.astype(float), X.astype(float), float(peak),
            normal.astype(float), float(youngsModulus), float(shearModulus),
            float(Iyy), float(Izz), float(J), axisVector.astype(float), float(
                x))
    elif degree == -1:
        return lambda x: linePointAngleX(
            A.astype(float), B.astype(float), X.astype(float), float(peak),
            normal.astype(float), youngsModulus, Iyy, Izz,
            axisVector.astype(float), float(x))
    else:
        if dot(unit(Y - X), unit(B - A)) > 0:
            return lambda x: linePolyAngleX(
                A.astype(float), B.astype(float), X.astype(float),
                Y.astype(float), degree, float(peak), normal.astype(float),
                float(youngsModulus), float(Iyy), float(Izz),
                axisVector.astype(float), float(x))
        else:
            return lambda x: linePolyAngleXNeg(
                A.astype(float), B.astype(float), X.astype(float),
                Y.astype(float), degree, float(peak), normal.astype(float),
                float(youngsModulus), float(Iyy), float(Izz),
                axisVector.astype(float), float(x))


def lineDisplaceX(A, B, X, Y, degree, peak, normal, youngsModulus,
                  shearModulus, Iyy, Izz, axisVector, J, area, shapeFactor):
    if degree == -2:
        return lambda x: lineMomentDisplaceX(
            A.astype(float), B.astype(float), X.astype(float), float(peak),
            normal.astype(float), float(youngsModulus), float(shearModulus),
            float(Iyy), float(Izz), float(J), axisVector.astype(float), float(
                x))
    elif degree == -1:
        return lambda x: linePointDisplaceX(
            A.astype(float), B.astype(float), X.astype(float), float(peak),
            normal.astype(float), float(youngsModulus), float(shearModulus),
            float(Iyy), float(Izz), axisVector.astype(float), float(area),
            shapeFactor.astype(float), float(x))
    else:
        if dot(unit(Y - X), unit(B - A)) > 0:
            return lambda x: linePolyDisplaceX(
                A.astype(float), B.astype(float), X.astype(float),
                Y.astype(float), degree, float(peak), normal.astype(float),
                float(youngsModulus), float(shearModulus), float(Iyy),
                float(Izz), axisVector.astype(float), float(area),
                shapeFactor.astype(float), float(x))
        else:
            return lambda x: linePolyDisplaceXNeg(
                A.astype(float), B.astype(float), X.astype(float),
                Y.astype(float), degree, float(peak), normal.astype(float),
                float(youngsModulus), float(shearModulus), float(Iyy),
                float(Izz), axisVector.astype(float), float(area),
                shapeFactor.astype(float), float(x))


# FEAs definitions
def linePointLocalFEA(A,
                      B,
                      X,
                      z1=array([0, 0, 1]),
                      z2=array([0, 0, 1]),
                      peak=1,
                      axisVector=array([1, 0, 0]),
                      normal=array([0, 0, -1]),
                      hinged=False):
    FEA = linePointGlobalFEA(A.astype(float), B.astype(float), X.astype(float),
                             z1.astype(float), z2.astype(float), peak,
                             axisVector.astype(float), normal.astype(float),
                             hinged)
    T = lineTransformation(A.astype(float), B.astype(float),
                           axisVector.astype(float), z1.astype(float),
                           z2.astype(float))
    return T @ FEA


def lineMomentLocalFEA(A,
                       B,
                       X,
                       z1=array([0, 0, 1]),
                       z2=array([0, 0, 1]),
                       peak=1,
                       axisVector=array([1, 0, 0]),
                       normal=array([0, 0, -1]),
                       hinged=False):
    FEA = lineMomentGlobalFEA(A.astype(float), B.astype(float),
                              X.astype(float), z1.astype(float),
                              z2.astype(float), peak, axisVector.astype(float),
                              normal.astype(float), hinged)
    T = lineTransformation(A.astype(float), B.astype(float),
                           axisVector.astype(float), z1.astype(float),
                           z2.astype(float))
    return T @ FEA


def linePolyLocalFEA(A,
                     B,
                     X,
                     Y,
                     z1=array([0, 0, 1]),
                     z2=array([0, 0, 1]),
                     degree=0,
                     peak=1,
                     axisVector=array([1, 0, 0]),
                     normal=array([1, 0, 0]),
                     hinged=False):
    FEA = linePolyGlobalFEA(A.astype(float), B.astype(float), X.astype(float),
                            Y.astype(float), z1.astype(float),
                            z2.astype(float), degree, peak,
                            axisVector.astype(float), normal.astype(float),
                            hinged)
    T = lineTransformation(A.astype(float), B.astype(float),
                           axisVector.astype(float), z1.astype(float),
                           z2.astype(float))
    return T @ FEA


def lineGlobalFEA(A,
                  B,
                  X,
                  Y,
                  z1,
                  z2,
                  degree=-1,
                  peak=1,
                  axisVector=array([1, 0, 0]),
                  normal=array([0, 0, -1]),
                  hinged=False):
    if (degree == -2):
        return lineMomentGlobalFEA(A.astype(float), B.astype(float),
                                   X.astype(float), z1.astype(float),
                                   z2.astype(float), peak,
                                   axisVector.astype(float),
                                   normal.astype(float), hinged)
    elif (degree == -1):
        return linePointGlobalFEA(A.astype(float), B.astype(float),
                                  X.astype(float), z1.astype(float),
                                  z2.astype(float), peak,
                                  axisVector.astype(float),
                                  normal.astype(float), hinged)
    else:
        return linePolyGlobalFEA(A.astype(float), B.astype(float),
                                 X.astype(float), Y.astype(float),
                                 z1.astype(float), z2.astype(float), degree,
                                 peak, axisVector.astype(float),
                                 normal.astype(float), hinged)


def lineLocalFEA(A,
                 B,
                 X,
                 Y,
                 z1=array([0, 0, 1]),
                 z2=array([0, 0, 1]),
                 degree=-1,
                 peak=1,
                 axisVector=array([1, 0, 0]),
                 normal=array([0, 0, -1]),
                 hinged=False):
    FEA = lineGlobalFEA(A, B, X, Y, z1, z2, degree, peak, axisVector, normal,
                        hinged)
    T = lineTransformation(A.astype(float), B.astype(float),
                           axisVector.astype(float), z1.astype(float),
                           z2.astype(float))
    return T @ FEA


# definition of local loads [temperature, misfit and gravity]


def tempLoad(tempLow, tempHigh, gradientNormal, width, parentSegment, psName):
    alpha = parentSegment['alpha']
    E = parentSegment['youngsModulus']
    A = parentSegment['area']
    xv = unit(parentSegment['P3'] - parentSegment['P1'])
    zv = parentSegment['axisVector']
    yv = unit(cross(zv, xv))
    if tolClose(gradientNormal, zv):
        I = parentSegment['Izz']
        tempLow = tempLow[0] - tempLow[2]
        tempHigh = tempHigh[0] - tempHigh[2]
        momAxis = yv
    else:
        I = parentSegment['Iyy']
        tempLow = tempLow[0] - tempLow[1]
        tempHigh = tempHigh[0] - tempHigh[1]
        momAxis = zv
    forceMagnitude = 0.5 * (tempHigh + tempLow) * alpha * E * A
    momentMagnitude = alpha * E * I * (tempHigh - tempLow) / width
    force1 = {
        'degree': -1,
        'parentSegment': parentSegment,
        'P1': parentSegment['P1'],
        'P3': parentSegment['P1'],
        'normal': xv,
        'peak': forceMagnitude,
        'class': 'tempLoad',
        'psName': psName
    }
    force2 = {
        'degree': -1,
        'parentSegment': parentSegment,
        'P1': parentSegment['P3'],
        'P3': parentSegment['P3'],
        'normal': -xv,
        'peak': forceMagnitude,
        'class': 'tempLoad',
        'psName': psName
    }
    moment1 = {
        'degree': -2,
        'parentSegment': parentSegment,
        'P1': parentSegment['P1'],
        'P3': parentSegment['P1'],
        'normal': momAxis,
        'peak': momentMagnitude,
        'class': 'tempLoad',
        'psName': psName
    }
    moment2 = {
        'degree': -2,
        'parentSegment': parentSegment,
        'P1': parentSegment['P3'],
        'P3': parentSegment['P3'],
        'normal': -momAxis,
        'peak': momentMagnitude,
        'class': 'tempLoad',
        'psName': psName
    }
    return [force1, force2, moment1, moment2]


def misfitLoad(misfit, parentSegment, psName):
    E = parentSegment['youngsModulus']
    A = parentSegment['area']
    xv = parentSegment['P3'] - parentSegment['P1']
    L = norm(xv)
    xv = unit(xv)
    mag = E * A * (misfit / L)
    force1 = {
        'degree': -1,
        'parentSegment': parentSegment,
        'P1': parentSegment['P1'],
        'P3': parentSegment['P1'],
        'normal': xv,
        'peak': mag,
        'class': 'misfitLoad',
        'psName': psName
    }
    force2 = {
        'degree': -1,
        'parentSegment': parentSegment,
        'P1': parentSegment['P3'],
        'P3': parentSegment['P3'],
        'normal': -xv,
        'peak': mag,
        'class': 'misfitLoad',
        'psName': psName
    }
    return [force1, force2]


def gravityLoad(parentSegment,
                g=9.80665,
                gNormal=array([0, 0, -1]),
                psName='none'):
    if type(gNormal) == type([0, 0, 0]):
        gNormal = array(gNormal)
    return {
        'degree': 0,
        'parentSegment': parentSegment,
        'P1': parentSegment['P1'],
        'P3': parentSegment['P3'],
        'normal': unit(gNormal),
        'peak': parentSegment['density'] * g * parentSegment['area'],
        'class': 'load',
        'psName': psName
    }


def tempLoad2(tempLow, tempHigh, width, parentSegment):
    alpha = parentSegment['alpha']
    E = parentSegment['youngsModulus']
    A = parentSegment['area']
    I = parentSegment['I']
    xv = unit(parentSegment['P3'] - parentSegment['P1'])
    forceMagnitude = 0.5 * (tempHigh + tempLow) * alpha * E * A
    momentMagnitude = alpha * E * I * (tempHigh - tempLow) / width
    force1 = {
        'degree': -1,
        'parentSegment': parentSegment,
        'P1': parentSegment['P1'],
        'P3': parentSegment['P1'],
        'normal': xv,
        'peak': forceMagnitude,
        'class': 'load'
    }
    force2 = {
        'degree': -1,
        'parentSegment': parentSegment,
        'P1': parentSegment['P3'],
        'P3': parentSegment['P3'],
        'normal': -xv,
        'peak': forceMagnitude,
        'class': 'load'
    }
    moment1 = {
        'degree': -2,
        'parentSegment': parentSegment,
        'P1': parentSegment['P1'],
        'P3': parentSegment['P1'],
        'normal': array([0, 0]),
        'peak': momentMagnitude,
        'class': 'load'
    }
    moment2 = {
        'degree': -2,
        'parentSegment': parentSegment,
        'P1': parentSegment['P3'],
        'P3': parentSegment['P3'],
        'normal': array([0, 0]),
        'peak': momentMagnitude,
        'class': 'load'
    }
    return [force1, force2, moment1, moment2]
