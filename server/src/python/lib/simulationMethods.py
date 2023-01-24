from numpy import cross, vstack, array, dot, tile, hstack, linspace, sign, repeat, zeros, arange, unique, isnan, prod, setdiff1d, log10, abs, Inf
from numpy import nan as NAN
from numpy.linalg import norm, inv
from lib.segmentMethods import segEqn, responseData, actionData, trussActionData, trussResponseData
from lib.functionDefinitions import apply, unit, rowPos, convertTo3D
from lib.extensions import childOf
# from lib.structureMethods import frame2d, frame3d, truss2d, truss3d


def extractComponents(vec, data):
    return apply(lambda x: x * vec, dot(vec, data.T))


def nanRows(matrixWithNanRows):
    return unique(isnan(matrixWithNanRows).nonzero()[0])


def regularizeScale(segments, funData, maxPlot=None):
    maximum = max(
        apply(lambda i: max(abs(funData[i][:, -1])), range(len(segments))))
    numerator = (min([
        3, 0.25 * min(apply(lambda x: norm(x['P1'] - x['P3']), segments))
    ]) if maxPlot == None else maxPlot)
    if maximum == 0:
        return 1
    else:
        scale = numerator / maximum
        if scale < 1:
            return 1 / int(round(1 / scale, -int(log10(1 / scale))))
        else:
            return int(round(scale, -int(log10(scale))))


def reScale(seg, fdata, scale):

    def e(x):
        return segEqn(seg['type'], seg['P1'], seg['P3'], x, seg['P2'])

    xs, fs = fdata[:, 0], fdata[:, 1:-1]
    if fs.shape[1] == 2:
        fs = hstack((zeros((fs.shape[0], 1)), fs))
        data = array([(1 - scale) * e(xs[i]) + scale * fs[i]
                      for i in range(len(xs))])
        return hstack((vstack(xs), data[:, 1:], vstack(fdata[:, -1])))
    else:
        data = array([(1 - scale) * e(xs[i]) + scale * fs[i]
                      for i in range(len(xs))])
        return hstack((vstack(xs), data, vstack(fdata[:, -1])))


def getRescaledData(segments, funData, scale=None, maxPlot=None, precision=15):
    if scale == None:
        scale = regularizeScale(segments, funData, maxPlot)
    return scale, apply(lambda x: reScale(segments[x], funData[x], scale),
                        range(len(segments)))


def makeFunData(oneFrameData):
    nR = nanRows(oneFrameData)

    def segmentKeyFrameData(segmentId):
        return oneFrameData[0 if segmentId == 0 else (nR[segmentId - 1] +
                                                      1):nR[segmentId]]

    return apply(segmentKeyFrameData, range(len(nR)))


def makeFrameData(funData):
    nanRow = repeat(NAN, funData[0].shape[1])
    return vstack(apply(lambda x: vstack((x, nanRow)), funData))


def vectorDiagramData3D(segment, rawData, component=None):
    A = segment['P1']
    B = segment['P3']
    C = segment['P2']

    def e(x):
        return segEqn(segment['type'], A, B, x, C)

    xs = rawData[:, 0][:-1]
    Xs = apply(e, xs)
    vecData = rawData[:-1, 1:]
    xv = unit(B - A)
    zv = segment['axisVector']
    yv = cross(zv, xv)
    L = vstack((xv, yv, zv))
    vecData = (L.T @ vecData.T).T
    if component:
        vecData = extractComponents(
            xv if component == 'x' else (yv if component == 'y' else zv),
            vecData)
    if component == 'x':
        vecData = apply(lambda x: dot(x, xv) * yv, vecData)
    return hstack(
        (xs, vecData + Xs,
         vstack(
             apply(lambda x: sign(dot(x, yv) or dot(x, zv)) * norm(x),
                   vecData))))


def simulateFrameMotion3D(frame,
                          frameData,
                          shear=False,
                          inextensible=True,
                          no=20,
                          scale=1):

    def individualData(seg):
        return vstack((vectorDiagramData3D(
            seg,
            responseData(seg, frameData, shear, inextensible, no, True, scale,
                         True)[:, :4])[1:-1], repeat(NAN, 5)))

    toReturn = apply(individualData, frame['segments'])
    finalPlot = vstack(toReturn)
    return finalPlot


