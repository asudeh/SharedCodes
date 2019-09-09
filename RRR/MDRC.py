#Abolfazl Asudeh Feb. 2018
#       http://asudeh.github.io

import numpy as np
import math;
from sets import Set;
import heapq;
from heapq import *;
import itertools

import basestuff;

comb = None
comb2 = None
corners = None

def MDRC():
    global comb, comb2, corners
    comb = list(itertools.product([0, 1], repeat=basestuff.d - 1))
    comb2 = list(itertools.product([0, 1], repeat=basestuff.d - 2))
    corners = dict()
    dp = basestuff.d -1
    tmp = list(range(dp))
    for c in comb:
        for j in range(dp):
            tmp[j] = c[j]*math.pi/2
        s = tuple(tmp)
        corners[s] = basestuff.top_k(tmp)
    # R = [[0,math.pi/2] for i in range(dp)]
    R = np.append(np.zeros(dp).reshape(dp,1),(np.ones(dp)*math.pi/2).reshape(dp,1),1)
    return _MDRC(0,R)



def _MDRC(l,R): # l: level, R: cube region
    global comb, comb2, corners
    # border condition
    dp = basestuff.d-1;
    s = set(corners[ tuple([(1-comb[0][j])*R[j][0] + comb[0][j]*R[j][1] for j in range(dp)]) ])
    for i in range(1,len(comb)):
        s.intersection_update(corners[ tuple([(1-comb[i][j])*R[j][0] + comb[i][j]*R[j][1] for j in range(dp)]) ])
        if len(s)==0: break
    if len(s)>0:
        return set([next(iter(s))])
    i = l%dp
    mid = (R[i][0] + R[i][1])/2.
    # find the top-k of new corners
    for c in comb2:
        tmp = list([0 for j in range(dp)])
        for j in range(i):
            tmp[j] = (1-c[j])*R[j][0] + c[j]*R[j][1]
        tmp[i] = mid
        for j in range(i+1,dp):
            tmp[j] = (1-c[j-1])*R[j][0] + c[j-1]*R[j][1]
        s = tuple(tmp)
        if s not in corners:
            corners[s] = basestuff.top_k(tmp)
    # apply the recursion
    lR = R.copy(); rR = R.copy();
    lR[i][1] = mid;
    rR[i][0]=mid;
    return _MDRC(l+1,lR).union(_MDRC(l+1,rR))
