import networkx as nx
import pandas as pd
import folium
import seaborn as sns

G = nx.Graph()
nodes = pd.read_csv('C:/Users/Daegu_nodes.csv')
links = pd.read_csv('C:/Users/Daegu_links.csv')

nodes = nodes[['NODE_ID', 'NODE_NAME', 'STNL_REG', 'Y', 'X']]

G_link = links[['F_NODE', 'T_NODE']]

G1 = list(G_link['F_NODE'])
G2 = list(G_link['T_NODE'])

Edge_List1 = []

for i in range(len(G1)):
    Edge_List1.append((G1[i], G2[i]))

Edge_List = []

G.add_nodes_from(nodes['NODE_ID'])

for i in range(len(Edge_List1)):
    if Edge_List1[i][0] in G.nodes:
        if Edge_List1[i][1] in G.nodes:
            Edge_List.append((Edge_List1[i][0], Edge_List1[i][1]))

G.add_edges_from(Edge_List)

daegu_map = folium.Map(location= [35.889882, 128.610504], zoom_start=15)

BC = nx.betweenness_centrality(G)
CC = nx.closeness_centrality(G)
KC = nx.katz_centrality(G)
DC = nx.degree_centrality(G)

BC_klist = list(BC.keys())
BC_vlist = list(BC.values())
CC_klist = list(CC.keys())
CC_vlist = list(CC.values())
KC_klist = list(KC.keys())
KC_vlist = list(KC.values())
DC_klist = list(DC.keys())
DC_vlist = list(DC.values())

BC1 = pd.DataFrame({'NODE_ID': BC_klist, 'BC': BC_vlist})
CC1 = pd.DataFrame({'NODE_ID': CC_klist, 'CC': CC_vlist})
KC1 = pd.DataFrame({'NODE_ID': KC_klist, 'KC': KC_vlist})
DC1 = pd.DataFrame({'NODE_ID': DC_klist, 'DC': DC_vlist})
nodes = pd.merge(nodes, BC1, on='NODE_ID')
nodes = pd.merge(nodes, CC1, on='NODE_ID')
nodes = pd.merge(nodes, KC1, on='NODE_ID')
nodes = pd.merge(nodes, DC1, on='NODE_ID')

n_reg = len(set(nodes['STNL_REG']))
palette = sns.color_palette('hls', n_colors= n_reg)
sns.palplot(palette)

palette2 = sns.color_palette("RdBu_r", 80)
sns.palplot(palette2)

palette3 = sns.color_palette("Purples", 600)
sns.palplot(palette3)

palette4 = sns.color_palette("Oranges", 35)
sns.palplot(palette4)

palette5 = sns.color_palette("Blues", 35)
sns.palplot(palette5)

def rgb_to_hex(rgb):
    rgb=(int(rgb[0]*256) ,int(rgb[1]*256) ,int(rgb[2]*256))
    return '#%02x%02x%02x' % rgb

for idx , color in enumerate(palette):
    hex_col=rgb_to_hex(color)
    palette[idx]=hex_col

for idx , color in enumerate(palette2):
    color
    hex_col=rgb_to_hex(color)
    palette2[idx]=hex_col

for idx , color in enumerate(palette3):
    color
    hex_col=rgb_to_hex(color)
    palette3[idx]=hex_col

for idx, color in enumerate(palette4):
    color
    hex_col = rgb_to_hex(color)
    palette4[idx] = hex_col

for idx, color in enumerate(palette5):
    color
    hex_col = rgb_to_hex(color)
    palette5[idx] = hex_col

layer1 = folium.FeatureGroup(name = 'Reg').add_to(daegu_map)

for e in G.edges():
    f_node, e_node = e[0], e[1]
    fx, fy = float((nodes.loc[nodes['NODE_ID'] == f_node])['X']), float((nodes.loc[nodes['NODE_ID'] == f_node])['Y'])
    ex, ey = float((nodes.loc[nodes['NODE_ID'] == e_node])['X']), float((nodes.loc[nodes['NODE_ID'] == e_node])['Y'])
    folium.PolyLine([(fy, fx), (ey, ex)], color='black', weight=1, opacity=0.5).add_to(layer1)
for v in G.nodes(data=True):
    x1, y1, reg1 = v[0], v[0], v[0]
    x, y = float((nodes.loc[nodes['NODE_ID'] == x1])['X']), float((nodes.loc[nodes['NODE_ID'] == y1])['Y'])
    reg = int((nodes.loc[nodes['NODE_ID'] == reg1])['STNL_REG'])
    idx = reg - 150
    folium.CircleMarker([y,x], radius=5, color=palette[idx], fill_color=palette[idx],
                        popup=str(reg)).add_to(layer1)

layer2 = folium.FeatureGroup(name = 'BC').add_to(daegu_map)

