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

class UDKanbun(object):
  def __init__(self,mecab):
    import ufal.udpipe
    m=ufal.udpipe.Model.load(os.path.join(PACKAGE_DIR,"ud-kanbun.udpipe"))
    self.model=m
    if mecab:
      import MeCab
      self.mecab=MeCab.Tagger("-d "+os.path.join(PACKAGE_DIR,"mecab-kanbun"))
      self.udpipe=ufal.udpipe.Pipeline(m,"conllu","none","","")
    else:
      self.mecab=False
      self.udpipe=ufal.udpipe.Pipeline(m,"tokenizer=presegmented","","","")
  def __call__(self,sentence):
    if self.mecab:
      u=""
      id=1
      for s in sentence.split("\n"):
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
            misc="SpaceAfter=No" if t[9]=="*" else "Gloss="+t[9]+"|SpaceAfter=No"
            u+="\t".join([str(id),s[0],lemma,t[7],t[0]+","+t[1]+","+t[2]+","+t[3],t[8].replace("*","_"),"_","_","_",misc])+"\n"
            id+=1
      return UDPipeEntry(self.udpipe.process(u))
    else:
      return UDPipeEntry(self.udpipe.process(sentence))

def load(MeCab=True):
  return UDKanbun(MeCab)

