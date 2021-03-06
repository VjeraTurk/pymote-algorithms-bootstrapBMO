# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 14:53:54 2018

@author: admin

%load_ext autoreload
%autoreload 2
%reload_ext autoreload
"""
#from pymote import NetworkGenerator
from pymote.npickle import read_pickle, write_pickle
from pymote.network import Network
from pymote.simulation import Simulation
from networkx import minimum_spanning_tree, prim_mst_edges, prim_mst, draw, Graph,  draw_networkx_edges, spring_layout, draw_networkx_edge_labels, draw_networkx_nodes,draw_networkx_labels
from pylab import show, figure
import random

#from pymote.algorithms.turk2018.megamerge_p import MegaMerger
from pymote.algorithms.turk2018.megamerge import MegaMerger

#test_net = read_pickle('RandomBezAlg.tar.gz')
#net = read_pickle('RandomBezAlg.tar.gz')


test_net = read_pickle('WorstCaseBezAlg.tar.gz')
net = read_pickle('WorstCaseBezAlg.tar.gz')


#test_net = read_pickle('WorstCaseBezAlg.tar.gz')
net.show()
#
figure(2)
#draw(g,pos)
# specifiy edge labels explicitly

g = Graph()
g.adj=net.adj

edge_labels=dict([((u,v,),d['weight'])
             for u,v,d in g.edges(data=True)])

pos=spring_layout(net.pos)
pos=net.pos #Ako pos nije izvuceno iz net.pos rasporede se tako da se bolje vide

draw_networkx_nodes(g,pos=pos, node_size=500)
draw_networkx_edges(g,pos=pos)
draw_networkx_labels(g,pos=pos,labels=net.labels)
draw_networkx_edge_labels(g,pos=pos,edge_labels=edge_labels)
# show graphs
show()


net.algorithms = (MegaMerger,)
write_pickle(net, 'RandomSAlg.tar.gz')

#write_pickle(net, 'WorstCaseSAlg.tar.gz')
##s ovom mrezom pokretati GUI simulator

dobro=True
count=0

while dobro==True and count<5:
    
    count=count+1    
    print("********************************\nNova simulacija")
    net.algorithms = (MegaMerger,)    
    
    sim = Simulation(net)
    sim.run()
    
    exclude = list()
    exclude.append('Neighbors')
    
    one_name=net.nodes()[0].memory['Name']
    
    for node in net.nodes():
    
        if node.memory['Name']!=one_name:
            dobro=False
    
        print(node.memory['Name'],one_name,node.memory['Name']==one_name)
        print node.id, node.status       
    
        for key in node.memory:
            print key, ':\t',node.memory[key]
            #for value in node.memory[key]:
                #print value 
        print  "\n"    



print("count",count)


#Uses Kruskal’s algorithm.
#If the graph edges do not have a weight attribute 
#a default weight of 1 will be used.
#test_graph = minimum_spanning_tree(net)
test_graph=prim_mst(net)
test_net.adj=test_graph.adj
#test_net.show()
test_sum= test_net.size(weight='weight')


print(one_name)
print("jedno ime =", dobro)
print("MST Sum ", test_sum)
    