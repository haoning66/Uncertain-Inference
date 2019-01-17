import argparse
import random
import collections
from copy import deepcopy
from xmlparser import *


# def parser(filename):
#     tree = et.parse(filename)
#     root = tree.getroot()
#     bn = {}
#     vars = []
#
#     if root.tag == 'BIF':
#         root = root[0]
#         if root.tag == 'NETWORK':
#             for i in range(1, len(root)):
#                 if root[i].tag == 'VARIABLE':
#                     vars.append(root[i][0].text)
#                     bn.update({root[i][0].text:[[],[]]})
#                 elif root[i].tag == 'DEFINITION':
#                     for j in range(0,len(root[i])):
#                         if root[i][j].tag == 'FOR':
#                             var = root[i][j].text
#                             if len(root[i]) == 2:
#                                 if root[i][1].tag == 'TABLE':
#                                     val= float(root[i][1].text.split(' ')[0])
#                                     bn.update({var:[[],[val]]})
#                                     #print bn
#                             elif len(root[i])!=2:
#                                 for k in range(1,len(root[i])):
#                                     if root[i][k].tag == 'GIVEN':
#                                         bn[root[i][0].text][0].append(root[i][k].text)
#                                     elif root[i][k].tag == 'TABLE':
#                                         list = root[i][k].text.strip().split('\n')
#                                         #print root[i][k].text.strip().split('\n')
#                                         if len(list) > 1:
#                                             for x in list:
#                                                 bn[root[i][0].text][1].append(float(x.strip().split(' ')[0]))
#                                         elif len(list) == 1:
#                                             list2 = list[0].split(' ')
#                                             if '' in list2:
#                                                 list2.remove('')
#                                             for n in range(0,len(list2)):
#                                                 if n%2 ==0:
#                                                     bn[root[i][0].text][1].append(float(list2[n]))
#     return bn,vars


def topo(bn,vars):
    varsTopo = []
    Vars = []
    for var in vars:
        if len(bn[var][0]) == 0:
            varsTopo.append(var)
        else: Vars.append(var)
    while len(Vars) != 0:
        for Var in Vars:
            k = 0
            for varstopo in varsTopo:
                if varstopo in bn[Var][0]:
                    k += 1
            if k == len(bn[Var][0]):
                varsTopo.append(Var)
                Vars.remove(Var)
    return varsTopo


def normalize(Qx):
    a = Qx['T']
    b = Qx['F']
    c = round(a/(a+b),4)
    d = round(b/(a+b),4)
    qx = {'T':c,'F':d}
    return qx


def likelihood_weighting(X,e,bn,N):
    W = {'T':0,'F':0}
    for i in range(1,N+1):
        x,w = weighted_sample(bn,e)
        if x[X] == 'T':
            W['T'] += w
        elif x[X] == 'F':
            W['F'] += w
    return normalize(W)


def weighted_sample(BN,e):
    w = 1.0
    x = collections.OrderedDict()
    bn = BN[0]
    vars = topo(BN[0],BN[1])
    for value1 in vars:
        x.update({value1:'N'})
    for value2 in e.keys():
        x.update({value2:e[value2]})
    for Xi in x.keys():
        if e.has_key(Xi):
            if len(bn[Xi][0]) == 0:
                if x[Xi] == 'T':
                    p = float(bn[Xi][1][0])
                elif x[Xi] == 'F':
                    p = float(1-bn[Xi][1][0])
            elif len(bn[Xi][0]) == 1:
                par1 = bn[Xi][0][0]
                if x[Xi] == 'T':
                    if x[par1] == 'T':
                        p = float(bn[Xi][1][0])
                    elif x[par1] == 'F':
                        p = float(bn[Xi][1][1])
                elif x[Xi] == 'F':
                    if x[par1] == 'T':
                        p = float(1-bn[Xi][1][0])
                    elif x[par1] == 'F':
                        p = float(1-bn[Xi][1][1])
            elif len(bn[Xi][0]) == 2:
                par1 = bn[Xi][0][0]
                par2 = bn[Xi][0][1]
                if x[Xi] == 'T':
                    if x[par1] == 'T':
                        if x[par2] == 'T':
                            p = float(bn[Xi][1][0])
                        elif x[par2] == 'F':
                            p = float(bn[Xi][1][1])
                    elif x[par1] == 'F':
                        if x[par2] == 'T':
                            p = float(bn[Xi][1][2])
                        elif x[par2] == 'F':
                            p = float(bn[Xi][1][3])
                elif x[Xi] == 'F':
                    if x[par1] == 'T':
                        if x[par2] == 'T':
                            p = float(1-bn[Xi][1][0])
                        elif x[par2] == 'F':
                            p = float(1-bn[Xi][1][1])
                    elif x[par1] == 'F':
                        if x[par2] == 'T':
                            p = float(1-bn[Xi][1][2])
                        elif x[par2] == 'F':
                            p = float(1-bn[Xi][1][3])
            w = w * p
        elif not(e.has_key(Xi)):
            rand = random.random()
            if len(bn[Xi][0]) == 0:
                if rand <= bn[Xi][1][0]:
                    x.update({Xi:'T'})
                else:
                    x.update({Xi:'F'})
            elif len(bn[Xi][0]) == 1:
                par1 = bn[Xi][0][0]
                if x[par1] == 'T':
                    if rand <= bn[Xi][1][0]:
                        x.update({Xi: 'T'})
                    else:
                        x.update({Xi: 'F'})
                elif x[par1] == 'F':
                    if rand <= bn[Xi][1][1]:
                        x.update({Xi: 'T'})
                    else:
                        x.update({Xi: 'F'})
            elif len(bn[Xi][0]) == 2:
                par1 = bn[Xi][0][0]
                par2 = bn[Xi][0][1]
                if x[par1] == 'T':
                    if x[par2] == 'T':
                        if rand <= bn[Xi][1][0]:
                            x.update({Xi: 'T'})
                        else:
                            x.update({Xi: 'F'})
                    elif x[par2] == 'F':
                        if rand <= bn[Xi][1][1]:
                            x.update({Xi: 'T'})
                        else:
                            x.update({Xi: 'F'})
                elif x[par1] == 'F':
                    if x[par2] == 'T':
                        if rand <= bn[Xi][1][2]:
                            x.update({Xi: 'T'})
                        else:
                            x.update({Xi: 'F'})
                    elif x[par2] == 'F':
                        if rand <= bn[Xi][1][3]:
                            x.update({Xi: 'T'})
                        else:
                            x.update({Xi: 'F'})
    return x,w


if __name__ == '__main__':
    aparser = argparse.ArgumentParser()
    aparser.add_argument('sample', type=int)
    aparser.add_argument('file', type=str)
    aparser.add_argument('query', type=str)
    aparser.add_argument('evidence', type=str, nargs='*')
    args = aparser.parse_args()
    N = args.sample
    if args.file == 'aima-alarm.xml':
        bn = parser('examples/aima-alarm.xml')
    elif args.file == 'aima-wet-grass.xml':
        bn = parser('examples/aima-wet-grass.xml')
    elif args.file == 'dog-problem.xml':
        bn = parser('examples/dog-problem.xml')
    q = args.query
    e = args.evidence
    ed = {}
    for i in range(0,len(e)/2):
        if e[2*i+1] == 'true':
            ed.update({e[2 * i]: 'T'})
        elif e[2*i+1] == 'false':
            ed.update({e[2 * i]: 'F'})
    print 'The probability of the query variable is ' + str(likelihood_weighting(q,ed,bn,N))