# from sympy import Matrix
from time import time
from warnings import warn

from numpy import (arange, array, asarray, diag, hstack, int, matmul, max,
                   repeat, shape, sort, tile, unique, vstack, zeros, mean)
from numpy.linalg import det, inv, norm

from lib.extensions import childOf, simplify
from lib.functionDefinitions import apply, dictInArr, rowPos, tolClose, unit
from lib.loadMethods import lineGlobalFEA
# from lib.numbaFunctions import lineTempGlobalFEA
from lib.segmentMethods import (lineStiffnessGlobal, lineStiffnessGlobal2,
                                lineStiffnessGlobalTruss,
                                lineStiffnessGlobalTruss2, lineStiffnessLocal,
                                lineStiffnessLocal2, lineStiffnessLocalTruss,
                                lineTransformation, lineTransformation2,
                                lineTransformationTruss,
                                lineTransformationTruss2)
from lib.supportMethods import rxn


def sortXY(mat):
    temp = unique(mat, axis=0)
    xs = unique(temp[:, 0])
    ys = array([temp[:, 1][t] for t in [(temp[:, 0] == xs[q]).nonzero()[0]
               for q in range(xs.shape[0])]])
    sortSign = array([(-1)**x for x in range(xs.shape[0])])
    Ys = []
    [Ys.extend(sortSign[t]*sort(sortSign[t]*ys[t]))
     for t in range(xs.shape[0])]
    temp[:, 1] = Ys
    return temp


def sortYZ(mat):
    mat = unique(mat, axis=0)
    a = mat[:, 1:]
    b = sortXY(a)
    i = [a.tolist().index(x) for x in b.tolist()]
    x = mat[:, 0][i]
    return hstack((vstack(x), b))


