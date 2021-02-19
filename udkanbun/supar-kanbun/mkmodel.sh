#! /bin/sh
# pip3 install torch==1.6.0+cu101 torchvision==0.7.0+cu101 -f https://download.pytorch.org/whl/torch_stable.html
# pip3 install supar@git+https://github.com/yzhangcs/parser
if [ $# -eq 0 ]
then set guwenbert-base guwenbert-large
fi
for M
do if [ -s $M.supar ]
   then continue
   elif [ -s $M.supar.10 ]
   then cat $M.supar.[1-9] $M.supar.[1-9][0-9] > $M.supar
   elif [ -s $M.supar.1 ]
   then cat $M.supar.[1-9] > $M.supar
   elif [ -s lzh_kyoto.conllu ]
   then cat lzh_kyoto.conllu | python3 -c '
c=[]
while True:
  try:
    s=input()
  except:
    quit()
  t=s.split("\t")
  if len(t)==10:
    if t[0]!="#":
      c.append(s)
  elif s.strip()=="":
    if len(c)>1:
      print("\n".join(c)+"\n")
    c=[]
' | tee traditional.conllu | python3 -c '
from udkanbun.simplify import simplify
c=[]
while True:
  try:
    s=input()
  except:
    quit()
  t=s.split("\t")
  if len(t)==10:
    if t[0]!="#":
      u=""
      for i in t[1]:
        if i in simplify:
          u+=simplify[i]
        else:
          u+=i
      t[1]=u
      c.append("\t".join(t))
  elif s.strip()=="":
    print("\n".join(c)+"\n")
    c=[]
' | tee simplified.conllu | nawk '
BEGIN{
  f[0]="test.conllu";
  f[1]="dev.conllu";
  for(i=2;i<10;i++)
    f[i]="train.conllu";
}
{
  printf("%s\n",$0)>f[i%10];
  if($0=="")
    i++;
}'
        python3 -m supar.cmds.biaffine_dependency train -b -d 0 -p ./$M.supar --epochs=1000 -f bert --bert ethanyt/$M --train train.conllu --dev dev.conllu --test test.conllu --embed=''
        split -a 2 -b 83886080 --numeric-suffixes=01 $M.supar $M.supar.
        ls -1 $M.supar.0[1-9] | sed 's/^\(.*\)0\([1-9]\)$/mv & \1\2/' | sh
done
   fi
done
ls -ltr *.supar | awk '{printf("%s %d\n",$NF,$5)}' > filesize.txt
exit 0
