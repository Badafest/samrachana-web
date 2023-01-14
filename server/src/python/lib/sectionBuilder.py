from lib.functionDefinitions import apply, rowPos, unit
from lib.segmentMethods import arcEqn, arcLength, quadEqn, quadLength
from numpy import array, vstack, sum, hstack, abs, arccos, append, arange, sort, min, max, unique, insert, sqrt, pi, cross, cos, sin, dot, log
from numpy.linalg import eig, norm


def breakArc(X, Z, Y, fac=0.9995):
    x = append(X, 0)
    z = append(Z, 0)
    y = append(Y, 0)
    def e(t): return arcEqn(x, z, y, t)[0:2]
    s = arcLength(x, z, y)
    l = norm(z-x)
    xs = array([0, l/2])
    pts = apply(e, xs)
    while (l <= fac*s):
        mids = apply(
            lambda x: 0.5*(l-sqrt((l-xs[x])*(l-xs[x+1]))+sqrt(xs[x]*xs[x+1])), arange(xs.size-1))
        # mids = apply(lambda x: 0.5*(xs[x]+xs[x+1]),arange(xs.size - 1))
        xs = sort(hstack((xs, mids)))
        pts = apply(e, xs)
        ls = apply(lambda x: norm(pts[x+1]-pts[x]), arange(xs.size-1))
        l = 2*sum(ls)
    xs = unique(hstack((xs, norm(z-x)-xs)))
    return apply(e, xs)


def breakQuad(X, Z, Y, fac=0.9995):
    x = append(X, 0)
    z = append(Z, 0)
    y = append(Y, 0)
    def e(t): return quadEqn(x, z, y, t)[0:2]
    s = quadLength(x, z, y)
    l = norm(z-x)
    xs = array([0, l/2])
    pts = apply(e, xs)
    # def midArcX(x1,x2):
    #     fv = y-x
    #     xv = unit(z-x)
    #     cp = dot(fv,xv)
    #     sp = sqrt(norm(fv)**2-cp**2)
    #     a2 = sp/(cp*(cp-l))
    #     a1 = -a2*l
    #     u = lambda f: -0.311*f**(1/3)+1.517*f**(1/2)-0.00037*f if f>0 else -u(-f)
    #     uMean = u(0.5*(quadLength(x,z,y,x1)+quadLength(x,z,y,x2))-quadLength(x,z,y,l/2))
    #     return 0.5*(uMean-a1)/a2
    while (l <= fac*s):
        # mids = apply(lambda x: midArcX(xs[x],xs[x+1]), arange(xs.size-1))
        mids = apply(lambda x: 0.5*(xs[x]+xs[x+1]), arange(xs.size-1))
        xs = sort(hstack((xs, mids)))
        pts = apply(e, xs)
        ls = apply(lambda x: norm(pts[x+1]-pts[x]), arange(xs.size-1))
        l = 2*sum(ls)
    xs = unique(hstack((xs, norm(z-x)-xs)))
    return apply(e, xs)


def lines(points): return hstack((points[0:-1], points[1:points.shape[0]]))


def del1(X): return X[0]*X[3]-X[1]*X[2]
def del2(X): return X[2]*X[3]-X[0]*X[1]
def del3(X): return X[0]*X[3]+X[1]*X[2]
def del4(X): return X[0]*X[1]+X[2]*X[3]


def I0(lines): return abs(0.5*sum(apply(del1, lines)))


def I1X(lines): return abs(
    (1/6)*sum(apply(lambda x: del1(x)*(x[0]+x[2]), lines)))


def I1Y(lines): return abs(
    (1/6)*sum(apply(lambda x: del1(x)*(x[1]+x[3]), lines)))


def I2X(lines): return abs(
    (1/12)*sum(apply(lambda x: (del1(x)+del2(x))*(x[0]**2+x[2]**2), lines)))


def I2Y(lines): return abs(
    (1/12)*sum(apply(lambda x: (del1(x)-del2(x))*(x[1]**2+x[3]**2), lines)))


