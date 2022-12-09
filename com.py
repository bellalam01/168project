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

"""
This code find takes in the a graph (G_test) and find its communities 
It returns a list of components 
The root of each component will be printed to screen while the components itself is written to a csv file. 
To change the input graph, just modify line 49, in the function parameter 

"""

f = open('components.csv', 'w')
writer = csv.writer(f)

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

communities = sorted(nxcom.greedy_modularity_communities(G_test), key=len, reverse=True)
all_sizes = []
components = [] 
for x in communities: 
    size = len(x)
    if size >=2:
        newlist = []
        for y in x:
            newlist.append(y)
        components.append(newlist)

for list1 in components:
    max_year = 3000.0
    for element in list1:
        i=df[df['Language']==element]
        year  = i["Year"].item()
        if year < max_year and year !=1:
            max_year = year
            root = element
    print(root)

for list1 in components: 
    row = [] 
    for element in list1:
        row.append(element)
    writer.writerow(row)







