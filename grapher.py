import networkx as nx
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

color_map = {
...
"site_name": "color"
...
}
coord_map = {
...
"ste_name": (latitude,longitude)
...
}

coord_map_flipped = {
...
"ste_name": (latitude,longitude)
...
}


Data = open('sorted_region_links.csv', "r")
Graphtype = nx.Graph()
G = nx.parse_edgelist(Data, delimiter=',', create_using=nx.Graph(), nodetype=str,data=(('weight',float),))

colors = [color_map.get(node) for node in G.nodes()]
weights = nx.get_edge_attributes(G,'weight').values()
coords = [coord_map.get(node) for node in G.nodes()]

nx.set_node_attributes(G, coord_map_flipped,'coord')
fig,ax = plt.subplots(figsize=(76,76))
ax.set_title("NETWORK", fontsize = 52)
#ax.invert_xaxis()

nx.draw(G, nx.get_node_attributes(G,'coord'), with_labels=True, ax=ax,width=list(weights),node_color=colors, node_size=12000, font_size=36, edge_color='black')
fig.set_facecolor('white')
plt.savefig('graph.png',format='PNG',facecolor=fig.get_facecolor())
