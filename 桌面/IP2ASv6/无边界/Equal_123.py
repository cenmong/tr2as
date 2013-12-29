#找出等于１，等于２，等于３的as
f=open("result_less3.txt","r")
f1=open("result_1.txt","a")
f2=open("result_2.txt","a")
f3=open("result_3.txt","a")
for i in f:
    tmp=i.split(':')
    tmp1=tmp[1].split()
    if len(tmp1)==1:
        if tmp1[0][0]=='1':
            f1.write(tmp[0]+":"+tmp[1])
        elif tmp1[0][0]=='2':
            f2.write(tmp[0]+":"+tmp[1])
        elif tmp1[0][0]=='3':
            f3.write(tmp[0]+":"+tmp[1])

