from lib.numbaFunctions import lineStiffnessLocal2, lineTransformation2, lineStiffnessGlobal2
from lib.numbaFunctions import smoothen
from lib.numbaFunctions import lineEqn, arceqn, quadeqn
from lib.numbaFunctions import lineStiffnessLocalTruss, lineTransformationTruss, lineStiffnessGlobalTruss, lineTransformationTruss2, lineStiffnessGlobalTruss2
from lib.numbaFunctions import lineStiffnessLocal, lineTransformation, lineStiffnessGlobal
from lib.numbaFunctions import quadLength as nmbQuadLength
from lib.numbaFunctions import arcLength as nmbArcLength
from lib.functionDefinitions import unit, apply, dictInArr, identicalObjects, axes
from numpy import array, unique, sum, dot, cross, round, linspace, vstack, float, diag, zeros, hstack, arange, sort, repeat, array_equal, log
from numpy.linalg import norm

# Functions for Equations and Plots


def checkCurveValidity(P1, P3, P2):
    fv = P2 - P1
    uv = P2 - P3
    if (norm(cross(fv, uv)) == 0):
        raise ValueError('Three points to define the curve are collinear.')


def checkArcValidity(P1, P3, P2, twoD):
    fv = P2 - P1
    uv = P2 - P3
    if (dot(fv, uv) > 0):
        rmax = round(norm(P3 - P1) / 2, 3)
        if twoD:
            rmax = round(rmax / 50, 3)
        raise ValueError(
            f'Please select intermediate point within allowed radius : R < {rmax}'
        )


def arcLength(P1, P3, P2, x=None):
    if x == None:
        x = norm(P3 - P1)
    return nmbArcLength(P1, P3, P2, x)


def quadLength(P1, P3, P2, x=None):
    if x == None:
        x = norm(P3 - P1)
    return nmbQuadLength(P1, P3, P2, x)


def arcEqn(P1, P3, P2, x, twoD=False):
    checkCurveValidity(P1, P3, P2)
    checkArcValidity(P1, P3, P2, twoD)
    return arceqn(P1, P3, P2, x)


def quadEqn(P1, P3, P2, x):
    checkCurveValidity(P1, P3, P2)
    return quadeqn(P1, P3, P2, x)


def segEqn(types, P1, P3, x, P2=None):
    if types == 'line':
        return lineEqn(P1, P3, x)
    elif types == 'arc':
        return arcEqn(P1, P3, P2, x)
    else:
        return quadEqn(P1, P3, P2, x)


def linePlotData(P1, P3, axisVector, scale=1):
    """
    Returns array of 3D points that lies on the line described by given parameters. [for plotting the line]
    Also incorporates the indication of local axes by the use of axisVector.

    parameters
    ----------

    P1 = initial point of the line

    P3 = terminal point of the line

    axisVector = axisVector of the line

    returns
    -------

    numpy array of numpy array of 3 floats corresponding to 3D point [a,b,c]
    """
    P2 = (P1 + P3) / 2
    k = P2 + 0.2 * axisVector
    j = P2 + 0.4 * unit(cross(axisVector, P3 - P1))
    arrow = vstack((P1, P2, j, P2, k, P2, P3)) / scale
    return arrow


