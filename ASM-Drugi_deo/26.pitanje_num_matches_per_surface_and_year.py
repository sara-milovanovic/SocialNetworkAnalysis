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

G = nx.Graph()
G.add_nodes_from(skup_id)

data_reduced18 = data18[['winner_id', 'loser_id']]
data_reduced19 = data19[['winner_id', 'loser_id']]
data_reduced20 = data20[['winner_id', 'loser_id']]

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

degreeDataFrame=pd.DataFrame(degrees, columns=['player','degree']) #pravi dataFrame od degreeView-a

#distribucija u odnosu na podlogu

data18["surface"].value_counts().plot.bar(title='Number of matches per surface - 2018')
plt.show()

data19["surface"].value_counts().plot.bar(title='Number of matches per surface - 2019')
plt.show()

data20["surface"].value_counts().plot.bar(title='Number of matches per surface - 2020')
plt.show()

data_total=data18.append(data19)
data_total=data_total.append(data20)
data_total["surface"].value_counts().plot.bar(title='Number of matches per surface - total')
plt.show()

#distribucija u odnosu na godinu odrzavanja

def extract_year(data_set):
    for i in range(data_set.shape[0]):
        date=data_set.loc[i,'tourney_date']
        data_set.loc[i,'year'] = int(str(date)[:4])
    return data_set

print(data18.shape[0],data18.shape[1] )

extract_year(data18)
extract_year(data19)
extract_year(data20)

data20.append(data19).append(data18)["year"].value_counts().plot.bar(title='Number of matches per year')
plt.show()

#distribucija u odnosu na sezonu

def add_season(data_set, season):
    for i in range(data_set.shape[0]):
        data_set.loc[i,'year'] = season
    return data_set

print(data18.shape[0],data18.shape[1] )

add_season(data18,2018)
add_season(data19,2019)
add_season(data20,2020)

data20.append(data19).append(data18)["year"].value_counts().plot.bar(title='Number of matches per season')
plt.show()