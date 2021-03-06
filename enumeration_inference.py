import argparse
from copy import deepcopy
from xmlparser import *


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


def enumeration_ask(x,e,bn):
    Qx = {'T':0,'F':0}
    vars = topo(bn[0],bn[1])
    for value in Qx.keys():
        e.update({x:value})
        ex = deepcopy(e)
        Qx.update({value:enumerate_all(bn,vars,ex)})
    return normalize(Qx)


def enumerate_all(BN,BN_vars,e):
    bn = BN[0]
    vars = deepcopy(BN_vars)
    if len(vars) == 0:
        return 1.0
    Y = vars[0]
    if e.has_key(Y):
        prob = 0
        if len(bn[Y][0]) == 0:    #no parent
            if e[Y] == 'T':
                prob = float(bn[Y][1][0])
            elif e[Y] == 'F':
                prob = float(1 - bn[Y][1][0])
        elif len(bn[Y][0]) == 1:   #1 parent
            par1 = bn[Y][0][0]
            if e[Y] == 'T':
                if e[par1] == 'T':
                    prob = float(bn[Y][1][0])
                elif e[par1] == 'F':
                    prob = float(bn[Y][1][1])
            elif e[Y] == 'F':
                if e[par1] == 'T':
                    prob = float(1 - bn[Y][1][0])
                elif e[par1] == 'F':
                    prob = float(1 - bn[Y][1][1])
        elif len(bn[Y][0]) == 2:     #2 parents
            par1 = bn[Y][0][0]
            par2 = bn[Y][0][1]
            if e[Y] == 'T':
                if e[par1] == 'T':
                    if e[par2] == 'T':
                        prob = float(bn[Y][1][0])
                    elif e[par2] == 'F':
                        prob = float(bn[Y][1][1])
                elif e[par1] == 'F':
                    if e[par2] == 'T':
                        prob = float(bn[Y][1][2])
                    elif e[par2] == 'F':
                        prob = float(bn[Y][1][3])
            elif e[Y] == 'F':
                if e[par1] == 'T':
                    if e[par2] == 'T':
                        prob = float(1-bn[Y][1][0])
                    elif e[par2] == 'F':
                        prob = float(1-bn[Y][1][1])
                elif e[par1] == 'F':
                    if e[par2] == 'T':
                        prob = float(1-bn[Y][1][2])
                    elif e[par2] == 'F':
                        prob = float(1-bn[Y][1][3])
        vars.remove(Y)
        return prob * enumerate_all(BN,vars,e)

    elif not(e.has_key(Y)):
        if len(bn[Y][0]) == 0:
            probt = bn[Y][1][0]
        elif len(bn[Y][0]) == 1:
            par1 = bn[Y][0][0]
            if e[par1] == 'T':
                probt = float(bn[Y][1][0])
            elif e[par1] == 'F':
                probt = float(bn[Y][1][1])
        elif len(bn[Y][0]) == 2:
            par1 = bn[Y][0][0]
            par2 = bn[Y][0][1]
            if e[par1] == 'T':
                if e[par2] == 'T':
                    probt = float(bn[Y][1][0])
                elif e[par2] == 'F':
                    probt = float(bn[Y][1][1])
            elif e[par1] == 'F':
                if e[par2] == 'T':
                    probt = float(bn[Y][1][2])
                elif e[par2] == 'F':
                    probt = float(bn[Y][1][3])
        probf = 1 - probt
        vars.remove(Y)
        e.update({Y: 'T'})
        et = deepcopy(e)
        e.update({Y: 'F'})
        ef = deepcopy(e)
        return probt * enumerate_all(BN,vars,et) + probf * enumerate_all(BN,vars,ef)


if __name__ == '__main__':
    aparser = argparse.ArgumentParser()
    aparser.add_argument('file', type=str)
    aparser.add_argument('query', type=str)
    aparser.add_argument('evidence', type=str, nargs='*')
    args = aparser.parse_args()
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
    print 'The probability of the query variable is ' + str(enumeration_ask(q,ed,bn))


