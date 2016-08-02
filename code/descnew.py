import re
import string
#description= "bonjour carte graphique intel hd,je vend cet ordinateur portable tactile en parfait état de marche. hp x360 310 g1.ssd de 256gb. 4gb de ram. ecran tactile.avec sa housse de transport, son chargeur d'origine et sa notice d'utilisation ainsi q'un cd d'installation. le tout 250e"
description = "Je vends mon hp pavilion x360 écran tactile sous windows 10 pour la somme de 150e. L'ordinateur est en bon état, et il sera vendu avec housse de protection ainsi que le chargeur. Le prix est ferme sachant que l'ordinateur vaut 500e neuf, me contacter uniquement par telephone"
#nettoyage de la description : 
# les accents : 
description = re.sub('[éèêë]',"e",description)
description = re.sub('[àâä]',"a",description)
description = re.sub('[ïî]',"i",description)
description = re.sub('[ûùü]',"u",description)
#ponctuation
#ajout d'espaces pour mots distincts
description = re.sub( r'([a-zA-Z])([,.!\'])', r'\1 \2', description )
translator = str.maketrans({key: None for key in string.punctuation})
description= description.translate(translator)

description=description.lower()
print (description)
#Stopwords
stopwords = []
with open('newstopwords.txt',"r",encoding="utf-8") as fileinput:
    for line in fileinput:
        stopwords.append(line.rstrip())
        
description=' '.join([word for word in description.split() if word not in stopwords])
print(description)



regmarquemodele = 'hp[ .,]*[a-z]*[ ]*x[ ]*360[ ]*(310)?'
print(re.search(regmarquemodele,description,re.IGNORECASE))


#regproc = 'intel[ ]*(pentium)?[ ]*n?[ ]*3540'
regproc ='[ .,]+intel [ ]*([a-z, ]*n?3540|pentium[ ]*n?[ ]*(3540)?)'
print(re.search(regproc,description,re.IGNORECASE))

regfreqproc= '[ .,]+2[., ]+66[ ]*ghz'
print(re.search(regfreqproc,description,re.IGNORECASE))

regos='(?P<os>w(indows)?)[ ](?P<num>([0-9]*([.,][0-9]*)?|vista))?(?P<type>[ ]*pro)?'
os = re.search(regos,description,re.IGNORECASE)
print(os.group('os'))
print(os.group('num'))
print(os.group('type'))
print(re.search(regos,description,re.IGNORECASE))
#peu être un peu trop large vu que w8 marche, laisser indows obligatoire ?

regarch = '[ .,]+64[ ]*bit(s)?'
print(re.search(regarch,description,re.IGNORECASE))

regram = '[ .,]+4[ ]*gi?[ob][ ]*(ddr3)?[a-z ]*[ ]*(sd)?ram'
print(re.search(regram,description,re.IGNORECASE))


regdd = '[ .,]+256[ ]*gi?[ob][a-z ]*(ssd)?'
#chercher également avec '[ .,]ssd[a-z ]256[ ]*gi?[ob]' ?
print(re.search(regdd,description,re.IGNORECASE))

reggraph = 'carte[ ]*graphique[a-z ]*intel[ ]*hd[ ]*(graphic)?'
print(re.search(reggraph,description,re.IGNORECASE))
#enlever carte graphique ?

#TODO : enlever les accents
regecran='[ ,.]+ecran[ ]*tactile[ ,]*(hd)?[ ]*(11[.,]6[ ]*(pouces?)?)?'
print(re.search(regecran,description,re.IGNORECASE))

