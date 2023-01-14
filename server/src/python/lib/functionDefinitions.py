from warnings import warn

from numpy import (allclose, append, array, array2string, cross, dot, equal,
                   float, fromstring, heaviside, hstack, meshgrid, round,
                   setdiff1d, sqrt, str, unique, vstack, zeros)
from numpy.linalg import norm
from numpy.random import sample

from lib.numbaFunctions import axes, arceqn, quadeqn

TOL = 1e-10


def roundDict(dict, precision):
    dictt = dict.copy()
    for x, y in dictt.items():
        try:
            dictt[x] = round(y, precision)
        except:
            try:
                dictt[x] = roundDict(y, precision)
            except:
                dictt[x] = y
    return dictt


def tolClose(a, b, tol=TOL):
    return allclose(a, b, rtol=0, atol=tol)


def rowPos(vec, mat):
    a = apply(lambda x: tolClose(x, vec), mat).nonzero()[0]
    if a.size > 0:
        return a[0]
    else:
        return False


def dictInArr(dic, arr):
    a = apply(lambda x: identicalObjects(x, dic), arr).nonzero()[0]
    if a.size > 0:
        return a[0]
    else:
        return False


def identicalObjects(a, b):
    if len(a.keys()) == len(b.keys()):
        for x in a.keys():
            try:
                if all(unique(a[x] == b[x])):
                    pass
                else:
                    return False
            except:
                try:
                    if identicalObjects(a[x], b[x]):
                        pass
                    else:
                        return False
                except:
                    return False
        return True
    else:
        return False


def apply(f, x):
    """
    This is a convenient syntax for generator expression.

    parameters
    ----------

    f = function to apply throughout a vector

    x = vector over which the function is to be applied

    returns
    -------

    The value returned by the function 'f' applied over the vector 'x'
    """
    return array([y for y in (f(i) for i in x)])


def unit(vec):
    return vec / norm(vec) if norm(vec) != 0 else vec


def ustep(x, a=0):
    return heaviside(x - a, 1)


def delta(x, a=0):
    return equal(x, a).astype(int)


def customTypes():
    return setdiff1d(
        apply(
            lambda x: array2string(x, separator='')[1:-1],
            array(meshgrid([0, 1], [0, 1], [0, 1], [0, 1], [0, 1],
                           [0, 1])).T.reshape((64, 6))), '000000')


# customTypes2 = lambda : setdiff1d(apply(lambda x: array2string(x,separator='')[1:-1],array(meshgrid([0,1],[0,1],[0,1])).T.reshape((8,3))),'000')


def customTypes2():
    return apply(lambda x: array2string(x, separator='')[1:-1],
                 array(meshgrid([0, 1], [0, 1], [0, 1])).T.reshape((8, 3)))


