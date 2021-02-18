#! /usr/bin/python3 -i
# coding=utf-8

import os,sys,time
tm=time.time()
fs=ft=0

def progress(block_count,block_size,total_size):
  t=time.time()
  p=100.0*(block_count*block_size+fs)/ft
  if p<1:
    t=-1
  elif p>=100:
    p=100
    t-=tm
  else:
    t=(t-tm)*(100-p)/p
  b=int(p/2)
  if b==50:
    s="="*50
  else:
    s=("="*b)+">"+(" "*(49-b))
  if t<0:
    u="   "
  elif t<3600:
    u=time.strftime("%M:%S   ",time.gmtime(t))
  elif t<86400:
    u=time.strftime("%H:%M:%S   ",time.gmtime(t))
  else:
    u=time.strftime("%d+%H:%M:%S   ",time.gmtime(t))
  print("\r ["+s+"] "+str(int(p))+"% "+u,end="",file=sys.stderr)

def download(url,file,dir="."):
  import urllib.request
  global fs,ft,tm
  t=os.path.join(dir,"filesize.txt")
  urllib.request.urlretrieve(url+"filesize.txt",t)
  with open(t,"r") as f:
    r=f.read()
  ft=0
  for t in r.split("\n"):
    s=t.split()
    if len(s)==2:
      if s[0]==file:
        ft=int(s[1])
  tm=time.time()
  with open(os.path.join(dir,file),"wb") as f:
    fs=0
    i=1
    while fs<ft:
      g,h=urllib.request.urlretrieve(url+file+"."+str(i),reporthook=progress)
      with open(g,"rb") as r:
        q=r.read()
      f.write(q)
      fs+=len(q)
      i+=1
  print("",flush=True,file=sys.stderr)

