#수리적빅데이터 과제2 2016111547 수학과 홍승이

import networkx as nx
from networkx.generators.random_graphs import erdos_renyi_graph
import matplotlib.pyplot as plt
import seaborn as sb

n1= 1000 #node개수 n1=1000, 10000일때
p1= 0.1 #확률 p1= 0.1,0.01,0.001일때
G1 = erdos_renyi_graph(n1,p1) #랜덤그래프 그리기

degrees= [G1.degree(n) for n in G1.nodes()]

sb.distplot(degrees,bins=100,hist=False,kde=True) # kde plot
#sb.distplot(degrees,bins=100,hist=True,kde=False) #히스토그램 plot

plt.title("KDE")
#plt.title("Histogram")
plt.ylabel("Density")
#plt.ylabel("Count")
plt.xlabel("Degree")
plt.show()

print('node = ', G1.nodes)
print('edge = ', G1.edges)
