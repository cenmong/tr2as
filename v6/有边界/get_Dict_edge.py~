f = open ("AS_Level","r")
f1 =open("AS_Num_edge_tmp1","a")
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
                f1.write(tmp[j]+","+str(count)+"    "+'\n')
                break
    else:
        continue
f.close()
f1.close()
f2=open("AS_Num_edge_tmp1","r")
f3=open("AS_Num_edge",'a')
for i in f2:
    tmp=i.split()
    tmp[0]=tmp[0]+'E'
    tmp[-1]=tmp[-1]+'E'
    f3.write('   '.join(tmp)+' ')
    #print tmp
f2.close()
f3.close()
f4=open("AS_Num_edge","r")
f5=open("get_Dict_edge","a")
for i in f4:
    tmp = i.split()
    print len(tmp)
    D={}
    j=-1
    while 1:
        print j
        j=j+1
        try:
		    str=tmp[j].split(',')
			try:
				D[str[0]]=D[str[0]]+","+str[1]
			except:
				D[str[0]]=str[1]
        except:
            for key in D:
                f5.write(key+":"+D[key]+"    "+'\n')
            break
f5.close()
