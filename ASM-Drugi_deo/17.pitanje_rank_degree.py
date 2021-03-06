import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

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


ser18w=(pd.DataFrame(list(list_winner18)))
ser18l=(pd.DataFrame(list(list_loser18)))
ser19w=(pd.DataFrame(list(list_winner19)))
ser19l=(pd.DataFrame(list(list_loser19)))
ser20w=(pd.DataFrame(list(list_winner20)))
ser20l=(pd.DataFrame(list(list_loser20)))

ser18w.columns = ['player_id2']
ser18l.columns = ['player_id2']
ser19w.columns = ['player_id2']
ser19l.columns = ['player_id2']
ser20w.columns = ['player_id2']
ser20l.columns = ['player_id2']

ser = pd.DataFrame()

ser = pd.concat([ser, ser18w]).drop_duplicates('player_id2').reset_index(drop=True)
ser = pd.concat([ser, ser18l]).drop_duplicates('player_id2').reset_index(drop=True)
ser = pd.concat([ser, ser19w]).drop_duplicates('player_id2').reset_index(drop=True)
ser = pd.concat([ser, ser19l]).drop_duplicates('player_id2').reset_index(drop=True)
ser = pd.concat([ser, ser20w]).drop_duplicates('player_id2').reset_index(drop=True)
ser = pd.concat([ser, ser20l]).drop_duplicates('player_id2').reset_index(drop=True)

#print(ser) #svi igraci u dataFrame-u


G = nx.Graph()
G.add_nodes_from(skup_id)

data_reduced18 = data18[['winner_id', 'loser_id']]
data_reduced19 = data19[['winner_id', 'loser_id']]
data_reduced20 = data20[['winner_id', 'loser_id']]

import pickle

with open("data/data_reduced18_17_pitanje", 'wb') as file:
    pickle.dump(data_reduced18, file)
    
with open("data/data_reduced19_17_pitanje", 'wb') as file:
    pickle.dump(data_reduced19, file)

with open("data/data_reduced20_17_pitanje", 'wb') as file:
    pickle.dump(data_reduced20, file)

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
        
degrees = G.degree()


dataRankings=dataRankings.sort_values('ranking_date').drop_duplicates('player_id',keep='first')
df=pd.merge(ser, dataRankings, left_on='player_id2', right_on='player_id', how='left').drop('player_id2', axis=1) # tabela igraca i rangova

df2=pd.DataFrame(degrees, columns=['player','degree'])
df3=pd.merge(df, df2, left_on='player_id', right_on='player', how='left').drop('player', axis=1)
#print((df3))
print(df2)



df3.plot(x ='rank', y='degree', kind = 'scatter')
plt.show()

n = G.number_of_nodes()
m = G.number_of_edges()

import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter

def plot_deg_frequency(G, weighted=False, xscale = "log", yscale = "log", title=''):

    if weighted:
        degrees = G.degree(weight="weight")
    else:
        degrees = G.degree()
    _, deg_list = zip(*degrees)
    deg_counts = Counter(deg_list)        
    print(deg_counts)
    x, y = zip(*deg_counts.items())                                                      

    plt.figure(1)   

    # prep axes   
    if weighted:
        plt.xlabel('weighted degree')  
    else:
        plt.xlabel('degree')                                                                                                             
    plt.xscale(xscale)                                                                                                                
    plt.xlim(1, max(x))  
    

    plt.ylabel('frequency')                                                                                                          
    plt.yscale(yscale)                                                                                                                
    plt.ylim(1, max(y))                                                                                                             
                                                                                                                                                                                                    
    plt.scatter(x, y, marker='.')                                                                                                    
    plt.show()

Gnm = nx.gnm_random_graph(n, m) 
plot_deg_frequency(G, weighted=True, title='Our network')
plot_deg_frequency(G, weighted=False, title='Our network')
plot_deg_frequency(Gnm, xscale = 'linear', yscale = 'linear', title='Linear random')
plot_deg_frequency(Gnm, xscale = 'log', yscale = 'log', title='Log random')

p = ( 2*float(m) ) / ( n* (n-1) )
print(p)

er_mreza = nx.erdos_renyi_graph(n,p)

delta_m = m - er_mreza.number_of_edges()
print(f"Broj čvorova originalne mreže minus broj čvorova u ER mreži iznosi {delta_m}, što je odstupanje od {abs(float(delta_m)) * 100 / m}%")

plot_deg_frequency(er_mreza, xscale = 'linear', yscale = 'linear')
plot_deg_frequency(er_mreza, xscale = 'log', yscale = 'log')

output_path = "models/random_network.gml"

nx.write_gml(Gnm, output_path)

output_path = "models/erdos_renyi_network.gml"

nx.write_gml(er_mreza, output_path)