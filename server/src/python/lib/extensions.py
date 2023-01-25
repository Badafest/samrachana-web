from numpy import array, linspace, arange, repeat, tile, hstack, vstack, savetxt, zeros, dot, sort, unique, max, cos, sin, sqrt, around
from numpy.linalg import norm
from lib.functionDefinitions import apply, unit, identicalObjects, structify, convertTo3D, tolClose
from lib.segmentMethods import segEqn, arcLength, quadLength, arcEqn, quadEqn
from lib.numbaFunctions import arcSecTheta, quadSecTheta


def snap2seg(segment, point):
    x = dot(point - segment['P1'], unit(segment['P3'] - segment['P1']))
    if x < 0:
        x = 0
    elif x > norm(segment['P3'] - segment['P1']):
        x = norm(segment['P3'] - segment['P1'])

    def e(x):
        return segEqn(segment['type'], segment['P1'], segment['P3'], x,
                      segment['P2'])

    return e(x)


def snap2seg2(segment, point):
    segment = convertTo3D(segment)
    point = hstack((0, point))

    def e(x):
        return segEqn(segment['type'], segment['P1'], segment['P3'], x,
                      segment['P2'])

    x = dot(point - segment['P1'], unit(segment['P3'] - segment['P1']))
    if x < 0:
        x = 0
    elif x > norm(segment['P3'] - segment['P1']):
        x = norm(segment['P3'] - segment['P1'])
    return e(x)[1:3]


def convert(value,
            dim=[1, -2, 0],
            unitFrom=['SI', 1, 1, 'C'],
            unitTo=['ENG', 1, 1, 'C']):

    tempFac = lenFac = forFac = 1
    if (unitFrom[0] == 'SI'):
        if (unitTo[0] == 'ENG'):
            lenFac = 3.280839895013123
            forFac = 7.233013851209894
    else:
        if (unitTo[0] == 'SI'):
            lenFac = 0.3048
            forFac = 0.138254954376

    if (unitFrom[3] == 'C'):
        if (unitTo[3] == 'F'):
            tempFac = 9 / 5
    else:
        if (unitTo[3] == 'C'):
            tempFac = 5 / 9

    lenRatio = unitFrom[2] / unitTo[2]
    forRatio = unitFrom[1] / unitTo[1]

    return value * (lenRatio * lenFac)**dim[1] * (
        forRatio * forFac)**dim[0] * (tempFac)**dim[2]


def quadNodes(curve, fac=0.9995, nmax=8):
    P1 = curve['P1']
    P3 = curve['P3']
    P2 = curve['P2']
    l = norm(P3 - P1)
    # fv = P2-P1
    # xv = unit(P3-P1)
    # cp = dot(fv,xv)
    # sp = sqrt(norm(fv)**2-cp**2)
    # a2 = sp/(cp*(cp-l))
    # a1 = -a2*l
    s = quadLength(P1, P3, P2)
    lmin = fac * s
    xs = array([0, 0.5 * l])

    def e(x):
        return quadEqn(P1, P3, P2, x)

    n = 1
    pts = apply(e, xs)
    # u = lambda f: -1.61426137428768*f**(1/3)+2.57459479639732*f**(1/2)-0.0453371324721755*f
    # def midArcX(x1,x2):
    #     sMean = 0.5*(quadLength(P1,P3,P2,x1)+quadLength(P1,P3,P2,x2))
    #     fMean = sMean-quadLength(P1,P3,P2,l/2)
    #     uMean = u(fMean*2*a2)
    #     xMean = 0.5*(uMean-a1)/a2
    #     print(f'{round(a1,3)}\t{round(a2,3)}\t{round(fMean,3)}\t{round(uMean,3)}\t{round(xMean,3)}\t{round(quadLength(P1,P3,P2,xMean)/sMean,3)}\n')
    #     return xMean
    while (l <= lmin and n <= nmax):
        # mids = apply(lambda x: midArcX(xs[x],xs[x+1]), arange(xs.size-1))
        mids = apply(lambda x: 0.5 * (xs[x] + xs[x + 1]), arange(xs.size - 1))
        xs = sort(hstack((xs, mids)))
        n = mids.size
        pts = apply(e, xs)
        ls = apply(lambda x: norm(pts[x + 1] - pts[x]), arange(xs.size - 1))
        l = 2 * sum(ls)
    xs = unique(hstack((xs, norm(P3 - P1) - xs)))
    pts = apply(e, xs)[1:-1]
    return apply(
        lambda x: {
            'type': 'Node',
            'location': x,
            'settlement': zeros(6),
            'normal': array([0, 0, 1]),
            'class': 'support'
        }, pts)


