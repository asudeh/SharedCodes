#Copr.: Abolfazl Asudeh Fab. 2018
#       http://asudeh.github.io

import numpy as np
from sets import Set
import math
import MyLPSolver
import basestuff
import math

Ksets=None
boundries=None

def UniqueID(ids,n):
    ids = ids[ids.argsort(-1)]
    return str(ids)

def Kset_Enum():
    global Ksets;
    id = np.arange(basestuff.n).reshape(basestuff.n,1)
    Ksets = Set()
    #nc = np.ones(basestuff.n)
    #for i in range(basestuff.n):
    #    for j in range(basestuff.d):
    #        nc[i]+=basestuff.dataset[i,j]*f[j]
    #tmp = np.concatenate((id,nc.reshape(n,1)), axis=1)
    #tmp =  tmp[tmp[:, 1].argsort()] # the higher the better
    #UID =  UniqueID(tmp[0:k,0],n)
    #Ksets.add(UID)
    tmp = basestuff.top_k([0 for i in range(basestuff.d - 1)])
    tmp = frozenset([tmp[i][0] for i in range(basestuff.k)])
    Ksets.add(tmp)
    _Kset_Enum(tmp)
    return list(Ksets)


def _Kset_Enum(s):
    global Ksets;
    tmp = list(s)
    for i in range(basestuff.k):
        tmp2 = tmp[i]
        for j in range(basestuff.n):
            if j in s: continue
            tmp[i]=j;
            if(isValid(frozenset(tmp))):
                Ksets.add(frozenset(tmp))
                _Kset_Enum(frozenset(tmp))
        tmp[i] = tmp2

def isValid(tmp):
    global Ksets,boundries;
    if tmp in Ksets: return False
    A_ub=None; b_u=[]
    for i in range(basestuff.n):
        if i in tmp:
            A_ub = np.append(A_ub,[[basestuff.dataset[i][k] for k in range(basestuff.d)]], axis=0) if A_ub is not None else np.array([[basestuff.dataset[i][k] for k in range(basestuff.d)]])
            b_u = np.append(b_u, 0)
            continue
        A_ub = np.append(A_ub,[[-basestuff.dataset[i][k] for k in range(basestuff.d)]], axis=0) if A_ub is not None else np.array([[-basestuff.dataset[i][k] for k in range(basestuff.d)]])
        b_u = np.append(b_u, 0)
    (status,x) = MyLPSolver.solve(A_ub=A_ub,b_ub=b_u,bnds=boundries)
    return status


def Kset_random(threshold=100):
    global Ksets;
    n = basestuff.n; d = basestuff.d
    id = np.arange(basestuff.n).reshape(basestuff.n,1)
    Ksets = Set()
    new = 0; iter = 0; stopiter = n*math.log(n,2)
    while new<threshold: #or iter<=stopiter:
        w = np.absolute(np.random.randn(d))
        #s = frozenset(basestuff.top_k(w,isweight=True))
        s = tuple(sorted(basestuff.top_k(w,isweight=True)))
        if s not in Ksets:
            Ksets.add(s)
            new=0
        else:
            new+=1
        iter+=1
    return list(Ksets)