#首先统计traceroute路径中的连续AS的个数存在AS_Num,例如：AS1,AS1,AS1,AS2,AS2,AS3,AS3-->AS1,3 AS2,2 AS3,3
#然后将统计AS_Num中每个AS对应的情况,存储在AS_Dict,例如： AS1,3 AS2,2 AS3,2 AS1,3 AS3,1-->AS1:3,3  AS2:2 AS3:2,1 
f = open ("AS_Level","r")
f1 =open("AS_Num","a")
for i in f:
    print i
    tmp = i.split()
    j=2
    count=1
    if len(tmp)>3:
        while 1:
            j=j+1
            try:
                if tmp[j] == tmp[j+1]:
                    count = count+1
                else:
                    f1.write(tmp[j]+","+str(count)+"    ")
                    count = 1
                
            except:
                f1.write(tmp[j]+","+str(count)+"    ")
                break
    else:
        continue
f1.close()
f2=open("AS_Num","r")
f3=open("AS_Dict","a")
for i in f2:
    tmp = i.split()
    D={}
    j=-1
    while 1:
        j=j+1
        try:
            str=tmp[j].split(',')
            if D.has_key(str[0]):
                D[str[0]]=D[str[0]]+","+str[1]
            else:
                D[str[0]]=str[1]
        except:
            for key in D:
                f3.write(key+":"+D[key]+"    "+'\n')
            break
f3.close()
