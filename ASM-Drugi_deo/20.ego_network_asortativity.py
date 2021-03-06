import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

dataPath18 = "data/atp_matches_2018.csv"
dataPath19 = "data/atp_matches_2019.csv"
dataPath20 = "data/atp_matches_2020.csv"
dataPathRankings = "data/atp_rankings_current.csv"

data18 = pd.read_csv(dataPath18)
data19 = pd.read_csv(dataPath19)
data20 = pd.read_csv(dataPath20)
dataRankings = pd.read_csv(dataPathRankings, names=["ranking_date", "rank", "player_id", "points"])


data_reduced18 = data18[['winner_id', 'loser_id']]
data_reduced19 = data19[['winner_id', 'loser_id']]
data_reduced20 = data20[['winner_id', 'loser_id']]

list_winner18 = set(data18['winner_id'].unique())
list_loser18 = set(data18['loser_id'].unique())

list_winner19 = set(data19['winner_id'].unique())
list_loser19 = set(data19['loser_id'].unique())

list_winner20 = set(data20['winner_id'].unique())
list_loser20 = set(data20['loser_id'].unique())

skup_id18 = list_winner18.union(list_loser18)
skup_id19 = list_winner19.union(list_loser19)
skup_id20 = list_winner20.union(list_loser20)

skup_id=[]
skup_id = skup_id18.union(skup_id19).union(skup_id20) #svi igraci
G = nx.Graph()
G.add_nodes_from(skup_id)

for _, winner_id, loser_id in data_reduced18.itertuples():
    if (winner_id, loser_id) in G.edges:
        G.edges[winner_id, loser_id]['weight'] += 1
    else:
        G.add_edge(winner_id, loser_id, weight=1)
        
for _, winner_id, loser_id in data_reduced19.itertuples():
    if (winner_id, loser_id) in G.edges:
        G.edges[winner_id, loser_id]['weight'] += 1
    else:
        G.add_edge(winner_id, loser_id, weight=1)

for _, winner_id, loser_id in data_reduced20.itertuples():
    if (winner_id, loser_id) in G.edges:
        G.edges[winner_id, loser_id]['weight'] += 1
    else:
        G.add_edge(winner_id, loser_id, weight=1)
        
ego_mreza = nx.ego_graph(G, 103819)
print(f"Čvorovi ego mreže igrača Federer su {ego_mreza.nodes}")
r2 = nx.degree_assortativity_coefficient(ego_mreza, weight='weight')
print(f"Koeficijent asortativnosti na osnovu težinskog stepena čvora: {r2}")

ego_mreza = nx.ego_graph(G, 104745)
print(f"Čvorovi ego mreže igrača Nadal su {ego_mreza.nodes}")
r2 = nx.degree_assortativity_coefficient(ego_mreza, weight='weight')
print(f"Koeficijent asortativnosti na osnovu težinskog stepena čvora: {r2}")

ego_mreza = nx.ego_graph(G, 104925)
print(f"Čvorovi ego mreže igrača Djokovic su {ego_mreza.nodes}")
r2 = nx.degree_assortativity_coefficient(ego_mreza, weight='weight')
print(f"Koeficijent asortativnosti na osnovu težinskog stepena čvora: {r2}")