def I1XY(lines): return abs((1/24)*sum(apply(lambda x: del1(x)
                                             * del3(x)+(2*del1(x)+3*del2(x))*del4(x), lines)))


def transformLine(X, e):
    T = array([[e[0], e[1]], [-e[1], e[0]]])
    zero = array([[0, 0], [0, 0]])
    T = vstack((hstack((T, zero)), hstack((zero, T))))
    return T @ X


def intersectionX(X, x=0):
    y = X[1]+((X[3]-X[1])/(X[2]-X[0]))*(x-X[0])
    return y if min([X[1], X[3]]) <= y <= max([X[1], X[3]]) else None


def intersectionY(X, y=0):
    x = X[0]+((X[2]-X[0])/(X[3]-X[1]))*(y-X[1])
    return x if min([X[0], X[2]]) <= x <= max([X[0], X[2]]) else None


def LR(X, x=0):
    if X[0] >= x and X[2] >= x:
        return 1
    elif (X[0]-x)*(X[2]-x) < 0:
        return 0
    else:
        return -1


def UD(X, y=0):
    if X[1] >= y and X[3] >= y:
        return 1
    elif (X[1]-y)*(X[3]-y) < 0:
        return 0
    else:
        return -1


def breakLinesX(lines, x=0):
    for X in lines:
        if (LR(X, x) == 0):
            index = rowPos(X, lines)+1
            lines = insert(lines, index, array(
                [x, intersectionX(X, x), X[2], X[3]]), 0)
            lines[index-1] = array([X[0], X[1], x, intersectionX(X, x)])

    left = apply(lambda X: LR(X, x) == -1, lines)
    right = apply(lambda X: LR(X, x) == 1, lines)

    return {'left': lines[left], 'right': lines[right]}


def breakLinesY(lines, y=0):
    for X in lines:
        if (UD(X, y) == 0):
            index = rowPos(X, lines)+1
            lines = insert(lines, index, array(
                [intersectionY(X, y), y, X[2], X[3]]), 0)
            lines[index-1] = array([X[0], X[1], intersectionY(X, y), y])

    down = apply(lambda X: UD(X, y) == -1, lines)
    up = apply(lambda X: UD(X, y) == 1, lines)
    return {'down': lines[down], 'up': lines[up]}


