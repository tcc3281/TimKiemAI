import string
from collections import defaultdict
from tabulate import tabulate

def pg(a, b):
    for i, ai in enumerate(a):
        if ai in string.ascii_uppercase:
            for j, bj in enumerate(b):
                if bj in string.ascii_uppercase and ai == bj and a[i + 1] != b[j + 1]:
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

def find(parent, child, tabulate_data, marked):
    if parent[child][0] == "None": return
    find(parent, parent[child][0], tabulate_data, marked)
    find(parent, parent[child][1], tabulate_data, marked)
    marked[child] = len(marked) + 1
    a, b = marked[parent[child][0]], marked[parent[child][1]]
    tabulate_data.append([len(tabulate_data)+1, f" {transfer(parent[child][0])} , {transfer(parent[child][1])} ({a} , {b})", f'{transfer(child)}'])

def printfile(filename, content):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)

if __name__ == '__main__':
    with open("input.txt") as f:
        L = [s.strip() for s in f]
    simple = {s[0] for s in L if len(s) == 2}
    parent = defaultdict(lambda: ["None"], {s: ["None"] for s in L})
    cm = L.pop()
    L.append(cm[0]+ '1' if cm[1]=='0' else cm[0]+ '0')
    init = L.copy()
    parent["P0"] = ["None"]
    visited = set()
    res = solve(L, visited, 0, simple, parent)
    res1 = res[0]+'0' if res[1]=='1' else res[0]+'1'
    header = ["STT","Assumption",'Conclusion']
    tabulate_data = [[i+1, transfer(init[i]), ""] for i in range(len(init))]
    marked = defaultdict(int, {init[i]: i+1 for i in range(len(init))})
    find(parent, res, tabulate_data, marked)
    find(parent, res1, tabulate_data, marked)
    printfile('output.txt', tabulate(tabulate_data, header, tablefmt='fancy_grid')+f'\n ({marked[res]}), ({marked[res1]}) => Res({transfer(res)},{transfer(res1)})\n'+f'=> {transfer(cm)}')