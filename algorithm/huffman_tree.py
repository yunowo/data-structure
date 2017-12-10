from pathlib import Path
from os import path, getcwd
import matplotlib

matplotlib.use('Qt5Agg')

import matplotlib.pyplot as plt
import networkx as nx


class HuffmanTree:
    def __init__(self, root, nodes):
        self.root = root
        self.nodes = nodes
        self.draw()

    def draw(self):
        labels = {}
        edge_labels = {}
        leafs = []

        def traverse(r):
            if not r:
                return
            if r.father:
                G.add_node(id(r), freq=r.freq)
                G.add_edge(id(r.father), id(r))
                labels[id(r)] = f'{r.freq}{"|" + r.char if r.char else ""}'
                edge_labels[(id(r), id(r.father))] = '0' if r.is_left() else '1'
                if r.char:
                    leafs.append(id(r))
            traverse(r.left)
            traverse(r.right)

        G = nx.Graph()

        G.add_node(id(self.root))
        labels[id(self.root)] = self.root.freq
        traverse(self.root)

        prog = 'dot'
        # A bundled GraphViz for Windows
        if Path(getcwd(), 'graphviz\\bin\\dot.exe').is_file():
            prog = path.join(getcwd(), 'graphviz\\bin\\dot.exe')
        pos = nx.nx_pydot.graphviz_layout(G, prog=prog, root=self.root)
        nx.draw(G, pos=pos)
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color='#ef5350')
        nx.draw_networkx_nodes(G, pos, nodelist=leafs, node_size=500, node_color='#29b6f6')
        nx.draw_networkx_labels(G, pos, labels, font_size=10, font_family='Consolas', font_weight='regular')
        # nx.draw_networkx_edge_labels(G, pos, edge_labels,
        #                             font_size=7, font_family='Consolas', font_weight='regular', rotate=False)
        plt.axis('off')

        plt.show()