def xCalc(points):
    main = lines(points['main'])
    holes = apply(lines, points['holes']) if points['holes'].size != 0 else array(
        [array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])])

    area = I0(main) - sum(apply(I0, holes))
    Xbar = (I1X(main) - sum(apply(I1X, holes)))/area
    Ybar = (I1Y(main) - sum(apply(I1Y, holes)))/area

    Iyy = I2X(main) - sum(apply(I2X, holes))
    Ixx = I2Y(main) - sum(apply(I2Y, holes))
    Ixy = I1XY(main) - sum(apply(I1XY, holes))

    IgYY = Iyy - area*Xbar**2
    IgXX = Ixx - area*Ybar**2
    IgXY = Ixy - area*Xbar*Ybar

    I = eig(array([[IgXX, IgXY], [IgXY, IgYY]]))
    IXX = I[0][0]
    IYY = I[0][1]
    ex = I[1][0]
    ey = I[1][1]
    theta = arccos(ex[0])

    xMax = max(abs(apply(lambda x: x-Xbar, main[:, 0])))
    yMax = max(abs(apply(lambda x: x-Ybar, main[:, 1])))
    SXX = IXX/yMax
    SYY = IYY/xMax

    centroid = array([Xbar, Ybar])
    cenLine = array([Xbar, Ybar, Xbar, Ybar])
    mainStar = apply(lambda x: transformLine(x-cenLine, ex), main)
    holesStar = apply(lambda x: apply(
        lambda t: transformLine(t-cenLine, ex), x), holes)

    aerr = area
    xea = 0
    n = 0

    while abs(aerr) >= area*(1e-4) and n <= 25:
        mainBrokenX = breakLinesX(mainStar, xea)
        holesBrokenX = apply(lambda lines: breakLinesX(lines, xea), holesStar)
        leftArea = I0(
            mainBrokenX['left']) - sum(apply(lambda lines: I0(lines['left']), holesBrokenX))
        rightArea = I0(
            mainBrokenX['right']) - sum(apply(lambda lines: I0(lines['right']), holesBrokenX))
        aerr = rightArea - leftArea
        # ys = mainBrokenX['right'][:,1]
        # intercept = max(ys)-min(ys)
        xea = xea + aerr*xMax/area
        n = n+1

    aerr = area
    yea = 0
    n = 0

    while abs(aerr) >= area*(1e-4) and n <= 25:
        mainBrokenY = breakLinesY(mainStar, yea)
        holesBrokenY = apply(lambda lines: breakLinesY(lines, yea), holesStar)
        downArea = I0(
            mainBrokenY['down']) - sum(apply(lambda lines: I0(lines['down']), holesBrokenY))
        upArea = I0(mainBrokenY['up']) - \
            sum(apply(lambda lines: I0(lines['up']), holesBrokenY))
        aerr = upArea - downArea
        # xs = mainBrokenY['up'][:,0]
        # intercept = max(xs)-min(xs)
        yea = yea + aerr*yMax/area
        n = n+1

    ZYY1 = I1X(mainBrokenX['left']) - \
        sum(apply(lambda lines: I1X(
            lines['left']), holesBrokenX)) - xea*leftArea
    ZYY2 = I1X(mainBrokenX['right']) - sum(
        apply(lambda lines: I1X(lines['right']), holesBrokenX)) - xea*rightArea
    ZXX1 = I1Y(mainBrokenY['down']) - \
        sum(apply(lambda lines: I1Y(
            lines['down']), holesBrokenY)) - yea*downArea
    ZXX2 = I1Y(mainBrokenY['up']) - \
        sum(apply(lambda lines: I1Y(lines['up']), holesBrokenY)) - yea*upArea

    ZXX = abs(ZXX1) + abs(ZXX2)
    ZYY = abs(ZYY1) + abs(ZYY2)

    kx = ZXX/SXX
    ky = ZYY/SYY

    k = min([kx, ky])

    return {'area': area,
            'centroid': centroid,
            'IgXX': IgXX,
            'IgYY': IgYY,
            'IgXY': IgXY,
            'IXX': IXX,
            'IYY': IYY,
            'IZZ': IXX+IYY,
            'rx': sqrt(IXX/area),
            'ry': sqrt(IYY/area),
            'r': sqrt(min([IXX, IYY])/area),
            'ex': ex,
            'ey': ey,
            'thetaX': (theta*180)/pi,
            'SXX': SXX,
            'SYY': SYY,
            'xea': xea,
            'yea': yea,
            'ZXX': ZXX,
            'ZYY': ZYY,
            'kx': kx,
            'ky': ky,
            'k': k}


def assign(segment, secData, alpha=0):
    xv = unit(segment['P3']-segment['P1'])

    if ((xv == 1).any()):
        if (xv[0] == 1):
            iv = array([0, 1, 0])
        else:
            iv = array([1, 0, 0])
    else:
        iv = unit(array([0.5*xv[1]*xv[2], -xv[0]*xv[2], 0.5*xv[0]*xv[1]]))

    jv = unit(cross(xv, iv))

    iv = iv*cos(alpha) + jv*sin(alpha)
    jv = unit(cross(xv, iv))

    av = iv*secData['ex'][0]+jv*secData['ex'][1]

    segment['area'] = secData['area']
    segment['Iyy'] = secData['IXX']
    segment['Izz'] = secData['IYY']
    segment['J'] = secData['IZZ']
    segment['shapeFactor'] = array([secData['kx'], secData['ky']])
    segment['axisVector'] = av


def xAssign(segments, secData, alpha=0):
    apply(lambda seg: assign(seg, secData, alpha), segments)
