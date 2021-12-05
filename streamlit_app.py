import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
import networkx as nx
from networkx.readwrite import json_graph

st.title("📚 Knowledge Visualizer")
df = pd.read_csv('diigo/diigo_csv_2021_12_05.csv')
e = pd.read_csv('diigo/edges_diigo.csv',index_col="Unnamed: 0")
n = pd.read_csv('diigo/nodes_diigo.csv',index_col="Unnamed: 0")
df.tags = df.tags.fillna('')
# st.dataframe(df)

list0 = ["," for i in range(len(df))]
s0 = pd.Series(list0)
s = df.tags.fillna('') + s0
tagsum = s.sum()
tagslist = tagsum.split(",")
tagslist = list(dict.fromkeys(tagslist))
tagslist.remove('')
choices = st.multiselect("Tag",tagslist)


if choices!=[]:
    l = choices[0]
    i = n.index[n.tag == l].tolist()
    g = e[e.source == i[0]]
    # st.write(g)

    G = nx.Graph()
    for index, row in g.iterrows():
        G.add_node(int(row['target']))
        G.add_edge(int(row['source']),int(row['target']))

    # st.write(G)
    for k in G:
        # nodes id start at 0
        G.nodes[k]["name"] = n.tag[k]

    d = json_graph.node_link_data(G)
    # st.write(d)
    json.dump(d, open("force/force.json", "w"))


    components.iframe("http://127.0.0.1:5000/",width=600,height=400)

st.dataframe(df[df.tags.str.contains('|'.join(choices))])