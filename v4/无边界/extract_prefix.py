import os
f=open("traceroute_path.txt","a")
os.chdir("data")
for filename in os.listdir(os.getcwd()):
    print filename
    #with open(filename,'r') as f0:
    for i in open(filename,'r'):
        tmp=i.split()
        f.write(tmp[0]+"    "+tmp[1]+"    "+tmp[2]+"    ")
        j=12
        while 1:
        #	tmp[j].split(",")[0]
            j=j+1
            try:
               f.write(tmp[j].split(",")[0]+"    ")
            except:
                f.write('\n')
                break
