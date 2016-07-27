import re
description= "bonjour,je vend cet ordinateur portable tactile en parfait état de marche. hp x360 310 g1.ssd de 256gb. 4gb de ram. ecran tactile.avec sa housse de transport, son chargeur d'origine et sa notice d'utilisation ainsi q'un cd d'installation. le tout 250e"
caracs = {}
caracs[2011,'marque']="dell"
caracs[2011,'modele']= ["vosotro","v","130"]
caracs[2011,'processeur']=['U3600']
caracs[2011,'frequence processeur']=['1','2','ghz']
caracs[2011,'OS']=['Windows','7','(pro)?']
caracs[2011,'architecture os']='64'
caracs[2011,'carte mere']=['Intel','hm57']
caracs[2011,'ram']=['2','Gi?[ob]?']
caracs[2011,'disque dur']=['320','Gi?[ob]?']
caracs[2011,'carte graphique']=['Intel','graphic','media','accelerator','hd']
caracs[2011,'ecran']=['HD','13','3','pouces']
caracs[2011,'webcam']=['2','Mega','pixels']
caracs[2011,'bluetooth']=['bluetooth','3.0']


caracs[2015,'marque']="hp"
caracs[2015,'modele']= ["x","360","310"]
caracs[2015,'processeur']=['intel','pentium','n','3540']
caracs[2015,'frequence processeur']=['2','66','ghz']
caracs[2015,'OS']=['Windows','8.1','(pro)?']
caracs[2015,'architecture os']='64'
caracs[2015,'carte mere']=[]
caracs[2015,'ram']=['4','Gi?[ob]?']
caracs[2015,'disque dur']=['256','Gi?[ob]?','(ssd)?']
caracs[2015,'carte graphique']=['Intel','hd','graphic']
caracs[2015,'ecran']=['tactile','HD','11','6','pouces']
caracs[2015,'webcam']=['hd','720','p']
caracs[2015,'bluetooth']=[]

print(re.search(r'[ .,]'+caracs[2015,'marque']+r'\b',description,re.IGNORECASE))
regmodele =""
for word in caracs[2015,'modele']:
    regmodele += r'[ .,]*'+word

print(re.search(regmodele,description,re.IGNORECASE))

regprocesseur=""
for word in caracs[2015,'processeur']:
    regprocesseur+= r'[ .,]*'+word

print(re.search(regprocesseur,description,re.IGNORECASE))

regfreqproc = caracs[2015,'frequence processeur'][0]+'[.,]'+caracs[2011,'frequence processeur'][1]+r'[ ]*'+caracs[2011,'frequence processeur'][2]

print(re.search(regfreqproc,description,re.IGNORECASE))

regos=""
for word in caracs[2015,'OS']:
    regos+= r'[ .,]*'+word

print(re.search(regos,description,re.IGNORECASE))

regarch= caracs[2015,'architecture os']+r'[ ]*bits?'
print(re.search(regarch,description,re.IGNORECASE))


regcarte=""
for word in caracs[2015,'carte mere']:
    regcarte+= r'[ .,]*'+word
if regcarte != "":
    print(re.search(regcarte,description,re.IGNORECASE))

regram=""
for word in caracs[2015,'ram']:
    regram+= r'[ .,]*'+word
print(re.search(regram,description,re.IGNORECASE))

regdd=""
for word in caracs[2015,'disque dur']:
    regdd+= r'[ .,]*'+word

print(re.search(regdd,description,re.IGNORECASE))

reggraph=""
for word in caracs[2015,'carte graphique']:
    reggraph+= r'[ .,]*'+word

print(re.search(reggraph,description,re.IGNORECASE))


