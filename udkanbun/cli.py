import sys
from udkanbun import UDKanbun

def main():
  argc=len(sys.argv)
  i=1
  optu=optt=optk=False
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
    else:
      break
    i+=1
  else:
    lzh=UDKanbun(True)
    while True:
      try:
        s=input()
      except:
        return
      print(output(lzh,optu,optt,optk,s),end="")
  lzh=UDKanbun(True)
  while i<argc:
    f=open(sys.argv[i],"r",encoding="utf-8")
    s=f.read()
    f.close()
    print(output(lzh,optu,optt,optk,s),end="")
    i+=1

def output(lzh,optu,optt,optk,sentence):
  if optt==True:
    return lzh(sentence).to_tree(BoxDrawingWidth=w,kaeriten=optk)
  if optu==True:
    if optk==False:
      return(lzh(sentence,raw=True))
    from udkanbun.kaeriten import kaeriten
    t=lzh(sentence)
    k=kaeriten(t).split("\n")
    s=""
    for i,r in enumerate(t.split("\n\n")):
      if r=="":
        continue
      for u in r.split("\n"):
        if u=="":
          continue
        s+=u+"\n"
        if s.startswith("# text = "):
          s+="# text_with_kaeriten = "+k[i]+"\n"
      s+="\n"
    return s
  if optk==True:
    return(lzh(sentence).kaeriten())
  return(lzh(sentence,raw=True))

def usage():
  from pkg_resources import get_distribution
  print("UD-Kanbun Version "+get_distribution("udkanbun").version,file=sys.stderr)
  print("Usage: udkanbun [-u|-t|-t2|-k] file",file=sys.stderr)
  print("  output format:",file=sys.stderr)
  print("    -u  Universal Dependencies CoNLL-U",file=sys.stderr)
  print("    -t  tree (optional BoxDrawingWidth)",file=sys.stderr)
  print("    -k  kaeriten",file=sys.stderr)
  sys.exit()

if __name__=="__main__":
  main()

