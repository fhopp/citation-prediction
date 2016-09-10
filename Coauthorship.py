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
    author_ids[key] = id


# Create the dict of authors with citations

path_author_citations = "data/author_citations.txt"

f = open(path_author_citations, 'r', encoding="Latin-1")
author_citations = {}
for line in f:
    line_content = line.split("\n")
    citation_count, author = line_content[0].split("\t")
    if author in author_ids.keys():
        author_citations[author] = int(citation_count)

# Paper and citation counts

path_paper_citations = "data/paper_citations.txt"

f = open(path_paper_citations, 'r', encoding="Latin-1")
paper_citations = {}
for line in f:
    line_content = line.split("\n")
    splitedParts = line_content[0].split("\t")
    citation_count, paper = splitedParts[0], splitedParts[1]
    paper_citations[paper] = int(citation_count)

    
# Paper and authors

path_paper_authors = "data/paper_author_affiliations.txt"

f = open(path_paper_authors, 'r', encoding="Latin-1")
paper_authors = {}
for line in f:
    line_content = line.split("\n")
    paper, authors = line_content[0].split("\t")
    authorlist = authors.split(";")
    paper_authors[paper] = authorlist
    

 
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

for v in author_citations.keys():
    author_collaboration_network.add_node(v)

for line in f:
    sumcitation = 0
    line_content = line.split("\n")
    name_author, name_coauthor = line_content[0].split("==>")
    #if name_author in top100_sorted_author_citations.keys() and name_coauthor in top100_sorted_author_citations.keys():
    #    author_collaboration_network.add_edge(name_author, name_coauthor)
    
    if name_author in author_ids.keys() and name_coauthor in author_ids.keys():
        for key, value in paper_authors.items():
            if author_ids[name_author] in value and author_ids[name_coauthor] in value :
                if key in paper_citations.keys():
                    sumcitation = sumcitation + paper_citations[key]
                #print (name_author + " & " + name_coauthor + " --> " + sumcitation)
        author_collaboration_network.add_edge(name_author, name_coauthor, weight=sumcitation)
        #if sumcitation>50:
        #    print (name_author + " & " + name_coauthor + " --> " + str(sumcitation))
    
f.close()
print("DRAWING")
# UNCOMMENT ALL
#try:
#    pos=nx.graphviz_layout(author_collaboration_network)
#except:
#    pos = nx.spring_layout(author_collaboration_network, iterations=20)


#plt.figure(1,figsize=(30,30))
#nx.draw(author_collaboration_network, pos, node_size=[author_citations[v] for v in author_collaboration_network.nodes()], with_labels=True)
#plt.show()  # display

#print(sorted(top100_sorted_author_citations.items(), key=operator.itemgetter(1), reverse=True)[:100])

#print(sum(top100_sorted_author_citations.values())/sum(sorted_author_citations.values()))

#print(sorted(nx.load_centrality(author_collaboration_network).items(), key=operator.itemgetter(1), reverse=True)[:100])

print("WRITING")

outputfile_centrality_eigen = open('data/author_eigenvector_centrality_weighted.txt', 'w', encoding="Latin-1")

for item in sorted(nx.eigenvector_centrality(author_collaboration_network, weight = 'weight').items(), key=operator.itemgetter(1), reverse=True):
    outputfile_centrality_eigen.write(item[0]+"\t"+str(item[1])+"\n")
outputfile_centrality_eigen.close()

outputfile_centrality_load = open('data/author_load_centrality_weighted.txt', 'w', encoding="Latin-1")
for item in sorted(nx.load_centrality(author_collaboration_network, weight = 'weight').items(), key=operator.itemgetter(1), reverse=True):
    outputfile_centrality_load.write(item[0]+"\t"+str(item[1])+"\n")
outputfile_centrality_load.close()
    
#outputfile_sorted_citations = open('data/author_citations_sorted.txt', 'w', encoding="Latin-1")
#for item in sorted(author_citations.items(), key=operator.itemgetter(1), reverse=True):
#    outputfile_sorted_citations.write(item[0]+"\t"+str(item[1])+"\n")


print("PLOTTING")

#print(item[0]+"\t"+str(item[1])+"\n")

#keys = list(sorted_author_citations.keys())
#values = sorted(sorted_author_citations.values(), reverse=True)

#x = range(len(keys))
#plt.figure(1,figsize=(10,10))
#plt.scatter(x, values)
