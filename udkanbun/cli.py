import sys
from udkanbun import UDKanbun

def main():
  if len(sys.argv)<2:
    lzh=UDKanbun(mecab=True)
    while True:
      try:
        s=input()
      except:
        return
      print(lzh(s,raw=True),end="")
  else:
    f=open(sys.argv[1],"r")
    s=f.read()
    f.close()
    lzh=UDKanbun(mecab=True)
    print(lzh(s,raw=True),end="")

if __name__=="__main__":
  main()

