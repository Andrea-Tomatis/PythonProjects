import random
import networkx as nx 
import matplotlib.pyplot as plt

class Node():
    def __init__(self, adiacenze, color):
        self.adiacenze = adiacenze
        self.color = color
    
    def colora(self, color):
        self.color = color


def isMassimale(grafo):
    for node in grafo:
        sum = 0
        for edge in node.adiacenze:
            if grafo[edge-1].color == node.color:
                sum += 1
            else: sum -= 1
        if sum < 0:
            return False
    return True

def main():
    #grafo bilancere
    grafo = [Node((2,3,4), random.choice(['red','blue'])),
            Node((1,3,4), random.choice(['red','blue'])),
            Node((1,2,4), random.choice(['red','blue'])),
            Node((1,2,3,5), random.choice(['red','blue'])),
            Node((4,6,7,8), random.choice(['red','blue'])),
            Node((5,7,8), random.choice(['red','blue'])),
            Node((5,6,8), random.choice(['red','blue'])),
            Node((5,6,7), random.choice(['red','blue']))]
    '''
    another test configuration
    grafo = [Node((2,4), 'red'),
            Node((1,3), 'red'),
            Node((2,4), 'blue'),
            Node((3,5), random.choice(['red','blue'])),
            Node((1,3), 'blue')]
    '''
    G = nx.Graph()
    color_map = []
    for i in range(len(grafo)):
        G.add_node(i)
        color_map.append(grafo[i].color)
        for j in grafo[i].adiacenze:
            G.add_edge(i,j-1)
    nx.draw(G, node_color=color_map, with_labels=True)
    plt.savefig('./before.png')

    while not isMassimale(grafo):
        for node in grafo:
            sum = 0
            for edge in node.adiacenze:
                if grafo[edge-1].color == node.color:
                    sum += 1
                else: sum -= 1
            if sum < 0:
                node.colora('red' if node.color=='blue' else 'blue')
    for node in grafo:
        print(node.color)

    for i in range(len(grafo)):
        color_map[i] = grafo[i].color
    plt.close()
    nx.draw(G, node_color=color_map, with_labels=True)
    plt.savefig('./after.png')

if __name__ == "__main__":
    main()
