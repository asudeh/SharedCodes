#Abolfazl Asudeh Fab. 2018
#       http://asudeh.github.io

import numpy as np
import math;
from sets import Set;
import heapq;
from heapq import *;
import basestuff;

heap = []
visited = None
ksets = None

def FindRanges(debug = False,findksets=False): # tested
    global heap, visited, ksets
    n = basestuff.n; k = basestuff.k;
    heap = []; visited = set();
    b = [-1 for i in range(n)]; e = b[:];
    Lp = sorted(list(range(n)),cmp = lambda x,y: cmp(basestuff.dataset[x][0], basestuff.dataset[y][0]), reverse=True); # sort by x descendingly
    for i in range(k): b[Lp[i]] = 0; # 0 degree angle
    if findksets:
        ksets = set([frozenset(Lp[0:k])])
    L = [0 for i in range(n)]
    for i in range(n): L[Lp[i]] = i; # create the "hash" of the sorted list
    for i in range(n-1):
        checkNadd(Lp[i],Lp[i+1])
    while len(heap)>0:
        (theta,i) = heappop(heap)
        j = L[i] # the index of t[i] in the ordered list Lp
        if j == k-1:
            if b[Lp[k]] == -1:
                b[Lp[k]] = theta
            e[Lp[k-1]] = theta
        # swap Lp[j] and Lp[j+1]
        L[Lp[j+1]] -= 1; # decrease the index of the item in position j+1 of the ordered list
        L[i] += 1
        Lp[j] = Lp[j+1]
        Lp[j+1] = i
        if findksets and j == k-1:
            ksets.add(frozenset(Lp[0:k]))
        if j>0: checkNadd(Lp[j-1],Lp[j])
        if j+2<n: checkNadd(Lp[j+1],Lp[j+2])
    for i in range(k): e[Lp[i]] = math.pi/2.
    #print '-------------'
    #print b
    #print e
    return (b,e)

def twoDRRR(debug = False,findksets=False):
    n = basestuff.n;
    (b,e) = FindRanges(debug,findksets)
    psi = []
    U = [[0,0],[math.pi/2.,1]] # initially the range is this
    ids = set([i for i in range(n) if b[i]!=-1])
    while len(U)>0:
        covm = -1; t=-1; toremove=set()
        for i in ids:
            k = bsearch(U,b[i]);
            if U[k][1] == 1:
                cov = min(U[k][0], e[i]) - b[i]
            else:
                cov = max(0, e[i] - U[k][0])
            if cov == 0:
                toremove.add(i)
            elif cov > covm:
                t = i; covm = cov; km = k
        if t == -1:
            # this should never happen
            return "ERROR"
        psi.append(t)
        toremove.add(t)
        ids = ids-toremove
        if U[km][1] == 0:
            if U[km+1][0] <= e[t]:
                del(U[km+1])
                del(U[km])
            else:
                U[km][0] = e[t]
        else:
            if U[km][0] > e[t]:
                U.insert(km,[b[t],1])
                U.insert(km+1,[e[t],0])
            else:
                U[km][0] = b[t]
    return psi

def maxk(theSet):
    n = basestuff.n;
    heap = []; mk = 0;
    S = list(theSet)
    Lp = sorted(list(range(n)),cmp = lambda x,y: cmp(basestuff.dataset[x][0], basestuff.dataset[y][0]), reverse=True); # sort by x descendingly
    L = [0 for i in range(n)]
    for i in range(n): L[Lp[i]] = i; # create the "hash" of the sorted list
    for i in range(n-1):
        checkNadd(Lp[i],Lp[i+1])
    while len(heap)>0:
        (theta,i) = heappop(heap)
        j = L[i] # the index of t[i] in the ordered list Lp
        k = min([L[s] for s in S])
        if k>mk: mk = k
        # swap Lp[j] and Lp[j+1]
        L[Lp[j+1]] -= 1; # decrease the index of the item in position j+1 of the ordered list
        L[i] += 1
        Lp[j] = Lp[j+1]
        Lp[j+1] = i
        if j>0: checkNadd(Lp[j-1],Lp[j])
        if j+2<n: checkNadd(Lp[j+1],Lp[j+2])
    k = min([L[s] for s in S])
    if k>mk: mk = k
    return mk

def bsearch(U,val): #test this function
    beg = 0; end = len(U)-1
    while beg+1<end:
        mid = (beg+end)/2
        if U[mid]<val: beg = mid
        else: end = mid
    if U[beg][0]>=val:
        return beg
    return end

def checkNadd(i,j):
    global heap, visited
    if basestuff.dataset[i][1] < basestuff.dataset[j][1] or basestuff.dataset[i][1]<basestuff.dataset[j][1]:
            if (i,j) in visited: return
            heappush(heap,(math.atan((basestuff.dataset[j][0] - basestuff.dataset[i][0])/(basestuff.dataset[i][1] - basestuff.dataset[j][1])), i))
            visited.add((i,j))