def arcNodes(curve, fac=0.9995, nmax=8):
    P1 = curve['P1']
    P3 = curve['P3']
    P2 = curve['P2']
    s = arcLength(P1, P3, P2)
    l = norm(P3 - P1)
    lmin = fac * s
    xs = array([0, 0.5 * l])

    def e(x):
        return arcEqn(P1, P3, P2, x)

    n = 1
    pts = apply(e, xs)
    while (l <= lmin and n <= nmax):
        mids = apply(
            lambda x: 0.5 * (l - sqrt(
                (l - xs[x]) * (l - xs[x + 1])) + sqrt(xs[x] * xs[x + 1])),
            arange(xs.size - 1))
        # mids = apply(lambda x: 0.5*(xs[x]+xs[x+1]),arange(xs.size-1))
        xs = sort(hstack((xs, mids)))
        n = mids.size
        pts = apply(e, xs)
        ls = apply(lambda x: norm(pts[x + 1] - pts[x]), arange(xs.size - 1))
        l = 2 * sum(ls)
    xs = unique(hstack((xs, norm(P3 - P1) - xs)))
    pts = apply(e, xs)[1:-1]
    return apply(
        lambda x: {
            'type': 'Node',
            'location': x,
            'settlement': zeros(6),
            'normal': array([0, 0, 1]),
            'class': 'support'
        }, pts)


def changeParent(l):
    l[0]['parentSegment'] = l[1]


def breakLoad(load, points, segments):

    ps = load['parentSegment']
    n = load['degree']

    xStart = points[0]
    xEnd = points[-1]
    a = load['peak'] / (xEnd - xStart)**n

    def X(x):
        return dot(x - ps['P1'], unit(ps['P3'] - ps['P1']))

    xSegs = apply(lambda x: X(x['P1']), segments)

    psIndex = apply(
        lambda y: int(max(((points[y] - xSegs) >= 0).nonzero()[0])),
        arange(points.size - 1))

    coords = apply(
        lambda x: segEqn(ps['type'], ps['P1'], ps['P3'], x, ps['P2']), points)

    udls = apply(
        lambda x: {
            'degree': 0,
            'parentSegment': segments[psIndex[x]],
            'P1': coords[x],
            'P3': coords[x + 1],
            'normal': load['normal'],
            'peak': a * (points[x] - xStart)**n,
            'class': 'load'
        }, arange(points.size - 1))

    dls = apply(
        lambda x: {
            'degree': n,
            'parentSegment': segments[psIndex[x]],
            'P1': coords[x],
            'P3': coords[x + 1],
            'normal': load['normal'],
            'peak': a * ((points[x + 1] - xStart)**n -
                         (points[x] - xStart)**n),
            'class': 'load'
        }, arange(points.size - 1))

    dls = dls[apply(lambda dls: dls['peak'] != 0, dls)]
    return hstack((udls, dls))


