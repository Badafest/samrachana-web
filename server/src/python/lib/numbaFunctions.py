from numba import jit_module
from numpy import array, interp, pi, dot, cross, all, sqrt, arccos, log, hstack, vstack, zeros, diag, fill_diagonal, repeat, append, arange, sum, prod, arange
from numpy.linalg import norm, inv

#@jit(nopython=True)
def comb(n,r):
    return int(prod(arange(n-r+1,n+1))/prod(arange(1,r+1)))

#@jit(nopython=True)
def tile(arr,no):
    t = arr.dtype
    brr = array(())
    for x in arr:
        brr = append(brr,(x)*no)
    return brr.astype(t)

#@jit(nopython=True)
def getSubMat(mat,rowIndex,colIndex,shape):
    fmat = zeros(shape)
    k = 0
    for i in rowIndex:
        l = 0
        for j in colIndex:
            fmat[k][l] = mat[i][j]
            l = l + 1
        k = k + 1
    return fmat

#@jit(nopython=True)
def setSubMat(mat,rowIndex,colIndex,target):
    k = 0
    for i in rowIndex:
        l = 0
        for j in colIndex:
            mat[i][j] = target[k][l]
            l = l + 1
        k = k + 1

#@jit(nopython=True)
def ustep(x,a=0):
    if x>=a:
        return 1
    else:
        return 0

#@jit(nopython=True)
def unit(vec):
    return vec/norm(vec)

#@jit(nopython=True)
def delta(x,a=0):
    if x==a:
        return 1
    else:
        return 0

#@jit(nopython=True)
def axes(z):
    z = unit(z)
    if(z[2]==1.0):
        return array([ [1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0] ])
    else:
        c1 = -z[1]/(sqrt(1-z[2]**2))
        s1 = z[0]/(sqrt(1-z[2]**2))
        c2 = z[2]
        s2 = sqrt(1-z[2]**2)
        return array([ [c1,s1,0],[-c2*s1,c1*c2,s2],[s1*s2,-c1*s2,c2] ])

