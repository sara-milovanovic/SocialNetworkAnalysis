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

#za godine pojedinacno
index=0
rows_list = []
broj_pobeda20=0
broj_poraza20=0
broj_pobeda19=0
broj_poraza19=0
broj_pobeda18=0
broj_poraza18=0
for i in range (degreeDataFrame.shape[0]): #za svakog igraca
    igrac=degreeDataFrame.loc[i]
    maska=data20['winner_id'] == igrac['player']
    broj_pobeda20=data20[maska].shape[0]
    maska=data19['winner_id'] == igrac['player']
    broj_pobeda19=data19[maska].shape[0]
    maska=data18['winner_id'] == igrac['player']
    broj_pobeda18=data18[maska].shape[0]
    maska=data20['loser_id'] == igrac['player']
    broj_poraza29=data20[maska].shape[0]
    maska=data19['loser_id'] == igrac['player']
    broj_poraza19=data19[maska].shape[0]
    maska=data18['loser_id'] == igrac['player']
    broj_poraza18=data18[maska].shape[0]
    broj_meceva=broj_pobeda20+broj_poraza20+broj_pobeda19+broj_poraza19+broj_pobeda18+broj_poraza18
    row=[igrac['player'], broj_meceva]
    rows_list.append(row)
    
sumMatches=pd.DataFrame(rows_list, columns=["winner","number_of_matches"])

rows_list = []
for i in range (sumMatches['number_of_matches'].max()): #za svakog igraca
    igrac=degreeDataFrame.loc[i]
    maska=sumMatches['number_of_matches'] == i
    broj_igraca_za_broj_meceva=sumMatches[maska].shape[0]
    row=[i, broj_igraca_za_broj_meceva]
    rows_list.append(row)
    
completeData=pd.DataFrame(rows_list, columns=["number_of_matches","number_of_players"])
completeData.plot(x ='number_of_matches', y='number_of_players', kind = 'scatter', title='total')
plt.show()

completeData.to_csv(r'C:\Users\HS\Desktop\ASM\ASM-Drugi_deo\data\24_number_of_players_number_of_matchesTOTAL.csv')
sumMatches.to_csv(r'C:\Users\HS\Desktop\ASM\ASM-Drugi_deo\data\sumMatchesTOTAL.csv')
#print(sumMatches)