def arcPlotData(P1, P3, P2, axisVector, scale=1, no=50):
    """
    Returns array of 3D points that lies on circlar arc described by given parameters. [for plotting the arc]
    Also incorporates the indication of local axes by the use of axisVector.

    parameters
    ----------

    P1 = initial point of the arc

    P3 = terminal point of the arc

    P2 = intermediate point of the arc

    axisVector = axisVector of the line along P1-P3

    no = number of points to use in plotting the arc [default = 50]

    returns
    -------

    numpy array of numpy array of 3 floats corresponding to 3D point [a,b,c]
    """
    l1 = linspace(0, norm(P3 - P1) / 2, no // 2)

    def e(x):
        return arcEqn(P1, P3, P2, x)

    d1 = apply(e, l1)
    k = d1[-1] + 0.35 * axisVector
    j = d1[-1] + 0.25 * unit(cross(axisVector, P3 - P1))
    arrow = vstack((j, d1[-1], k))
    l2 = linspace(norm(P3 - P1) / 2, norm(P3 - P1), no - no // 2)
    d2 = apply(e, l2)
    return vstack((d1, arrow, d2)) / scale


def quadPlotData(P1, P3, P2, axisVector, scale=1, no=50):
    """
    Returns array of 3D points that lies on parabolic arc described by given parameters. [for plotting the arc]
    Also incorporates the indication of local axes by the use of axisVector.

    parameters
    ----------

    P1 = initial point of the arc

    P3 = terminal point of the arc

    P2 = intermediate point of the arc

    axisVector = axisVector of the line along P1-P3

    no = number of points to use in plotting the arc [default = 50 and is ignored if is greater than 50]

    returns
    -------

    numpy array of numpy array of 3 floats corresponding to 3D point [a,b,c]
    """
    no = min(no, 50)
    l1 = linspace(0, norm(P3 - P1) / 2, no // 2)

    def e(x):
        return quadEqn(P1, P3, P2, x)

    d1 = apply(e, l1)
    k = d1[-1] + 0.35 * axisVector
    j = d1[-1] + 0.25 * unit(cross(axisVector, P3 - P1))
    arrow = vstack((j, d1[-1], k))
    l2 = linspace(norm(P3 - P1) / 2, norm(P3 - P1), no - no // 2)
    d2 = apply(e, l2)
    return vstack((d1, arrow, d2)) / scale


def segPlotData(types,
                P1,
                P3,
                axisVector=array([1, 0, 0]),
                scale=2,
                P2=None,
                no=400):
    """
    Returns array of 3D points that lies on the segment described by given parameters. [for plotting the segment]
    Also incorporates the indication of local axes by the use of axisVector.
    Makes use of linePlotData, arcPlotData and qadPlotData. [see documentation of respective functions]

    parameters
    ----------

    types = type of segment. One of 'line', 'arc' or 'quad'

    P1 = initial point of the segment

    P3 = terminal point of the segment

    axisVector = axisVector of the line along P1-P3 [default = (1,0,0)]

    P2 = intermediate point of the segment [not compulsory]

    no = number of points to use in plotting the segment (used for arcs only) [default = 400]

    returns
    -------

    numpy array of numpy array of 3 floats corresponding to 3D point [a,b,c]
    """
    if (types == 'line'):
        return linePlotData(P1, P3, axisVector, scale)
    elif (types == 'arc'):
        return arcPlotData(P1, P3, P2, axisVector, scale, no)
    else:
        return quadPlotData(P1, P3, P2, axisVector, scale, no)


# Plotting Functions of segments extended for 2d interface


def linePlotData2(P1, P3, scale=1):
    return vstack((P1, P3)) / scale


def arcPlotData2(P1, P3, P2, scale=1, no=50):
    l = linspace(0, norm(P3 - P1), no)

    def e(x):
        return arcEqn(hstack((0, P1)),
                      hstack((0, P3)),
                      hstack((0, P2)),
                      x,
                      twoD=True)[1:3]

    d = apply(e, l)
    d = vstack((d, P3))
    return d / scale


def quadPlotData2(P1, P3, P2, scale=1, no=50):
    l = linspace(0, norm(P3 - P1), no)

    def e(x):
        return quadEqn(hstack((0, P1)), hstack((0, P3)), hstack((0, P2)),
                       x)[1:3]

    d = apply(e, l)
    d = vstack((d, P3))
    return d / scale


def segPlotData2(types, P1, P3, scale=1, P2=None, no=400):
    scale = 1
    if (types == 'line'):
        return linePlotData2(P1, P3, scale)
    elif (types == 'arc'):
        return arcPlotData2(P1, P3, P2, scale, no)
    else:
        return quadPlotData2(P1, P3, P2, scale, no)


# Functions related to analysis of 3d frame

# Functions related to diagrams plot


def actionFun(line, frame, data, scale=1):
    from lib.loadMethods import lineForceX, lineMomentX
    L = lineTransformation(line['P1'], line['P3'], line['axisVector'],
                           array([0.0, 0.0, 1.0]), array([0.0, 0.0, 1.0]))[0:6,
                                                                           0:6]
    id = dictInArr(line, frame['segments'])
    actions = L.T @ data[2 * id, 3:9]
    FA = actions[0:3]  # Force at end A [taken from frame3d]
    MA = actions[3:6]  # Moment at end A [taken from frame3d]
    loads = frame['loads']
    tempLoads = loads[apply(
        lambda x: x['class'] in ['tempLoad', 'misfitLoad'] and array_equal(
            x['P1'], line['P1']), loads)]
    if tempLoads.size:
        for x in tempLoads:
            if x['degree'] == -1:
                FA -= x['peak'] * x['normal']
            else:
                MA -= x['peak'] * x['normal']
    loads = loads[apply(
        lambda x: x['class'] == 'load' and identicalObjects(
            line, x['parentSegment']), loads)]
    index = apply(
        lambda x: x['degree'] >= 0 or not array_equal(x['P1'], line['P1']),
        loads)
    loads = loads[index] if index.size != 0 else array(
        [{
            'degree': 0,
            'parentSegment': line,
            'P1': line['P1'],
            'P3': line['P3'],
            'normal': array([0, 0, 1]),
            'peak': 0,
            'class': 'load'
        }])

    def actionFunction(x):
        P = apply(
            lambda x: lineForceX(line['P1'], line['P3'], x['P1'], x['P3'], x[
                'degree'], x['peak'], x['normal']), loads)
        mf = apply(lambda t: P[t]
                   (x), arange(P.size)) if P.size > 0 else array([zeros(3)])
        f = FA + apply(lambda x: sum(mf[:, x]), arange(3))

        M = apply(
            lambda x: lineMomentX(line['P1'], line['P3'], x['P1'], x['P3'], x[
                'degree'], x['peak'], x['normal']), loads)
        mm = apply(lambda t: M[t]
                   (x), arange(M.size)) if M.size > 0 else array([zeros(3)])
        m = MA + cross(line['P1'] - lineEqn(line['P1'], line['P3'], x),
                       FA) + apply(lambda x: sum(mm[:, x]), arange(3))
        return L @ (scale * hstack((f, m)))

    return actionFunction


def responseFun(line,
                frame,
                dataAct,
                dataRes,
                memLoc,
                shear,
                inextensible,
                scale=1,
                dispOnly=False,
                angleOnly=False):
    from lib.loadMethods import lineAngleX, lineDisplaceX
    k = line['shapeFactor'] if shear else array([0, 0])
    A = 1e12 if inextensible else line['area']
    Id = dictInArr(line, frame['segments'])
    actions = dataAct[2 * Id, 3:9]
    responses = lineTransformation(
        line['P1'], line['P3'], line['axisVector'], array([0.0, 0.0, 1.0]),
        array([0.0, 0.0, 1.0]))[0:6, 0:6] @ dataRes[memLoc[Id, 0], 3:9]
    thetaA = responses[3:6]  # slope at end A [taken from frame3d]
    deltaA = responses[0:3]  # deflection at end A [taken from frame3d]
    loads = frame['loads']
    loads = loads[apply(
        lambda x: x['class'] == 'load' and identicalObjects(
            line, x['parentSegment']), loads)]
    index = apply(
        lambda x: x['degree'] >= 0 or not array_equal(x['P1'], line['P1']),
        loads)
    loads = loads[index] if index.size != 0 else array(
        [{
            'degree': 0,
            'parentSegment': line,
            'P1': line['P1'],
            'P3': line['P3'],
            'normal': array([0, 0, 1]),
            'peak': 0,
            'class': 'load'
        }])

    if not dispOnly and not angleOnly:

        def responseFunction(x):
            theta = apply(
                lambda x: lineAngleX(line['P1'], line['P3'], x['P1'], x[
                    'P3'], x['degree'], x['peak'], x['normal'], line[
                        'youngsModulus'], line['shearModulus'], line[
                            'Iyy'], line['Izz'], line['J'], line['axisVector']
                                     ), loads)
            mf = apply(lambda t: theta[t](x), arange(
                theta.size)) if theta.size > 0 else array([zeros(3)])
            Theta = thetaA + apply(lambda x: sum(mf[:, x]), arange(3))
            thF = array([
                0, (0.5 * actions[2] * x**2) /
                (line['youngsModulus'] * line['Iyy']),
                (0.5 * actions[1] * x**2) /
                (line['youngsModulus'] * line['Izz'])
            ])
            thM = array([
                (actions[3] * x) / (line['shearModulus'] * line['J']),
                (actions[4] * x) / (line['youngsModulus'] * line['Iyy']),
                -(actions[5] * x) / (line['youngsModulus'] * line['Izz'])
            ])
            Theta = Theta + thF + thM

            delta = apply(
                lambda x: lineDisplaceX(line['P1'], line['P3'], x['P1'], x[
                    'P3'], x['degree'], x['peak'], x['normal'], line[
                        'youngsModulus'], line['shearModulus'], line[
                            'Iyy'], line['Izz'], line['axisVector'], line['J'],
                                        A, k), loads)
            mm = apply(lambda t: delta[t](x), arange(
                delta.size)) if delta.size > 0 else array([zeros(3)])
            Delta = deltaA+array([0, thetaA[2]*x, thetaA[1]*x]) + \
                apply(lambda x: sum(mm[:, x]), arange(3))*array([-1, 1, 1])
            delF = array([
                -(actions[0] * x) / (line['youngsModulus'] * A),
                (thF[2] * x) / 3 +
                (k[0] * actions[1] * x) / (line['shearModulus'] * A),
                (thF[1] * x) / 3 + (k[1] * actions[2] * x) /
                (line['shearModulus'] * A)
            ])
            delM = array([0, (thM[2] * x) / 2, (thM[1] * x) / 2])
            Delta = Delta + delF + delM
            return scale * hstack((Delta, Theta * array([1, -1, 1])))
    elif dispOnly:

        def responseFunction(x):
            thF = array([
                0, (0.5 * actions[2] * x**2) /
                (line['youngsModulus'] * line['Iyy']),
                (0.5 * actions[1] * x**2) /
                (line['youngsModulus'] * line['Izz'])
            ])
            thM = array([
                (actions[3] * x) / (line['shearModulus'] * line['J']),
                (actions[4] * x) / (line['youngsModulus'] * line['Iyy']),
                -(actions[5] * x) / (line['youngsModulus'] * line['Izz'])
            ])
            delta = apply(
                lambda x: lineDisplaceX(line['P1'], line['P3'], x['P1'], x[
                    'P3'], x['degree'], x['peak'], x['normal'], line[
                        'youngsModulus'], line['shearModulus'], line[
                            'Iyy'], line['Izz'], line['axisVector'], line['J'],
                                        A, k), loads)
            mm = apply(lambda t: delta[t](x), arange(
                delta.size)) if delta.size > 0 else array([zeros(3)])
            Delta = deltaA+array([0, thetaA[2]*x, thetaA[1]*x]) + \
                apply(lambda x: sum(mm[:, x]), arange(3))*array([-1, 1, 1])
            delF = array([
                -(actions[0] * x) / (line['youngsModulus'] * A),
                (thF[2] * x) / 3 +
                (k[0] * actions[1] * x) / (line['shearModulus'] * A),
                (thF[1] * x) / 3 + (k[1] * actions[2] * x) /
                (line['shearModulus'] * A)
            ])
            delM = array([0, (thM[2] * x) / 2, (thM[1] * x) / 2])
            Delta = Delta + delF + delM
            return scale * hstack((Delta, 0, 0, 0))
    else:

        def responseFunction(x):
            theta = apply(
                lambda x: lineAngleX(line['P1'], line['P3'], x['P1'], x[
                    'P3'], x['degree'], x['peak'], x['normal'], line[
                        'youngsModulus'], line['shearModulus'], line[
                            'Iyy'], line['Izz'], line['J'], line['axisVector']
                                     ), loads)
            mf = apply(lambda t: theta[t](x), arange(
                theta.size)) if theta.size > 0 else array([zeros(3)])
            Theta = thetaA + apply(lambda x: sum(mf[:, x]), arange(3))
            thF = array([
                0, (0.5 * actions[2] * x**2) /
                (line['youngsModulus'] * line['Iyy']),
                (0.5 * actions[1] * x**2) /
                (line['youngsModulus'] * line['Izz'])
            ])
            thM = array([
                (actions[3] * x) / (line['shearModulus'] * line['J']),
                (actions[4] * x) / (line['youngsModulus'] * line['Iyy']),
                -(actions[5] * x) / (line['youngsModulus'] * line['Izz'])
            ])
            Theta = Theta + thF + thM
            return scale * hstack((0, 0, 0, Theta))

    return responseFunction


def extractData(line, frame, fun, special=True, no=20, precision=15):
    if (line['type'] != 'line'):
        l = array([0])
        includeMe = array([0])
        if special:
            jumpLoad = frame['loads']
            logvec = apply(
                lambda x: identicalObjects(line, x['parentSegment']) and x[
                    'degree'] < 0, jumpLoad)
            if logvec.size != 0 and any(logvec):
                jumpLoad = jumpLoad[logvec]
                jumpXs1 = apply(
                    lambda x: dot(x['P1'] - line['P1'],
                                  unit(line['P3'] - line['P1'])), jumpLoad)
                jumpXs2 = apply(
                    lambda x: dot(x['P3'] - line['P1'],
                                  unit(line['P3'] - line['P1'])), jumpLoad)
                jumpXs = hstack(
                    (jumpXs1, 0.5 * (jumpXs1 + jumpXs2), jumpXs2, 0.5))
                step = 10**(-3) * norm(line['P3'] - line['P1'])
                includeMe = apply(lambda x: array([x - step, x, x + step]),
                                  jumpXs).flatten()
        l = unique(hstack((l, includeMe)))
    else:
        includeMe = array([0])
        if special:
            jumpLoad = frame['loads']
            logvec = apply(
                lambda x: identicalObjects(line, x['parentSegment']), jumpLoad)
            if logvec.size != 0 and any(logvec):
                jumpLoad = jumpLoad[logvec]
                jumpXs1 = apply(
                    lambda x: dot(x['P1'] - line['P1'],
                                  unit(line['P3'] - line['P1'])), jumpLoad)
                jumpXs2 = apply(
                    lambda x: dot(x['P3'] - line['P1'],
                                  unit(line['P3'] - line['P1'])), jumpLoad)
                jumpXs = hstack(
                    (jumpXs1, 0.5 * (jumpXs1 + jumpXs2), jumpXs2, 0.5))
                step = 10**(-3) * norm(line['P3'] - line['P1'])
                includeMe = apply(lambda x: array([x - step, x, x + step]),
                                  jumpXs).flatten()
            else:
                includeMe = array([0.25, 0.5, 0.75]) * \
                    norm(line['P3']-line['P1'])
        l = unique(
            hstack((linspace(0, norm(line['P3'] - line['P1']),
                             no + 1), includeMe)))

    def normalize(x):
        return 0 if x <= 0 else (
            norm(line['P3'] -
                 line['P1']) if x >= norm(line['P3'] - line['P1']) else x)

    l = apply(normalize, l)
    data = hstack((l.reshape(l.size, 1), apply(fun, l)))
    return round(data, precision)


def actiondata(line, frame, data, scale=1, special=True, no=20, precision=15):
    fun = actionFun(line, frame, data, scale)
    data = extractData(line, frame, fun, special, no, precision)
    return data


def responsedata(line,
                 frame,
                 dataAct,
                 dataRes,
                 memLoc,
                 shear=False,
                 inextensible=False,
                 scale=1,
                 special=True,
                 no=20,
                 dispOnly=False,
                 angleOnly=False,
                 precision=15):
    fun = responseFun(line, frame, dataAct, dataRes, memLoc, shear,
                      inextensible, scale, dispOnly, angleOnly)
    data = extractData(line, frame, fun, special, no, precision)
    return data


def extractDataGeneral(line, simFrame, dataFun):
    from lib.extensions import childOf
    children = childOf(line, simFrame)
    allData = apply(dataFun, children)
    xss = apply(
        lambda x: dot(x['P1'] - line['P1'], unit(line['P3'] - line['P1'])),
        children)
    xfs = apply(
        lambda x: dot(x['P3'] - line['P1'], unit(line['P3'] - line['P1'])),
        children)
    ls = apply(lambda x: norm(x['P3'] - x['P1']), children)
    xs = [[xss[i] + ((xfs[i] - xss[i]) / ls[i]) * x for x in allData[i][:, 0]]
          for i in arange(allData.shape[0])]
    allData = vstack((allData))
    allData[:, 0] = hstack((xs))
    if line['type'] != 'line':
        s = allData[:, 0]
        for i in arange(1, 7):
            smoothen(s, allData[:, i])
    Data = vstack((zeros(7), allData, hstack((xfs[-1], zeros(6))), zeros(7)))
    return Data


def actionData(line, simFrame, rawData, no=20, special=True, scale=1):
    if line['type'] != 'line':
        no = 1

    def dataFun(x):
        return actiondata(x, simFrame, rawData, scale, special, no)

    Data = extractDataGeneral(line, simFrame, dataFun)
    return Data


def responseData(line,
                 frameData,
                 shear=False,
                 inextensible=False,
                 no=20,
                 special=True,
                 scale=1,
                 dispOnly=False,
                 angleOnly=False):
    if line['type'] != 'line':
        no = 1

    def dataFun(x):
        return responsedata(x, frameData['simplified'], frameData['actionRaw'],
                            frameData['responseRaw'], frameData['memLoc'],
                            shear, inextensible, scale, special, no, dispOnly,
                            angleOnly)

    Data = extractDataGeneral(line, frameData['simplified'], dataFun)
    return Data


# Functions related to analysis of 2d untwistable frame

# Function related to analysis of truss

# Functions related to truss diagram plot


def trussActionData(segment, simTruss, actionRaw, scale=1):
    from lib.extensions import childOf
    children = childOf(segment, simTruss)

    def af(x):
        return actionRaw[2 * dictInArr(x, simTruss['segments']), -1] * scale

    def l(x):
        return norm(x['P3'] - x['P1'])

    def data(x):
        return array([[0, af(x)], [l(x), af(x)]])

    datas = vstack(apply(data, children))
    ls = repeat(array([0, *apply(l, children)[:-1]]), 2)
    datas[:, 0] += ls
    return vstack(([0] * 7, hstack((datas, zeros(
        (len(datas), 5)))), [datas[-1, 0], *[0] * 6], [0] * 7))


def trussResponseData(segment, frameData, scale=1):
    simTruss, responseRaw, memLoc = frameData['simplified'], frameData[
        'responseRaw'], frameData['memLoc']
    from lib.extensions import childOf
    children = childOf(segment, simTruss)

    def l(line):
        return norm(line['P3'] - line['P1'])

    def responses(line):        return hstack((responseRaw[memLoc[dictInArr(line, simTruss['segments'])], 3:], zeros((2, 3)))) \
@ (lineTransformation(line['P1'], line['P3'], line['axisVector'])[:6, :6]).T

    def data(line):
        return hstack((vstack((0, l(line))), scale * responses(line)))

    datas = vstack(apply(data, children))
    ls = repeat(array([0, *apply(l, children)[:-1]]), 2)
    datas[:, 0] += ls
    return vstack(([0] * 7, datas, [datas[-1, 0], *[0] * 6], [0] * 7))
