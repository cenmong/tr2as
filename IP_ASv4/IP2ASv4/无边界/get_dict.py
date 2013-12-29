import sys
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
f=open("AS_Num","r")
f1=open("AS_Dict","a")
for i in f:
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
                f1.write(key+":"+D[key]+"    "+'\n')
            break
f1.close()
