# _*_ coding:utf-8 _*_
# __AUTHOR__ = "syd"
# DATA:2018/7/25
# PROJECT:Pyworkplace

import codecs
import json
import networkx as nx
import matplotlib.pyplot as plt


class MakeGraph:
    def __init__(self, inpath):
        self.inpath = inpath

    def makegraph(self):
        with codecs.open(self.inpath, "r", "utf-8") as f:
            for line in f:
                i = 0
                edgelist = []
                X_X = json.loads(line)
                keys = X_X.keys()
                for key in keys:
                    values = X_X.get(key)
                    for value in values:
                        i = i + 1
                        if i < 201:
                            edgelist.append([key, value])
                            print("{}/200".format(i))
        G = nx.DiGraph()
        G.add_edges_from(edgelist)
        nx.draw(G, pos=nx.spectral_layout(G), node_color='b', edge_color='r',\
                with_labels=True, font_size=2, node_size=20)
        plt.savefig("200spectral.png",dpi=1080)
        plt.show()


if __name__ == "__main__":
    inpath = "E:\ALLworkspace\Pyworkplace\dblp-ref\P_P.json"
    G = MakeGraph(inpath)
    G.makegraph()