def frame3d(struct, shear=False, inextensible=True, simplified=True):
    t1 = time()
    segmentsOrg = struct['segments']

    nodes = apply(lambda x: array([x['P1'], x['P3']]), segmentsOrg)
    # nodesOrg = unique(nodes.reshape(nodes.shape[0]*nodes.shape[1],3),axis=0)
    nodesOrg = sortYZ(nodes.reshape(nodes.shape[0]*nodes.shape[1], 3))

    structure = simplify(struct) if simplified else struct
    segments = structure['segments']
    loads = structure['loads']
    supports = structure['supports']

    nodes = apply(lambda x: array([x['P1'], x['P3']]), segments)
    # nodes = unique(nodes.reshape(nodes.shape[0]*nodes.shape[1],3),axis=0)
    nodes = sortYZ(nodes.reshape(nodes.shape[0]*nodes.shape[1], 3))

    def filter1(x): return apply(
        lambda t: tolClose(t['location'], x['P1']), supports)

    def filter2(x): return apply(
        lambda t: tolClose(t['location'], x['P3']), supports)

    suspects = supports[apply(lambda x: x['type'] ==
                              'Internal Hinge', supports)]

    def hinged(seg):
        if (suspects.size == 0):
            return False
        else:
            hinged = True if any(apply(lambda x: tolClose(
                x['location'], seg['P3']), suspects)) else False
            return hinged

    def filter(x):
        if type(rowPos(x['location'], nodes)) != type(False):
            return rowPos(x['location'], nodes)

    def z1(seg):
        sps = supports[filter1(seg)]
        sps = sps[apply(lambda x: x['type'] != 'Node', sps)
                  ] if sps.size != 0 else sps
        normals = apply(lambda x: x['normal'], sps) if sps.size != 0 else array(
            [array([0, 0, 1])])
        normal = unit(sum(normals, 0))
        if normals.shape[0] > 1:
            warn(f'{normals.shape[0]} normals are resolved to: {normal}')
        return normal

    def z2(seg):
        sps = supports[filter2(seg)]
        sps = sps[apply(lambda x: x['type'] != 'Node', sps)
                  ] if sps.size != 0 else sps
        normals = apply(lambda x: x['normal'], sps) if sps.size != 0 else array(
            [array([0, 0, 1])])
        normal = unit(sum(normals, 0))
        if normals.shape[0] > 1:
            warn(f'{normals.shape[0]} normals are resolved to: {normal}')
        return normal

    start = apply(lambda x: rowPos(x, nodes),
                  apply(lambda x: x['P1'], segments))
    stops = apply(lambda x: rowPos(x, nodes),
                  apply(lambda x: x['P3'], segments))
    memberLocation = vstack((start, stops)).T

    locationMatrix = zeros(6*shape(nodes)[0]).reshape(shape(nodes)[0], 6)

    supports = supports[apply(lambda x: filter(x) != None, supports)]
    if (supports.size == 0):
        raise KeyError('No valid support found in the structure')
    b = apply(filter, supports)
    spfilter = b
    c = apply(lambda x: supports[x], apply(lambda t: b == t, b))
    a = apply(lambda x: sum(apply(lambda y: rxn(y['type']), x)), c)
    locationMatrix[b.astype(int)] = a
    b = locationMatrix.reshape(-1)
    b[b != 0] = -1
    c = asarray(b == 0).nonzero()[0]
    b[c] = (arange(c.size))+1
    b[b == -1] = 0

    jLoadMatrix = zeros(6*shape(nodes)[0]).reshape(shape(nodes)[0], 6)
    jforce = loads[apply(lambda x: x['degree'] == -
                         1 and type(rowPos(x['P1'], nodes)) != type(False), loads)]
    jmomnt = loads[apply(lambda x: x['degree'] == -
                         2 and type(rowPos(x['P1'], nodes)) != type(False), loads)]

    for x in jforce:
        jLoadMatrix[rowPos(x['P1'], nodes), 0:3] += x['peak']*x['normal']
    for x in jmomnt:
        jLoadMatrix[rowPos(x['P1'], nodes), 3:6] += x['peak']*x['normal']

    memLoadMatrix = zeros(12*shape(memberLocation)
                          [0]).reshape(shape(memberLocation)[0], 12)
    jlods = hstack((jforce, jmomnt))
    memloads = loads[apply(lambda x: x['degree'] >= 0 or type(
        rowPos(x['P1'], nodes)) == type(False), loads)]

    memloads = memloads if memloads.size != 0 else array([{'degree': 0,
                                                           'parentSegment': segments[0],
                                                           'P1': segments[0]['P1'],
                                                           'P3': segments[0]['P3'],
                                                           'normal': array([0, 0, 1]),
                                                           'peak': 0,
                                                           'class': 'load'}])
    for x in memloads:
        memLoadMatrix[dictInArr(x['parentSegment'], segments)] += lineGlobalFEA(x['parentSegment']['P1'],
                                                                                x['parentSegment']['P3'], x['P1'], x['P3'], z1(
                                                                                    x), z2(x), x['degree'], x['peak'],
                                                                                x['parentSegment']['axisVector'], x['normal'], hinged(x['parentSegment']))

    settlements = apply(lambda t: t['settlement'], supports)
    if unique(settlements).any():
        def add(x):
            K = lineStiffnessLocal(x['youngsModulus'], x['Iyy'], x['Izz'], norm(
                x['P3']-x['P1']), x['area'], x['shearModulus'], x['J'], shear, inextensible, hinged(x))
            T = lineTransformation(
                x['P1'], x['P3'], x['axisVector'], z1(x), z2(x))
            settlement1 = sum(apply(lambda t: t['settlement'], supports[filter1(
                x)]), 0) if filter1(x).any() else zeros(6)
            settlement2 = sum(apply(lambda t: t['settlement'], supports[filter2(
                x)]), 0) if filter2(x).any() else zeros(6)
            settlements = hstack((settlement1, settlement2))
            FEAs = T.T @ (K @ (T @ settlements)
                          ) if settlements.any() else zeros(12)
            return FEAs

        memLoadMatrix += apply(add, segments)

    mLoadMatrix = zeros(6*shape(nodes)[0]).reshape(shape(nodes)[0], 6)
    for x in arange(segments.size):
        mLoadMatrix[memberLocation[x][0]] += memLoadMatrix[x][0:6]
        mLoadMatrix[memberLocation[x][1]] += memLoadMatrix[x][6:12]

    locvec = (locationMatrix.flatten() > 0).nonzero()[0]
    superFEA = mLoadMatrix.flatten()[locvec]

    superStiffness = diag(zeros(max(locationMatrix).astype(int)))

    for id in arange(segments.size):
        x = segments[id]
        nj = memberLocation[id, 0]
        nk = memberLocation[id, 1]
        vec = array([locationMatrix[nj], locationMatrix[nk]]
                    ).astype(int).flatten()
        sel = (vec > 0).nonzero()[0]
        superStiffness[repeat(vec[sel]-1, sel.size), tile(vec[sel]-1, sel.size)] += lineStiffnessGlobal(x['P1'], x['P3'], x['axisVector'], z1(x), z2(x), x['youngsModulus'],
                                                                                                        x['Iyy'], x['Izz'], norm(x['P3']-x['P1']), x['area'], x['shearModulus'], x['J'], shear, inextensible, hinged(x))[repeat(sel, sel.size), tile(sel, sel.size)]

    if not det(superStiffness/mean(superStifnness)):
        raise ValueError('Global Stiffness Matrix has zero determinant')

    superJload = zeros(max(locationMatrix).astype(int))

    for i in arange(shape(nodes)[0]):
        vec = locationMatrix[i].astype(int)
        sel = (vec > 0).nonzero()[0]
        superJload[vec[sel]-1] += jLoadMatrix[i, sel]

    deflections = matmul(inv(superStiffness), superJload -
                         superFEA) if superStiffness.size != 0 else 0

    locvec = locationMatrix.flatten().astype(int)

    responses = apply(
        lambda x: deflections[x-1] if x != 0 else 0, locvec).reshape((shape(nodes)[0], 6))
    responses = responses.astype(float)

    a = apply(lambda x: x['settlement'], supports)
    responses[spfilter.astype(int)] += a.astype(float)

    responsesRaw = hstack((nodes, responses))

    responses = responsesRaw[apply(lambda x: type(
        rowPos(x, nodesOrg)) != type(False), nodes)]

    actionsRaw = zeros((segments.size*2, 9))
    actions = zeros((segmentsOrg.size*2, 9))

    for id in arange(segments.size):
        x = segments[id]
        nj = memberLocation[id, 0]
        nk = memberLocation[id, 1]
        vec = array([locationMatrix[nj], locationMatrix[nk]]
                    ).astype(int).flatten()
        actions[2*id, 0:3] = nodes[nj]
        actions[2*id+1, 0:3] = nodes[nk]
        globalDeflections = apply(
            lambda x: deflections[x-1] if x != 0 else x, vec)
        memLoad = lineTransformation(
            x['P1'], x['P3'], x['axisVector'], z1(x), z2(x)) @ memLoadMatrix[id]
        localDeflections = matmul(lineTransformation(
            x['P1'], x['P3'], x['axisVector'], z1(x), z2(x)), globalDeflections)
        localActions = matmul(lineStiffnessLocal(x['youngsModulus'], x['Iyy'], x['Izz'], norm(x['P3']-x['P1']),
                                                 x['area'], x['shearModulus'], x['J'], shear, inextensible, hinged(x)), localDeflections)+memLoad
        actions[2*id, 3:9] = localActions[0:6]
        actions[2*id+1, 3:9] = -localActions[6:12]

    for i in arange(segmentsOrg.size):
        for x in childOf(segmentsOrg[i], structure):
            id = dictInArr(x, segments)
            if x['parent'] == None:
                actions[2*i], actions[2*i +
                                      1] = actionsRaw[2*id], actionsRaw[2*id+1]
            else:
                if all(x['P1'] == x['parent']['P1']):
                    actions[2*i] = actionsRaw[2*id]
                elif all(x['P3'] == x['parent']['P3']):
                    actions[2*i+1] = actionsRaw[2*id+1]
                else:
                    pass
    # actionsRaw = actions
    # actions = actionsRaw[apply(lambda x: type(rowPos(x[0:3],nodesOrg))!=type(False),actionsRaw)]

    multiplier = array([[1, 1, 1, 1, 1, 1], [-1, -1, -1, -1, -1, -1]])

    def globalActions(index): return multiplier*(lineTransformation(segments[index]['P1'], segments[index]['P3'], segments[index]['axisVector'], z1(
        segments[index]), z2(segments[index])).T @ hstack(actionsRaw[(2*index):(2*index+2), 3:])).reshape((2, 6))
    reactionsRaw = hstack((actionsRaw[:, :3], vstack(
        apply(globalActions, arange(segments.size)))))
    reactions = reactionsRaw[apply(lambda x: type(
        rowPos(x[0:3], nodesOrg)) != type(False), reactionsRaw)]

    def addAllRxns(node): return sum(
        reactions[apply(lambda x: tolClose(node, x), reactions[:, :3]), 3:], 0)
    reactions = hstack((nodesOrg, apply(addAllRxns, nodesOrg)))

    t = time()-t1
    return ({'simplified': structure, 'responseRaw': responsesRaw, 'response': responses, 'actionRaw': actionsRaw, 'action': actions, 'memLoc': memberLocation, 'reactions': reactions, 'time': t})


