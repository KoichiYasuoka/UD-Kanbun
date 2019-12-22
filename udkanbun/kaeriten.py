def kaeriten(ud,matrix=False):
  w=len(ud)
  t=[[] for i in range(w)]
  h=[i+t.head.id-t.id for i,t in enumerate(ud)]
  s=[0]*w
  j=w
  for i in reversed(range(1,w)):
    s[i]=j
    if ud[i].id==1:
      j=i
# rule 1
  for i in range(1,w):
    if ud[i].deprel=="obj" and h[i]<i:
      t[i].append((h[i],1))
# rule 2
  for i in range(1,w):
    if ud[i].deprel.startswith("obl") and h[i]<i:
      t[i].append((h[i],2))
# rule 3
  for i in range(1,w):
    if ud[i].deprel=="expl" and h[i]<i:
      t[i].append((h[i],3))
# rule 4
  for i in range(1,w):
    if (ud[i].deprel=="ccomp" or ud[i].deprel=="xcomp" or ud[i].deprel=="advcl") and h[i]<i:
      t[i].append((h[i],4))
# rule 5
  for i in range(1,w):
    if ud[i].deprel=="cop" and h[i]>i:
      t[h[i]].append((i,5))
# rule 6
  for i in range(1,w):
    if (ud[i].deprel=="case" or ud[i].deprel=="mark") and h[i]>i:
      if not ud[i].xpos.startswith("v,前置詞,基盤,"):
        t[h[i]].append((i,6))
# rule 7
  for i in range(1,w):
    if ud[i].deprel=="aux" and h[i]>i:
      t[h[i]].append((i,7))
# rule 8
  for i in range(1,w):
    if ud[i].deprel=="advmod" and h[i]>i:
      x=ud[i].xpos.split(",")
      if x[1]=="副詞":
        if x[2]=="否定" or (x[2]=="判断" and x[3]=="逆接") or (x[2]=="時相" and x[3]=="将来"):
          t[h[i]].append((i,8))
      f=ud[i].form
      if f=="難" or f=="易" or f=="無":
        t[h[i]].append((i,8))
# rule 9
  for i in range(1,w):
    if ud[i].deprel=="cc" and h[i]>i:
      if ud[i].xpos.startswith("v,前置詞,関係,"):
        t[h[i]].append((i,9))
# rule 10
  for i in range(1,w):
    if ud[i].form=="況":
      for j in reversed(range(i+1,s[i])):
        x=[(a,b) for a,b in t[j] if a==i and b<5]
        if x!=[]:
          t[j]=[]
          for k in reversed(range(i+1,j)):
            if h[k]==j and (ud[k].deprel=="case" or ud[k].deprel=="mark"):
              t[j].append((k,10))
              break
# rule 11
  for i in range(1,w):
    if ud[i].form=="所":
      if ud[i].deprel=="case" or ud[i].deprel=="mark":
        if ud[h[i]].form=="謂" and h[i]>i:
          for j in reversed(range(h[i]+1,s[i])):
            x=[(a,b) for a,b in t[j] if a==h[i] and b<5]
            if x!=[]:
              t[j]=[]
# rule 12
  for i in range(1,w):
    if ud[i].form=="請":
      x=[ud[j].deprel for j in range(i-ud[i].id+1,s[i]) if h[j]==i]
      if "vocative" in x:
        for j in reversed(range(i+1,s[i])):
          x=[(a,b) for a,b in t[j] if a==i and b<5]
          if x!=[]:
            t[j]=[]
# rule 13
  for i in range(1,w):
    if ud[i].form!="焉":
      continue
    if ud[h[i]].xpos.startswith("v,動詞,描写,"):
      continue
    x=[(a,b) for a,b in t[i] if b==2]
    if x!=[]:
      t[i]=[]
# rule 14
  for i in range(1,w):
    if ud[i].deprel!="xcomp" and ud[i].deprel!="ccomp":
      continue
    for a,b in t[i]:
      f=ud[a].lemma
      if b==4 and (f=="如" or f=="若" or f=="奈"):
        x=[ud[j].deprel for j in range(i-ud[i].id+1,s[i]) if h[j]==a]
        if "obj" in x or "expl" in x:
          t[i].remove((a,4))
          t[i].extend(t[a])
          t[a]=[]
        break
# rule 15
  for i in reversed(range(1,w)):
    if ud[i].deprel!="xcomp":
      continue
    for a,b in t[i]:
      if b==4 and ud[a].lemma=="助":
        t[i].remove((a,4))
        t[i].extend(t[a])
        t[a]=[]
        break
# rule 16
  for i in reversed(range(1,w)):
    if ud[i].deprel!="xcomp":
      continue
    for a,b in t[i]:
      if b==4 and ud[a].lemma=="勸":
        t[i].remove((a,4))
        t[i].extend(t[a])
        t[a]=[]
        break
# rule 17
  for i in range(1,w):
    j=h[i]
    if ud[i].form!="所" or ud[j].form!="以":
      continue
    if ud[j].deprel!="advmod":
      continue
    x=[(a,17) for a,b in t[j] if b==6]
    if x!=[]:
      t[h[j]].extend(x)
      t[j]=[]
# rule 18
  for i in range(1,w):
    j=h[i]
    if ud[i].form!="所" or ud[j].form!="以":
      continue
    if ud[j].deprel=="advmod":
      continue
    x=[(a,b) for a,b in t[j] if b==6]
    if x==[]:
      continue
    x=[(a,18) for a,b in t[j] if b!=6 or a!=i]
    t[j]=[]
    for k in range(j-ud[j].id+1,s[j]):
      for y,(a,b) in enumerate(t[k]):
        if a==j:
          t[k][y]=(i,18)
    t[i].extend(x)
