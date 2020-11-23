#! /usr/bin/python3 -i
# coding=utf-8

import numpy
from spacy.language import Language
from spacy.symbols import LANG,NORM,LEMMA,POS,TAG,DEP,HEAD
from spacy.tokens import Doc,Span,Token
from spacy.util import get_lang_class

class UDKanbunLanguage(Language):
  lang="lzh"
  max_length=10**6
  def __init__(self,MeCab,Danku):
    self.Defaults.lex_attr_getters[LANG]=lambda _text:"lzh"
    try:
      self.vocab=self.Defaults.create_vocab()
      self.pipeline=[]
    except:
      from spacy.vocab import create_vocab
      self.vocab=create_vocab("lzh",self.Defaults)
      self._components=[]
      self._disabled=set()
    self.tokenizer=UDKanbunTokenizer(MeCab,Danku,self.vocab)
    self._meta={
      "author":"Koichi Yasuoka",
      "description":"derived from UD-Kanbun",
      "lang":"UD_Kanbun_lzh",
      "license":"MIT",
      "name":"UD_Kanbun_lzh",
      "parent_package":"udkanbun",
      "pipeline":"Tokenizer, POS-Tagger, Parser",
      "spacy_version":">=2.1.0"
    }
    self._path=None

class UDKanbunTokenizer(object):
  to_disk=lambda self,*args,**kwargs:None
  from_disk=lambda self,*args,**kwargs:None
  to_bytes=lambda self,*args,**kwargs:None
  from_bytes=lambda self,*args,**kwargs:None
  def __init__(self,mecab,danku,vocab):
    import udkanbun
    self.model=udkanbun.load(mecab,danku)
    self.vocab=vocab
  def __call__(self,text):
    u=self.model(text,raw=True) if text else ""
    vs=self.vocab.strings
    r=vs.add("ROOT")
    words=[]
    lemmas=[]
    pos=[]
    tags=[]
    feats=[]
    heads=[]
    deps=[]
    spaces=[]
    norms=[]
    for t in u.split("\n"):
      if t=="" or t.startswith("#"):
        continue
      s=t.split("\t")
      if len(s)!=10:
        continue
      id,form,lemma,upos,xpos,feat,head,deprel,dummy_deps,misc=s
      words.append(form)
      lemmas.append(vs.add(lemma))
      pos.append(vs.add(upos))
      tags.append(vs.add(xpos))
      feats.append(feat)
      if deprel=="root":
        heads.append(0)
        deps.append(r)
      else:
        heads.append(int(head)-int(id))
        deps.append(vs.add(deprel))
      spaces.append(False if "SpaceAfter=No" in misc else True)
      i=misc.find("Gloss=")
      if i<0:
        norms.append(vs.add(form))
      else:
        j=misc.find("|",i)
        norms.append(vs.add(misc[i+6:] if j<0 else misc[i+6:j]))
    doc=Doc(self.vocab,words=words,spaces=spaces)
    a=numpy.array(list(zip(lemmas,pos,tags,deps,heads,norms)),dtype="uint64")
    doc.from_array([LEMMA,POS,TAG,DEP,HEAD,NORM],a)
    try:
      doc.is_tagged=True
      doc.is_parsed=True
    except:
      for i,j in enumerate(feats):
        if j!="_" and j!="":
          doc[i].set_morph(j)
    return doc

def load(MeCab=True,Danku=False):
  return UDKanbunLanguage(MeCab,Danku)

def to_conllu(item,offset=1):
  if type(item)==Doc:
    return "".join(to_conllu(s)+"\n" for s in item.sents)
  elif type(item)==Span:
    return "# text = "+str(item)+"\n"+"".join(to_conllu(t,1-item.start)+"\n" for t in item)
  elif type(item)==Token:
    m="_" if item.whitespace_ else "SpaceAfter=No"
    if item.norm_!="":
      if item.norm_!=item.orth_:
        m="Gloss="+item.norm_+"|"+m
        m=m.replace("|_","")
    try:
      f=str(item.morph)
      if f.startswith("<spacy") or f=="":
        f="_"
    except:
      f="_"
    return "\t".join([str(item.i+offset),item.orth_,item.lemma_,item.pos_,item.tag_,f,str(0 if item.head==item else item.head.i+offset),item.dep_.lower(),"_",m])
  return "".join(to_conllu(s)+"\n" for s in item)

