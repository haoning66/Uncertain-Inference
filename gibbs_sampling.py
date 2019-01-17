import argparse
import xml.etree.ElementTree as et
import random
from copy import deepcopy
from extract_inference import *
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
#                             elif len(root[i])!=2:
#                                 for k in range(1,len(root[i])):
#                                     if root[i][k].tag == 'GIVEN':
#                                         bn[root[i][0].text][0].append(root[i][k].text)
#                                     elif root[i][k].tag == 'TABLE':
#                                         list = root[i][k].text.strip().split('\n')
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
#     varsTopo = topo(bn, vars)
#     return bn, varsTopo

def topo(bn, vars):
    varsTopo = []
    Vars = []
    for var in vars:
        if len(bn[var][0]) == 0:
            varsTopo.append(var)
        else:
            Vars.append(var)
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


def Gibbs(x,e,BN,itra):
    res = {'T':0.00,'F':0.00}
    Non_e = []
    currSamp = {}
    for var in BN[1]:
        if not e.has_key(var):
            Non_e.append(var)
            if random.randint(1,3) == 1:
                currSamp.update({var: 'T'})
            else:
                currSamp.update({var: 'F'})
        else:
            currSamp.update({var:e[var]})
    for k in range(0,itra):
        for var in Non_e:
            MB = Markov(var,BN,currSamp)
            prob = enumeration_ask(var,MB,BN)
            rand = random.random()
            if prob['T'] < rand:
                currSamp.update({var: 'F'})
            else:
                currSamp.update({var: 'T'})
            if currSamp[x] == 'T':
                T = res['T'] + 1
                res.update({'T':T})
            else:
                F = res['F'] + 1
                res.update({'F': F})
    Res = normalize(res)
    return Res

def Markov(var,BN,currSamp):
    mb = []
    MB = {}
    if BN[0][var][0] is not None:
        for par in BN[0][var][0]:
            mb = Append(mb,par)
    for Var in BN[1]:
        if var in BN[0][Var][0]:
            mb = Append(mb, Var)
            for VAR in BN[0][Var][0]:
                if not VAR == var:
                    mb = Append(mb, VAR)
    for mb_ele in mb:
        MB.update({mb_ele:currSamp[mb_ele]})
    return MB


def Append(mb,ele):
    if ele not in mb:
        mb.append(ele)
    return mb

if __name__ == '__main__':
    # BN = parser('/Users/zexuan_wang/Desktop/aima-alarm.xml')
    # e = {'J': 'T', 'E': 'F'}
    # x = 'A'
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
    for i in range(0, len(e) / 2):
        if e[2 * i + 1] == 'true':
            ed.update({e[2 * i]: 'T'})
        elif e[2 * i + 1] == 'false':
            ed.update({e[2 * i]: 'F'})
    print 'The probability of the query variable is ' + str(Gibbs(q, ed, bn, N))
