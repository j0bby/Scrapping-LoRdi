from bs4 import BeautifulSoup #parse html

import requests # GET

import re  #regex

url = "https://www.leboncoin.fr/informatique/offres/languedoc_roussillon/?th=1&q="

requete = ["lordi","hp%20x360","hp%20360x"]

for i in requete:
    
    print("-"*100)
    print("URL : " + url+i)
    
    r= requests.get(url+i)
    data = r.text
    
    # parse html
    soup = BeautifulSoup(data,"lxml") 
    
    # obtenir la section des annonces
    blockAnnonces = soup.find('section',{'class':'tabsContent block-white dontSwitch'})
    
    # obtenir les annonces
    annonces = blockAnnonces.find_all('li')
    print('nb annonces : ' + str(len(annonces)))
    
    # obtenir le titre de l'annonce
    titres= [ x.a['title'] for x in annonces]
    print("les titres :" + str(titres))
    
    # obtenir l'url de l'annonce
    urls= [ x.a['href'] for x in annonces]
    print(urls)
    