def make(parameter):
    """
    To define a dictionary for segment, support and load based on user given detials, may be broken details.

    parameter
    ---------

    parameter - list of non empty parameters

    returns
    -------

    respective dictionary with adjusted properties [like axis vector for segment]
    """
    # precision = 0
    # for x in parameter:
    #     try:
    #         s = str(x)
    #         if '[' not in s:
    #             i = s.index('.')
    #             precision = max(precision, len(s[i+1:]))
    #         else:
    #             for x in s[1:-1].split(' '):
    #                 i = s.index('.')
    #                 precision = max(precision, len(s[i+1:]))
    #     except:
    #         pass
    types = parameter[0]
    # if types == '':
    #     raise ValueError('type is missing')
    if types in {'line', 'arc', 'quad'}:
        if all(parameter[1]):
            P1 = array(parameter[1]).astype(float)
        else:
            raise ValueError(
                'P1 has missing values. It should be a vector [x,y,z]')

        if all(parameter[2]):
            P3 = array(parameter[2]).astype(float)
        else:
            raise ValueError(
                'P3 has missing values. It should be a vector [x,y,z]')

        if types == 'line':
            P2 = (P1 + P3) / 2
        else:
            if all(parameter[3]):
                P2 = array(parameter[3]).astype(float)
            else:
                raise ValueError(
                    'P2 has missing values. It should be a vector [x,y,z]')

        if parameter[11] != '':
            axisVector = unit(fromstring(parameter[11], sep=','))
        else:
            if norm(cross(P3 - P1, [1, 0, 0])):
                axisVector = array([1, 0, 0])
            else:
                axisVector = array([0, 1, 0])

        if norm(cross(P3 - P1, axisVector)) == 0:
            axisVector = cross(cross(P3 - P1, axisVector + sample(3)), P3 - P1)

        elif dot(P3 - P1, axisVector) != 0:
            if dot(P3 - P1, array([0, 1, 0])):
                axisVector = unit(cross(cross(P3 - P1, axisVector), P3 - P1))
            else:
                axisVector = array([0, 1, 0])

        if '[' + parameter[11] + ']' != array2string(axisVector,
                                                     separator=','):
            warn(f'axis vector is assumed to be: {axisVector}')

        if parameter[4] == '':
            youngsModulus = 1
        else:
            youngsModulus = float(parameter[4])

        if parameter[5] == '':
            shearModulus = 1
        else:
            shearModulus = float(parameter[5])

        if parameter[6] == '':
            area = 1
        else:
            area = float(parameter[6])

        if parameter[7] == '':
            Ixx = 1
        else:
            Ixx = float(parameter[7])

        if parameter[8] == '':
            Iyy = 1
        else:
            Iyy = float(parameter[8])

        if parameter[9] == '':
            J = Ixx + Iyy
        else:
            J = float(parameter[9])

        if parameter[10] == '':
            shapeFactor = array([3 / 2, 3 / 2])
        else:
            shapeFactor = array([parameter[10]]).astype(float)

        if (len(parameter) > 12):
            if parameter[12] == '':
                density = 1
            else:
                density = float(parameter[12])

            if parameter[13] == '':
                alpha = 1
            else:
                alpha = float(parameter[13])

        else:
            density = alpha = 1

        s = {
            'type': types,
            'P1': round(P1, precision),
            'P3': round(P3, precision),
            'P2': round(P2, precision),
            'youngsModulus': round(youngsModulus, precision),
            'shearModulus': round(shearModulus, precision),
            'area': round(area, precision),
            'Iyy': round(Ixx, precision),
            'Izz': round(Iyy, precision),
            'J': round(J, precision),
            'shapeFactor': round(shapeFactor, precision),
            'axisVector': round(axisVector, precision),
            'density': round(density, precision),
            'alpha': round(alpha, precision),
            'class': 'segment',
            'parent': None
        }
    elif types in {'Fixed', 'Roller', 'Hinge', 'Internal Hinge'
                   } or str(types) in customTypes():

        if all(parameter[1]):
            location = array(parameter[1]).astype(float)
        else:
            raise ValueError(
                'Position has missing values. It should be a vector [x,y,z]')

        if all(parameter[3]):
            normal = unit(array(parameter[3]).astype(float))
        else:
            normal = array([0, 0, 1])

        axs = axes(normal)
        zeroes = zeros((3, 3))
        T = vstack((hstack((axs, zeroes)), hstack((zeroes, axs))))
        settlement = array(parameter[2])
        settlement[settlement == ''] = 0
        settlement = T @ settlement.astype(float)

        if all(parameter[3]):
            normal = unit(array(parameter[3]).astype(float))
        else:
            normal = array([0, 0, 1])

        s = {
            'type': types,
            'location': round(location, precision),
            'settlement': round(settlement, precision),
            'normal': round(normal, precision),
            'class': 'support'
        }
    else:
        if types == '000000':
            raise (ValueError('Redundant support type'))

        ps = parameter[1]
        p1 = ps['P1']
        p3 = ps['P3']
        degree = int(types)
        if degree < -4:
            raise ValueError('This type of load is not defined')
        if degree > -3:
            if all(parameter[4]):
                normal = unit(array(parameter[4]).astype(float))
            else:
                if (float(types) == -2.0):
                    normal = array([1, 0, 0])
                else:
                    normal = array([0, 0, -1])
            className = 'load'
            from lib.segmentMethods import segEqn

            def e(x):
                return segEqn(ps['type'], ps['P1'], ps['P3'], x, ps['P2'])

            if isinstance(parameter[2], float):
                P1 = e(parameter[2])
                P3 = e(parameter[3])

            else:
                if all(parameter[2]):
                    P1 = array(parameter[2]).astype(float)
                    P1t = e(dot(P1 - p1, unit(p3 - p1)))
                    if max([norm(P1t - p1), norm(p3 - P1t)]) > norm(p1 - p3):
                        P1t = p1
                    P1 = P1t
                else:
                    raise ValueError(
                        'P1 has missing values. It should be a vector [x,y,z]')

                if all(parameter[3]):
                    P3 = array(parameter[3]).astype(float)
                    P3t = e(dot(P3 - p1, unit(p3 - p1)))
                    if max([norm(P3t - p1), norm(p3 - P3t)]) > norm(p1 - p3):
                        P3t = p3
                    P3 = P3t
                else:
                    P3 = P1

            if degree < 0:
                P3 = P1
            # elif norm(P3-p1) < norm(P1-p1):
            #     Pt = P3
            #     P3 = P1
            #     P1 = Pt
            warn(f'P1 = {P1} and P3 = {P3}')
        elif degree == -3:
            className = 'temprLoad'
            X = array([float(parameter[2]), 0, 0])
            Y = array([float(parameter[3]), 0, 0])
            normal = unit(array(parameter[4]).astype(float))
            peak = parameter[5]
        else:
            className = 'misfitLoad'
            X = ps['P1']
            Y = ps['P3']
            normal = unit(Y - X)
            peak = parameter[2]

        s = {
            'degree': degree,
            'parentSegment': ps,
            'P1': round(P1, precision),
            'P3': round(P3, precision),
            'normal': round(normal, precision),
            'peak': float(peak),
            'class': className
        }

    return s