def breakSegment(seg, points, loads=array([])):
    if (points.size == 0):
        return hstack((seg, loads))

    xs = unique(
        sort(
            apply(
                lambda loc: dot(loc - seg['P1'], unit(seg['P3'] - seg['P1'])),
                points)))
    xs = hstack((0, xs, norm(seg['P3'] - seg['P1'])))
    mids = apply(lambda x: 0.5 * (xs[x] + xs[x + 1]), arange(xs.size - 1))

    def e(x):
        return segEqn(seg['type'], seg['P1'], seg['P3'], x, seg['P2'])
    secTheta = (lambda x: arcSecTheta(seg['P1'], seg['P3'], seg['P2'], x)) if seg['type'] == 'arc' else \
        (lambda x: quadSecTheta(seg['P1'], seg['P3'],
         seg['P2'], x) if seg['type'] == 'quad' else 1)
    # secTheta = lambda x: 1
    segments = apply(
        lambda x: {
            'type': seg['type'],
            'P1': e(xs[x]),
            'P3': e(xs[x + 1]),
            'P2': e(mids[x]),
            'youngsModulus': seg['youngsModulus'],
            'shearModulus': seg['shearModulus'],
            'area': seg['area'] * secTheta(mids[x]),
            'Iyy': seg['Iyy'] * secTheta(mids[x]),
            'Izz': seg['Izz'] * secTheta(mids[x]),
            'J': seg['J'] * secTheta(mids[x]),
            'shapeFactor': seg['shapeFactor'],
            'axisVector': seg['axisVector'],
            'class': 'segment',
            'parent': seg.copy()
        }, arange(xs.size - 1))

    if (loads.size == 0):
        return hstack((segments, loads))

    # tempLoads = loads[apply(lambda loads: loads['degree']==-3,loads)]
    pointLoads = loads[apply(lambda loads: loads['degree'] < 0, loads)]
    distLoads = loads[apply(lambda loads: loads['degree'] >= 0, loads)]

    # if tempLoads.size!=0:
    #     tempLoadList = apply(lambda x: repeat(x,len(segments)),tempLoads)
    #     tempLoadList = hstack((apply(lambda y: \
    #         apply(lambda x: changeParent([y[x],segments[x]]),range(len(segments))),\
    #             tempLoadList)))

    if (pointLoads.size != 0):
        ts = apply(
            lambda x: dot(x['P1'] - seg['P1'], unit(seg['P3'] - seg['P1'])),
            pointLoads)
        index = apply(
            lambda x: max(
                hstack((0, *(around(x - xs[:-1], 10) > 0).nonzero()[0]))), ts)
        apply(
            changeParent,
            apply(lambda x: [pointLoads[x], segments[index[x]]],
                  arange(index.size)))

    if (distLoads.size != 0):
        ts = apply(
            lambda x: array([
                dot(x['P1'] - seg['P1'], unit(seg['P3'] - seg['P1'])),
                dot(x['P3'] - seg['P1'], unit(seg['P3'] - seg['P1']))
            ]), distLoads)
        index = apply(
            lambda ts: array([
                min((around(xs - ts[0], 10) > 0).nonzero()[0]) - 1,
                min((around(xs - ts[1], 10) >= 0).nonzero()[0]) - 1
            ]), ts)
        goodIndex = apply(lambda x: x[0] == x[1], index).nonzero()[0]
        badIndex = apply(lambda x: x[0] != x[1], index).nonzero()[0]

        goodDists = distLoads[goodIndex]
        badDists = distLoads[badIndex]

        if (goodIndex.size != 0):
            goodIndex = apply(lambda x: index[x][0], goodIndex)
            apply(
                changeParent,
                apply(lambda x: [goodDists[x], segments[goodIndex[x]]],
                      arange(goodIndex.size)))

        if (badIndex.size != 0):
            badTs = ts[badIndex]
            badXs = apply(
                lambda x: unique(
                    sort(
                        hstack((x, xs[apply(
                            lambda xs: xs >= x[0] and xs <= x[1], xs)])))),
                badTs)
            badDists = apply(
                lambda x: breakLoad(badDists[x], badXs[x], segments),
                arange(badIndex.size)).flatten()

        distLoads = hstack((goodDists, badDists))

    loads = hstack((pointLoads, distLoads))
    loads = loads[apply(lambda loads: type(loads) == dict, loads)].flatten()

    return hstack((segments, loads))


def childOf(seg, simFrame):
    segments = simFrame['segments']
    return segments[array([
        identicalObjects(
            seg, x['parent'] if
            (x['parent'] != None and x['parent'] != "None") else x)
        for x in segments
    ]).nonzero()[0]]


