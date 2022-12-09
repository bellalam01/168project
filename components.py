import networkx as nx #networks package we will use for demos
import matplotlib.pyplot as plt #networkx uses matplotlib to generate its plots
import numpy as np #this is the linear algebra package for working with matrices
import pandas as pd #pandas is a dataframe package that is useful for managing network attributes
import math #use this package to take the log of a scalar, use numpy to take the element-wise log of an array
import os
import scipy
from collections import Counter
import networkx.algorithms.community as nxcom

import csv

df = pd.read_csv('final_cleaned.csv', sep=",", header = None)
df.columns = ["Order","Language", "Influenced By", "Influenced", "Year"]
df.at[462,"Influenced By"] = "[Self, Lisp, Smalltalk]"
df.loc[df['Language'] == "Squeak"]
df.at[464,"Influenced"] = "[StarLogo, Scratch]"
df.loc[df['Language'] == "Etoys"]
G = nx.DiGraph()
G_test = nx.DiGraph()

for index, row in df.iterrows():
    lang = row["Language"]
    G_test.add_node(lang)
    if type(row["Influenced"]) == str:
        st = row["Influenced"]
        lis_infl = st.strip('][').split(', ')
        
        for infl in lis_infl:
            G_test.add_edge(lang, infl)

    if type(row["Influenced By"]) == str:
        st_by = row["Influenced By"]
        lis_inf_by = st_by.strip('][').split(', ')
        
        for inf_by in lis_inf_by:
            G_test.add_edge(inf_by, lang)

print("Components:")
numOfStrong = nx.number_strongly_connected_components(G_test)
strong = nx.is_strongly_connected(G_test)
print("The graph is strongly connected: "+ str(strong))
print("Number of Strongly connected components: "+str(numOfStrong))


numofWeak = nx.number_weakly_connected_components(G_test)
weak = nx.is_weakly_connected(G_test)
print("\nThe graph is weakly connected: "+ str(weak))
print("Number of Weakly connected components: "+str(numofWeak))

print("\n\nCommunities:")
communities = sorted(nxcom.greedy_modularity_communities(G_test), key=len, reverse=True)
top5 = dict(Counter(communities).most_common(1))
print("Below is the biggest community:")
for x,y in top5.items():
    print(x,y)
print(f"\nThere are {len(communities)} communities.")

all_sizes = []
print("\nSizes of the communities:")
for x in communities: 
    size = len(x)
    all_sizes.append(size)
print(all_sizes)
#count the number of sizes with 2 
print ("number of sizes with 2 is "+str(all_sizes.count(2)))
#count the number of sizes with 1 
print ("number of sizes with 1 is "+str(all_sizes.count(1)))

length = 0 
for x in communities:
    length = length+ len(x) 
print("the average length is "+ str(length/len(communities)) )
def set_node_community(G, communities):
    '''Add community to node attributes'''
    for c, v_c in enumerate(communities):
        for v in v_c:
            # Add 1 to save 0 for external edges
            G.nodes[v]['community'] = c + 1
def set_edge_community(G):
    '''Find internal edges and add their community to their attributes'''
    for v, w, in G.edges:
        if G.nodes[v]['community'] == G.nodes[w]['community']:
            # Internal edge, mark with community
            G.edges[v, w]['community'] = G.nodes[v]['community']
        else:
            # External edge, mark as 0
            G.edges[v, w]['community'] = 0
def get_color(i, r_off=1, g_off=1, b_off=1):
    '''Assign a color to a vertex.'''
    r0, g0, b0 = 0, 0, 0
    n = 16
    low, high = 0.1, 0.9
    span = high - low
    r = low + span * (((i + r_off) * 3) % n) / (n - 1)
    g = low + span * (((i + g_off) * 5) % n) / (n - 1)
    b = low + span * (((i + b_off) * 7) % n) / (n - 1)
    return (r, g, b)

pos = nx.spring_layout(G_test, k=0.1)
plt.rcParams.update(plt.rcParamsDefault)
plt.rcParams.update({'figure.figsize': (15, 10)})
plt.style.use('dark_background')
# Set node and edge communities
set_node_community(G_test, communities)
set_edge_community(G_test)
# Set community color for internal edges
external = [(v, w) for v, w in G_test.edges if G_test.edges[v, w]['community'] == 0]
internal = [(v, w) for v, w in G_test.edges if G_test.edges[v, w]['community'] > 0]
internal_color = ["black" for e in internal]
node_color = [get_color(G_test.nodes[v]['community']) for v in G_test.nodes]
# external edges
nx.draw_networkx(
    G_test,
    pos=pos,
    node_size=0,
    edgelist=external,
    edge_color="silver",
    node_color=node_color,
    alpha=0.2,
    with_labels=False)
# internal edges
nx.draw_networkx(
    G_test, pos=pos,
    edgelist=internal,
    edge_color=internal_color,
    node_color=node_color,
    alpha=0.05,
    with_labels=False)
plt.show()


