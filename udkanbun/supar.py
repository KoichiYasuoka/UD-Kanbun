#! /usr/bin/python3 -i
# coding=utf-8

import os
DOWNLOAD_DIR=os.path.join(os.path.abspath(os.path.dirname(__file__)),"supar-kanbun")
MODEL_URL="https://raw.githubusercontent.com/KoichiYasuoka/UD-Kanbun/master/udkanbun/supar-kanbun/"
filesize={}
with open(os.path.join(DOWNLOAD_DIR,"filesize.txt"),"r") as f:
  r=f.read()
for t in r.split("\n"):
  s=t.split()
  if len(s)==2:
    filesize[s[0]]=int(s[1])

from supar import Parser

class SuParAPI(object):
  def __init__(self,model):
    f=os.path.join(DOWNLOAD_DIR,model)
    try:
      s=os.path.getsize(f)
    except:
      s=-1
    if filesize[model]!=s:
      from udkanbun.download import download
      download(MODEL_URL,model,DOWNLOAD_DIR)
    self.supar=Parser.load(f)
  def process(self,conllu):
    c=conllu.split("\n")
    u=[]
    e=""
    for s in c:
      if s.startswith("#"):
        continue
      if s=="":
        if e!="":
          u.append(e.strip().split())
          e=""
      else:
        t=s.split("\t")
        i=t[9].find("Translit=")
        if i<0:
          j=t[1]
          if t[4]=="n,名詞,*,*":
            from udkanbun.simplify import simplify
            if t[1] in simplify:
              j=simplify[t[1]]
        else:
          j=t[9][i+9:]
        e+=j+" "
    d=self.supar.predict(u,lang=None)
    i=j=0
    for k,s in enumerate(c):
      if s.startswith("#"):
        continue
      if s=="":
        i+=1
        j=0
      else:
        t=s.split("\t")
        t[6]=str(d.sentences[i].values[6][j])
        t[7]=d.sentences[i].values[7][j]
        c[k]="\t".join(t)
        j+=1
    return "\n".join(c)