#section property function
#@jit(nopython=True)
def sectionProperty(types,length,breadth=0,flanges=0,width=0):
    dimensions = array([length,breadth,flanges,width])
    if types=='Rectangle':
        a = dimensions[1]
        b = dimensions[0]
        A = a*b
        Ixx = (1/12)*(a*(b**3))
        Iyy = (1/12)*(b*(a**3))
        if b>a:
            a,b=b,a
        r=a/b
        if r<=10:
            beta =  interp(r,array([1,1.5,2,2.5,3,4,5,6,10]),array([2.25/16,0.196,0.229,0.249,0.263,0.281,0.291,0.299,0.312]))
        else:
            beta = 1/3
        Izz = beta*a*(b**3)
        k = [3/2]*2
    elif types=='Square':
        a = dimensions[0]
        A = a**2
        Ixx = Iyy = (a**4)/12
        Izz = 2.25*((a/2)**4)
        k = [3/2]*2
    elif types=='Circle':
        D = dimensions[0]
        A = 0.25*pi*(D**2)
        Ixx = Iyy = (1/64)*pi*(D**4)
        Izz = Ixx + Iyy
        k = [1.7]*2
    elif types=='I':
        D = dimensions[0]
        H = dimensions[0]-2*dimensions[2]
        B = dimensions[1]
        h = dimensions[2]
        b = dimensions[3]
        A = 2*B*h+H*b
        Ixx = (b*H**3)/12+(B*h**3)/6+0.5*(B*h*(H+h)**2)
        Iyy = (H*b**3)/12+(h*B**3)/6
        if h<(min(B,D)/10) and b<(min(D,B)/10):
            Izz = ((2*B*(h**3)+(D-h)*(b**3)))/3
        else:
            Izz = Ixx+Iyy
        kx = ((h+0.5*H)*(0.25*b*H**2+B*h*(H+h)))/Ixx
        ky = (0.125*B*(H*b**2+h*B**2))/Iyy
        k = [kx,ky]
    elif types=='C':
        D = dimensions[0]
        H = dimensions[0]-2*dimensions[2]
        B = dimensions[1]
        h = dimensions[2]
        b = dimensions[3]
        A = 2*B*h+H*b
        Ixx = (b*H**3)/12+(B*h**3)/6+0.5*(B*h*(H+h)**2)
        xg = (h*B**2+0.5*H*b**2)/A
        Iyy = (H*b**3)/12+(h*B**3)/6+b*H*(xg-0.5*H)**2
        if b<(min(D,B)/10) and h<(min(D,B)/10):
            Izz = ((2*B-b)*h**3+(D-h)*b**3)/3
        else:
            Izz = Ixx+Iyy
        kx = ((h+H/2)*(0.5*b*H**2+B*h*(H+h)))/Ixx
        if 2*B*h > b*H:
            xa = 0.5*B - 0.25*b*H/h
            ky = (B-xg)*(b*D*(xa-0.5*b)+h*((xa-b)**2+(B-xa)**2))/Iyy
        else:
            xa = 0.5*A/D
            ky = (B-xg)*(0.5*(D*xa**2+h*(b-xa)**2)+h*(B-xa)**2)/Iyy
        k = [kx,ky]
    elif types=='T':
        D = dimensions[0]
        H = dimensions[0]-dimensions[2]
        B = dimensions[1]
        h = dimensions[2]
        b = dimensions[3]
        A = B*h + H*b
        yg = ((H+h/2)*h*B+0.5*(H**2)*b)/A
        Ixx = (b*H**3)/12 + (B*h**3)/12 + (b*H*(yg-0.5*H)**2) + (B*h*(yg-H-0.5*h)**2)
        Iyy = (H*b**3+h*B**3)/12
        if b<(min(D,B)/10) and h<(min(D,B)/10):
            Izz = (B*h**3+(D-0.5*h)*b**3)/3
        else:
            Izz = Ixx+Iyy
        kyy = 0.125*B*(H*b**2+h*B**2)/Iyy
        if 2*B*(D+H)>b*H:
            ya = 0.5*(D+H-b*H/B)
            kxx = (D-ya)*(0.5*(B*((D-ya)**2+(ya-H)**2)+b*H*(2*ya-H)))/Ixx
        else:
            ya = 0.5*(H+B*h/b)
            kxx = (D-ya)*(B*h*(H-ya+0.5*h)+0.5*b*((H-ya)**2+ya**2))/Ixx
        k = [kxx,kyy]
    elif types=='L':
        d = dimensions[0]
        b = dimensions[1]
        t = dimensions[2]
        h = d-t
        A = t*(b+d-t)
        xc = 0.5*(b**2 + d*t - t**2)/(b+d-t)
        yc = 0.5*(d**2 + b*t - t**2)/(b+d-t)
        Ixx = (b*d**3 - (b-t)*(d-t)**3)/3 - A*(d-yc)**2
        Iyy = (d*b**3 - (d-t)*(b-t)**3)/3 - A*(b-xc)**2
        if t<(min(d,b)/10):
            Izz = ((d+b-t)*t**3)/3
        else:
            Izz = Ixx+Iyy
        if d+t>b:
            ya = 0.5*(d+t-b)
            kxx = (d-yc)*(t*(0.5*((d-ya)**2+(ya-t)**2)+b*(ya-0.5*t)**2))/Ixx
        else:
            ya = 0.5*t*(1+h/b)
            kxx = (d-yc)*(0.5*b*(ya**2+(t-ya)**2)+h*t*(d-ya))/Ixx
        if b+t>d:
            xa = 0.5*(b+t-d)
            kyy = (b-xc)*(t*(0.5*((b-xa)**2+(xa-t)**2)+d*(xa-0.5*t)**2))/Iyy
        else:
            xa = 0.5*t*(1+(b-t)/d)
            kyy = (b-yc)*(0.5*d*(xa**2+(t-xa)**2)+(b-t)*t*(b-xa))/Iyy
        k = [kxx,kyy]
    elif types=='Hollow Rectangle':
        H = dimensions[0]
        B = dimensions[1]
        w = dimensions[2]
        h = H-2*w
        b = B-2*w
        A = B*H - b*h
        Ixx = (B*H**3)/12 - (b*h**3)/12
        Iyy = (H*B**3)/12 - (h*b**3)/12
        U = H+B+h+b
        if w<(B/10) and w<(H/10):
            Izz = (U*(w**3))/3 
        else:
            Izz = Ixx+Iyy
        k = [3*B*w*(1+0.5*(H/B))/H*w*(1+3*(B/H))]*2
    elif types=='Hollow Square':
        H = dimensions[0]
        w = dimensions[2]
        h = H-2*w
        A = H**2 - h**2
        Ixx = Iyy = (H**4)/12 - (h**4)/12
        U = 2*(H+h)
        if w<(H/10):
            Izz = (U*(w**3))/3 
        else:
            Izz = 2*Ixx
        k = [1.125]*2
    elif types=='Hollow Circle':
        Do = dimensions[0]
        Di = dimensions[0]-2*dimensions[2]
        A = 0.25*pi*(Do**2-Di**2)
        Ixx = Iyy = (pi*(Do**4-Di**4))/64
        Izz = 2*Ixx
        k = [32*Do*(Do**3-Di**3)/3*pi*(Do**4-Di**4)]*2
    else: 
        raise NameError('Section Not Defined Yet')
    return array([A,Ixx,Iyy,Izz,k[0]])

#segmentMethods: segment Equations
#@jit(nopython=True)
def lineEqn(P1,P3,x):
    return P1 + unit(P3-P1)*x

#@jit(nopython=True)
def arceqn(P1,P3,P2,x):
    span = norm(P3-P1)
    H = span/2
    fv = P2-P1
    uv = P2-P3
    xv = unit(P3-P1)
    cp = dot(fv,xv)
    sp = sqrt(norm(fv)**2-cp**2)
    # sp = sqrt(sum(fv**2)-cp**2)
    K = (sp/2) + (cp*(cp-span))/(2*sp)
    R = sqrt(H**2+K**2)
    yv = unit(cross(cross(fv,uv),xv))
    if(round(norm(P1+cp*xv+sp*yv-P2),10)): 
        yv = -yv
    return P1 + xv*x + (sqrt(R**2-(x-H)**2)+K)*yv

