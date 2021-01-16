#! /usr/bin/python -i
# coding=utf-8

import os
PACKAGE_DIR=os.path.abspath(os.path.dirname(__file__))

class UDPipeEntry(object):
  def __init__(self,result):
    if "\n" in result:
      t=[UDPipeEntry("0\t_\t_\t_\t_\t_\t0\t_\t_\t_")]
      for r in result.split("\n"):
        w=UDPipeEntry(r)
        if w.id>0:
          t.append(w)
      self._tokens=t
      for w in t:
        w._parent=self
        w.head=w._head
      self._result=result
    else:
      w=result.split("\t")
      try:
        w[0],w[6]=int(w[0]),int(w[6])
      except:
        w=[0]*10
      self.id,self.form,self.lemma,self.upos,self.xpos,self.feats,self._head,self.deprel,self.deps,self.misc=w if len(w)==10 else [0]*10
      self._result=""
  def __setattr__(self,name,value):
    v=value
    if name=="head":
      t=self._parent._tokens
      i=t.index(self)
      v=self if v==0 else t[i+v-self.id]
    if hasattr(self,name):
      if getattr(self,name)!=v:
        super(UDPipeEntry,self._parent).__setattr__("_result","")
        if name=="id":
          t=self._parent._tokens
          i=t.index(self)
          j=i+v-self.id
          super(UDPipeEntry,t[j]).__setattr__("id",t[i].id)
          t[i],t[j]=t[j],t[i]
    super(UDPipeEntry,self).__setattr__(name,v)
  def __repr__(self):
    if self._result!="":
      r=self._result
    elif hasattr(self,"_tokens"):
      r="".join(str(t)+"\n" for t in self._tokens[1:]).replace("\n1\t","\n\n1\t")
    else:
      r="\t".join([str(self.id),self.form,self.lemma,self.upos,self.xpos,self.feats,str(0 if self.head is self else self.head.id),self.deprel,self.deps,self.misc])
    return r if type(r) is str else r.encode("utf-8")
  def __getitem__(self,item):
    return self._tokens[item]
  def __len__(self):
    return len(self._tokens)
  def index(self,item):
    return self._tokens.index(item)
  def to_svg(self,item=0):
    if not hasattr(self,"_tokens"):
      return self._parent.to_svg(self._parent.index(self))
    s='<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"  width="100%" height="100%" onload="conllusvg.view(this,+conllu+)" onresize="conllusvg.rewrite(+conllu+)">\n'.replace("+","'")
    s+='<text id="conllu" fill="none" visibility="hidden">\n'
    if item==0:
      s+=str(self)
    else:
      from itertools import takewhile
      i=item-self[item].id
      for j in takewhile(lambda j:j-self[j].id==i,range(i+1,len(self))):
        s+=str(self[j])+'\n'
    s+='</text>\n<script type="text/javascript"><![CDATA[\n'
    import deplacy
    f=open(os.path.join(deplacy.PACKAGE_DIR,"conllusvgview.js"),"r",encoding="utf-8")
    s+=f.read()
    f.close()
    s+=']]></script>\n</svg>\n'
    return s

