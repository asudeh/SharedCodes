#Copr.: Abolfazl Asudeh Fab. 2018
#       http://asudeh.github.io

import KsetEnum
from KsetEnum import *
from time import time

M = None
ids = None

def maxk_rand(theSet,iter):
    n = basestuff.n; d = basestuff.d
    id = np.arange(basestuff.n).reshape(basestuff.n,1)
    max = 0; i=0
    for i in range(iter): #or iter<=stopiter:
        w = np.absolute(np.random.randn(d))
        s = sorted([[j,basestuff.score(j, w)] for j in range(n)], cmp = lambda x,y: cmp(x[1], y[1]), reverse=True)
        k = n
        for j in range(n):
            if s[j][0] in theSet:
                k = j
                break
        if k>max: max = k
    return max

def MDRRR(randkset=True, RandStopTh = 100, ksets = None, turnonlog = False):
    global M,ids;
    n = basestuff.n;
    ids = np.array(range(n)).reshape(n,1)
    stats = ""
    if ksets == None:
        t = time()
        ksets = Kset_random()
        #ksets = Kset_random(RandStopTh) if randkset else Kset_Enum()
        stats += str(time()-t)
    # M = np.append(np.zeros(n,len(ksets)),ids,axis=1)
    if turnonlog:
        st = str(basestuff.d)+','+str(basestuff.k)+','+str(len(ksets))+','+stats
        basestuff.mylog(st,'results/MDRRRlog.csv')
    M = np.zeros(n*len(ksets)).reshape(n,len(ksets))
    for j in range(len(ksets)):
        for i in ksets[j]:
            M[i,j] = 1
    Indx = ~np.all(M == 0, axis=1)
    M = M[Indx]; ids = ids[Indx]
    return _HSN(),stats

def _HSN():
    global M,ids;
    n = basestuff.n;
    selected = []
    while( len(M)>0):
        maxR = M.sum(axis=0).argmax()
        selected.append(ids[maxR][0])
        M = M[:,M[maxR]==0]
        Indx = ~np.all(M == 0, axis=1)
        M = M[Indx]; ids = ids[Indx]
    return selected