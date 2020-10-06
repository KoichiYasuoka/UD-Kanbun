#! /usr/bin/python -i
# coding=utf-8

class SegUDKanbun(object):
  def __init__(self):
    import udkanbun
    self.udpipe=udkanbun.load(MeCab=False,Danku=True)
  def __call__(self,paragraph):
    p=paragraph.replace("\n","")
    s=""
    for t in self.udpipe(p):
      if t.id==1:
        s+="\n"
      if t.form!="_":
        s+=t.form
    return s[1:]+"\n"

class SegShenShen(object):
  def __init__(self):
    self.shenURL="https://seg.shenshen.wiki"
    self.apiURL=self.shenURL+"/api.php"
    self.header={"Content-Type":"application/x-www-form-urlencoded","Referer":self.shenURL,"User-Agent":"Mozilla 5.0 (SegShenShen)"}
  def __call__(self,paragraph):
    import re
    from urllib.parse import quote
    import urllib.request as req
    p=paragraph.replace("\n","")
    s=""
    while p>"":
      d='text={"text":"'+quote(p)+'"}&seg=duanju'
      u=req.Request(self.apiURL,d.encode(),self.header)
      with req.urlopen(u) as r:
        q=r.read()
      q=re.sub(r'<span class="tags0"> [^ ]+ </span>',"\n",q.decode("utf-8"))
      q=re.sub(r'<[^>]+>',"",q)
      q=q if type(q) is str else q.encode("utf-8")
      if len(p)==len(q.replace("\n","")):
        s+=q
        p=""
      else:
        q=q[0:q.rindex("\n",0,q.rindex("\n",0,q.rindex("\n")-1)-1)+1]
        s+=q
        p=p[len(q.replace("\n","")):]
    return s