def vectorDiagramDataForces3D(segment,
                              frameData,
                              component=None,
                              shear=False,
                              inextensible=True,
                              special=False,
                              no=20,
                              scale=1):
    return vectorDiagramData3D(
        segment,
        actionData(segment, frameData['simplified'], frameData['actionRaw'],
                   no, special, scale)[:, :4])


def vectorDiagramDataMoments3D(segment,
                               frameData,
                               component=None,
                               shear=False,
                               inextensible=True,
                               special=False,
                               no=20,
                               scale=1):
    return vectorDiagramData3D(
        segment,
        actionData(segment, frameData['simplified'], frameData['actionRaw'],
                   no, special, scale)[:, [0, 4, 5, 6]])


def vectorDiagramDataForces3Dcomp(segment,
                                  frameData,
                                  component,
                                  shear=False,
                                  inextensible=True,
                                  special=False,
                                  no=20,
                                  scale=1):
    return vectorDiagramData3D(
        segment,
        actionData(segment, frameData['simplified'], frameData['actionRaw'],
                   no, special, scale)[:, :4], component)


def vectorDiagramDataMoments3Dcomp(segment,
                                   frameData,
                                   component,
                                   shear=False,
                                   inextensible=True,
                                   special=False,
                                   no=20,
                                   scale=1):
    return vectorDiagramData3D(
        segment,
        actionData(segment, frameData['simplified'], frameData['actionRaw'],
                   no, special, scale)[:, [0, 4, 5, 6]], component)


def vectorDiagramDataAngles3Dcomp(segment,
                                  frameData,
                                  component,
                                  shear=False,
                                  inextensible=True,
                                  special=False,
                                  no=20,
                                  scale=1):
    return vectorDiagramData3D(
        segment,
        responseData(segment,
                     frameData,
                     shear,
                     inextensible,
                     no,
                     special,
                     scale,
                     angleOnly=True)[:, [0, 4, 5, 6]], component)


def vectorDiagramDataDisps3Dcomp(segment,
                                 frameData,
                                 component,
                                 shear=False,
                                 inextensible=True,
                                 special=False,
                                 no=20,
                                 scale=1):
    return vectorDiagramData3D(
        segment,
        responseData(segment,
                     frameData,
                     shear,
                     inextensible,
                     no,
                     special,
                     scale,
                     dispOnly=True)[:, :4], component)


def vectorDiagramDataTrussForces3Dcomp(segment,
                                       frameData,
                                       component,
                                       shear=False,
                                       inextensible=True,
                                       special=False,
                                       no=20,
                                       scale=1):
    return vectorDiagramData3D(
        segment,
        trussActionData(segment, frameData['simplified'],
                        frameData['actionRaw'], scale)[:, :4], component)


def vectorDiagramDataTrussDisps3Dcomp(segment,
                                      frameData,
                                      component,
                                      shear=False,
                                      inextensible=True,
                                      special=False,
                                      no=20,
                                      scale=1):
    return vectorDiagramData3D(
        segment,
        trussResponseData(segment, frameData['simplified'],
                          frameData['responseRaw'], frameData['memLoc'],
                          scale)[:, :4], component)


def vectorDiagramData2D(segment, rawData, component=None):
    A = segment['P1']
    B = segment['P3']
    C = segment['P2']

    def e(x):
        return segEqn(segment['type'], A, B, x, C)

    xs = vstack((rawData[:, 0][:-1]))
    Xs = apply(e, xs)[:, 1:]
    vecData = rawData[:-1, 1:3]
    xv = unit(B - A)
    zv = segment['axisVector']
    yv = cross(zv, xv)
    xv = xv[1:]
    yv = yv[1:]
    L = vstack((xv, yv))
    vecData = (L.T @ vecData.T).T
    if component:
        vecData = extractComponents(xv if component == 'x' else yv, vecData)
    if component == 'x':
        vecData = apply(lambda x: dot(x, xv) * yv, vecData)
    return hstack((xs, vecData + Xs,
                   vstack(apply(lambda x: sign(dot(x, yv)) * norm(x),
                                vecData))))


def simulateFrameMotion2D(frame,
                          frameData,
                          shear=False,
                          inextensible=True,
                          no=20,
                          scale=1):

    def individualData(seg):
        return vstack((vectorDiagramData2D(
            seg,
            responseData(seg, frameData, shear, inextensible, no, True, scale,
                         True)[:, :4])[1:-1], repeat(NAN, 4)))

    toReturn = apply(individualData, frame['segments'])
    finalPlot = vstack(toReturn)
    return finalPlot


