import re
description= "bonjour carte graphique intel hd,je vend cet ordinateur portable tactile en parfait état de marche. hp x360 310 g1.ssd de 256gb. 4gb de ram. ecran tactile.avec sa housse de transport, son chargeur d'origine et sa notice d'utilisation ainsi q'un cd d'installation. le tout 250e"

regmarquemodele = 'hp[ .,]*[a-z]*[ ]*x[ ]*360[ ]*(310)?'
print(re.search(regmarquemodele,description,re.IGNORECASE))


#regproc = 'intel[ ]*(pentium)?[ ]*n?[ ]*3540'
regproc ='[ .,]+intel [ ]*([a-z, ]*n?3540|pentium[ ]*n?[ ]*(3540)?)'
print(re.search(regproc,description,re.IGNORECASE))

regfreqproc= '[ .,]+2[., ]+66[ ]*ghz'
print(re.search(regfreqproc,description,re.IGNORECASE))

regos='[ .,]+w(indows)?[ ]*8([.,]1)?([ ]*pro)?'
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

