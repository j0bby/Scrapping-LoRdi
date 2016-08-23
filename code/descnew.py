import re
import string
def findPatterns(description):
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
	#print (description)
	#Stopwords
	stopwords = []
	with open('newstopwords.txt',"r",encoding="utf-8") as fileinput:
		for line in fileinput:
	    		stopwords.append(line.rstrip())
	        
	description=' '.join([word for word in description.split() if word not in stopwords])
	#print(description)
	
	
	
	regmarquemodele = '(?P<marque>hp)[ ]*(?P<divers>[a-z]*)[ ]*(?P<modele>x[ ]*360)[ ]*(?P<modadd>310)?'
	marquemodele = re.search(regmarquemodele,description,re.IGNORECASE)
	if marquemodele is not None:
		if marquemodele.group('marque') is not None:
			print("Marque : "+marquemodele.group('marque'))
		if marquemodele.group('divers') is not None:
			print("Marque divers : "+marquemodele.group('divers'))
		if marquemodele.group('modele') is not None:
			print("Modele : "+marquemodele.group('modele'))
		if marquemodele.group('modadd') is not None: 
			print("Modele info " + marquemodele.group('modadd'))
	
	#regproc = 'intel[ ]*(pentium)?[ ]*n?[ ]*3540'
	regproc ='[ .,]+intel [ ]*([a-z, ]*n?3540|pentium[ ]*n?[ ]*(3540)?)'
	proc = re.search(regproc,description,re.IGNORECASE)
	if proc is not None:
		print("Processeur : "+proc.group())
	
	regfreqproc= '[ .,]+2[., ]+66[ ]*ghz'
	freqproc=re.search(regfreqproc,description,re.IGNORECASE)
	if freqproc is not None:
		print("Frequence processeur : "+freqproc.group())
	
	regos='(?P<os>w(indows)?)[ ](?P<num>([0-9]*([.,][0-9]*)?|vista|xp))?(?P<type>[ ]*pro|familial|n)?'
	os = re.search(regos,description,re.IGNORECASE)
	if os is not None:
		if os.group('os') is not None:
			print("OS : "+os.group('os'))
		if os.group('num') is not None:
			print("Version : "+os.group('num'))
		if os.group('type') is not None:
	   		print("Type"+os.group('type'))
	   # print(re.search(regos,description,re.IGNORECASE))
	#peu être un peu trop large vu que w8 marche, laisser indows obligatoire ?
	
	regarch = '[ .,]+64[ ]*bit(s)?'
	arch = re.search(regarch,description,re.IGNORECASE)
	if arch is not None:
		print("Architecture : "+arch.group())
	
	regram = '[ .,]+4[ ]*gi?[ob][ ]*(ddr3)?[a-z ]*[ ]*(sd)?ram'
	ram = re.search(regram,description,re.IGNORECASE)
	if ram is not None:
		print("Memoire ram "+ram.group())
	
	
	regdd = '[ .,]+256[ ]*gi?[ob][a-z ]*(ssd)?'
	#chercher également avec '[ .,]ssd[a-z ]256[ ]*gi?[ob]' ?
	dd=re.search(regdd,description,re.IGNORECASE)
	if dd is not None:
		print("Disque dur : "+dd.group())
	
	reggraph = 'carte[ ]*graphique[a-z ]*(?P<marque>intel)[ ]*(?P<c1>hd)[ ]*(?P<c2>graphic)?'
	graph = re.search(reggraph,description,re.IGNORECASE)
	if graph is not None:
		if graph.group('marque') is not None : 
	   		print("Carte graphique marque : "+ graph.group('marque'))
		if graph.group('c1') is not None : 
			print("HD ? : "+graph.group('c1'))
		if graph.group('c2') is not None : 
	   		print("Modele : "+graph.group('c2'))
	#enlever carte graphique ?
	
	regecran='[ ,.]+(?P<ecran>ecran[ ]*tactile)[ ,]*(?P<c1>hd)?[ ]*(?P<c2>11[.,]6[ ]*(pouces?)?)?'
	ecr = re.search(regecran,description,re.IGNORECASE)
	if ecr is not None:
		if ecr.group('ecran') is not None:
			print("Ecran : "+ecr.group('ecran'))
		if ecr.group('c1') is not None:
			print("HD ? "+ecr.group('c1'))
		if ecr.group('c2') is not None:
			print("Taille : "+ecr.group('c2'))
	
