import sys
from udkanbun import UDKanbun

def main():
  argc=len(sys.argv)
  i=w=1
  optu=optt=optk=opts=False
  while i<argc:
    o=sys.argv[i]
    if o=="-h" or o=="--help" or o=="-v" or o=="--version":
      usage()
    elif o=="-u":
      optu=True
    elif o=="-t" or o=="-t1":
      optt=True
      w=1
    elif o=="-t2":
      optt=True
      w=2
    elif o=="-k":
      optk=True
    elif o=="-s":
      opts=True
    else:
      break
    i+=1
  else:
    lzh=UDKanbun(True,opts,None)
    while True:
      try:
        s=input()
      except:
        return
      print(output(lzh,optu,optt,optk,w,s),end="")
  lzh=UDKanbun(True,opts,None)
  while i<argc:
    f=open(sys.argv[i],"r",encoding="utf-8")
    s=f.read()
    f.close()
    print(output(lzh,optu,optt,optk,w,s),end="")
    i+=1

def output(lzh,optu,optt,optk,width,sentence):
  if optu:
    if optt:
      return lzh(sentence).to_svg()
    if not optk:
      return lzh(sentence,raw=True)
    t=lzh(sentence)
    k=t.kaeriten().split("\n")
    s=""
    for i,r in enumerate(str(t).split("\n\n")):
      if r=="":
        continue
      for u in r.split("\n"):
        if u=="":
          continue
        s+=u+"\n"
        if u.startswith("# text = "):
          s+="# text_with_kaeriten = "+k[i]+"\n"
      s+="\n"
    return s
  if optt:
    return lzh(sentence).to_tree(BoxDrawingWidth=width,kaeriten=optk,Japanese=optk)
  if optk:
    return lzh(sentence).kaeriten()
  return lzh(sentence,raw=True)

def usage():
  from pkg_resources import get_distribution
  print("UD-Kanbun Version "+get_distribution("udkanbun").version,file=sys.stderr)
  print("Usage: udkanbun [-u|-t|-t2|-s|-k] file",file=sys.stderr)
  print("  output format:",file=sys.stderr)
  print("    -u  Universal Dependencies CoNLL-U",file=sys.stderr)
  print("    -t  tree  (-t2  tree with BoxDrawingWidth=2)",file=sys.stderr)
  print("    -s  sentence segmentation",file=sys.stderr)
  print("    -k  kaeriten",file=sys.stderr)
  sys.exit()

if __name__=="__main__":
  main()

