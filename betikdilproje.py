#Gerekli Kütüphaneler
from twython import Twython
import pandas as pd
import matplotlib.pyplot as plt

#Credentials
consumerKey = 'YldWSX26xHZRxxLL0SAmJEcVt'
consumerSecret = 'GixVGSt7p5Sd5b6L9nAoSD6HS5zXafX2pWOcq9R14yXe9s2M2J'


#Check edilcek kelimeler
mylist = ['kadın', 'silah','iletişim','bıçak','alkol','çok','işsizlik','küfür','güç',
          'yüksek','erkek','ölüm','saldırmak','aşırı','tecavüz','incitmek','mutsuzluk',
          'kavga','huzursuzluk','cinayet','çocuk']


#Kütüphaneyi aktif etme
python_tweets = Twython(consumerKey , consumerSecret)


#Twitter'dan verileri çekip DataFrame'e save etme işlemi
#1 seferde En fazla 100 tweet çekilebilceği için 10 kez bu işlemi tekrarladık.
result_count = 0
last_id = None
num_result = 10
dict_ = {'text': []}
while result_count < num_result:
    query = {'q': '' + " -filter:retweets",
            'result_type': 'recent',
            'count' : 100,
            'lang': 'tr',
            'geocode' : "40.903413,31.176321,35km",
            'max_id' : last_id
            }

    for status in python_tweets.search(**query)['statuses']:
        dict_['text'].append(status['text'])
        
    result_count += 1
    last_id = status['id']

df = pd.DataFrame(dict_)


#Tweetleri içeren DataFrame'deki her bir satırda dolaşıp listemizdeki kelimeleri
#içeren herhangi bir kelime varsa , o kelimeyle ilgili sütun oluşturup True dedik değilse False.
for i in range (0,len(mylist)):
    df[mylist[i]] = df["text"].apply(lambda x : mylist[i] in x)
  
    
#tweet column'una artık ihtiyacımız olmadığı için drop ettik.
new_df = df.drop(columns=["text"] , axis = 1)


#yeni bir liste oluşturup new_df'deki elementleri tek tek gezdik.
#Ve her tweette listemizdeki kelimelerden kaçtane olduğunu hesaplayıp new_list'e ekledik.
toplam = 0
cokfazla = 0
fazla = 0
orta = 0
cokaz = 0
az = 0
new_list = []
for i in range(0,new_df.shape[0]):
    count = 0
    for j in range (0,21):
        if new_df.values[i][j] == True:
            count += 1
            toplam = toplam + count
            new_list.append(count)
        if(toplam >= 32 and toplam <39):
            cokfazla +=1
        elif(toplam >= 24 and toplam <32):
            fazla +=1
        elif(toplam >= 16 and toplam <24):
            orta+=1
        elif (toplam >= 8  and toplam <16):
            az += 1
        elif(toplam >= 1 and toplam <8):
            cokaz+= 1

print(toplam)

cokfazla = cokfazla/100
fazla = fazla /100
orta = orta/100
az = az /100
cokaz = cokaz / 100

print("Detailed Report: ")
print(str(cokfazla) + "% insan 'çok fazla' düşündü.")
print(str(fazla) + "% insan 'fazla' düşündü.")
print(str(orta) + "% insan 'orta' düşündü.")
print(str(az) + "% insan 'az' düşündü.")
print(str(cokaz) + "% insan 'çok az' düşündü.")

#Sonuçlar
d={
   'Çok Fazla ' : cokfazla,
   'Fazla': fazla,
   'Orta' : orta,
   'Az': az,
   'Çok Az':cokaz}
deger = pd.Series(d)
deger.index.name = "Değerler"
deger.name = "DÜ ATILAN TWEET ANALİZİ"
deger.plot(kind = "pie")
plt.figure(figsize= (12,12))
plt.show()
