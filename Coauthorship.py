%matplotlib inline
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random
import operator

randomList = random.sample(range(1, 504), 304)

path_author_ids = "data/author_ids.txt"

f = open(path_author_ids, 'r', encoding="Latin-1")
author_ids = {}
for line in f:
    line_content = line.split("\n")
    id, key = line_content[0].split("\t")
    author_ids[key] = int(id)


# Create the dict of authors with citations

path_author_citations = "data/author_citations.txt"

f = open(path_author_citations, 'r', encoding="Latin-1")
author_citations = {}
for line in f:
    line_content = line.split("\n")
    citation_count, author = line_content[0].split("\t")
    if author in author_ids.keys():
        author_citations[author] = int(citation_count)

print (len (author_ids.keys()))
print (len (author_citations.keys()))


# TOP 100 authors in terms of citation count
top100_sorted_author_citations = dict(sorted(author_citations.items(), key=operator.itemgetter(1), reverse=True)[:100])
sorted_author_citations = dict(sorted(author_citations.items(), key=operator.itemgetter(1), reverse=True))
#sorted_author_citations = sorted(author_citations.items(), key=operator.itemgetter(1))
#top100_author_citations = sorted_author_citations[len(author_citations.items())-100:len(author_citations.items())]
#print(sorted_author_citations.keys())
    
path_author_collaboration_network = "data/author-collaboration-network.txt"
#path_author_collaboration_network = "data/test.txt"

f = open(path_author_collaboration_network, 'r', encoding="Latin-1")

author_collaboration_network = nx.Graph()

for v in top100_sorted_author_citations.keys():
    author_collaboration_network.add_node(v)

for line in f:
    line_content = line.split("\n")
    name_author, name_coauthor = line_content[0].split("==>")
    if name_author in top100_sorted_author_citations.keys() and name_coauthor in top100_sorted_author_citations.keys():
        author_collaboration_network.add_edge(name_author, name_coauthor)
        

    
f.close()
print("DRAWING")
#G = nx.star_graph(20)
try:
    pos=nx.graphviz_layout(author_collaboration_network)
except:
    pos = nx.spring_layout(author_collaboration_network, iterations=20)
#colors = range(20)
#nx.draw(author_collaboration_network, pos, node_size=[v for v in author_citations.values()], node_color='#A0CBE2', width=1, edge_cmap=plt.cm.Blues, with_labels=False)
plt.figure(1,figsize=(30,30))
nx.draw(author_collaboration_network, pos, node_size=[author_citations[v] for v in author_collaboration_network.nodes()], with_labels=False)
plt.show()  # display

print("PLOTTING")
keys = list(sorted_author_citations.keys())
values = sorted(sorted_author_citations.values(), reverse=True)
print(type(keys))
x = range(len(keys))
plt.figure(1,figsize=(10,10))
plt.scatter(x, values)

