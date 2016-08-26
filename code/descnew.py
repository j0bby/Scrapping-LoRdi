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
	score = 0
	
	
	regmarquemodele = '(?P<marque>hp)[ ]*(?P<divers>[a-z]*)[ ]*(?P<modele>(x[ ]*360)|(360[ ]*x))[ ]*(?P<modadd>310)?'
	marquemodele = re.search(regmarquemodele,description,re.IGNORECASE)
	if marquemodele is not None:#les groupes marque et modele sont obligatoires si la regex est trouvée
		if marquemodele.group('marque') is not None:
			print("Marque : "+marquemodele.group('marque'))
			score +=25
		if marquemodele.group('divers') is not None:
			if marquemodele.group('divers'):
				print("Marque divers : "+marquemodele.group('divers'))
		if marquemodele.group('modele') is not None:
			print("Modele : "+marquemodele.group('modele'))
			score+=20
		if marquemodele.group('modadd') is not None: 
			print("Modele info " + marquemodele.group('modadd'))
			if marquemodele.group('modadd'):	
				score +=10
			else:
				score-=5
	else:
		score-=22
	
	#regproc = 'intel[ ]*(pentium)?[ ]*n?[ ]*3540'
	regproc ='intel [ ]*([a-z, ]*n?3540|pentium[ ]*n?[ ]*(3540)?)'
	proc = re.search(regproc,description,re.IGNORECASE)
	if proc is not None:
		print("Processeur : "+proc.group())
		score+=8
	else : 
		score-=4
	
	regfreqproc= '(2[ ]*66[ ]*ghz)'
	freqproc=re.search(regfreqproc,description,re.IGNORECASE)
	if freqproc is not None:
		print("Frequence processeur : "+freqproc.group())
		score+=3
	else : 
		score-=1

	regos='(?P<os>w(indows)?)[ ]?(?P<num>[0-9]{1,2}|vista|xp)[ ]*(?P<type>[ ]*pro|familial|n)?'
	os = re.search(regos,description,re.IGNORECASE)
	if os is not None:
		if os.group('os') is not None:
			print("OS : "+os.group('os'))
			score+=8
		if os.group('num') is not None:
			print("Version : "+os.group('num'))
			if (os.group('num') == "8") or (os.group('num') == "81") :
				score+=15
			else:
				score-=8
		if os.group('type') is not None:
			print("Type"+os.group('type'))
			if 'pro' in os.group('type'):
				score +=7
			else:
				score-=3
		else:
			score-=3
	else:
		score-=15
	
	regarch = '64[ ]*bit(s)?'
	arch = re.search(regarch,description,re.IGNORECASE)
	if arch is not None:
		print("Architecture : "+arch.group())
		if '64' in arch.group(): 
			score+=3
		else :
			score-=2
	else:
		score-=1
	regram = '(4[ ]*gi?[ob][ ]*(ddr3)?[ ]*(sd)?ram)'
	ram = re.search(regram,description,re.IGNORECASE)
	if ram is not None:
		print("Memoire ram "+ram.group(1))
		score+=7
	else: 
		score-=3
	
	
	regdd = '(?P<ssd1>ssd)?[ ]*(?P<taille>[0-9]{3}[ ]*gi?[ob])[ ]*(?P<ssd>ssd)?'
	dd=re.search(regdd,description,re.IGNORECASE)
	if dd is not None:
		print("Taille disque dur : "+dd.group('taille'))
		if dd.group('ssd1') is not None : 
			print('ssd ? : '+dd.group('ssd1'))
			score+=4
		elif dd.group('ssd') is not None : 
			print('ssd ? : '+dd.group('ssd'))
			score+=4
		else : 
			score-=2
		if '256' in dd.group('taille'):
			score+=7
		else :
			score-=4


	reggraph = '(carte[ ]*graphique[a-z ]*(?P<marque>intel)[ ]*(?P<c1>hd)?[ ]*(?P<c2>graphic)?)|((?P<marque2>intel)[ ]*((?P<c4>hd[ ]*graphic)|(?P<c5>(hd)|(graphic))))'
	graph = re.search(reggraph,description,re.IGNORECASE)
	if graph is not None:
		score+=15
		if graph.group('marque') is not None : 
	   		print("Carte graphique marque : "+ graph.group('marque'))
		if graph.group('c1') is not None : 
			print("HD ? : "+graph.group('c1'))
		if graph.group('c2') is not None :
	   		print("Modele : "+graph.group('c2'))
		if graph.group('marque2') is not None:
			print("Carte graphique marque : "+ graph.group('marque2'))
		if graph.group('c4') is not None:
			print("Carte graphique detail : "+ graph.group('c4'))
		if graph.group('c5') is not None:
			print("Carte graphique detail : "+ graph.group('c5'))

	
	regecran='[ ,.]+((?P<ecran>ecran[ ]*(tactile)?)[ ,]*(?P<c1>hd)?[ ]*(?P<c2>11[., ]*6[ ]*((pouces?)|")?)?)|((?P<c3>hd)?[ ]*(?P<c4>11[., ]*6[ ]*((pouces?)|")))'
	ecr = re.search(regecran,description,re.IGNORECASE)
	if ecr is not None:
		score+=10
		if ecr.group('ecran') is not None:
			print("Ecran : "+ecr.group('ecran'))
		if ecr.group('c1') is not None:
			print("HD ? "+ecr.group('c1'))
		if ecr.group('c2') is not None:
			print("Taille : "+ecr.group('c2'))
		if ecr.group('c3') is not None:
			print("HD ? "+ecr.group('c3'))
		if ecr.group('c4') is not None:
			print("Taille : "+ecr.group('c4'))
	reghousse='([ ]*housse)'
	housse = re.search(reghousse,description,re.IGNORECASE)
	if housse is not None:
		print("Housse ? "+housse.group())
		score+=7
	reglordi='([ ]lordi)'
	lordi = re.search(reglordi,description,re.IGNORECASE)
	if lordi is not None:
		print("Lordi ? "+lordi.group())
		score+=20
	regaudio='([ ]beats?[ ]*audio)'
	audio = re.search(regaudio,description,re.IGNORECASE)
	if audio is not None:
		print("Audio : "+audio.group())
		score+=7
	print("-"*100)
	print("score : ",score)
