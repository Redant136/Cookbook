import os
import re

# print(os.walk("~/")[0])

bestOf=["- [Tuna rice](Homemade%20-%20Antoine%20Chevalier/Homemade%20-%20Antoine%20Chevalier.md#Tuna%20rice)",
"- [Seared sesame tuna](5%20Ingredients%20-%20Jamie%20Oliver/5%20Ingredients%20-%20Jamie%20Oliver.md#Seared%20sesame%20tuna)",
"- [Pork porcini pasta](5%20Ingredients%20-%20Jamie%20Oliver/5%20Ingredients%20-%20Jamie%20Oliver.md#Pork%20porcini%20pasta)"]
dirs=["Homemade - Antoine Chevalier"]
dirs.extend(os.listdir("./"))

objectList={}


for d in dirs:
    if d[0]==".":
        continue
    if re.match(".*\..+",d):
        continue
    filePath=d+"/"+d+".md"
    with open(filePath) as f:
        lang="en"
        h1=""
        h2=""
        for line in f:
            if(re.match("lang=.+",line)):
                lang=re.match("lang=(.+)",line).groups()[0]
                if not (lang in objectList):
                    objectList[lang]={}
                    objectList[lang]["Books"]=[]
                continue
            if(re.match("# .*",line)):
                line=line.replace("# ","")
                line=line.replace("\n","")
                if not (line in objectList[lang]):
                    objectList[lang][line]={}
                h1=line
            if(re.match("## .*",line)):
                line=line.replace("## ","")
                line=line.replace("\n","")
                if not (line in objectList[lang][h1]):
                    objectList[lang][h1][line]=[]
                h2=line
            if(re.match("### .*",line)):
                line=line.replace("### ","")
                line=line.replace("\n","")
                line="- ["+line+"]("+filePath.replace(" ","%20")+"#"+line.replace(" ","%20")+")"
                if not(line in objectList[lang][h1][h2]):
                    objectList[lang][h1][h2].append(line)
        if not ("Books" in objectList[lang]):
            objectList["Books"]=[]
        toWrite="- ["+d+"]("+filePath.replace(" ","%20")+")"
        if not(toWrite in objectList[lang]["Books"]):
            objectList[lang]["Books"].append(toWrite)

f=open("Index.md","w")


for lang in objectList.keys():
    for h1 in objectList[lang].keys():
        f.write("# "+h1+"\n")
        if type(objectList[lang][h1]) is list:
            for e in objectList[lang][h1]:
                f.write(e+"\n")
        if type(objectList[lang][h1]) is dict:
            for h2 in objectList[lang][h1].keys():
                f.write("## "+h2+"\n")
                for e in objectList[lang][h1][h2]:
                    f.write(e+"\n")

f.write("# Best Of\n")
for b in bestOf:
    f.write(b+"\n")