def structify(listOfDictionaries):
    segments = listOfDictionaries[apply(lambda x: x['class'] == 'segment',
                                        listOfDictionaries)]
    # loads = listOfDictionaries[apply(lambda x: x['class'] in ['load','temprLoad','misfitLoad'], listOfDictionaries)]
    loads = listOfDictionaries[apply(lambda x: x['class'] == 'load',
                                     listOfDictionaries)]
    tempLoads = listOfDictionaries[apply(lambda x: x['class'] == 'temprLoad',
                                         listOfDictionaries)]
    misfitLoads = listOfDictionaries[apply(
        lambda x: x['class'] == 'misfitLoad', listOfDictionaries)]
    if tempLoads.size != 0:
        from lib.loadMethods import tempLoad
        tempLoadList = hstack(([
            tempLoad(x['P1'], x['P3'], x['normal'], x['peak'],
                     x['parentSegment'], x['psName']) for x in tempLoads
        ]))
        loads = append(loads, tempLoadList)
    if misfitLoads.size != 0:
        from lib.loadMethods import misfitLoad
        tempLoadList = hstack(([
            misfitLoad(x['peak'], x['parentSegment'], x['psName'])
            for x in misfitLoads
        ]))
        loads = append(loads, tempLoadList)
    if loads.size == 0:
        loads = array([{
            'degree': -1,
            'parentSegment': segments[0],
            'P1': array([0, 0, 0]),
            'P3': array([0, 0, 0]),
            'normal': array([0, 0, 1]),
            'peak': 0,
            'class': 'load'
        }])
    supports = listOfDictionaries[apply(lambda x: x['class'] == 'support',
                                        listOfDictionaries)]
    return {'segments': segments, 'loads': loads, 'supports': supports}


def structifyFromLists(listOfLists):
    listOfLists = array(listOfLists)
    listOfDictionaries = apply(make, listOfLists)
    return structify(listOfDictionaries)


