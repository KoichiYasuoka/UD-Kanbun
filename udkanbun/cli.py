import sys
from udkanbun import UDKanbun

def main():
  if len(sys.argv)<2:
    lzh=UDKanbun(True)
    while True:
      try:
        s=input()
      except:
        return
      print(lzh(s,raw=True),end="")
  else:
    f=open(sys.argv[1],"r",encoding="utf-8")
    s=f.read()
    f.close()
    lzh=UDKanbun(True)
    print(lzh(s,raw=True),end="")

if __name__=="__main__":
  main()

