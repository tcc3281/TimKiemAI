import string
from collections import defaultdict
from tabulate import tabulate

def pg(a, b):
    for i in range(len(a)):
        if a[i] in string.ascii_uppercase:
            for j in range(len(b)):
                if b[j] in string.ascii_uppercase:
                    if a[i] == b[j] and a[i + 1] != b[j + 1]:
                        return a[:i] + a[i + 2:] + b[:j] + b[j + 2:]


def transfer(a):
    s=[]
    for i in range(0,len(a),2):
        s.append(a[i]+a[i+1])
    res=''
    for i in s:
        if i[1]=='0':
            res+='!'+i[0]
        else:
            res+=i[0]
        res+=' v '
    return res[:len(res)-3]


def solve(L, vit: set, pos, simple: set,parent:defaultdict(list)):
    if pos == len(L): return
    i = pos + 1
    l = len(L)
    while i < l:
        if i == pos:
            i += 1
            continue
        if L[i] + L[pos] in vit: continue
        if L[pos] + L[i] in vit: continue
        p = pg(L[i], L[pos])
        if p:
            parent[p]=[L[i],L[pos]]
            p = p.replace(' ', '')
            if len(p) == 2:
                if (p[0] in simple) and (p not in L):
                    return p
                else:
                    simple.add(p[0])
            if p not in L:
                L.append(p)
                vit.add(L[i] + L[pos])
                vit.add(L[pos] + L[i])

        i += 1
        l = len(L)
    return solve(L, vit, pos + 1, simple,parent)

def find(parent,child,tabulate_data,marked:defaultdict(int)):
    if parent[child][0]=="None":
        return
    find(parent,parent[child][0],tabulate_data,marked)
    find(parent,parent[child][1],tabulate_data,marked)
    marked[child]=len(marked)+1
    a=marked[parent[child][0]]
    b=marked[parent[child][1]]
    tabulate_data.append([len(tabulate_data)+1,f" {transfer(parent[child][0])} , {transfer(parent[child][1])} ({a} , {b})",f'{transfer(child)}'])


def printfile(filename: str, content: str):
    file = open(filename, "w", encoding="utf-8")
    file.write(content)
    file.close()



if __name__ == '__main__':
    f = open("input.txt")
    L = []
    s = f.readline()
    simple = set()
    parent=defaultdict(list)
    while s:
        if (s == ''): break
        L.append(s[:len(s) - 1])
        parent[s[:len(s) - 1]]=["None"]
        if len(s) == 2:
            simple.add(s[0])
        s = f.readline()
    f.close()

    cm= L.pop()
    print(cm)
    cm0=cm
    cm=cm[0]+ '1' if cm[1]=='0' else cm[0]+ '0'
    L.append(cm)
    init = L.copy()
    parent["P0"]=["None"]
    i = 0
    visited = set()
    res=solve(L, visited, 0, simple,parent)
    res1=res

    if res[1]==1:
        res1=res[0]+'0'
    else:
        res1=res[0]+'1'
    header=["STT","Assumption",'Conclusion']
    tabulate_data=[]
    marked=defaultdict(int)

    for i in init:
        print(transfer(i))
        marked[i]=len(marked)+1
        tabulate_data.append([marked[i],transfer(i),""])
    find(parent,res,tabulate_data,marked)
    find(parent,res1,tabulate_data,marked)
    print(f"Res({transfer(res)},{transfer(res1)})")
    printfile('output.txt',tabulate(tabulate_data,header,tablefmt='fancy_grid')+f'\n ({marked[res]}), ({marked[res1]}) => Res({transfer(res)},{transfer(res1)})\n'+f'=> {transfer(cm0)}')