#@jit(nopython=True)
def arcLength(P1,P3,P2,x=None):
    span = norm(P3-P1)
    if(x==None):
        x = span
    H = span/2
    fv = P2-P1
    uv = P2-P3
    xv = unit(P3-P1)
    cp = dot(fv,xv)
    sp = sqrt(norm(fv)**2-cp**2)
    K = (sp/2) + (cp*(cp-span))/(2*sp)
    R = sqrt(H**2+K**2)
    return R*arccos(1-(H*x+K*(sqrt(R**2-(x-H)**2)+K))/(R**2))

def arcSecTheta(P1,P3,P2,x):
    span = norm(P3-P1)
    H = span/2
    fv = P2-P1
    xv = unit(P3-P1)
    cp = dot(fv,xv)
    sp = sqrt(norm(fv)**2-cp**2)
    # sp = sqrt(sum(fv**2)-cp**2)
    K = (sp/2) + (cp*(cp-span))/(2*sp)
    R = sqrt(H**2+K**2)
    return sqrt(1+((H-x)**2)/(R**2-(H-x)**2))
#@jit(nopython=True)
def quadeqn(P1,P3,P2,x):
    span = norm(P3-P1)
    fv = P2-P1
    uv = P2-P3
    xv = unit(P3-P1)
    cp = dot(fv,xv)
    sp = sqrt(norm(fv)**2-cp**2)
    a2 = sp/(cp*(cp-span))
    a1 = -a2*span
    yv = unit(cross(cross(fv,uv),xv))
    if(round(norm(P1+cp*xv+sp*yv-P2),10)): 
        yv = -yv    
    return P1+xv*x+(a1*x + a2*(x**2))*yv

#@jit(nopython=True)
def quadLength(P1,P3,P2,x=None):
    span = norm(P3-P1)
    if(x==None):
        x=span
    fv = P2-P1
    uv = P2-P3
    xv = unit(P3-P1)
    cp = dot(fv,xv)
    sp = sqrt(norm(fv)**2-cp**2)
    a2 = sp/(cp*(cp-span))
    a1 = -a2*span
    def u(x):
        return a1+2*a2*x
    def F(x):
        return (1/(4*a2))*(log(x+sqrt(1+x**2))+x*sqrt(1+x**2))
    return F(u(x))-F(a1)

def quadSecTheta(P1,P3,P2,x):
    span = norm(P3-P1)
    fv = P2-P1
    xv = unit(P3-P1)
    cp = dot(fv,xv)
    sp = sqrt(norm(fv)**2-cp**2)
    a2 = sp/(cp*(cp-span))
    a1 = -a2*span
    return sqrt(1+(a1+2*a2*x)**2)

#segmentMethods : stiffness and transformation
#@jit(nopython=True)
def lineStiffnessLocal(E,Iyy,Izz,L,A=1.0,G=1.0,J=1.0,shear=False,inextensible=False,hinged=False):
    if(shear):
        alphax = (12*E*Iyy)/(A*G*L**2)
        alphay = (12*E*Izz)/(A*G*L**2)
    else:
        alphax=alphay=0
    scalarx = (E*Iyy)/(1+alphax)
    scalary = (E*Izz)/(1+alphay)
    TS = (G*J)/L
    ay = (12/(L**3))*scalarx
    az = (12/(L**3))*scalary
    by = (6/(L**2))*scalarx
    bz = (6/(L**2))*scalary
    cy = ((4+alphax)/L)*scalarx
    cz = ((4+alphay)/L)*scalary
    dy = ((2-alphax)/L)*scalarx
    dz = ((2-alphay)/L)*scalary
    AS = 1e12 if inextensible else (E*A)/L
    mainDiagonal = array([AS,az,ay,TS,cy,cz,AS,az,ay,TS,cy,cz])
    subDiagonal = array([-AS,-az,-ay,-TS,dy,dz])
    mainMatrix = diag(mainDiagonal)
    subMatrix = diag(subDiagonal)
    bindme = zeros((6,6))
    mainMatrix = mainMatrix + vstack((hstack((bindme,subMatrix)),hstack((bindme,bindme))))
    mainMatrix[1,5]=mainMatrix[1,11]=bz
    mainMatrix[2,4]=mainMatrix[2,10]=-by
    mainMatrix[4,8]=mainMatrix[8,10]=by
    mainMatrix[5,7]=mainMatrix[7,11]=-bz
    mainMatrix = mainMatrix+mainMatrix.T
    fill_diagonal(mainMatrix,diag(mainMatrix)/2)

    if(hinged):
        index1 = array([1,2,4,5,7,8])
        index2 = array([10,11])
        K11 = getSubMat(mainMatrix,index1,index1,(6,6))
        # K12 = mainMatrix[repeat(index1,2),tile(index2,6)].reshape((6,2))
        K12 = getSubMat(mainMatrix,index1,index2,(6,2))
        # K21 = mainMatrix[repeat(index2,6),tile(index1,2)].reshape((2,6))
        K21 = getSubMat(mainMatrix,index2,index1,(2,6))
        # K22 = mainMatrix[repeat(index2,2),tile(index2,2)].reshape((2,2))
        K22 = getSubMat(mainMatrix,index2,index2,(2,2))
        Kc = K11 - K12 @ inv(K22) @ K21
        # mainMatrix[repeat(index1,6),tile(index1,6)] = Kc
        setSubMat(mainMatrix,index1,index1,Kc)
        mainMatrix[index2] = mainMatrix[:,index2]=0
    return mainMatrix