def vectorizeMoments2D(unitVec, momArr):
    return apply(lambda x: x * unitVec, momArr)


def vectorDiagramDataForces2D(segment,
                              frameData,
                              component=None,
                              shear=False,
                              inextensible=True,
                              special=False,
                              no=20,
                              scale=1):
    simFrame, actionRaw = frameData['simplified'], frameData['actionRaw']
    rawData = actionData(segment, simFrame, actionRaw, no, special,
                         scale)[:, :4]
    return vectorDiagramData2D(segment, rawData, component)


def vectorDiagramDataMoments2D(segment,
                               frameData,
                               component=None,
                               shear=False,
                               inextensible=True,
                               special=False,
                               no=20,
                               scale=1):
    simFrame, actionRaw = frameData['simplified'], frameData['actionRaw']
    data = actionData(segment, simFrame, actionRaw, no, special, scale)
    xs = vstack(data[:, 0])
    rawData = hstack((xs, data[:, -2:]))
    return vectorDiagramData2D(segment, rawData)


def vectorDiagramDataForces2Dcomp(segment,
                                  frameData,
                                  component,
                                  shear=False,
                                  inextensible=True,
                                  special=False,
                                  no=20,
                                  scale=1):
    return vectorDiagramData2D(
        segment,
        actionData(segment, frameData['simplified'], frameData['actionRaw'],
                   no, special, scale)[:, :4], component)


def vectorDiagramDataDisps2Dcomp(segment,
                                 frameData,
                                 component,
                                 shear=False,
                                 inextensible=True,
                                 special=False,
                                 no=20,
                                 scale=1):
    return vectorDiagramData2D(
        segment,
        responseData(segment,
                     frameData,
                     shear,
                     inextensible,
                     no,
                     special,
                     scale,
                     dispOnly=True)[:, :4], component)


def vectorDiagramDataTrussForces2Dcomp(segment,
                                       frameData,
                                       component,
                                       shear=False,
                                       inextensible=True,
                                       special=False,
                                       no=20,
                                       scale=1):
    return vectorDiagramData2D(
        segment,
        trussActionData(segment, frameData['simplified'],
                        frameData['actionRaw'], scale)[:, :4], component)


def vectorDiagramDataTrussDisps2Dcomp(segment,
                                      frameData,
                                      component,
                                      shear=False,
                                      inextensible=True,
                                      special=False,
                                      no=20,
                                      scale=1):
    return vectorDiagramData2D(
        segment,
        trussResponseData(segment, frameData, scale)[:, :4], component)


def vectorDiagramDataAngles2Dcomp(segment,
                                  frameData,
                                  component,
                                  shear=False,
                                  inextensible=True,
                                  special=False,
                                  no=20,
                                  scale=1):
    data = responseData(segment,
                        frameData,
                        shear,
                        inextensible,
                        no,
                        special,
                        scale,
                        angleOnly=True)
    xs = vstack(data[:, 0])
    # unitVec = unit(segment['P3']-segment['P1'])
    # momArr = data[:,-1]
    # mom3Ddata = vectorizeMoments2D(unitVec,momArr)
    rawData = hstack((xs, data[:, -2:]))
    return vectorDiagramData2D(segment, rawData)


def simulateTrussMotion(truss, responseRaw, shear, inextensible, no, scale=1):
    simTruss = responseRaw['simplified']
    responseRaw = responseRaw['responseRaw']
    segments = truss['segments']
    nodes = responseRaw[:, :3]
    deflections = scale * responseRaw[:, 3:]

    def segmentData(seg):
        d1, d2 = deflections[rowPos(seg['P1'], nodes)], deflections[rowPos(
            seg['P3'], nodes)]
        n1, n2 = norm(d1), norm(d2)
        return vstack(
            (array([0, *(seg['P1'] + d1), n1]),
             array([norm(seg['P3'] - seg['P1']), *(seg['P3'] + d2), n2])))

    def parentSegmentData(seg):
        children = childOf(seg, simTruss)
        ls = repeat(
            array(
                [0, *apply(lambda x: norm(x['P3'] - x['P1']), children)[:-1]]),
            2)
        data = vstack((apply(segmentData, children)))
        data[:, 0] += ls
        return vstack((data, repeat(NAN, 5)))

    return vstack(apply(parentSegmentData, segments))


