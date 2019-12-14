import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import collections
import nltk
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#imdb 사이트에서 synopsis 끌어오기
address_list =['tt0371746','tt1300854','tt1228705','tt0800080','tt2015381',
                   'tt3896198','tt0458339','tt4154796','tt4154756','tt5095030',
                   'tt0478970','tt3501632','tt1981115','tt0800369','tt2395427',
                   'tt0848228','tt6320628','tt2250912','tt4154664','tt1843866',
                   'tt3498820','tt1825683','tt1211837']
marvel_list = []
marvel_list.extend(address_list)
whole_story =''

for i in range(0, 23):
    URL = 'https://www.imdb.com/title/'+marvel_list[i]+'/plotsummary?ref_=tt_stry_pl#synopsis'
    response= requests.get(URL)
    whole_story = whole_story + response.text

c = whole_story
html = BeautifulSoup(c,'html.parser')

f = open('marvel.txt','w', encoding='utf-8')
location = html.select('#plot-synopsis-content')

#변수 선언
stop_words = set(stopwords.words('english'))
result = []
result2 = []
sent = []
word=[]

# word 빈도수 세기 위해 사용
word2 = [] #
result3=[]
result4=[]

# 파일로 데이터 쓰기, sentence, word tokenize
for synopsis in location:
    synopsis = synopsis.text
    synopsis= synopsis.lower()
    synopsis2 = synopsis.split('.')
    synopsis2 = ' '.join(synopsis2)
    sent.append(sent_tokenize(synopsis))
    word2.append(word_tokenize(synopsis2))
    f.write(synopsis)
f.close()

# sent, word 2차원배열 -> 1차원배열로 낮추기 & set 사용으로 단어 중복 없애기
sent= sum(sent, [])
word2 =sum(word2,[])
word = list(set(word2))

# word,word2의 stopword 제거
for w in word:
    if w not in stop_words:
        result.append(w)
for w in word2:
    if w not in stop_words:
        result3.append(w)


# 각 word에 tag 달기
tag = nltk.pos_tag(result)
tag2 = nltk.pos_tag(result3)

# NN & NNS & JJ & FW 단어만 가져오기
nouns_list1 = [t[0] for t in tag if t[1] == "NN"]
nouns_list2 = [t[0] for t in tag if t[1] == "NNS"]
adj_list1 = [t[0] for t in tag if t[1] == "JJ"]
nouns_list3 = [t[0] for t in tag if t[1] == "FW"]

nouns_list11 = [t[0] for t in tag2 if t[1] == "NN"]
nouns_list22 = [t[0] for t in tag2 if t[1] == "NNS"]
adj_list11 = [t[0] for t in tag2 if t[1] == "JJ"]
nouns_list33 = [t[0] for t in tag2 if t[1] == "FW"]

result2 = nouns_list1 + nouns_list2 + nouns_list3 + adj_list1
result4 = nouns_list11 + nouns_list22 + nouns_list33 + adj_list11

word = result2
word2= result4

# sent(행)-word(열) matrix A 생성하기
num_sent = len(sent)
num_word = len(word)

A_zero = np.zeros((num_sent,num_word))

# i(행),j(열) 위치 기억
count = -1
count2 = -1

# sentence에 존재하는 word마다 1부여
for s in sent:
    count = count + 1
    s2 = word_tokenize(s)
    for w in s2:
        for w2 in word:
            count2 = count2 + 1
            if w == w2:
                A_zero[count][count2] = 1
                count2 = -1
                break
        count2 = -1

# matrix A_t*A = M(word(행) * word(열))  생성
A = A_zero
A_t = np.transpose(A)
M = np.dot(A_t,A)

# network G 생성 node = work , M의 값에 따라 edge 부여
G = nx.Graph()
G.add_nodes_from(word)

# network 시각화
for i in range(num_word):
    for j in range(num_word):
        if M[i][j] > 5:
            G.add_edge(word[i],word[j])

# word frequency 측정
counter_number = dict(collections.Counter(word2))
fr_top10 = sorted(counter_number.items(), key=lambda x: x[1] , reverse= True)[:10]
print("frequency top10:",fr_top10)

# measure 측정
BC = nx.betweenness_centrality(G)
CC = nx.closeness_centrality(G)
DC = nx.degree_centrality(G)
#KC = nx.katz_centrality(G)

bc_top10 = sorted(BC.items(), key=lambda x: x[1] , reverse= True)[:10]
cc_top10 = sorted(CC.items(), key=lambda x: x[1] , reverse= True)[:10]
dc_top10 = sorted(DC.items(), key=lambda x: x[1] , reverse= True)[:10]
#kc_top10 = sorted(KC.items(), key=lambda x: x[1] , reverse= True)[:10]

print("bc top10:",bc_top10)
print("cc top10:",cc_top10)
print("dc top10:",dc_top10)
#print("kc top10:",kc_top10)

nx.draw(G,with_labels=True)
plt.show()