#@jit(nopython=True)
def lineTransformation(P1,P3,axisVector,z1=array([0.0,0.0,1.0]),z2=array([0.0,0.0,1.0])):
    x = unit(P3-P1)
    z = axisVector
    y = unit(cross(z,x))
    
    l = vstack((x,y,z))
    zero = zeros((3,3))
    l1 = l @ axes(z1).T
    l2 = l @ axes(z2).T

    return vstack((
        hstack((l1,zero,zero,zero)),
        hstack((zero,l1,zero,zero)),
        hstack((zero,zero,l2,zero)),
        hstack((zero,zero,zero,l2))
        ))
#@jit(nopython=True)

def lineStiffnessGlobal(P1,P3,axisVector,z1,z2,E,Iyy,Izz,L,A=1.0,G=1.0,J=1.0,shear=False,inextensible=False,hinged=False):
    K = lineStiffnessLocal(E,Iyy,Izz,L,A,G,J,shear,inextensible,hinged)
    T = lineTransformation(P1,P3,axisVector,z1,z2)
    return T.T @ K @ T

#@jit(nopython=True)
def lineStiffnessLocal2(E,I,L,A=1.0,G=1e40,shear=False,inextensible=False,hinged=False):
    alpha = (12*E*I)/(A*G*L**2) if shear else 0
    scalar = (E*I)/(1+alpha)
    a = (12/(L**3))*scalar
    b = (6/(L**2))*scalar
    c = ((4+alpha)/L)*scalar
    d = ((2-alpha)/L)*scalar
    A = max(a,b,c,d)*1e7 if inextensible else (E*A)/L
    mainMatrix = array([a,b,-a,b, b,c,-b,d, -a,-b,a,-b, b,d,-b,c]).reshape((4,4))
    if(hinged):
        # K11 = mainMatrix[0:3,0:3].reshape((3,3))
        K11 = getSubMat(mainMatrix,array([0,1,2]),array([0,1,2]),(3,3))
        # K12 = mainMatrix[0:3,3].reshape((3,1))
        K12 = getSubMat(mainMatrix,array([0,1,2]),array([3]),(3,1))
        # K21 = mainMatrix[3,0:3].reshape((1,3))
        K21 = getSubMat(mainMatrix,array([3]),array([0,1,2]),(1,3))
        K22 = mainMatrix[3,3]
        Kc = K11 - (1/K22)*K12 @ K21
        setSubMat(mainMatrix,array([0,1,2]),array([0,1,2]),Kc)
        mainMatrix[3]=mainMatrix[:,3]=0
    # M11 = hstack((array([[A],[0],[0]]),vstack((zeros(2),mainMatrix[0:2,0:2]))))
    # M12 = hstack((array([[-A],[0],[0]]),vstack((zeros(2),mainMatrix[0:2,2:4]))))
    # M21 = hstack((array([[-A],[0],[0]]),vstack((zeros(2),mainMatrix[2:4,0:2]))))
    # M22 = hstack((array([[A],[0],[0]]),vstack((zeros(2),mainMatrix[2:4,2:4]))))
    # mainMatrix = vstack((hstack((M11,M12)),hstack((M21,M22))))
    mat = zeros((6,6))
    mat[0,0] = mat[3,3] = A
    mat[0,3] = mat[3,0] = -A
    setSubMat(mat,array([1,2]),array([1,2]),getSubMat(mainMatrix,array([0,1]),array([0,1]),(2,2)))
    setSubMat(mat,array([1,2]),array([4,5]),getSubMat(mainMatrix,array([0,1]),array([2,3]),(2,2)))
    setSubMat(mat,array([4,5]),array([1,2]),getSubMat(mainMatrix,array([2,3]),array([0,1]),(2,2)))
    setSubMat(mat,array([4,5]),array([4,5]),getSubMat(mainMatrix,array([2,3]),array([2,3]),(2,2)))
    return mat

#@jit(nopython=True)
def lineTransformation2(P1,P3,z1=array([0.0,0.0,1.0]),z2=array([0.0,0.0,1.0])):
    x = unit(P3-P1)
    z = array([1,0,0])
    y = unit(cross(z,x))
    
    l = vstack((x,y,z))
    zero = zeros((3,3))

    g1 = axes(z1)
    g1 = vstack((g1[1],g1[2],g1[0]))
    g2 = axes(z2)
    g2 = vstack((g2[1],g2[2],g2[0]))
    l1 = l @ g1.T
    l2 = l @ g2.T
    
    return vstack(( hstack(( l1,zero)),
                    hstack(( zero,l2)) ))

#@jit(nopython=True)
def lineStiffnessGlobal2(P1,P3,z1,z2,E,I,L,A=1.0,G=1e40,shear=False,inextensible=False,hinged=False):
    K = lineStiffnessLocal2(E,I,L,A,G,shear,inextensible,hinged)
    T = lineTransformation2(P1,P3,z1,z2)
    return T.T @ K @ T

#@jit(nopython=True)
def lineStiffnessLocalTruss(E,A,L):
    return (E*A/L)*array(((1.0,-1.0),(-1.0,1.0)))

