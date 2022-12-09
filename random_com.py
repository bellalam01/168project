#import required packages

import networkx as nx #networks package we will use for demos
import matplotlib.pyplot as plt #networkx uses matplotlib to generate its plots
from collections import Counter

import numpy as np #this is the linear algebra package for working with matrices
import pandas as pd #pandas is a dataframe package that is useful for managing network attributes
import networkx.algorithms.community as nxcom

import os

df = pd.read_csv('final_cleaned.csv',sep=",", header = None)
df.columns = ["idx","Language", "Influenced By", "Influenced","Year"]
df = df[["Language","Influenced By","Influenced","Year"]]

# get the in degree and out degree sequence
k_in = []
k_out = []
for index, row in df.iterrows():
    #print(index)
    if pd.isna(row[1]):
        k_in.append(0)
    else:
        k_in.append(row[1].count(',')+1)
    if pd.isna(row[2]):
        k_out.append(0)
    else:
        k_out.append(row[2].count(',')+1)


import random
def randomgraph_edgelist(k_in,k_out):
    #value in edgelist holds [["Influenced By"],["Influenced"]] nodes according to their index
    edgelist = {}
    edgelist[0] = [[],[]]
    unclaimed_instub = []
    # initialize unclaimed instub
    for i in range(k_out[0]):
        unclaimed_instub.append(0)
    for node in range(1,len(k_out)):
        edgelist[node] = [[],[]]
        if k_in[node] > 0:
            # pick random outstub to connect with 
            for i in range(k_in[node]):
                rand_idx = random.randrange(len(unclaimed_instub))
                # should we make sure that we don't have multiedges or will it mess up our calculation? Maybe ask professor
                # while unclaimed_instub[rand_idx] in edgelist:
                #     rand_idx = random.randrange(len(unclaimed_instub))
                edgelist[node][0].append(unclaimed_instub[rand_idx])
                edgelist[unclaimed_instub[rand_idx]][1].append(node)
                unclaimed_instub.pop(rand_idx)
        for j in range(k_out[node]):
            unclaimed_instub.append(node)
    return edgelist

def calculation (G):
    """
    print('IN AVG:', np.mean([G.in_degree(n) for n in G.nodes]))
    print('OUT AVG:', np.mean([G.out_degree(n) for n in G.nodes]))
    print('ALL AVG:', np.mean([G.degree(n) for n in G.nodes]))
    print('IN SUM:', np.sum([G.in_degree(n) for n in G.nodes]))
    print('OUT SUM:', np.sum([G.out_degree(n) for n in G.nodes]))
    print('ALL SUM:', np.sum([G.degree(n) for n in G.nodes]))
    print("Components:")
    numOfStrong = nx.number_strongly_connected_components(G)
    strong = nx.is_strongly_connected(G)
    print("The graph is strongly connected: "+ str(strong))
    print("Number of Strongly connected components: "+str(numOfStrong))

    numofWeak = nx.number_weakly_connected_components(G)
    weak = nx.is_weakly_connected(G)
    print("\nThe graph is weakly connected: "+ str(weak))
    print("Number of Weakly connected components: "+str(numofWeak))
    print("\n\nCommunities:")
    """
    communities = sorted(nxcom.greedy_modularity_communities(G), key=len, reverse=True)
    top = dict(Counter(communities).most_common(1))
    """
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
    """
    length = 0 
    for x in communities:
        length = length+ len(x) 
    return length/len(communities)
    print("the average length is "+ str(length/len(communities)) )


total = 0
counter = 0 
for x in range(1,100):
    elist1 = randomgraph_edgelist(k_in,k_out)
    df1 = pd.DataFrame.from_dict(elist1)
    df1 = df1.T
    df1.columns = ['Influenced', 'Influenced By']
    #print(df1.head())
    counter = 0 
    G = nx.DiGraph()
    for index, row in df1.iterrows():
        index = counter
        G.add_node(index)
        if row["Influenced"]:
            st = row["Influenced"]
            for x in st:
                G.add_edge(index, x)

        if ["Influenced By"]:
            st_by = row["Influenced By"]
            for x in st_by:
                G.add_edge(x, index)
        counter = counter+1
    #nx.draw(G, with_labels = True)
    #plt.show()
    average = calculation(G)
    total = average + total
    counter = counter+1

print("The average of 100 graphs is "+ str(total/counter))

