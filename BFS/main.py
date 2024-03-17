from collections import defaultdict, deque
from tabulate import tabulate


def readfile(s: str):
    file = open(s, "r")
    k = file.readline()
    edges = defaultdict(list)
    while k:
        a, b = k.split()
        edges[a[0]].append(b[0])
        k = file.readline()
    file.close()
    return edges


def printfile(filename: str, content: str):
    file = open(filename, "w", encoding="utf-8")
    file.write(content)
    file.close()


def bfs(edges, start, end):
    heads = ["Phát triển TT", "Trạng thái kề (K)", "Danh sách Q", "Danh sách L"]  #
    L = []
    Q = []
    K = []
    rows = []
    queue = deque()  # queue
    queue.append(start)
    L.append(start)
    Q.append(start)
    visited = defaultdict(chr)  # dict
    while queue:
        node = queue.popleft()  # lay node
        K.clear()
        L.remove(node)
        if node == end:  # tim thay roi
            res = [end]
            k = node
            while k != start:
                k = visited[k]
                res.append(k)
            rows.append([node, "TTKT-DỪNG!", None, None])
            return tabulate(tabular_data=rows, headers=heads,
                            tablefmt="fancy_grid") + "\nĐường đi là: " + " => ".join(res[::-1])
        for i in edges[node]:
            K.append(i)  # edge[node] dai dien cho K
            if i not in visited and i != start:
                queue.append(i)  # queue dai dien cho L
                visited[i] = node  # visited dai dien Q
                L.append(i)
                Q.append(i)
        rows.append([node, ", ".join(K), ", ".join(Q), ", ".join(L)])
    return "Không tìm thấy!"


if __name__ == '__main__':
    edges = readfile("input.txt")
    res = bfs(edges, 'A', 'G')
    printfile("output.txt", res)