class UDKanbunEntry(UDPipeEntry):
  def kaeriten(self):
    import udkanbun.kaeriten
    k=udkanbun.kaeriten.kaeriten(self)
    s="".join("\n"+self[i].form+k[i] if self[i].id==1 else self[i].form+k[i] for i in range(1,len(self))).strip()
    return s+"\n"
  def to_tree(self,BoxDrawingWidth=1,kaeriten=False,Japanese=False,CatenaAnalysis=True):
    import deplacy
    if not hasattr(self,"_tokens"):
      return None
    p=deplacy.renderMatrix(self,CatenaAnalysis)
    if kaeriten:
      import udkanbun.kaeriten
      k=udkanbun.kaeriten.kaeriten(self)
    else:
      k=[[]]*len(self)
    u=[" ","\u2578","\u257A","\u2550","\u2579","\u255D","\u255A","\u2569","\u257B","\u2557","\u2554","\u2566","\u2551","\u2563","\u2560","\u256C","<"]
    if CatenaAnalysis:
      u[7]=u[5]
      u[11]=u[9]
      u[15]=u[12]
    if Japanese:
      import deplacy.deprelja
      r=deplacy.deprelja.deprelja
    else:
      r={}
    s=""
    for i in range(1,len(self)):
      w=self[i].form[0]
      w="  " if w=="_" else w
      t="".join(u[j] for j in p[i-1])
      if BoxDrawingWidth>1:
        t=t.replace(" "," "*BoxDrawingWidth).replace("<"," "*(BoxDrawingWidth-1)+"<")
      if self[i].deprel in r:
        s+=w+" "+t+" "+self[i].deprel+"("+r[self[i].deprel]+")\n"
      else:
        s+=w+" "+t+" "+self[i].deprel+"\n"
      if len(self[i].form)>1 or k[i]!=[]:
        t="".join(u[((j&8)>>1)*3] for j in p[i-1])
        if BoxDrawingWidth>1:
          t=t.replace(" "," "*BoxDrawingWidth)
        for w in self[i].form[1:]:
          s+=(w+" "+t).rstrip()+"\n"
        for w in k[i]:
          s+=(w+" "+t).rstrip()+"\n"
    return s

class UDKanbun(object):
  def __init__(self,mecab,danku,model):
    import ufal.udpipe
    if model==None:
      m=ufal.udpipe.Model.load(os.path.join(PACKAGE_DIR,"ud-kanbun.udpipe"))
    else:
      m=ufal.udpipe.Model.load(model)
    self.model=m
    if mecab:
      try:
        from MeCab import Tagger
      except:
        from fugashi import GenericTagger as Tagger
      self.mecab=Tagger("-r "+os.path.join(PACKAGE_DIR,"mecabrc")+" -d "+os.path.join(PACKAGE_DIR,"mecab-kanbun"))
      self.udpipe=ufal.udpipe.Pipeline(m,"conllu","none","","")
    else:
      self.mecab=False
      if danku:
        self.udpipe=ufal.udpipe.Pipeline(m,"tokenizer=joint_with_parsing","","","")
      else:
        self.udpipe=ufal.udpipe.Pipeline(m,"tokenizer=presegmented","","","")
    self.danku=danku
  def __call__(self,sentence,raw=False):
    if self.mecab:
      if self.danku==False:
        p=sentence.replace("\u3001","\u3001\n").replace("\u3002","\u3002\n")
      elif self.danku==True:
        import udkanbun.danku
        try:
          self.danku=udkanbun.danku.SegShenShen()
          p=self.danku(sentence)
        except:
          self.danku=udkanbun.danku.SegUDKanbun()
          p=self.danku(sentence)
      else:
        p=self.danku(sentence)
      u=""
      id=1
      for s in p.split("\n"):
        if s=="":
          continue
        m=self.mecab.parse(s)
        u+="# text = "+s+"\n"
        for w in m.split("\n"):
          if w=="EOS":
            u+="\n"
            id=1
          elif w!="":
            s=w.split("\t")
            t=s[1].split(",")
            lemma=s[0] if t[6]=="*" else t[6]
            i=lemma.find("/")
            if i>0:
              translit=lemma[i+1:]
              lemma=lemma[0:i]
            else:
              translit=lemma
            misc="SpaceAfter=No" if t[9]=="*" else "Gloss="+t[9]+"|SpaceAfter=No"
            if translit!=s[0]:
              misc+="|Translit="+translit
            u+="\t".join([str(id),s[0],lemma,t[7],t[0]+","+t[1]+","+t[2]+","+t[3],t[8].replace("*","_"),"_","_","_",misc])+"\n"
            id+=1
    elif self.danku==False:
      u=sentence.replace("\u3002","\u3002\n").replace("\uFF0E","\uFF0E\n").replace(".",".\n")
    else:
      u=sentence
    if raw:
      return self.udpipe.process(u)
    else:
      return UDKanbunEntry(self.udpipe.process(u))

def load(MeCab=True,Danku=False):
  return UDKanbun(MeCab,Danku,None)