def simplify(str, simFac=0.9995):
    segments = apply(lambda t: t.copy(), str['segments'])
    supports = apply(lambda t: t.copy(), str['supports'])
    loads = apply(lambda t: t.copy(), str['loads'])

    segNodes = apply(
        lambda x: [{
            'type': 'Node',
            'location': x['P1'],
            'settlement': zeros(6),
            'normal': array([0, 0, 1]),
            'class': 'support'
        }, {
            'type': 'Node',
            'location': x['P3'],
            'settlement': zeros(6),
            'normal': array([0, 0, 1]),
            'class': 'support'
        }], segments)
    supports = hstack((supports, hstack((segNodes))))

    arcCheck = apply(lambda seg: seg['type'] == 'arc', segments)
    if (arcCheck.any()):
        arcs = segments[arcCheck]
        arcnodes = hstack((apply(lambda x: arcNodes(x, simFac), arcs)))
        supports = hstack((supports, arcnodes))

    quadCheck = apply(lambda seg: seg['type'] == 'quad', segments)
    if (quadCheck.any()):
        quads = segments[quadCheck]
        quadnodes = hstack((apply(lambda x: quadNodes(x, simFac), quads)))
        supports = hstack((supports, quadnodes))

    def checkLoc(loc, seg):
        A, B = seg['P1'], seg['P3']
        if norm(loc - A) < norm(B - A) and norm(loc - B) < norm(B - A):
            return tolClose(
                loc,
                segEqn(seg['type'], seg['P1'], seg['P3'],
                       dot(loc - seg['P1'], unit(seg['P3'] - seg['P1'])),
                       seg['P2']))
        else:
            return False

    # check = apply(lambda sp:
    #                 apply(lambda seg:
    #                         not tolClose(sp['location'],seg['P1']) and not tolClose(sp['location'],seg['P3']),
    #                                 segments).all(),supports)

    check = apply(
        lambda sp: apply(lambda seg: checkLoc(sp['location'], seg), segments).
        any(), supports)

    if (not check.any()):
        return str

    badSps = supports[check]
    locations = apply(lambda x: x['location'], badSps)

    check2 = apply(
        lambda seg: apply(lambda loc: checkLoc(loc, seg), locations), segments)
    breakMatrix = apply(lambda x: apply(lambda y: y['location'], x),
                        apply(lambda x: badSps[x], check2))

    def segLoads(seg):
        return loads[apply(lambda x: identicalObjects(x['parentSegment'], seg),
                           loads)]

    elements = apply(
        lambda x: breakSegment(segments[x], breakMatrix[x],
                               segLoads(segments[x])), arange(segments.size))
    elements = hstack((supports, hstack((elements))))
    return structify(elements)