def simulateTrussMotion2(truss, responseRaw, shear, inextensible, no, scale=1):
    simTruss = responseRaw['simplified']
    responseRaw = responseRaw['responseRaw'][:, [0, 1, 2, 4, 5]]
    segments = truss['segments']
    nodes = responseRaw[:, :3]
    deflections = hstack((zeros(
        (nodes.shape[0], 1)), scale * responseRaw[:, 3:]))

    def segmentData(seg):
        d1, d2 = deflections[rowPos(seg['P1'], nodes)], deflections[rowPos(
            seg['P3'], nodes)]
        n1, n2 = norm(d1), norm(d2)
        return vstack(
            (array([0, *(seg['P1'] + d1), n1]),
             array([norm(seg['P3'] - seg['P1']), *(seg['P3'] + d2), n2])))

    def parentSegmentData(seg):
        children = childOf(seg, simTruss)
        ls = repeat(
            array(
                [0, *apply(lambda x: norm(x['P3'] - x['P1']), children)[:-1]]),
            2)
        data = vstack((apply(segmentData, children)))
        data[:, 0] += ls
        return vstack((data, repeat(NAN, 5)))

    datas = apply(parentSegmentData, segments)
    return vstack(datas)[:, [0, 2, 3, 4]]


def interpolateFramesLinear(keyFrameData, givenFrames, fillFrame):
    t = fillFrame
    signs = sign(t - array(givenFrames))
    index = arange(len(givenFrames) - 1).astype(int)
    boundaries = apply(lambda x: signs[x] * signs[x + 1] == -1, index)
    index = boundaries.nonzero()[0][0]
    t1 = givenFrames[index]
    t2 = givenFrames[index + 1]
    y2 = keyFrameData[t2]
    y1 = keyFrameData[t1]
    y = (y2 - y1) / (t2 - t1) * (t - t1) + y1
    keyFrameData[fillFrame] = y


def interpolateFramesNatSpline(splineConstants, keyFrameData, givenFrames,
                               fillFrame):
    t = fillFrame
    signs = sign(t - array(givenFrames))
    index = arange(len(givenFrames) - 1)
    boundaries = apply(lambda x: signs[x] * signs[x + 1] == -1, index)
    i = boundaries.nonzero()[0][0]
    delt1 = t - givenFrames[i]
    delt2 = givenFrames[i + 1] - t
    A = splineConstants[i][0]
    B = splineConstants[i][1]
    C = splineConstants[i][2]
    D = splineConstants[i][3]
    keyFrameData[t] = A * delt1**3 + B * delt2**3 + C * delt1 + D * delt2


def interpolateFramesLagrange(keyFrameData, givenFrames, fillFrame):
    t = fillFrame
    x = givenFrames
    yp = sum([
        keyFrameData[i] * prod([(t - j) / (i - j) for j in setdiff1d(x, i)])
        for i in x
    ])
    keyFrameData[t] = yp


def splineConstantsVector(t, x):
    i = arange(t.size - 1)
    h = zeros(t.size - 1)
    b = zeros(t.size - 1)
    u = zeros(t.size - 1)
    v = zeros(t.size - 1)
    a = zeros(t.size - 1)
    b = zeros(t.size - 1)
    c = zeros(t.size - 1)
    d = zeros(t.size - 1)
    h[i] = t[i + 1] - t[i]
    b[i] = (x[i + 1] - x[i]) / h[i]
    j = i[1:]
    v[j] = 2 * (h[j - 1] + h[j])
    u[j] = 6 * (b[j] - b[j - 1])
    mat = zeros((v.size - 1, v.size - 1))
    mat[i[:-2], i[1:-1]] = h[i[1:-1]]
    mat = mat + mat.T
    mat[j - 1, j - 1] = v[j]
    z = inv(mat) @ u[1:]
    z = hstack((0, z, 0))
    a[i] = z[i + 1] / (6 * h[i])
    b[i] = z[i] / (6 * h[i])
    c[i] = x[i + 1] / h[i] - z[i + 1] * h[i] / 6
    d[i] = x[i] / h[i] - z[i] * h[i] / 6
    return array([a, b, c, d]).T


