import re
with open('stopwords.txt', encoding="utf-8") as fileinput:
    with open('newstopwords.txt',"w", encoding="utf-8") as fileoutput :
        for line in fileinput:
           line = re.sub('[éèêë]',"e",line)
           line = re.sub('[àâä]',"a",line)
           line = re.sub('[ïî]',"i",line)
           line = re.sub('[ûùü]',"u",line)
           fileoutput.write(line)
print('Done')