# rule 19
  for i in range(1,w):
    if ud[i].form!="能":
      continue
    if t[i]!=[]:
      continue
    j=h[i]
    x=[(a,b) for a,b in t[j] if a==i and b==7]
    if x!=[]:
      t[j].remove((i,7))
# rule 20
  for i in range(1,w):
    if ud[i].form!="敢" and ud[i].form!="肯":
      continue
    j=h[i]
    x=[(a,b) for a,b in t[j] if a==i and b==7]
    if x==[]:
      continue
    t[j].remove((i,7))
    t[j].extend(t[i])
    t[i]=[]
# rule 21
  for i in range(1,w):
    j=h[i]
    if ud[j].form!="得" or ud[i].form!="而":
      continue
    if i-j!=1:
      continue
    k=h[j]
    x=[(a,b) for a,b in t[k] if a==j and b==7]
    if x==[]:
      continue
    t[k].remove((j,7))
    t[k].extend(t[j])
    t[j]=[]
# rule 22
  for x in range(2):
    for i in reversed(range(1,w)):
      j=h[i]
      if j>i:
        continue
      d=ud[i].deprel
      if d=="clf" or d=="flat" or d=="case":
        t[i].extend(t[j])
        t[j]=[]
      elif d=="conj":
        for a,b in t[j]:
          if b!=8:
            t[i].append((a,b))
            t[j].remove((a,b))
# rule 23
  p=[]
  for i in range(w):
    p.append(None)
    for a,b in t[i]:
      if p[a]!=None:
        j,k,l=p[a]
        t[j].remove((k,l))
      p[a]=(i,a,b)
# rule 24
  for i in range(1,w):
    if t[i]==[]:
      continue
    t[i]=list(set(a for a,b in t[i]))
  for i in reversed(range(1,w)):
    if len(t[i])<2:
      continue
    m=max(t[i])
    for j in t[i]:
      if j<m:
        t[m].append(j)
    t[i]=[m]
# 交差チェック
  for i in reversed(range(1,w)):
    if t[i]==[]:
      continue
    j=t[i][0]
    for k in range(j+1,i):
      if t[k]!=[]:
        if t[k][0]<j:
          break
    else:
      continue
    t[i]=[]
  if matrix:
    return t
# レ点
  k=[]
  for i in range(w-1):
    if t[i+1]==[i] and len(ud[i+1].form)==1:
      k.append("\u3191")
      t[i+1]=[]
    else:
      k.append("")
  k.append("")
# 一二点
  p="\u3192\u3193\u3194\u3195五六七八九十"
  for i in reversed(range(1,w)):
    if t[i]==[]:
      continue
    x=[j for j in range(i+1,s[i]) if t[j]==[i]]
    if x!=[]:
      continue
    x=i
    n=1
    while t[x]!=[]:
      y=t[x][0]
      x=[j for j in range(y+1,x) if t[j]!=[]]
      if x!=[]:
        n=0
        break
      x=y
      n+=1
    if n==0 or n>len(p):
      continue
    x=i
    n=0
    while t[x]!=[]:
      k[x]=p[n]+k[x]
      n+=1
      y=t[x][0]
      t[x]=[]
      x=y
    k[x]=p[n]+k[x]
# 上下点
  p="\u3196\u3197\u3198"
  for i in reversed(range(1,w)):
    if t[i]==[]:
      continue
    x=[j for j in range(i+1,s[i]) if t[j]==[i]]
    if x!=[]:
      continue
    x=i
    n=1
    while t[x]!=[]:
      y=t[x][0]
      x=[j for j in range(y+1,x) if t[j]!=[]]
      if x!=[]:
        n=0
        break
      x=y
      n+=1
    if n==0 or n>len(p):
      continue
    x=i
    n=0
    while t[x]!=[]:
      k[x]=p[n]+k[x]
      n+=1
      y=t[x][0]
      t[x]=[]
      x=y
    k[x]=p[2]+k[x]
# 甲乙点
  p="\u3199\u319A\u319B\u319C戊己庚辛壬癸"
  for i in reversed(range(1,w)):
    if t[i]==[]:
      continue
    x=[j for j in range(i+1,s[i]) if t[j]==[i]]
    if x!=[]:
      continue
    x=i
    n=1
    while t[x]!=[]:
      y=t[x][0]
      x=[j for j in range(y+1,x) if t[j]!=[]]
      if x!=[]:
        n=0
        break
      x=y
      n+=1
    if n==0 or n>len(p):
      continue
    x=i
    n=0
    while t[x]!=[]:
      k[x]=p[n]+k[x]
      n+=1
      y=t[x][0]
      t[x]=[]
      x=y
    k[x]=p[n]+k[x]
# 天地点
  p="\u319D\u319E\u319F"
  for i in reversed(range(1,w)):
    if t[i]==[]:
      continue
    x=i
    n=1
    while t[x]!=[]:
      y=t[x][0]
      x=[j for j in range(y+1,x) if t[j]!=[]]
      if x!=[]:
        n=0
        break
      x=y
      n+=1
    if n==0 or n>len(p):
      continue
    x=i
    n=0
    while t[x]!=[]:
      k[x]=p[n]+k[x]
      n+=1
      y=t[x][0]
      t[x]=[]
      x=y
    k[x]=p[n]+k[x]
  return k