#@jit(nopython=True)
def lineTransformationTruss(P1,P3,z1=array([0.0,0.0,1.0]),z2=array([0.0,0.0,1.0])):
    x = unit(P3-P1)
    zero = zeros(3)
    l1 = x @ axes(z1).T
    l2 = x @ axes(z2).T
    return vstack(( hstack((l1,zero)),
                    hstack((zero,l2)) ))

#@jit(nopython=True)
def lineStiffnessGlobalTruss(P1,P3,z1,z2,E,A,L):
    K = lineStiffnessLocalTruss(E,A,L)
    T = lineTransformationTruss(P1,P3,z1,z2)
    return T.T @ K @ T

#@jit(nopython=True)
def lineTransformationTruss2(P1,P3,z1=array([0.0,0.0,1.0]),z2=array([0.0,0.0,1.0])):
    x = unit(P3-P1)
    zero = zeros(2)
    l1 = x @ axes(z1).T
    l2 = x @ axes(z2).T
    return vstack(( hstack((l1[1:3],zero)),
                    hstack((zero,l2[1:3])) ))

#@jit(nopython=True)
def lineStiffnessGlobalTruss2(P1,P3,z1,z2,E,A,L):
    K = lineStiffnessLocalTruss(E,A,L)
    T = lineTransformationTruss2(P1,P3,z1,z2)
    return T.T @ K @ T
# lineStiffnessGlobalTruss2(array([0.0,0.0,0.0]),array([0.0,10.0,0.0]),array([0.0,0.0,1.0]),array([0.0,0.0,1.0]),1.0,1.0,1.0)

#segmentMethods : others
#@jit(nopython=True)
def smoothen(x,a):
    t = arange(x.size-1)
    Reduce = lambda x,y : array([0.5*(x+y),0.5*(x+y)])
    for i in t:
        if x[i]==x[i+1]:
            a[i:i+2] = Reduce(a[i],a[i+1])

#oadMethods : action breakdown
#@jit(nopython=True)
def linePointForceX(A,B,X,peak,normal,x):
    a = dot(X-A,unit(B-A))
    return peak*ustep(x-a)*normal

#@jit(nopython=True)
def lineMomentForceX(x):
    return zeros(3)

#@jit(nopython=True)
def linePolyForceX(A,B,X,Y,degree,peak,normal,x):
    a = dot(X-A,unit(B-A))
    l = norm(Y-X)
    def scalar(x):
        return ((peak/(l**degree))*x**(1+degree))/(1+degree)
    return (scalar(x-a)*(ustep(x-a)-ustep(x-a,l))+scalar(l)*ustep(x-a,l))*normal

#@jit(nopython=True)
def linePolyForceXNeg(A,B,X,Y,degree,peak,normal,x):
    a = dot(Y-A,unit(B-A))
    l = norm(Y-X)
    def scalar(x):
        return ((peak/(l**degree))*(l**(1+degree) - (l-x)**(1+degree)))/(1+degree)
    return (scalar(x-a)*(ustep(x-a)-ustep(x-a,l))+scalar(l)*ustep(x-a,l))*normal

#@jit(nopython=True)
def linePointMomentX(A,B,X,peak,normal,x):
    a = dot(X-A,unit(B-A))
    return cross(X-lineEqn(A,B,x),peak*normal)*ustep(x-a)

#@jit(nopython=True)
def lineMomentMomentX(A,B,X,peak,normal,x):
    a = dot(X-A,unit(B-A))
    return peak*ustep(x-a)*normal

#@jit(nopython=True)
def linePolyMomentX(A,B,X,Y,degree,peak,normal,x):
    a = dot(X-A,unit(B-A))
    l = norm(Y-X)
    def scalar(x):
        return (peak/l**degree)*(x**(2+degree))/((degree+1)*(degree+2))
        # return dot((linePolyForceX(A,B,X,Y,degree,peak,normal,x+a)*x)/(2+degree),normal)
    vt = cross(normal,unit(B-A))
    return (scalar(x-a)*(ustep(x-a)-ustep(x-a,l))+
             (scalar(l)/l)*((2+degree)*(x-a)-(1+degree)*l)*ustep(x-a,l))*vt

#@jit(nopython=True)
def linePolyMomentXNeg(A,B,X,Y,degree,peak,normal,x):
    a = dot(Y-A,unit(B-A))
    l = norm(Y-X)
    def scalar(x):
        # return dot((linePolyForceXNeg(A,B,X,Y,degree,peak,normal,x+a)*(l-x))/(2+degree),normal)
        return (peak/l**degree)*((l**(degree+1)*x)/(1+degree)+((l-x)**(degree+2)-l**(degree+2))/((1+degree)*(2+degree)))
    vt = cross(normal,unit(B-A))
    return (scalar(x-a)*(ustep(x-a)-ustep(x-a,l))+
            (scalar(l) + (peak*l**(1+degree)*(x-a-l))/(l**degree*(1+degree)))*ustep(x-a,l))*vt

#loadMethods: response breakdown
#@jit(nopython=True)
def linePointAngleX(A,B,X,peak,normal,youngsModulus,Iyy,Izz,axisVector,x):
    a = dot(X-A,unit(B-A))
    return array([0,
                    -((dot(cross(X-lineEqn(A,B,x),peak*normal)*ustep(x-a),cross(unit(B-A),axisVector))*(x-a))/(2*youngsModulus*Iyy)),
                    -((dot(cross(X-lineEqn(A,B,x),peak*normal)*ustep(x-a),axisVector)*(x-a))/(2*youngsModulus*Izz))])

