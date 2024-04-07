import math


class Node:
    def __init__(self, val=0, name=''):
        self.val = val
        self.name = name
        self.nodes = []

    def add_node(self, node, parent):
        if self.name == parent:
            self.nodes.append(node)
        else:
            for _node in self.nodes:
                _node.add_node(node, parent)


def readfile(filename):
    file = open(filename)
    line = file.readline().split()
    root = Node(int(line[1]), line[0])
    line = file.readline().split()
    while line:
        temp = Node(int(line[1]), line[0])
        root.add_node(temp, line[2])
        line = file.readline().split()
    file.close()
    return root


def solve(root, isMax=True):
    def max_val(node, alpha, beta):
        if node.val > 0:
            return node.val
        else:
            node.val = -math.inf
            for i in node.nodes:
                node.val = max(node.val, min_val(i, alpha, beta))
                if node.val >= beta:
                    return node.val
                alpha = max(alpha, node.val)
            return node.val

    def min_val(node, alpha, beta):
        if node.val > 0:
            return node.val
        else:
            node.val = math.inf
            for i in node.nodes:
                node.val = min(node.val, max_val(i, alpha, beta))
                if node.val <= alpha:
                    return node.val
                beta = min(beta, node.val)
        return node.val

    alpha, beta = -math.inf, math.inf
    if isMax:
        res = max_val(root, alpha, beta)
    else:
        res = min_val(root, alpha, beta)
    return res



if __name__ == '__main__':
    root = readfile("input.txt")
    print(solve(root, False))
