 # -*-coding:Latin-1 -*
from bs4 import BeautifulSoup #parse html
from urllib.request import urlretrieve
import requests # GET
import time
import re  #regex
from descnew import findPatterns
url = "https://www.leboncoin.fr/informatique/offres/languedoc_roussillon/?th=1&q="

requete = ["lordi","hp%20x360","hp%20360x"]

ids=[]
for i in requete:
    
    print("-"*100)
    print("URL : " + url+i)
    
    r= requests.get(url+i)
    data = r.text
    
    # parse html
    soup = BeautifulSoup(data,"lxml") 
    
    # obtenir la section des annonces
    blockAnnonces = soup.find('section',{'class':'tabsContent block-white dontSwitch'})
    
    urls=[]
 
    try:
        # obtenir les annonces
        annonces = blockAnnonces.find_all('li')
        print('nb annonces : ' + str(len(annonces)))
        
        # obtenir le titre de l'annonce
        titres= [ x.a['title'] for x in annonces]
        print("les titres :" + str(titres))
        
        # obtenir l'url de l'annonce
        urls= [ x.a['href'] for x in annonces]
        print(urls)
        
        regid = '/(?P<id>[0-9]+).htm'
        ids = set(ids)|set([re.search(regid,x,re.IGNORECASE).group("id") for x in urls])
        print(ids)
        
    except AttributeError:
        print("aucune annonce trouvée")
        
for i in ids:
    print(i)
    cpt=0
    r= requests.get("https://www.leboncoin.fr/informatique/"+i+".htm?ca=13_s")
    data = r.text   
    
    # parse html
    soup = BeautifulSoup(data,"lxml") 

    # obtenir la description
    desc = soup.find('p',{'class':'value'})
    print(desc.get_text(" "))
    findPatterns(desc.get_text(" "))
    
    #obtenir le titre de l'annonce
    titre = soup.find('h1',{'class':'no-border'})
    titre = titre.get_text()
    print(titre)
    #obtenir les images 
    img_urls =[]
    
    section = soup.find('section',{'class':'adview_main'})
    script = section.find('script')
    script = script.get_text()
    
    regurl = '"(.*xxl.*)"'
    img_urls= re.findall(regurl,script,re.IGNORECASE)
 
            
    if img_urls==[]:
        images = soup.find('div',{'class':'item_image big popin-open trackable'}) 
        img_url = images.img["src"]
        
        file_name = "..\\images_Annoces\\"+i+str(cpt)+".jpg"
        url = "https:"+img_url
        cpt+=1
        print(url)
        urlretrieve(url, file_name)

    else : 
        for img_url in img_urls:
            file_name = "..\\images_Annoces\\"+i+"-img"+str(cpt)+".jpg"
            url = "https:"+img_url
            cpt+=1
            urlretrieve(url, file_name)
    
    time.sleep(1)
