import numpy as np

#***Koliko je puta pobedio odredjeni igrac

pobednik = 'Novak Djokovic'
odredjeni_pobedio_maska = data18['winner_name'] == pobednik 
data_black = data18[odredjeni_pobedio_maska]
labele_kolona = ['winner_name','count']
data_selektovano = data_black[labele_kolona].groupby('winner_name')
print(data_selektovano.agg(np.size))

#***Koliko je puta izgubio odredjeni igrac

gubitnik = 'Novak Djokovic'
odredjeni_izgubio_maska = data18['loser_name'] == gubitnik 
data_black = data18[odredjeni_izgubio_maska]
labele_kolona = ['loser_name','count']
data_selektovano = data_black[labele_kolona].groupby('loser_name')
print(data_selektovano.agg(np.size))

#***Sortirani igraci po broju pobeda

data18["count"] = 0
kolone = ['winner_name','count']
grupisani = data18[kolone].groupby('winner_name').count()
grupisani.sort_values('count', ascending=False)