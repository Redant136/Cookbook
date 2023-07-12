import os
import re

dirs=[]
dirs.extend(os.listdir("./"))

aggregatedRecipes={}
aggregatedRecipes["Books"]=[]

with open("IndexFormat.md") as f:
    h1=""
    h2=""
    for line in f:
        if(re.match("# .*",line)):
            line=line.replace("# ","")
            line=line.replace("\n","")
            if not (line in aggregatedRecipes):
                aggregatedRecipes[line]={}
            h1=line
        if(re.match("## .*",line)):
            line=line.replace("## ","")
            line=line.replace("\n","")
            if not (line in aggregatedRecipes[h1]):
                aggregatedRecipes[h1][line]=[]
            h2=line



for d in dirs:
    if d[0]==".":
        continue
    if re.match(".*\..+",d):
        continue
    filePath=d+"/"+d+".md"
    toWrite="- ["+d+"]("+filePath.replace(" ","%20")+")"
    if not(toWrite in aggregatedRecipes["Books"]):
        aggregatedRecipes["Books"].append(toWrite)
    with open(filePath) as f:
        lang="en"
        h1=""
        h2=""
        for line in f:
            if(re.match("lang=.+",line)):
                lang=re.match("lang=(.+)",line).groups()[0]
                continue
            if(re.match("# .*",line)):
                line=line.replace("# ","")
                line=line.replace("\n","")
                if not (line in aggregatedRecipes):
                    aggregatedRecipes[line]={}
                h1=line
            if(re.match("## .*",line)):
                line=line.replace("## ","")
                line=line.replace("\n","")
                if not (line in aggregatedRecipes[h1]):
                    aggregatedRecipes[h1][line]=[]
                h2=line
            if(re.match("### .*",line)):
                line=line.replace("### ","")
                line=line.replace("\n","")
                line="- ["+line+"]("+filePath.replace(" ","%20")+"#"+line.replace(" ","%20")+")"
                if not(next((item for item in aggregatedRecipes[h1][h2] if item["entry"] == line), None)):
                    rec={"entry":line,"lang":lang,"img":"","tags":[]}
                    aggregatedRecipes[h1][h2].append(rec)
            if (re.match("tags=.+(;.*)*",line)):
                line=line.replace("tags=","")
                line=line.replace("\n","")
                line=line.replace(" ","")
                tags=line.split(";")
                aggregatedRecipes[h1][h2][-1]["tags"]=tags
            if(re.match("also=(h1|h2):.+(;[h1,h2]:.+)*",line)):
                rec=aggregatedRecipes[h1][h2][-1]
                line=line.replace("also=","")
                line=line.replace("\n","")
                line=line.replace(" ","")
                also=line.split(";")
                nH1=h1
                nH2=h2
                for a in also:
                    match=re.match("(h1|h2):(.+)",a)
                    if(match[1]=="h1"):
                        nH1=match[2]
                    if(match[1]=="h2"):
                        nH2=match[2]
                aggregatedRecipes[nH1][nH2].append(rec)
            if(re.match("!\\[.+\\]\\(.+\\)",line)):
                img=re.match("!\\[.+\\]\\((.+)\\)",line)[1]
                if(re.match("img/.+",img)):
                    img=img.replace("img/","")
                aggregatedRecipes[h1][h2][-1]["img"]=img




f=open("Index.md","w")

# print(aggregatedRecipes)
bestOf=[]
for h1 in aggregatedRecipes.keys():
    f.write("# "+h1+"\n")
    if type(aggregatedRecipes[h1]) is list:
        for e in aggregatedRecipes[h1]:
            f.write(e+"\n")
    if type(aggregatedRecipes[h1]) is dict:
        for h2 in aggregatedRecipes[h1].keys():
            f.write("## "+h2+"\n")
            for e in aggregatedRecipes[h1][h2]:
                f.write(e["entry"]+"\n")
                if("bestOf" in e["tags"]):
                    if not(e in bestOf):
                        bestOf.append(e)
    
f.write("# Best Of\n")
for b in bestOf:
    f.write(b["entry"]+"\n")