def generate3d(buildingDimension=array([2, 3, 4]),
               roomDimension=array([5, 4, 3]),
               XbeamProp=array([1, 1, 1, 1, 1, 1, 1.5]),
               YbeamProp=array([1, 1, 1, 1, 1, 1, 1.5]),
               columnProp=array([1, 1, 1, 1, 1, 1, 1.5]),
               add=False,
               origin=array([0, 0, 0]),
               support=True,
               name='3dFrame-'):

    origin = origin.astype(float)
    height = roomDimension[2]
    length = roomDimension[1]
    breadth = roomDimension[0]

    noOfFloors = buildingDimension[2] + 1
    noOflongs = buildingDimension[1]
    noOfwides = buildingDimension[0]

    x = linspace(0, noOflongs * length, noOflongs + 1)
    y = linspace(0, noOfwides * breadth, noOfwides + 1)

    noOfPoints = (noOflongs + 1) * (noOfwides + 1)
    firstFloorXbeams = apply(lambda yy: apply(lambda xx: array([xx, yy]), x),
                             y).reshape((noOfPoints, 2))
    firstFloorYbeams = apply(lambda yy: apply(lambda xx: array([yy, xx]), y),
                             x).reshape((noOfPoints, 2))

    notX = arange(noOflongs, (noOfwides + 1) * noOflongs + 1,
                  noOflongs) + arange(noOfwides + 1)
    indexX = arange(noOfPoints)
    indexX = indexX[apply(lambda x: x not in notX, indexX)]

    notY = arange(noOfwides, (noOflongs + 1) * noOfwides + 1,
                  noOfwides) + arange(noOflongs + 1)
    indexY = arange(noOfPoints)
    indexY = indexY[apply(lambda x: x not in notY, indexY)]

    firstFloorX2d = apply(
        lambda x: array([firstFloorXbeams[x, ], firstFloorXbeams[x + 1, ]]).
        flatten(), indexX)
    firstFloorY2d = apply(
        lambda x: array([firstFloorYbeams[x, ], firstFloorYbeams[x + 1, ]]).
        flatten(), indexY)
    X2d = tile(firstFloorX2d, (noOfFloors, 1))
    Y2d = tile(firstFloorY2d, (noOfFloors, 1))

    heightsX = repeat(arange(0, noOfFloors * height, height),
                      firstFloorX2d.shape[0]).reshape(
                          (noOfFloors * firstFloorX2d.shape[0], 1))
    heightsY = repeat(arange(0, noOfFloors * height, height),
                      firstFloorY2d.shape[0]).reshape(
                          (noOfFloors * firstFloorY2d.shape[0], 1))
    X3d = hstack(
        (X2d[:, 0:2], heightsX, X2d[:, 2:4], heightsX)) + tile(origin, 2)
    Y3d = hstack(
        (Y2d[:, 0:2], heightsY, Y2d[:, 2:4], heightsY)) + tile(origin, 2)

    heightsZ = tile(arange(0, noOfFloors * height, height),
                    (noOfPoints, 1)).reshape((noOfFloors * noOfPoints, 1))
    Z2d = repeat(firstFloorYbeams, noOfFloors, axis=0)
    Zpoints = hstack((Z2d, heightsZ))

    notZ = arange(noOfFloors - 1, noOfFloors * noOfPoints, noOfFloors)
    indexZ = arange(noOfFloors * noOfPoints)
    indexZ = indexZ[apply(lambda x: x not in notZ, indexZ)]

    Z3d = apply(lambda x: array([Zpoints[x, ], Zpoints[x + 1, ]]).flatten(),
                indexZ) + tile(origin, 2)

    if (add):
        X3d = X3d[noOflongs * (noOfwides + 1):X3d.shape[0]]
        Y3d = Y3d[noOfwides * (noOflongs + 1):Y3d.shape[0]]

    beamsX = apply(
        lambda x: '"' + str({
            'type': 'line',
            'P1': X3d[x][0:3],
            'P3': X3d[x][3:6],
            'P2': 0.5 * (X3d[x][0:3] + X3d[x][3:6]),
            'youngsModulus': XbeamProp[0],
            'shearModulus': XbeamProp[1],
            'area': XbeamProp[2],
            'Iyy': XbeamProp[3],
            'Izz': XbeamProp[4],
            'J': XbeamProp[5],
            'shapeFactor': XbeamProp[6],
            'axisVector': array([0, 1, 0]),
            'class': 'segment'
        }) + '"', arange(X3d.shape[0]))

    beamsY = apply(
        lambda x: '"' + str({
            'type': 'line',
            'P1': Y3d[x][0:3],
            'P3': Y3d[x][3:6],
            'P2': 0.5 * (Y3d[x][0:3] + Y3d[x][3:6]),
            'youngsModulus': YbeamProp[0],
            'shearModulus': YbeamProp[1],
            'area': YbeamProp[2],
            'Iyy': YbeamProp[3],
            'Izz': YbeamProp[4],
            'J': YbeamProp[5],
            'shapeFactor': YbeamProp[6],
            'axisVector': array([1, 0, 0]),
            'class': 'segment'
        }) + '"', arange(Y3d.shape[0]))

    column = apply(
        lambda x: '"' + str({
            'type': 'line',
            'P1': Z3d[x][0:3],
            'P3': Z3d[x][3:6],
            'P2': 0.5 * (Z3d[x][0:3] + Z3d[x][3:6]),
            'youngsModulus': columnProp[0],
            'shearModulus': columnProp[1],
            'area': columnProp[2],
            'Iyy': columnProp[3],
            'Izz': columnProp[4],
            'J': columnProp[5],
            'shapeFactor': columnProp[6],
            'axisVector': array([1, 0, 0]),
            'class': 'segment'
        }) + '"', arange(Z3d.shape[0]))

    def XName(x):
        X = str(int(x[0] / length))
        Y = str(int(x[1] / breadth))
        Z = str(int(x[2] / height))
        return 'X' + '-' + X + '-' + Y + '-' + Z

    namesX = apply(XName, X3d[:, 0:3])

    def YName(x):
        X = str(int(x[0] / length))
        Y = str(int(x[1] / breadth))
        Z = str(int(x[2] / height))
        return 'Y' + '-' + X + '-' + Y + '-' + Z

    namesY = apply(YName, Y3d[:, 0:3])

    def ZName(x):
        X = str(int(x[0] / length))
        Y = str(int(x[1] / breadth))
        Z = str(int(x[2] / height))
        return 'Z' + '-' + X + '-' + Y + '-' + Z

    namesZ = apply(ZName, Z3d[:, 0:3])

    XsegmentsList = apply(
        lambda x: array([x, namesX[x], 'segment', beamsX[x], 'True']),
        arange(X3d.shape[0]))
    YsegmentsList = apply(
        lambda x: array(
            [x + X3d.shape[0], namesY[x], 'segment', beamsY[x], 'True']),
        arange(Y3d.shape[0]))
    ZsegmentsList = apply(
        lambda x: array([
            x + X3d.shape[0] + Y3d.shape[0], namesZ[x], 'segment', column[x],
            'True'
        ]), arange(Z3d.shape[0]))

    segmentsList = vstack(
        (array(['', 'Name', 'Class', 'RObject',
                'Flag']), ZsegmentsList, YsegmentsList, XsegmentsList))

    if (support):
        supports = apply(
            lambda x: '"' + str({
                'type':
                'Fixed',
                'location':
                array([firstFloorXbeams[x][0], firstFloorXbeams[x][1], 0]),
                'settlement':
                zeros(6),
                'normal':
                array([0, 0, 1]),
                'class':
                'support'
            }) + '"', arange(noOfPoints))
        supportList = apply(
            lambda x: array([
                x + X3d.shape[0] + Y3d.shape[0] + Z3d.shape[0], 'Fixed-' + str(
                    x), 'support', supports[x], 'True'
            ]), arange(noOfPoints))
        segmentsList = vstack((segmentsList, supportList))

    fname = './sampleFiles/' + name + str(buildingDimension) + '.csv'
    savetxt(fname, segmentsList, '%s', ',', '\r', '', '', '', 'UTF')