#@jit(nopython=True)
def lineMomentAngleX(A,B,X,peak,normal,youngsModulus,shearModulus,Iyy,Izz,J,axisVector,x):
    a = dot(X-A,unit(B-A))
    return array([(dot(peak*ustep(x-a)*normal,unit(B-A))*(x-a))/(shearModulus*J),
           -((dot(peak*ustep(x-a)*normal,cross(unit(B-A),axisVector))*(x-a))/(youngsModulus*Iyy)),
           -((dot(peak*ustep(x-a)*normal,axisVector)*(x-a))/(youngsModulus*Iyy))])

#@jit(nopython=True)
def linePolyAngleX(A,B,X,Y,degree,peak,normal,youngsModulus,Iyy,Izz,axisVector,x):
    a = dot(X-A,unit(Y-X))
    l = norm(Y-X)
    # def Mzz(x):
    #     return dot(linePolyMomentX(A,B,X,Y,degree,peak,normal,x),axisVector)
    # def Myy(x):
    #     return dot(linePolyMomentX(A,B,X,Y,degree,peak,normal,x),cross(unit(B-A),axisVector))
    
    def thetaY(x):
        def scalar(x):
            return (((peak*dot(cross(normal,unit(B-A)),cross(unit(B-A),axisVector)))/l**degree)*x**(degree+3))/((degree+1)*(degree+2)*(degree+3))
            # return (Myy(t+a)*t)/(degree+3)
        value1 = scalar(x-a)
        value2 = (scalar(l)/(l**2))*(((degree+2)*(degree+3)/2)*(x-a)**2-l*(degree+1)*(degree+3)*(x-a)+(l**2)*((degree+1)*(degree+2)/2))
        return -(value1*(ustep(x-a)-ustep(x-a,l))+value2*ustep(x-a,l))/(youngsModulus*Iyy)

    def thetaZ(x):
        def scalar(x):
            return (((peak*dot(cross(normal,unit(B-A)),axisVector))/l**degree)*x**(degree+3))/((degree+1)*(degree+2)*(degree+3))
            # return (Mzz(t+a)*t)/(degree+3)
        value1 = scalar(x-a)
        value2 = (scalar(l)/(l**2))*(((degree+2)*(degree+3)/2)*(x-a)**2-l*(degree+1)*(degree+3)*(x-a)+(l**2)*((degree+1)*(degree+2)/2))
        return -(value1*(ustep(x-a)-ustep(x-a,l))+value2*ustep(x-a,l))/(youngsModulus*Izz)
    
    return array([0,thetaY(x),thetaZ(x)])

#@jit(nopython=True)
def linePolyAngleXNeg(A,B,X,Y,degree,peak,normal,youngsModulus,Iyy,Izz,axisVector,x):
    l = norm(Y-X)
    s = array([0.0,0.0,0.0])
    for r in range(degree+1):
        s = s + linePolyAngleX(A,B,Y,X,r,peak*(-1)**r*comb(degree,r),normal,youngsModulus,Iyy,Izz,axisVector,x)
    return s

#@jit(nopython=True)
def linePointDisplaceX(A,B,X,peak,normal,youngsModulus,shearModulus,Iyy,Izz,axisVector,area,shapeFactor,x):
    a = dot(X-A,unit(B-A))

    def thY(x):
        return linePointAngleX(A,B,X,peak,normal,youngsModulus,Iyy,Izz,axisVector,x)[1]
    def thZ(x):
        return linePointAngleX(A,B,X,peak,normal,youngsModulus,Iyy,Izz,axisVector,x)[2]
    def Fxx(x):
        return dot(linePointForceX(A,B,X,peak,normal,x),unit(B-A))
    
    def Myy(x):
        return dot(linePointMomentX(A,B,X,peak,normal,x),axisVector)
    def Mzz(x):
        return dot(linePointMomentX(A,B,X,peak,normal,x),cross(unit(B-A),axisVector))

    return array([(Fxx(x)*(x-a))/(youngsModulus*area),
                        (thZ(x)*(x-a))/3 + (shapeFactor[0]/(shearModulus*area))*Mzz(x),
                        (thY(x)*(x-a))/3 + (shapeFactor[1]/(shearModulus*area))*Myy(x)])

#@jit(nopython=True)
def lineMomentDisplaceX(A,B,X,peak,normal,youngsModulus,shearModulus,Iyy,Izz,J,axisVector,x):
    a = dot(X-A,unit(B-A))
    delta = lineMomentAngleX(A,B,X,peak,normal,youngsModulus,shearModulus,Iyy,Izz,J,axisVector,x)*(x-a)/2
    return delta*array([0,1,1])