def frame2d(struct, shear=False, inextensible=True, simplified=True, simFac=0.9995):
    t1 = time()
    segmentsOrg = struct['segments']
    nodes = apply(lambda x: array([x['P1'], x['P3']]), segmentsOrg)
    # nodesOrg = unique(nodes.reshape(nodes.shape[0]*nodes.shape[1],3),axis=0)
    nodesOrg = sortYZ(nodes.reshape(nodes.shape[0]*nodes.shape[1], 3))
    structure = simplify(struct, simFac) if simplified else struct
    segments = structure['segments']
    loads = structure['loads']
    supports = structure['supports']

    # print("Members = \n"+'\n\n'.join(str(x) for x in segments)+'\n********************\n')
    # print("Loads = \n"+'\n\n'.join(str(x) for x in struct['loads'])+'\n********************\n')
    # print("Supports = \n"+ '\n\n'.join(str(x) for x in struct['supports'])+'\n********************\n')
    nodes = apply(lambda x: array([x['P1'], x['P3']]), segments)
    # nodes = unique(nodes.reshape(nodes.shape[0]*nodes.shape[1],3),axis=0)
    nodes = sortYZ(nodes.reshape(nodes.shape[0]*nodes.shape[1], 3))

    def filter1(x): return apply(
        lambda t: tolClose(t['location'], x['P1']), supports)

    def filter2(x): return apply(
        lambda t: tolClose(t['location'], x['P3']), supports)

    suspects = supports[apply(lambda x: x['type'] ==
                              'Internal Hinge', supports)]

    def hinged(seg):
        if (suspects.size == 0):
            return False
        else:
            hinged = True if any(apply(lambda x: tolClose(
                x['location'], seg['P3']), suspects)) else False
            return hinged

    def filter(x):
        if type(rowPos(x['location'], nodes)) != type(False):
            return rowPos(x['location'], nodes)

    def z1(seg):
        sps = supports[filter1(seg)]
        sps = sps[apply(lambda x: x['type'] != 'Node', sps)
                  ] if sps.size != 0 else sps
        normals = apply(lambda x: x['normal'], sps) if sps.size != 0 else array(
            [array([0, 0, 1])])
        normal = unit(sum(normals, 0))
        if normals.shape[0] > 1:
            warn(f'{normals.shape[0]} normals are resolved to: {normal}')
        return normal

    def z2(seg):
        sps = supports[filter2(seg)]
        sps = sps[apply(lambda x: x['type'] != 'Node', sps)
                  ] if sps.size != 0 else sps
        normals = apply(lambda x: x['normal'], sps) if sps.size != 0 else array(
            [array([0, 0, 1])])
        normal = unit(sum(normals, 0))
        if normals.shape[0] > 1:
            warn(f'{normals.shape[0]} normals are resolved to: {normal}')
        return normal

    start = apply(lambda x: rowPos(x, nodes),
                  apply(lambda x: x['P1'], segments))
    stops = apply(lambda x: rowPos(x, nodes),
                  apply(lambda x: x['P3'], segments))
    memberLocation = vstack((start, stops)).T

    locationMatrix = zeros((shape(nodes)[0], 3))

    supports = supports[apply(lambda x: filter(x) != None, supports)]
    if (supports.size == 0):
        raise KeyError('No valid support found in the structure')

    b = apply(filter, supports)
    spfilter = b
    c = apply(lambda x: supports[x], apply(lambda t: b == t, b))
    a = apply(lambda x: sum(apply(lambda y: rxn(y['type'])[1:4], x)), c)
    locationMatrix[b.astype(int)] = a
    b = locationMatrix.reshape(-1)
    b[b != 0] = -1
    c = asarray(b == 0).nonzero()[0]
    b[c] = (arange(c.size))+1
    b[b == -1] = 0

    jLoadMatrix = zeros((shape(nodes)[0], 3))
    jforce = loads[apply(lambda x: x['degree'] == -
                         1 and type(rowPos(x['P1'], nodes)) != type(False), loads)]
    jmomnt = loads[apply(lambda x: x['degree'] == -
                         2 and type(rowPos(x['P1'], nodes)) != type(False), loads)]

    for x in jforce:
        jLoadMatrix[rowPos(x['P1'], nodes), 0:2] += x['peak'] * \
            x['normal'][[1, 2]]
    for x in jmomnt:
        jLoadMatrix[rowPos(x['P1'], nodes), 2] += x['peak']*x['normal'][0]

    memLoadMatrix = zeros((shape(memberLocation)[0], 6))
    # jlods = hstack((jforce,jmomnt))
    memloads = loads[apply(lambda x: ((x['degree'] >= 0 or type(
        rowPos(x['P1'], nodes)) == type(False)) and x['degree'] > -3), loads)]

    memloads = memloads if memloads.size != 0 else array([{'degree': 0,
                                                           'parentSegment': segments[0],
                                                           'P1': segments[0]['P1'],
                                                           'P3': segments[0]['P3'],
                                                           'normal': array([0, 0, 1]),
                                                           'peak': 0,
                                                           'class': 'load'}])
    for x in memloads:
        memLoadMatrix[dictInArr(x['parentSegment'], segments)] += lineGlobalFEA(x['parentSegment']['P1'],
                                                                                x['parentSegment']['P3'], x['P1'], x['P3'], z1(x['parentSegment']), z2(
                                                                                    x['parentSegment']), x['degree'], x['peak'],
                                                                                x['parentSegment']['axisVector'], x['normal'], hinged(x['parentSegment']))[[1, 2, 3, 7, 8, 9]]

    # tempLoads = loads[apply(lambda x: x['degree']==-3,loads)]
    # if tempLoads.size!=0:
    #     for x in tempLoads:
    #         print('calculationg temp loads...'+str(dictInArr(x['parentSegment'],segments)))
    #         memLoadMatrix[dictInArr(x['parentSegment'],segments)] += lineTempGlobalFEA(x['parentSegment']['P1'],
    #             x['parentSegment']['P3'],x['P1'],x['P3'],z1(x['parentSegment']),z2(x['parentSegment']),x['peak'],
    #             x['parentSegment']['axisVector'],x['normal'],x['parentSegment']['youngsModulus'],x['parentSegment']['area'],
    #             x['parentSegment']['alpha'],x['parentSegment']['Iyy'],x['parentSegment']['Izz'],
    #             hinged(x['parentSegment']))[[1,2,3,7,8,9]]

    settlements = apply(lambda t: t['settlement'], supports)
    if unique(settlements).any():
        def add(x):
            K = lineStiffnessLocal2(x['youngsModulus'], x['Iyy'], norm(
                x['P3']-x['P1']), x['area'], x['shearModulus'], shear, inextensible, hinged(x))
            T = lineTransformation2(x['P1'], x['P3'], z1(x), z2(x))
            settlement1 = sum(apply(lambda t: t['settlement'][[1, 2, 3]], supports[filter1(
                x)]), 0) if filter1(x).any() else zeros(3)
            settlement2 = sum(apply(lambda t: t['settlement'][[1, 2, 3]], supports[filter2(
                x)]), 0) if filter2(x).any() else zeros(3)
            settlements = hstack((settlement1, settlement2))
            FEAs = T.T @ (K @ (T @ settlements)
                          ) if settlements.any() else zeros(6)
            return FEAs

        memLoadMatrix += apply(add, segments)

    mLoadMatrix = zeros((shape(nodes)[0], 3))
    for x in arange(segments.size):
        mLoadMatrix[memberLocation[x][0]] += memLoadMatrix[x][0:3]
        mLoadMatrix[memberLocation[x][1]] += memLoadMatrix[x][3:6]

    locvec = (locationMatrix.flatten() > 0).nonzero()[0]
    superFEA = mLoadMatrix.flatten()[locvec]

    superStiffness = diag(zeros(max(locationMatrix).astype(int)))

    for id in arange(segments.size):
        x = segments[id]
        nj = memberLocation[id, 0]
        nk = memberLocation[id, 1]
        vec = array([locationMatrix[nj], locationMatrix[nk]]
                    ).astype(int).flatten()
        sel = (vec > 0).nonzero()[0]
        superStiffness[repeat(vec[sel]-1, sel.size), tile(vec[sel]-1, sel.size)] += lineStiffnessGlobal2(x['P1'], x['P3'], z1(x), z2(x), x['youngsModulus'],
                                                                                                         x['Iyy'], norm(x['P3']-x['P1']), x['area'], x['shearModulus'], shear, inextensible, hinged(x))[repeat(sel, sel.size), tile(sel, sel.size)]

    if not det(superStiffness/mean(superStiffness)):
        raise ValueError('Global Stiffness Matrix has zero determinant')

    superJload = zeros(max(locationMatrix).astype(int))

    for i in arange(shape(nodes)[0]):
        vec = locationMatrix[i].astype(int)
        sel = (vec > 0).nonzero()[0]
        superJload[vec[sel]-1] += jLoadMatrix[i, sel]

    deflections = inv(superStiffness) @ (superJload -
                                         superFEA) if superStiffness.size != 0 else 0

    locvec = locationMatrix.flatten().astype(int)

    responses = apply(
        lambda x: deflections[x-1] if x != 0 else 0, locvec).reshape((shape(nodes)[0], 3))
    responses = responses.astype(float)

    a = apply(lambda x: x['settlement'][[1, 2, 3]], supports)
    responses[spfilter.astype(int)] += a.astype(float)

    responsesRaw = hstack(
        (nodes, zeros((nodes.shape[0], 1)), responses, zeros((nodes.shape[0], 2))))
    responses = responsesRaw[apply(lambda x: type(
        rowPos(x, nodesOrg)) != type(False), nodes)][:, [1, 2, 4, 5, 6]]

    actionsRaw = zeros((segments.size*2, 6))
    actions = zeros((segmentsOrg.size*2, 6))

    for id in arange(segments.size):
        x = segments[id]
        nj = memberLocation[id, 0]
        nk = memberLocation[id, 1]
        vec = array([locationMatrix[nj], locationMatrix[nk]]
                    ).astype(int).flatten()
        actionsRaw[2*id, 0:3] = nodes[nj]
        actionsRaw[2*id+1, 0:3] = nodes[nk]
        globalDeflections = apply(
            lambda x: deflections[x-1] if x != 0 else x, vec)
        memLoad = lineTransformation2(
            x['P1'], x['P3'], z1(x), z2(x)) @ memLoadMatrix[id]
        localDeflections = matmul(lineTransformation2(
            x['P1'], x['P3'], z1(x), z2(x)), globalDeflections)
        localActions = matmul(lineStiffnessLocal2(x['youngsModulus'], x['Iyy'], norm(x['P3']-x['P1']),
                                                  x['area'], x['shearModulus'], shear, inextensible, hinged(x)), localDeflections)+memLoad
        actionsRaw[2*id, 3:6] = localActions[0:3]
        actionsRaw[2*id+1, 3:6] = -localActions[3:6]

    for i in arange(segmentsOrg.size):
        for x in childOf(segmentsOrg[i], structure):
            id = dictInArr(x, segments)
            if x['parent'] == None:
                actions[2*i], actions[2*i +
                                      1] = actionsRaw[2*id], actionsRaw[2*id+1]
            else:
                if tolClose(x['P1'], x['parent']['P1']):
                    actions[2*i] = actionsRaw[2*id]
                elif tolClose(x['P3'], x['parent']['P3']):
                    actions[2*i+1] = actionsRaw[2*id+1]
                else:
                    pass

    tempLoads = loads[apply(lambda x: x['class'] in [
                            'tempLoad', 'misfitLoad'], loads)]
    if tempLoads.size > 0:
        for x in tempLoads:
            seg = x['parentSegment']['parent'] if x['parentSegment']['parent'] else x['parentSegment']
            actions[2*dictInArr(seg, segmentsOrg) + all(x['P1']
                                                        == seg['P3']), int(1-2*x['degree'])] -= x['peak']

    actionsRaw = hstack((actionsRaw[:, 0:5], zeros(
        (actionsRaw.shape[0], 3)), actionsRaw[:, 5].reshape((actionsRaw.shape[0], 1))))
    actions = hstack((actions[:, 0:5], zeros((actions.shape[0], 3)), actions[:, 5].reshape(
        (actions.shape[0], 1))))[:, [1, 2, 3, 4, 8]]

    # actions = actionsRaw[apply(lambda x: type(rowPos(x[0:3],nodesOrg))!=type(False),actionsRaw)][:,[1,2,3,4,8]]

    multiplier = array([[1, 1, 1], [-1, -1, -1]])

    def globalActions(index): return multiplier*(lineTransformation2(segments[index]['P1'], segments[index]['P3'], array(
        [0.0, 0.0, 1.0]), array([0.0, 0.0, 1.0])).T @ hstack(actionsRaw[(2*index):(2*index+2), [3, 4, 8]])).reshape((2, 3))
    reactionsRaw = hstack((actionsRaw[:, :3], vstack(
        apply(globalActions, arange(segments.size)))))
    reactions = reactionsRaw[apply(lambda x: type(
        rowPos(x[:3], nodesOrg)) != type(False), reactionsRaw)]

    def addAllRxns(node): return sum(
        reactions[apply(lambda x: tolClose(node, x), reactions[:, :3])][:, 3:], 0)
    reactions = apply(addAllRxns, nodesOrg)
    reactions = hstack((nodesOrg[:, 1:], reactions))

    t = time()-t1
    from numpy import around
    print(f"FEA = {around(superFEA,3)}\nJLoad = {around(superJload,3)}\nStiffness="+'\n'.join(
        [str([round(x, 3) for x in y])for y in superStiffness])+f"\nDeflections = {around(deflections,3)}")
    return ({'simplified': structure, 'responseRaw': responsesRaw, 'response': responses, 'actionRaw': actionsRaw, 'action': actions, 'memLoc': memberLocation, 'reactions': reactions, 'time': t})


