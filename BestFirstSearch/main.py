from collections import defaultdict
from tabulate import tabulate
from queue import PriorityQueue


def readfile(s: str):
    file = open(s, "r")
    k = file.readline()
    edges = defaultdict(list)
    while k != '\n':
        a, b = k.split()
        edges[a[0]].append(b[0])
        k = file.readline()
    k = file.readline()
    w = defaultdict(int)
    while k:
        a, b = k.split()
        w[a[0]] = int(b)
        k = file.readline()
    file.close()
    return [edges, w]


def bestfirstsearch(edges: defaultdict[list], weights: defaultdict[int], start: str, end: str):
    pq = PriorityQueue()
    pq.put((weights[start], start))
    visited = defaultdict(chr)
    L = [start + str(weights[start])]
    K = []
    head = ["Phát triển trạng thái", "Trạng thái kề", "Danh sách L"]
    rows = []
    key_func = lambda x: int(x[1:])
    while not pq.empty():
        K.clear()
        w, node = pq.get()
        L.remove(node + str(w))
        if node == end:
            res = [node]
            k = node
            rows.append([node + str(weights[node]), "TTKT-DỪNG!", None])
            while k != start:
                k = visited[k]
                res.append(k)

            return (tabulate(tabular_data=rows, headers=head, tablefmt="fancy_grid") +
                    "\n" + " => ".join(res[::-1]))
        for i in edges[node]:
            K.append(i + str(weights[i]))
            if i not in visited and i != start:
                pq.put((weights[i], i))
                L.append(i + str(weights[i]))
                visited[i] = node

        L = sorted(L, key=key_func)
        rows.append([node + str(weights[node]), ", ".join(K), ", ".join(L)])
    return "Không tìm thấy!"


def printfile(filename: str, content: str):
    file = open(filename, "w", encoding="utf-8")
    file.write(content)
    file.close()


if __name__ == '__main__':
    edges, weights = readfile("input.txt")
    res = bestfirstsearch(edges, weights, "A", "B")
    printfile("output.txt", res)