def generate2d(frameDimension=array([2, 4]),
               elementDimension=array([5, 3]),
               beamProp=array([1, 1, 1, 1, 1, 1, 1.5]),
               columnProp=array([1, 1, 1, 1, 1, 1, 1.5]),
               add=True,
               origin=array([0, 0, 0]),
               support=True,
               name='2dFrame-'):
    origin = origin.astype(float)
    height = elementDimension[1]
    breadth = elementDimension[0]

    noOfFloors = frameDimension[1] + 1
    noOfwides = frameDimension[0]

    y = tile(linspace(0, noOfwides * breadth, noOfwides + 1), (noOfFloors, 1))
    beamsCoord1 = apply(
        lambda h: apply(lambda x: array([0, x, h * height]), y[
            h, arange(noOfwides)]), arange(noOfFloors))
    beamsCoord1 = beamsCoord1.flatten().reshape(
        (int(beamsCoord1.size / 3), 3)) + origin
    beamsCoord2 = apply(
        lambda h: apply(lambda x: array([0, x, h * height]), y[
            h, linspace(1, noOfwides, noOfwides, dtype=int)]),
        arange(noOfFloors))
    beamsCoord2 = beamsCoord2.flatten().reshape(
        (int(beamsCoord2.size / 3), 3)) + origin
    beamsCoord = hstack((beamsCoord1, beamsCoord2))

    z = tile(linspace(0, (noOfFloors - 1) * height, noOfFloors),
             (noOfwides + 1, 1))
    columnsCoord1 = apply(
        lambda h: apply(lambda x: array([0, h * breadth, x]), z[
            h, arange(noOfFloors - 1)]), arange(noOfwides + 1))
    columnsCoord1 = columnsCoord1.flatten().reshape(
        (int(columnsCoord1.size / 3), 3)) + origin
    columnsCoord2 = apply(
        lambda h: apply(
            lambda x: array([0, h * breadth, x]), z[
                h, linspace(1, noOfFloors - 1, noOfFloors - 1, dtype=int)]),
        arange(noOfwides + 1))
    columnsCoord2 = columnsCoord2.flatten().reshape(
        (int(columnsCoord2.size / 3), 3)) + origin
    columnsCoord = hstack((columnsCoord1, columnsCoord2))

    if (support):
        supports = apply(
            lambda x: '"' + str({
                'type': 'Fixed',
                'location': beamsCoord[x][0:3],
                'settlement': zeros(6),
                'normal': array([0, 0, 1]),
                'class': 'support'
            }) + '"', arange(noOfwides))
        supports = hstack((supports, '"' + str(
            {
                'type': 'Fixed',
                'location':
                beamsCoord[noOfwides - 1][0:3] + array([0, breadth, 0]),
                'settlement': zeros(6),
                'normal': array([0, 0, 1]),
                'class': 'support'
            }) + '"'))
        supportList = apply(
            lambda x: array([
                x + beamsCoord.shape[0] + columnsCoord.shape[0], 'Fixed-' +
                str(x), 'support', supports[x], 'True'
            ]), arange(noOfwides + 1))

    if (add):
        beamsCoord = beamsCoord[noOfwides:beamsCoord.shape[0]]

    beams = apply(
        lambda x: '"' + str(
            {
                'type': 'line',
                'P1': beamsCoord[x][0:3],
                'P3': beamsCoord[x][3:6],
                'P2': 0.5 * (beamsCoord[x][0:3] + beamsCoord[x][3:6]),
                'youngsModulus': beamProp[0],
                'shearModulus': beamProp[1],
                'area': beamProp[2],
                'Iyy': beamProp[3],
                'Izz': beamProp[4],
                'J': beamProp[5],
                'shapeFactor': beamProp[6],
                'axisVector': array([1, 0, 0]),
                'class': 'segment'
            }) + '"', arange(beamsCoord.shape[0]))

    columns = apply(
        lambda x: '"' + str(
            {
                'type': 'line',
                'P1': columnsCoord[x][0:3],
                'P3': columnsCoord[x][3:6],
                'P2': 0.5 * (columnsCoord[x][0:3] + columnsCoord[x][3:6]),
                'youngsModulus': columnProp[0],
                'shearModulus': columnProp[1],
                'area': columnProp[2],
                'Iyy': columnProp[3],
                'Izz': columnProp[4],
                'J': columnProp[5],
                'shapeFactor': columnProp[6],
                'axisVector': array([1, 0, 0]),
                'class': 'segment'
            }) + '"', arange(columnsCoord.shape[0]))

    def beamsName(x):
        Y = str(int(x[1] / breadth))
        Z = str(int(x[2] / height))
        return 'beam' + '-' + Y + '-' + Z

    namesBeam = apply(beamsName, beamsCoord[:, 0:3])

    def columnsName(x):
        Y = str(int(x[1] / breadth))
        Z = str(int(x[2] / height))
        return 'column' + '-' + Y + '-' + Z

    namesColumns = apply(columnsName, columnsCoord[:, 0:3])

    beamsList = apply(
        lambda x: array([x, namesBeam[x], 'segment', beams[x], 'True']),
        arange(beamsCoord.shape[0]))
    columnsList = apply(
        lambda x: array([
            x + beamsCoord.shape[0], namesColumns[x], 'segment', columns[x],
            'True'
        ]), arange(columnsCoord.shape[0]))

    segmentsList = vstack((array(['', 'Name', 'Class', 'RObject',
                                  'Flag']), columnsList, beamsList))

    if (support):
        segmentsList = vstack((segmentsList, supportList))
    fname = './sampleFiles/' + name + str(frameDimension) + '.csv'
    savetxt(fname, segmentsList, '%s', ',', '\r', '', '', '', 'UTF')


def transform(x, y, pan=array([0, 0]), zoom=1, rotate=0):
    rot = array([[cos(rotate), sin(rotate)], [-sin(rotate), cos(rotate)]])
    return rot @ (array([x, y]) - pan) / zoom