def convertTo3D(Dictionary2d):
    dictionary = Dictionary2d.copy()
    cl = dictionary['class']
    if cl == 'segment':
        dictionary['P1'] = hstack((0.0, dictionary['P1']))
        dictionary['P3'] = hstack((0.0, dictionary['P3']))
        dictionary['P2'] = hstack((0.0, dictionary['P2']))
        dictionary['Iyy'] = dictionary['I']
        dictionary['Izz'] = dictionary['I']
        dictionary['J'] = 2 * dictionary['I']
        dictionary['axisVector'] = array([1.0, 0.0, 0.0])
        dictionary['shapeFactor'] = array([dictionary['shapeFactor']] * 2)
        dictionary.pop('I')
    elif cl in ['load', 'temprLoad', 'misfitLoad']:
        dictionary['parentSegment'] = convertTo3D(dictionary['parentSegment'])
        dictionary['P1'] = hstack((0.0, dictionary['P1']))
        dictionary['P3'] = hstack((0.0, dictionary['P3']))
        dictionary['normal'] = hstack(
            (0.0,
             dictionary['normal'])) if dictionary['degree'] != -2.0 else array(
                 [1.0, 0.0, 0.0])
    else:
        dictionary['type'] = '0'+dictionary['type'] + \
            '00' if dictionary['type'] in customTypes2(
        ) else dictionary['type']
        dictionary['location'] = hstack((0.0, dictionary['location']))
        dictionary['normal'] = hstack((0.0, dictionary['normal']))
        dictionary['settlement'] = hstack(
            (0.0, dictionary['settlement'], 0.0, 0.0))
    return dictionary


def convertTo2D(Dictionary3d):
    dictionary = Dictionary3d.copy()
    cl = dictionary['class']
    if cl == 'segment':
        dictionary['P1'] = dictionary['P1'][1:3]
        dictionary['P3'] = dictionary['P3'][1:3]
        dictionary['P2'] = dictionary['P2'][1:3]
        dictionary['I'] = dictionary['Iyy']
        dictionary.pop('Iyy')
        dictionary.pop('Izz')
        dictionary.pop('axisVector')
        dictionary.pop('J')
    elif cl in ['load', 'temprLoad', 'misfitLoad']:
        dictionary['parentSegment'] = convertTo2D(dictionary['parentSegment'])
        dictionary['P1'] = dictionary['P1'][1:3]
        dictionary['P3'] = dictionary['P3'][1:3]
        dictionary['normal'] = unit(
            dictionary['normal']
            [1:3]) if dictionary['degree'] != -2.0 else array([0, 0])
    else:
        dictionary['type'] = dictionary['type'][1:4] if dictionary[
            'type'] in customTypes() else dictionary['type']
        dictionary['location'] = dictionary['location'][1:3]
        dictionary['normal'] = unit(dictionary['normal'][1:3])
        dictionary['settlement'] = dictionary['settlement'][1:4]
    return dictionary


def getPrecision(parameter, indices=None):
    if indices == None:
        indices = range(len(parameter))
    precision = 0
    for i in indices:
        s = str(parameter[i])
        if '[' not in s:
            i = s.index('.') if '.' in s else len(s) - 1
            precision = int(max(precision, len(s[i + 1:])))
        else:
            for x in s[1:-1].split(' '):
                i = x.index('.') if '.' in x else len(x) - 1
                precision = int(max(precision, len(x[i + 1:])))
    return precision