def truss3d(struct, shear=False, inextensible=False, simplified=True):
    t1 = time()
    segmentsOrg = struct['segments']

    nodes = apply(lambda x: array([x['P1'], x['P3']]), segmentsOrg)
    # nodesOrg = unique(nodes.reshape(nodes.shape[0]*nodes.shape[1],3),axis=0)
    nodesOrg = sortYZ(nodes.reshape(nodes.shape[0]*nodes.shape[1], 3))

    structure = simplify(struct) if simplified else struct

    segments = structure['segments']
    loads = structure['loads']
    supports = structure['supports']

    if (supports.size == 0):
        raise KeyError('No support found in the structure')

    nodes = apply(lambda x: array([x['P1'], x['P3']]), segments)
    # nodes = unique(nodes.reshape(nodes.shape[0]*nodes.shape[1],3),axis=0)
    nodes = sortYZ(nodes.reshape(nodes.shape[0]*nodes.shape[1], 3))

    def filter1(x): return apply(
        lambda t: tolClose(t['location']-x['P1']), supports)

    def filter2(x): return apply(
        lambda t: tolClose(t['location']-x['P3']), supports)

    suspects = supports[apply(lambda x: x['type'] ==
                              'Internal Hinge', supports)]

    def filter(x):
        if type(rowPos(x['location'], nodes)) != type(False):
            return rowPos(x['location'], nodes)

    def z1(seg):
        sps = supports[filter1(seg)]
        sps = sps[apply(lambda x: x['type'] != 'Node', sps)
                  ] if sps.size != 0 else sps
        normals = apply(lambda x: x['normal'], sps) if sps.size != 0 else array(
            [array([0, 0, 1])])
        normal = unit(sum(normals, 0))
        if normals.shape[0] > 1:
            warn(f'{normals.shape[0]} normals are resolved to: {normal}')
        return normal

    def z2(seg):
        sps = supports[filter2(seg)]
        sps = sps[apply(lambda x: x['type'] != 'Node', sps)
                  ] if sps.size != 0 else sps
        normals = apply(lambda x: x['normal'], sps) if sps.size != 0 else array(
            [array([0, 0, 1])])
        normal = unit(sum(normals, 0))
        if normals.shape[0] > 1:
            warn(f'{normals.shape[0]} normals are resolved to: {normal}')
        return normal

    start = apply(lambda x: rowPos(x, nodes),
                  apply(lambda x: x['P1'], segments))
    stops = apply(lambda x: rowPos(x, nodes),
                  apply(lambda x: x['P3'], segments))
    memberLocation = vstack((start, stops)).T

    locationMatrix = zeros((shape(nodes)[0], 3))
    supports = supports[apply(lambda x: filter(x) != None, supports)]
    b = apply(filter, supports)
    spfilter = b
    c = apply(lambda x: supports[x], apply(lambda t: b == t, b))
    a = apply(lambda x: sum(apply(lambda y: rxn(y['type'])[[0, 1, 2]], x)), c)
    locationMatrix[b.astype(int)] = a
    b = locationMatrix.reshape(-1)
    b[b != 0] = -1
    c = asarray(b == 0).nonzero()[0]
    b[c] = (arange(c.size))+1
    b[b == -1] = 0

    jLoadMatrix = zeros((shape(nodes)[0], 3))
    jforce = loads[apply(lambda x: x['degree'] == -
                         1 and type(rowPos(x['P1'], nodes)) != type(False), loads)]
    jmomnt = loads[apply(lambda x: x['degree'] == -
                         2 and type(rowPos(x['P1'], nodes)) != type(False), loads)]
    if jmomnt.size != 0:
        warn('external moments are excluded')

    for x in jforce:
        jLoadMatrix[rowPos(x['P1'], nodes)] += x['peak']*x['normal']

    memLoadMatrix = zeros((shape(memberLocation)[0], 6))
    jlods = hstack((jforce, jmomnt))
    memloads = loads[apply(lambda x: x['degree'] >= 0 or type(
        rowPos(x['P1'], nodes)) == type(False), loads)]
    if memloads.size != 0:
        warn('member loads are excluded')

    settlements = apply(lambda t: t['settlement'], supports)
    if unique(settlements).any():
        def add(x):
            K = lineStiffnessLocalTruss(
                x['youngsModulus'], x['area'], norm(x['P3']-x['P1']))
            T = lineTransformationTruss(x['P1'], x['P3'], z1(x), z2(x))
            settlement1 = sum(apply(lambda t: t['settlement'][0:3], supports[filter1(
                x)]), 0) if filter1(x).any() else zeros(3)
            settlement2 = sum(apply(lambda t: t['settlement'][0:3], supports[filter2(
                x)]), 0) if filter2(x).any() else zeros(3)
            settlements = hstack((settlement1, settlement2))
            FEAs = T.T @ (K @ (T @ settlements)
                          ) if settlements.any() else zeros(6)
            return FEAs

        memLoadMatrix += apply(add, segments)

    mLoadMatrix = zeros((shape(nodes)[0], 3))
    for x in arange(segments.size):
        mLoadMatrix[memberLocation[x][0]] += memLoadMatrix[x][0:3]
        mLoadMatrix[memberLocation[x][1]] += memLoadMatrix[x][3:6]

    locvec = (locationMatrix.flatten() > 0).nonzero()[0]
    superFEA = mLoadMatrix.flatten()[locvec]

    superStiffness = diag(zeros(max(locationMatrix).astype(int)))

    for id in arange(segments.size):
        x = segments[id]
        nj = memberLocation[id, 0]
        nk = memberLocation[id, 1]
        vec = array([locationMatrix[nj], locationMatrix[nk]]
                    ).astype(int).flatten()
        sel = (vec > 0).nonzero()[0]
        superStiffness[repeat(vec[sel]-1, sel.size), tile(vec[sel]-1, sel.size)] += lineStiffnessGlobalTruss(x['P1'], x['P3'], z1(
            x), z2(x), x['youngsModulus'], x['area'], norm(x['P3']-x['P1']))[repeat(sel, sel.size), tile(sel, sel.size)]

    if not det(superStiffness/mean(superStifnness)):
        raise ValueError('Global Stiffness Matrix has zero determinant')

    superJload = zeros(max(locationMatrix).astype(int))

    for i in arange(shape(nodes)[0]):
        vec = locationMatrix[i].astype(int)
        sel = (vec > 0).nonzero()[0]
        superJload[vec[sel]-1] += jLoadMatrix[i, sel]

    deflections = matmul(inv(superStiffness), superJload -
                         superFEA) if superStiffness.size != 0 else 0

    locvec = locationMatrix.flatten().astype(int)

    responses = apply(
        lambda x: deflections[x-1] if x != 0 else 0, locvec).reshape((shape(nodes)[0], 3))
    responses = responses.astype(float)

    a = apply(lambda x: x['settlement'][[0, 1, 2]], supports)
    responses[spfilter.astype(int)] += a.astype(float)

    responsesRaw = hstack((nodes, responses))

    responses = responsesRaw[apply(lambda x: type(
        rowPos(x, nodesOrg)) != type(False), nodes)]

    actionsRaw = zeros((segments.size*2, 4))
    actions = zeros((segmentsOrg.size*2, 4))

    for id in arange(segments.size):
        x = segments[id]
        nj = memberLocation[id, 0]
        nk = memberLocation[id, 1]
        vec = array([locationMatrix[nj], locationMatrix[nk]]
                    ).astype(int).flatten()
        actions[2*id, 0:3] = nodes[nj]
        actions[2*id+1, 0:3] = nodes[nk]
        globalDeflections = apply(
            lambda x: deflections[x-1] if x != 0 else x, vec)
        memLoad = lineTransformationTruss(
            x['P1'], x['P3'], z1(x), z2(x)) @ memLoadMatrix[id]
        localDeflections = matmul(lineTransformationTruss(
            x['P1'], x['P3'], z1(x), z2(x)), globalDeflections)
        localActions = matmul(lineStiffnessLocalTruss(
            x['youngsModulus'], x['area'], norm(x['P3']-x['P1'])), localDeflections)+memLoad
        actions[2*id, 3] = localActions[0]
        actions[2*id+1, 3] = -localActions[1]

    for i in arange(segmentsOrg.size):
        for x in childOf(segmentsOrg[i], structure):
            id = dictInArr(x, segments)
            if x['parent'] == None:
                actions[2*i], actions[2*i +
                                      1] = actionsRaw[2*id], actionsRaw[2*id+1]
            else:
                if all(x['P1'] == x['parent']['P1']):
                    actions[2*i] = actionsRaw[2*id]
                elif all(x['P3'] == x['parent']['P3']):
                    actions[2*i+1] = actionsRaw[2*id+1]
                else:
                    pass
    # actionsRaw = actions
    # actions = actionsRaw[apply(lambda x: type(rowPos(x[0:3],nodesOrg))!=type(False),actionsRaw)]

    multiplier = array([[1, 1, 1], [-1, -1, -1]])

    def globalActions(index): return multiplier*(lineTransformationTruss(segments[index]['P1'], segments[index]['P3'], z1(
        segments[index]), z2(segments[index])).T @ hstack(actionsRaw[(2*index):(2*index+2), 3:])).reshape((2, 3))
    reactionsRaw = hstack((actionsRaw[:, :3], vstack(
        apply(globalActions, arange(segments.size)))))
    reactions = reactionsRaw[apply(lambda x: type(
        rowPos(x[0:3], nodesOrg)) != type(False), reactionsRaw)]

    def addAllRxns(node): return sum(
        reactions[apply(lambda x: tolClose(node, x), reactions[:, :3]), 3:], 0)
    reactions = hstack((nodesOrg, apply(addAllRxns, nodesOrg)))

    t = time()-t1
    return ({'simplified': structure, 'responseRaw': responsesRaw, 'response': responses, 'actionRaw': actionsRaw, 'action': actions, 'memLoc': memberLocation, 'reactions': reactions, 'time': t})