def generateSplineConstants(keyFrameData, givenFrames):
    t = array(givenFrames)
    orgi = array(list(keyFrameData.values()))
    dim = orgi.shape[-1]
    constMatrix = zeros((t.size - 1, 4, orgi.shape[1], dim))
    X = apply(lambda x: x.flatten(), orgi)

    def updateConst(index):
        vec = splineConstantsVector(t, X[:, index]).flatten()
        a = repeat(arange(t.size - 1), 4)
        b = tile(arange(4), t.size - 1)
        c = repeat(index // dim, vec.size)
        d = repeat(index % dim, vec.size)
        constMatrix[a, b, c, d] = vec

    apply(updateConst, arange(X.shape[1]))
    return constMatrix


def fillAnimationFrames(keyFrameData, interpolateMode='spline'):
    givenFrames = list(keyFrameData.keys())
    firstFrame = min(givenFrames)
    lastFrame = max(givenFrames)
    noOfFrames = lastFrame - firstFrame + 1
    mustBe = linspace(firstFrame, lastFrame, noOfFrames).astype(int)
    missing = setdiff1d(mustBe, givenFrames)
    # missing = mustBe[apply(lambda x: x not in givenFrames,mustBe)]
    if interpolateMode == 'linear':
        apply(lambda x: interpolateFramesLinear(keyFrameData, givenFrames, x),
              missing)
    elif interpolateMode == 'lagrange':
        apply(
            lambda x: interpolateFramesLagrange(keyFrameData, givenFrames, x),
            missing)
    elif interpolateMode == 'spline':
        constants = generateSplineConstants(keyFrameData, givenFrames)
        apply(
            lambda x: interpolateFramesNatSpline(constants, keyFrameData,
                                                 givenFrames, x), missing)
    else:
        raise TypeError(f'{interpolateMode} is not defined yet.')


def defaultKeyFrameStructures(keyFrames, defaultStructure):
    keyFrameStructures = {}

    def assign(t):
        segments = apply(lambda x: x.copy(), defaultStructure['segments'])
        supports = apply(lambda x: x.copy(), defaultStructure['supports'])
        loads = apply(lambda x: x.copy(), defaultStructure['loads'])
        keyFrameStructures[t] = {
            'segments': segments,
            'supports': supports,
            'loads': loads
        }

    apply(assign, keyFrames)
    return keyFrameStructures


def updateKeyFrameStructures(keyFrame, keyFrameLoads, keyFrameStructures):
    keyFrameStructures[keyFrame]['loads'] = keyFrameLoads


def interpolateLoads(keyFrameStructures, interpolateMode='spline', dim=3):
    loadData = {}
    keys = list(keyFrameStructures.keys())

    def assignLoadData(key):
        loadData[key] = array([
            hstack(array([x['P1'], x['P3'], x['peak']], dtype='object'))
            for x in keyFrameStructures[key]['loads']
        ])

    apply(assignLoadData, keys)
    fillAnimationFrames(loadData, interpolateMode)
    keys2 = list(loadData.keys())
    toReturn = defaultKeyFrameStructures(keys2, keyFrameStructures[keys[0]])

    def assignBack(key):

        def jpt(x):
            t = toReturn[key]['loads'][x]
            t['P1'] = loadData[key][x][:dim]
            t['P3'] = loadData[key][x][dim:2 * dim]
            t['peak'] = loadData[key][x][-1]

        apply(jpt, arange(toReturn[key]['loads'].size))

    apply(assignBack, keys2)
    return toReturn


def timeGraphData(segmentId, segment, keyFrameData, zoomFactor):
    segmentKeyFrameData = {
        x[0]: x[1][0 if segmentId ==
                   0 else nanRows(x[1])[segmentId -
                                        1]:nanRows(x[1])[segmentId]][1:-1,
                                                                     1:-1]
        for x in keyFrameData.items()
    }
    segment = convertTo3D(segment)
    A = segment['P1']
    B = segment['P3']

    def e(x):
        return segEqn(segment['type'], A, B, x, segment['P2'])

    def x(pt):
        return dot(array([0, *pt]) - A, unit(B - A))

    ts = list(segmentKeyFrameData.keys())
    xs = [x(pt) for pt in segmentKeyFrameData[ts[0]]]
    ts.sort()
    xs.sort()

    def getData(t, x):
        segData = segmentKeyFrameData[t]
        i = xs.index(x)
        return round(
            dot(
                array([0, *segData[i]]) - e(x),
                cross(segment['axisVector'], unit(B - A))), 10) / zoomFactor

    data = {
        x: vstack((array([0, 0]), apply(lambda t: array([t, getData(t, x)]),
                                        ts), array([ts[-1], 0]), array([0,
                                                                        0])))
        for x in xs
    }
    return data
