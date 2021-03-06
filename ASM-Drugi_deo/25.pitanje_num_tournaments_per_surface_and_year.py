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

#broj turnira po podlozi

def draw(data_set, season):
    data_set=data_set[['tourney_name', 'surface']]
    df = data_set.drop_duplicates(subset=['tourney_name'], keep='first')
    df=df.groupby(['surface']).size()
    df.plot.bar(title='Number of tournaments per surface - '+str(season))
    plt.show()

draw(data18,2018)
draw(data19,2019)
draw(data20,2020)

data_total=data18.append(data19).append(data20)
draw(data_total, 'total')

#broj turnira po godini

def calculate(data_set):
    df = data_set.drop_duplicates(subset=['tourney_name'], keep='first')
    df=df.shape[0]
    return df

tournaments18 = calculate(data18)
tournaments19 = calculate(data19)
tournaments20 = calculate(data20)

data = [['2018', tournaments18], ['2019', tournaments19], ['2020', tournaments20]]
tournaments_total = pd.DataFrame(data, columns = ['year', 'count']) 
print(tournaments_total)
tournaments_total.plot(x ='year', y='count', kind = 'bar',title='Number of tournaments per year')
plt.show()