def truss2d(struct, shear=False, inextensible=False, simplified=True, simFac=0.9995):
    t1 = time()
    segmentsOrg = struct['segments']

    nodes = apply(lambda x: array([x['P1'], x['P3']]), segmentsOrg)
    # nodesOrg = unique(nodes.reshape(nodes.shape[0]*nodes.shape[1],3),axis=0)
    nodesOrg = sortYZ(nodes.reshape(nodes.shape[0]*nodes.shape[1], 3))

    structure = simplify(struct, simFac) if simplified else struct

    segments = structure['segments']
    loads = structure['loads']
    supports = structure['supports']

    if (supports.size == 0):
        raise KeyError('No support found in the structure')

    nodes = apply(lambda x: array([x['P1'], x['P3']]), segments)
    # nodes = unique(nodes.reshape(nodes.shape[0]*nodes.shape[1],3),axis=0)
    nodes = sortYZ(nodes.reshape(nodes.shape[0]*nodes.shape[1], 3))

    if not all(apply(lambda x: x == nodes[:, 0][0], nodes[:, 0])):
        raise TypeError('Structure should lie in some vertical plane X=C')

    def filter1(x): return apply(
        lambda t: tolClose(t['location'], x['P1']), supports)

    def filter2(x): return apply(
        lambda t: tolClose(t['location'], x['P3']), supports)

    def filter(x):
        if type(rowPos(x['location'], nodes)) != type(False):
            return rowPos(x['location'], nodes)

    def z1(seg):
        sps = supports[filter1(seg)]
        sps = sps[apply(lambda x: x['type'] != 'Node', sps)
                  ] if sps.size != 0 else sps
        normals = apply(lambda x: x['normal'], sps) if sps.size != 0 else array(
            [array([0, 0, 1])])
        normal = unit(sum(normals, 0))
        if normals.shape[0] > 1:
            warn(f'{normals.shape[0]} normals are resolved to: {normal}')
        return normal

    def z2(seg):
        sps = supports[filter2(seg)]
        sps = sps[apply(lambda x: x['type'] != 'Node', sps)
                  ] if sps.size != 0 else sps
        normals = apply(lambda x: x['normal'], sps) if sps.size != 0 else array(
            [array([0, 0, 1])])
        normal = unit(sum(normals, 0))
        if normals.shape[0] > 1:
            warn(f'{normals.shape[0]} normals are resolved to: {normal}')
        return normal

    start = apply(lambda x: rowPos(x, nodes),
                  apply(lambda x: x['P1'], segments))
    stops = apply(lambda x: rowPos(x, nodes),
                  apply(lambda x: x['P3'], segments))
    memberLocation = vstack((start, stops)).T

    locationMatrix = zeros((shape(nodes)[0], 2))
    supports = supports[apply(lambda x: filter(x) != None, supports)]
    b = apply(filter, supports)
    spfilter = b
    c = apply(lambda x: supports[x], apply(lambda t: b == t, b))
    a = apply(lambda x: sum(apply(lambda y: rxn(y['type'])[1:3], x)), c)
    locationMatrix[b.astype(int)] = a
    b = locationMatrix.reshape(-1)
    b[b != 0] = -1
    c = asarray(b == 0).nonzero()[0]
    b[c] = (arange(c.size))+1
    b[b == -1] = 0

    jLoadMatrix = zeros((shape(nodes)[0], 2))
    jforce = loads[apply(lambda x: x['degree'] == -
                         1 and type(rowPos(x['P1'], nodes)) != type(False), loads)]
    jmomnt = loads[apply(lambda x: x['degree'] == -
                         2 and type(rowPos(x['P1'], nodes)) != type(False), loads)]
    if jmomnt.size != 0:
        warn('external moments are excluded')

    for x in jforce:
        jLoadMatrix[rowPos(x['P1'], nodes)] += x['peak']*x['normal'][1:3]

    memLoadMatrix = zeros((shape(memberLocation)[0], 4))
    # jlods = hstack((jforce,jmomnt))
    memloads = loads[apply(lambda x: x['degree'] >= 0 or type(
        rowPos(x['P1'], nodes)) == type(False), loads)]
    if memloads.size != 0:
        warn('member loads are excluded')

    settlements = apply(lambda t: t['settlement'], supports)
    if unique(settlements).any():
        def add(x):
            K = lineStiffnessLocalTruss(
                x['youngsModulus'], x['area'], norm(x['P3']-x['P1']))
            T = lineTransformationTruss2(x['P1'], x['P3'], z1(x), z2(x))
            settlement1 = sum(apply(lambda t: t['settlement'][1:3], supports[filter1(
                x)]), 0) if filter1(x).any() else zeros(2)
            settlement2 = sum(apply(lambda t: t['settlement'][1:3], supports[filter2(
                x)]), 0) if filter2(x).any() else zeros(2)
            settlements = hstack((settlement1, settlement2))
            FEAs = T.T @ (K @ (T @ settlements)
                          ) if settlements.any() else zeros(4)
            return FEAs

        memLoadMatrix += apply(add, segments)

    mLoadMatrix = zeros((shape(nodes)[0], 2))
    for x in arange(segments.size):
        mLoadMatrix[memberLocation[x][0]] += memLoadMatrix[x][0:2]
        mLoadMatrix[memberLocation[x][1]] += memLoadMatrix[x][2:4]

    locvec = (locationMatrix.flatten() > 0).nonzero()[0]
    superFEA = mLoadMatrix.flatten()[locvec]

    superStiffness = diag(zeros(max(locationMatrix).astype(int)))

    for id in arange(segments.size):
        x = segments[id]
        nj = memberLocation[id, 0]
        nk = memberLocation[id, 1]
        vec = array([locationMatrix[nj], locationMatrix[nk]]
                    ).astype(int).flatten()
        sel = (vec > 0).nonzero()[0]
        superStiffness[repeat(vec[sel]-1, sel.size), tile(vec[sel]-1, sel.size)] += lineStiffnessGlobalTruss2(x['P1'], x['P3'], z1(
            x), z2(x), x['youngsModulus'], x['area'], norm(x['P3']-x['P1']))[repeat(sel, sel.size), tile(sel, sel.size)]

    if not det(superStiffness/mean(superStiffness)):
        raise ValueError('Global Stiffness Matrix has zero determinant')

    superJload = zeros(max(locationMatrix).astype(int))

    for i in arange(shape(nodes)[0]):
        vec = locationMatrix[i].astype(int)
        sel = (vec > 0).nonzero()[0]
        superJload[vec[sel]-1] += jLoadMatrix[i, sel]

    deflections = matmul(inv(superStiffness), superJload -
                         superFEA) if superStiffness.size != 0 else 0

    locvec = locationMatrix.flatten().astype(int)

    responses = apply(
        lambda x: deflections[x-1] if x != 0 else 0, locvec).reshape((shape(nodes)[0], 2))
    responses = responses.astype(float)

    a = apply(lambda x: x['settlement'][1:3], supports)
    responses[spfilter.astype(int)] += a.astype(float)

    responses = hstack((zeros((shape(nodes)[0], 1)), responses))
    responsesRaw = hstack((nodes, responses))

    responses = responsesRaw[apply(lambda x: type(
        rowPos(x, nodesOrg)) != type(False), nodes)][:, [0, 1, 2, 4, 5]]

    actions = zeros((segmentsOrg.size*2, 4))
    actionsRaw = zeros((segments.size*2, 4))

    for id in arange(segments.size):
        x = segments[id]
        nj = memberLocation[id, 0]
        nk = memberLocation[id, 1]
        vec = array([locationMatrix[nj], locationMatrix[nk]]
                    ).astype(int).flatten()
        actionsRaw[2*id, 0:3] = nodes[nj]
        actionsRaw[2*id+1, 0:3] = nodes[nk]
        globalDeflections = apply(
            lambda x: deflections[x-1] if x != 0 else x, vec)
        memLoad = lineTransformationTruss2(
            x['P1'], x['P3'], z1(x), z2(x)) @ memLoadMatrix[id]
        localDeflections = matmul(lineTransformationTruss2(
            x['P1'], x['P3'], z1(x), z2(x)), globalDeflections)
        localActions = matmul(lineStiffnessLocalTruss(
            x['youngsModulus'], x['area'], norm(x['P3']-x['P1'])), localDeflections)+memLoad
        actionsRaw[2*id, 3] = localActions[0]
        actionsRaw[2*id+1, 3] = -localActions[1]

    for i in arange(segmentsOrg.size):
        for x in childOf(segmentsOrg[i], structure):
            id = dictInArr(x, segments)
            if x['parent'] == None:
                actions[2*i], actions[2*i +
                                      1] = actionsRaw[2*id], actionsRaw[2*id+1]
            else:
                if tolClose(x['P1'], x['parent']['P1']):
                    actions[2*i] = actionsRaw[2*id]
                elif tolClose(x['P3'], x['parent']['P3']):
                    actions[2*i+1] = actionsRaw[2*id+1]
                else:
                    pass
    # actionsRaw = actions
    # actions = actionsRaw[apply(lambda x: type(rowPos(x[0:3],nodesOrg))!=type(False),actionsRaw)]

    tempLoads = loads[apply(lambda x: x['class'] in [
                            'tempLoad', 'misfitLoad'] and x['degree'] == -1, loads)]
    if tempLoads.size > 0:
        for x in tempLoads:
            seg = x['parentSegment']['parent'] if x['parentSegment']['parent'] else x['parentSegment']
            actions[2*dictInArr(seg, segmentsOrg) +
                    all(x['P1'] == seg['P3']), 3] -= x['peak']

    multiplier = array([[1, 1, 1], [-1, -1, -1]])

    def globalActions(index): return multiplier*(lineTransformationTruss(
        segments[index]['P1'], segments[index]['P3']).T @ hstack(actionsRaw[(2*index):(2*index+2), 3:])).reshape((2, 3))
    reactionsRaw = hstack((actionsRaw[:, :3], vstack(
        apply(globalActions, arange(segments.size)))))
    reactions = reactionsRaw[apply(lambda x: type(
        rowPos(x[0:3], nodesOrg)) != type(False), reactionsRaw)]

    def addAllRxns(node): return sum(
        reactions[apply(lambda x: tolClose(node, x), reactions[:, :3]), 3:], 0)
    reactions = hstack((nodesOrg, apply(addAllRxns, nodesOrg)))

    t = time()-t1
    # from numpy import around
    # print(f"JLoad = {around(superJload,3)}\nStiffness="+'\n'.join([str([round(x,3) for x in y])for y in superStiffness])+f"\nDeflections = {around(deflections,3)}")
    return ({'simplified': structure, 'responseRaw': responsesRaw, 'response': responses, 'actionRaw': actionsRaw, 'action': actions, 'memLoc': memberLocation, 'reactions': reactions, 'time': t})
