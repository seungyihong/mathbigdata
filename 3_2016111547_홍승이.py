#3번째 과제 2016111547 수학과 홍승이

import requests
from bs4 import BeautifulSoup
import re
import networkx as nx
import matplotlib.pyplot as plt

r= requests.get('https://www.imdb.com/')
c = r.content
html = BeautifulSoup(c,'html.parser')


f = open('imdb.txt','w', encoding='utf-8')

location = html.select('#sidebar > div:nth-child(2) > span > div > div')
for title in location:
    title = title.text
    f.write(title)
    list1 = title.split('  ')
    titleset = list(set(list1))
    titleset.remove('')
    #print(titleset)

f.close()

f= open("imdb.txt",'r')
read= f.read()
G= nx.Graph()
for alpha in read:
    alpha = str(alpha)
    G.add_nodes_from(alpha)
for i in range(len(titleset)):
    a=titleset[i]
    print(a)
    b=list(a)
    print(b)
    for k in range(len(b)):
        for j in range(len(b)):
            G.add_edge(b[k],b[j])


nx.draw(G,with_labels=True)
plt.show()

f.close()
