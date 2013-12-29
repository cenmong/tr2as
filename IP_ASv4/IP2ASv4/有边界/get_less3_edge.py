import sys
f2=open("get_Dict_edge","r")
f3=open("result_edge_less3_tmp1","a")
for k in f2:
    tmp1=k.split(':')
    l=0
    val=tmp1[1].split(',')
    while 1:
        try:
            if int(val[l][0])>3:
                break
            else:
                l=l+1
        except:
            f3.write(k)
            break
f2.close()
f3.close()
f4=open("result_edge_less3_tmp1","r")
f5=open("result_edge_less3_tmp2.txt","w")
for i in f4:
    i=i.rstrip('\n')
    i=i.rstrip()
    tmp = i.split(':')
    f5.write(tmp[0]+":")
    tmp1 = tmp[1].split(',')
    tmp1.sort()
    myset = set(tmp1)
    for item in myset:
        f5.write(item+"("+str(tmp1.count(item))+")"+'  ')
    f5.write('\n')
f4.close()
f5.close()
f6=open("result_edge.txt","a")
f7=open("result_edge_less3_tmp2.txt","r")
D={}
k=0
m=0
n=0
for j in f7:
    tmp2=j.split(':')
    if tmp2[0].find("_")!=-1:
        f6.write(j)
    elif tmp2[0].find(";")!=-1:
	    f6.write(j)
    elif tmp2[0]=="None":
	    f6.write(j)
    elif tmp2[0]=="q":
	    f6.write(j)
    else:
        try:
            D[int(tmp2[0])]=tmp2[1]
            k=k+1
        except:
            break
sorted(D.keys())
for m in sorted(D.keys()):
    f6.write(str(m)+':'+D[m])