#@jit(nopython=True)
def linePolyDisplaceX(A,B,X,Y,degree,peak,normal,youngsModulus,shearModulus,Iyy,Izz,axisVector,area,shapeFactor,x):
    a = dot(X-A,unit(B-A))
    l = norm(Y-X)
    # def thY(x):
    #     return linePolyAngleX(A,B,X,Y,degree,peak,normal,youngsModulus,Iyy,Izz,axisVector,x)[1]
    # def thZ(x):
    #     return linePolyAngleX(A,B,X,Y,degree,peak,normal,youngsModulus,Iyy,Izz,axisVector,x)[2]

    def deltaX(x):
        def scalar(x):
            return (dot(linePolyForceX(A,B,X,Y,degree,peak,normal,x+a),unit(B-A))*x)/(degree+2)
        value1 = scalar(x-a)
        value2 = (scalar(l)/l)*((degree+2)*(x-a)-(degree+1)*l)
        return (value1*(ustep(x-a)-ustep(x-a,l))+value2*(ustep(x-a,l)))/(youngsModulus*area)

    def deltaY(x):
        def scalar(x):
            return -(((peak*dot(normal,cross(unit(B-A),axisVector)))/l**degree)*x**(degree+4))/((degree+1)*(degree+2)*(degree+3)*(degree+4)*youngsModulus*Iyy)
        value1 = scalar(x-a)
        C1 = (scalar(l)*(degree+1)*(degree+2)*(degree+4))/(2*l)
        C2 = -(scalar(l)*(degree+1)*(degree+3)*(degree+4))/(l**2)
        C3 = (scalar(l)*(degree+2)*(degree+3)*(degree+4))/(2*l**3)
        value2 = scalar(l) + (C1+C2*l+C3*l**2)*(x-a-l) + ((C2+2*C3*l)/2)*(x-a-l)**2 + (C3/3)*(x-a-l)**3
        return value1*(ustep(x-a)-ustep(x-a,l))+value2*(ustep(x-a,l)) + (shapeFactor[0]/(shearModulus*area))*dot(linePolyMomentX(A,B,X,Y,degree,peak,normal,x),axisVector)

    def deltaZ(x):
        def scalar(x):
            # return (thY(x+a)*x)/(degree+4)
            return -(((peak*dot(normal,axisVector))/l**degree)*x**(degree+4))/((degree+1)*(degree+2)*(degree+3)*(degree+4)*youngsModulus*Izz)
        value1 = scalar(x-a)
        C1 = (scalar(l)*(degree+1)*(degree+2)*(degree+4))/(2*l)
        C2 = -(scalar(l)*(degree+1)*(degree+3)*(degree+4))/(l**2)
        C3 = (scalar(l)*(degree+2)*(degree+3)*(degree+4))/(2*l**3)
        value2 = scalar(l) + (C1+C2*l+C3*l**2)*(x-a-l) + ((C2+2*C3*l)/2)*(x-a-l)**2 + (C3/3)*(x-a-l)**3
        return value1*(ustep(x-a)-ustep(x-a,l))+value2*(ustep(x-a,l)) + (shapeFactor[1]/(shearModulus*area))*dot(linePolyMomentX(A,B,X,Y,degree,peak,normal,x),cross(unit(B-A),axisVector))

    return array([deltaX(x),deltaY(x),deltaZ(x)])

#@jit(nopython=True)
def linePolyDisplaceXNeg(A,B,X,Y,degree,peak,normal,youngsModulus,shearModulus,Iyy,Izz,axisVector,area,shapeFactor,x):
    s = array([0.0,0.0,0.0])
    for r in range(degree+1):
        s = s + linePolyDisplaceX(A,B,Y,X,r,peak*(-1)**r*comb(degree,r),normal,youngsModulus,shearModulus,Iyy,Izz,axisVector,area,shapeFactor,x)
    return s

#loadMethods : FEAs
#@jit(nopython=True)
# def lineTempGlobalFEA(A,B,X,Y,z1=array([0.0,0.0,1.0]),z2=array([0.0,0.0,1.0]),peak=1.0,axisVector=array([0.0,0.0,1.0]),normal=array([0.0,0.0,1.0]),youngsModulus=1.0,area=1.0,alpha=1.0,Iyy=1.0,Izz=1.0,hinged=False):
#     xv = unit(B-A)
#     yv = unit(cross(axisVector,xv))
#     if all(normal==axisVector):
#         I = Izz
#         tempLow = X[0]-X[2]
#         tempHigh = Y[0]-Y[2]
#         momAxis = yv
#     else:
#         I = Iyy
#         tempLow = X[0]-X[1]
#         tempHigh = Y[0]-Y[1]
#         momAxis = axisVector
#     forceMagnitude = 0.5*(tempHigh+tempLow)*alpha*youngsModulus*area
#     momentMagnitude = alpha*youngsModulus*I*(tempHigh-tempLow)/peak
#     return hstack((-forceMagnitude*xv,momentMagnitude*momAxis,forceMagnitude*xv,-momentMagnitude*momAxis))

def linePointGlobalFEA(A,B,X,z1=array([0.0,0.0,1.0]),z2=array([0.0,0.0,1.0]),peak=1.0,axisVector=array([1.0,0.0,0.0]),normal=array([0.0,0.0,-1.0]),hinged=False):
    i = unit(B-A)
    j = cross(axisVector,i)
    
    a = dot(X-A,i)
    l = norm(B-A)
 
    P = peak*normal
    Pi = dot(P,i)
    Pj = dot(P,j)
    Pk = dot(P,axisVector)
    
    Pt = Pi*i
    Pn = Pj*j+Pk*axisVector
    
    if norm(Pn)!=0:
        ncap = cross(P,i)
    else:
        ncap = array([0.0,0.0,0.0])
    
    MA = ((((l-a)**2)*a)/l**2)*ncap
    MB = -((a**2*(l-a))/l**2)*ncap
    nc = ((a**3+3*a**2*(l-a))/(l**3))*Pn

    if hinged:
        MA = MA-MB/2
        MB= array([0.0]*3)
        nc = ((a**3+1.5*a**2*(l-a))/(l**3))*Pn

    FB = -nc - (a/l)*Pt
    FA = -P-FB

    zeroes = zeros((3,3))
    T = vstack(( hstack((axes(z1),zeroes,zeroes,zeroes)),
                 hstack((zeroes,axes(z1),zeroes,zeroes)),
                 hstack((zeroes,zeroes,axes(z2),zeroes)),
                 hstack((zeroes,zeroes,zeroes,axes(z2))) ))
    FEA = hstack((FA,MA,FB,MB))
    return T @ FEA

