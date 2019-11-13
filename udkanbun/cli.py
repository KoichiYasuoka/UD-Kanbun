import sys
from udkanbun import UDKanbun

def main():
  argc=len(sys.argv)
  i=1
  optu=optt=False
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
      if optt==True:
        print(lzh(s).to_tree(w),end="")
      else:
        print(lzh(s,raw=True),end="")
  lzh=UDKanbun(True)
  while i<argc:
    f=open(sys.argv[i],"r",encoding="utf-8")
    s=f.read()
    f.close()
    if optt==True:
      print(lzh(s).to_tree(w),end="")
    else:
      print(lzh(s,raw=True),end="")
    i+=1

def usage():
  from pkg_resources import get_distribution
  print("UD-Kanbun Version "+get_distribution("udkanbun").version,file=sys.stderr)
  print("Usage: udkanbun [-u|-t|-t2] file",file=sys.stderr)
  sys.exit()

if __name__=="__main__":
  main()

