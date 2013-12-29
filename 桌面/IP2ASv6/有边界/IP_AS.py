from patricia import *
#import ipaddr
from netaddr import *
import os
t = trie(None)
l = list()
f2 = open('result_trie', 'a')
f = open('routeviews-rv6-20131101-1200.pfx2as', 'r')
# print 'file No.' + str(i)
s = f.readline().split()
s_addr = IPAddress(s[0]).bits()
s_addr = s_addr.replace(':', '')
s_addr = s_addr[:int(s[1])]
#print s_addr + '/' + str(len(s_addr))
while 1:
    t[s_addr] = s[2]
    try:
        s = f.readline().split()
        s_addr = IPAddress(s[0]).bits()
        s_addr = s_addr.replace(':', '')
        s_addr = s_addr[:int(s[1])]
        #print s_addr + '/' + str(len(s_addr))
    except:
        break

ite = t.iter('')
ite.next()

while 1:
    try:
        f2.write(ite.next() + '\n')
    except:
        break

f2.close()
f3 = open("traceroute_path.txt","r")
f4 =open("IP_AS","a")
f5 = open("AS_Level","a")
for i in f3:
    tmp = i.split()
    j = 0
    f4.write("T"+"  ")
    f5.write("T"+"  ")
    while 1:
        j=j+1
        try:
            if tmp[j]!="q":
                str = IPAddress(tmp[j]).bits()
                str = str.replace(':','')
                value =t.value(str,start = 0,end = None)
                if value ==None:
                    f4.write(tmp[j]+",None"+"    ")
                    f5.write("None"+"    ")
                else:
                    f4.write(tmp[j]+","+value+"    ")
                    f5.write(value+"    ")
              #  print tmp[j],t.value(str,start=0,end=None,default=NULL)
            else:
               f4.write(tmp[j]+",q"+"    ")
               f5.write("q"+"    ")
              # print tmp[j],tmp[j]
        except:
            f4.write('\n')
            f5.write('\n')
            break