#@jit(nopython=True)
def lineMomentGlobalFEA(A,B,X,z1=array([0.0,0.0,1.0]),z2=array([0.0,0.0,1.0]),peak=1.0,axisVector=array([1.0,0.0,0.0]),normal=array([1.0,0.0,0.0]),hinged=False):
    i = unit(B-A)
    j = cross(axisVector,i)
    
    a = dot(X-A,i)
    l = norm(B-A)
 
    M = peak*normal
    Mi = dot(M,i)
    Mj = dot(M,j)
    Mk = dot(M,axisVector)
    Mt = Mi*i
    Mn = Mj*j+Mk*axisVector
    
    MA = (-1+4*(a/l)-3*(a/l)**2)*Mn-Mt*(1-a/l)
    MB = ((a/l)*(2-3*(a/l)))*Mn-Mt*(a/l)
    if(hinged):
        MA=MA-MB/2
        MB=-Mt*(a/l)
    
    if norm(Mn)!=0:
        ncap = unit(cross(Mn,i))
    else:
        ncap = zeros(3)
    FA = 6*peak*a*(l-a)/(l**3)*ncap
    FB = -FA

    zeroes = zeros((3,3))
    T = vstack(( hstack((axes(z1),zeroes,zeroes,zeroes)),
                 hstack((zeroes,axes(z1),zeroes,zeroes)),
                 hstack((zeroes,zeroes,axes(z2),zeroes)),
                 hstack((zeroes,zeroes,zeroes,axes(z2))) ))
    FEA = hstack((FA,MA,FB,MB))
    return T @ FEA

#@jit(nopython=True)
def linePolyGlobalFEAPlus(A,B,X,Y,z1=array([0.0,0.0,1.0]),z2=array([0.0,0.0,1.0]),degree=0,peak=1.0,axisVector=array([1.0,0.0,0.0]),normal=array([1.0,0.0,0.0]),hinged=False):
    i = unit(B-A)
    k = axisVector
    j = cross(k,i)
    
    a = dot(X-A,i)
    b = dot(Y-A,i)
    l = norm(B-A)

    w = peak/(norm(Y-X)**degree)
    P = (w/(degree+1))*((b-a)**(degree+1))*normal
    act = a+(b-a)*(degree+1)/(degree+2)
    Pt = dot(P,i)*i
    Pn = P - Pt
    if norm(Pn):
        value1 = lambda x: (w/l**2)*(((l**2)*x**(degree+2))/(degree+2)-(2*l*x**(degree+3))/(degree+3)+(x**(degree+4))/(degree+4))
        value2 = lambda x: (w/l**2)*((l*x**(degree+3))/(degree+3)-(x**(degree+4))/(degree+4))
        MA = (value1(b)-value1(a))*cross(normal,i)
        MB = -(value2(b)-value2(a))*cross(normal,i)
        if(hinged):
            MA = MA-MB/2
            MB = zeros(3)
        moment = dot(cross(i,MA+MB),unit(Pn))
        nc = -(moment/l)*unit(Pn)+Pn*(act/l)
        FBn = -nc
        FAn = -Pn-FBn
    
    else: 
        FAn = FBn = MA = MB = zeros(3)
    
    FBt = -Pt*act/l
    FAt = -Pt-FBt
    FA = FAt + FAn
    FB = FBt + FBn

    zeroes = zeros((3,3))
    T = vstack(( hstack((axes(z1),zeroes,zeroes,zeroes)),
                 hstack((zeroes,axes(z1),zeroes,zeroes)),
                 hstack((zeroes,zeroes,axes(z2),zeroes)),
                 hstack((zeroes,zeroes,zeroes,axes(z2))) ))
    FEA = hstack((FA,MA,FB,MB))
    return T @ FEA

def linePolyGlobalFEA(A,B,X,Y,z1=array([0.0,0.0,1.0]),z2=array([0.0,0.0,1.0]),degree=0,peak=1.0,axisVector=array([1.0,0.0,0.0]),normal=array([1.0,0.0,0.0]),hinged=False):
    if dot(B-A,Y-X)<0:
        A,B = B,A
        FEA = linePolyGlobalFEAPlus(A,B,X,Y,z1,z2,degree,peak,axisVector,normal,hinged)
        return hstack((FEA[6:],FEA[:6]))
    else:
        return linePolyGlobalFEAPlus(A,B,X,Y,z1,z2,degree,peak,axisVector,normal,hinged)

if __name__=='__main__':
    jit_module(nopython=True,cache=True)