for e in G.edges():
    f_node, e_node = e[0], e[1]
    fx, fy = float((nodes.loc[nodes['NODE_ID'] == f_node])['X']), float((nodes.loc[nodes['NODE_ID'] == f_node])['Y'])
    ex, ey = float((nodes.loc[nodes['NODE_ID'] == e_node])['X']), float((nodes.loc[nodes['NODE_ID'] == e_node])['Y'])
    folium.PolyLine([(fy, fx), (ey, ex)], color='red', weight=1, opacity=0.5).add_to(layer2)
for v in G.nodes(data=True):
    x1, y1, bc1 = v[0], v[0], v[0]
    x, y = float((nodes.loc[nodes['NODE_ID'] == x1])['X']), float((nodes.loc[nodes['NODE_ID'] == y1])['Y'])
    bc = float((nodes.loc[nodes['NODE_ID'] == bc1])['BC'])
    idx = int(100 * bc) # color gradient 범위 0~80 으로 맞추려고 100*bc로 인덱스 설정
    degree = G.degree[v[0]]
    folium.CircleMarker([y, x], radius=100*bc, color=palette2[idx], fill=True, fill_color=palette2[idx],
                        fill_opacity=1, popup='BC :' + str(bc) + ' Degree : ' + str(degree)).add_to(layer2)


layer3 = folium.FeatureGroup(name = 'CC').add_to(daegu_map)

for e in G.edges():
    f_node, e_node = e[0], e[1]
    fx, fy = float((nodes.loc[nodes['NODE_ID'] == f_node])['X']), float((nodes.loc[nodes['NODE_ID'] == f_node])['Y'])
    ex, ey = float((nodes.loc[nodes['NODE_ID'] == e_node])['X']), float((nodes.loc[nodes['NODE_ID'] == e_node])['Y'])
    folium.PolyLine([(fy, fx), (ey, ex)], color='blue', weight=1, opacity=0.5).add_to(layer3)
for v in G.nodes(data=True):
    x1, y1, cc1 = v[0], v[0], v[0]
    x, y = float((nodes.loc[nodes['NODE_ID'] == x1])['X']), float((nodes.loc[nodes['NODE_ID'] == y1])['Y'])
    cc = float((nodes.loc[nodes['NODE_ID'] == cc1])['CC'])
    idx=int(10000*cc)
    degree = G.degree[v[0]]
    folium.CircleMarker([y,x], radius=100*cc, color=palette3[idx],fill=True, fill_color=palette3[idx],
                        fill_opacity =1, popup='CC :' + str(cc) + ' Degree : ' + str(degree)).add_to(layer3)

layer4 = folium.FeatureGroup(name = 'KC').add_to(daegu_map)

for e in G.edges():
    f_node, e_node = e[0], e[1]
    fx, fy = float((nodes.loc[nodes['NODE_ID'] == f_node])['X']), float((nodes.loc[nodes['NODE_ID'] == f_node])['Y'])
    ex, ey = float((nodes.loc[nodes['NODE_ID'] == e_node])['X']), float((nodes.loc[nodes['NODE_ID'] == e_node])['Y'])
    folium.PolyLine([(fy, fx), (ey, ex)], color='purple', weight=1, opacity=0.5).add_to(layer4)
for v in G.nodes(data=True):
    x1, y1, kc1 = v[0], v[0], v[0]
    x, y = float((nodes.loc[nodes['NODE_ID'] == x1])['X']), float((nodes.loc[nodes['NODE_ID'] == y1])['Y'])
    kc = float((nodes.loc[nodes['NODE_ID'] == kc1])['KC'])
    idx=int(1000*kc)
    degree = G.degree[v[0]]
    folium.CircleMarker([y,x], radius=100*kc, color=palette4[idx],fill=True, fill_color=palette4[idx],
                        fill_opacity =1, popup='KC :' + str(kc) + ' Degree : ' + str(degree)).add_to(layer4)

layer5 = folium.FeatureGroup(name = 'DC').add_to(daegu_map)

for e in G.edges():
    f_node, e_node = e[0], e[1]
    fx, fy = float((nodes.loc[nodes['NODE_ID'] == f_node])['X']), float((nodes.loc[nodes['NODE_ID'] == f_node])['Y'])
    ex, ey = float((nodes.loc[nodes['NODE_ID'] == e_node])['X']), float((nodes.loc[nodes['NODE_ID'] == e_node])['Y'])
    folium.PolyLine([(fy, fx), (ey, ex)], color='black', weight=1, opacity=0.5).add_to(layer5)
for v in G.nodes(data=True):
    x1, y1, dc1 = v[0], v[0], v[0]
    x, y = float((nodes.loc[nodes['NODE_ID'] == x1])['X']), float((nodes.loc[nodes['NODE_ID'] == y1])['Y'])
    dc = float((nodes.loc[nodes['NODE_ID'] == dc1])['DC'])
    idx=int(10000*dc)
    degree = G.degree[v[0]]
    folium.CircleMarker([y,x], radius=1000*dc, color=palette5[idx],fill=True, fill_color=palette5[idx],
                        fill_opacity =1, popup='DC :' + str(dc) + ' Degree : ' + str(degree)).add_to(layer5)


folium.LayerControl().add_to(daegu_map)

daegu_map.save('daegu_map.html')

