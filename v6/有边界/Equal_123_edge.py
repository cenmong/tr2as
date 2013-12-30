#找出等于１，等于２，等于３的AS
f=open("result_edge_less3.txt","r")
f1=open("result_1_edge.txt","a")
f2=open("result_2_edge.txt","a")
f3=open("result_3_edge.txt","a")
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
		elif len(tmp1)==2:
				if int(tmp1[0][0])==1:
						print tmp1[0][0]
						if int(tmp1[1][0])==1:
								f1.write(tmp[0]+":"+tmp[1])
				if tmp1[0][0]=='2':
						print tmp1[0][0]
						if int(tmp1[1][0])==2:
								f2.write(tmp[0]+":"+tmp[1])
				if tmp1[0][0]=='3':
						print tmp1[0][0]
						if int(tmp1[1][0])==3:
								f3.write(tmp[0]+":"+tmp[1])