def make2d(parameter, precision=15):
    types = parameter[0]
    if types == '':
        raise ValueError('type is missing')
    if types in {'line', 'arc', 'quad'}:
        # precision = getPrecision(parameter,[1,2,3])
        try:
            P1 = array(parameter[1]).astype(float)
        except:
            raise ValueError(
                'P1 has missing values. It should be a vector [x,y]')

        try:
            P3 = array(parameter[2]).astype(float)
        except:
            raise ValueError(
                'P3 has missing values. It should be a vector [x,y]')

        if types == 'line':
            P2 = (P1 + P3) / 2
        elif types == 'arc':
            P2 = parameter[3].astype(float)
            P2 = arceqn(array([0, *P1]), array([0, *P3]), array([0, *P2]),
                        norm(P3 - P1) / 2)[1:]
        else:
            P2 = parameter[3].astype(float)
            P2 = quadeqn(array([0, *P1]), array([0, *P3]), array([0, *P2]),
                         norm(P3 - P1) / 2)[1:]

        s = {
            'type': types,
            'P1': round(P1, precision).astype(float),
            'P3': round(P3, precision).astype(float),
            'P2': round(P2, precision).astype(float),
            'youngsModulus': float(parameter[4]),
            'shearModulus': float(parameter[5]),
            'area': float(parameter[6]),
            'I': float(parameter[7]),
            'shapeFactor': float(parameter[8]),
            'alpha': float(parameter[9]),
            'density': float(parameter[10]),
            'class': 'segment',
            'parent': None
        }
    elif types in {'Fixed', 'Roller', 'Hinge', 'Internal Hinge', 'Node'
                   } or str(types) in customTypes2():
        if types == '000':
            types = 'Node'
        # precision = getPrecision(parameter,[1,2,3])
        try:
            location = array(parameter[1]).astype(float)
        except:
            raise ValueError(
                'Position has missing values. It should be a vector [x,y,z]')

        if all(parameter[3]):
            normal = unit(array(parameter[3]).astype(float))
        else:
            normal = array([0, 1])
        normal = unit(parameter[3])
        axs = axes(hstack((0, normal)))
        zeroes = zeros((3, 3))
        T = vstack((hstack((axs, zeroes)), hstack((zeroes, axs))))

        settlement = parameter[2]
        settlement[settlement == ''] = 0
        settlement3D = hstack((0, settlement, 0, 0))
        settlement = (T @ settlement3D.astype(float))[1:4]

        s = {
            'type': types,
            'location': round(parameter[1], precision).astype(float),
            'settlement': settlement.astype(float),
            'normal': normal.astype(float),
            'class': 'support'
        }
    else:
        if types == '000':
            raise (ValueError('Redundant support type'))
        degree = int(types)
        ps = parameter[1]
        # precision = getPrecision(list(ps.values()),[1,2,3])
        try:
            normal = unit(array(parameter[4]).astype(float))
        except:
            if (float(types) != -2.0):
                normal = array([0, -1])
            else:
                normal = None

        # if isinstance(parameter[2],float):
        #     P1 = e(parameter[2])[1:3]
        #     P3 = e(parameter[3])[1:3]

        # else:
        if degree < -4:
            raise ValueError('This type of load is not defined')

        if -3 < degree:
            className = 'load'
            normal = unit(parameter[4]) if degree != -2.0 else array([0, 0])
            peak = parameter[5]
            X = parameter[2]
            Y = parameter[3] if degree >= 0 else X
            A = ps['P1']
            B = ps['P3']
            C = ps['P2']
            l = norm(Y - X)
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
            #     t=b
            #     b=a
            #     a=t
            from lib.segmentMethods import segEqn

            def eSeg(x):
                return segEqn(ps['type'], hstack((0, A)), hstack((0, B)), x,
                              hstack((0, C)))[1:3]

            X = eSeg(a)
            Y = eSeg(b)
        elif degree == -3:
            className = 'temprLoad'
            X = array([parameter[2], 0]) if type(
                parameter[2]) == float else parameter[2]
            Y = array([parameter[3], 0]) if type(
                parameter[3]) == float else parameter[3]
            xv = unit(ps['P3'] - ps['P1'])
            normal = array([-xv[1], xv[0]])
            # normal = unit(cross(array([1,0,0]),unit(hstack((0,ps['P3']))-hstack((0,ps['P1']))))[:2])
            peak = parameter[4] if type(
                parameter[4]) == float else parameter[5]
        else:
            className = 'misfitLoad'
            X = ps['P1']
            Y = ps['P3']
            normal = unit(Y - X)
            peak = parameter[2] if type(
                parameter[2]) == float else parameter[5]

        s = {
            'degree': degree,
            'parentSegment': ps,
            'P1': round(X, precision).astype(float),
            'P3': round(Y, precision).astype(float),
            'normal': normal.astype(float),
            'peak': float(peak),
            'class': className,
            'psName': parameter[-1]
        }
    return s


def structify2d(listOfDictionaries):
    listOfDictionaries = apply(convertTo3D, array(listOfDictionaries))
    return structify(listOfDictionaries)


def structifyFromLists2d(listOfLists):
    listOfLists = array(listOfLists)
    listOfDictionaries = apply(make2d, listOfLists)
    return structify2d(listOfDictionaries)
