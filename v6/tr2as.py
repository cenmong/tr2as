from patricia import *
from netaddr import *
import os

#START:store prefix2AS mapping in a trie
t = trie(None)
f = open('routeviews-rv6-20131220-1200.pfx2as', 'r')
s = f.readline().split()
s_addr = IPAddress(s[0]).bits()
s_addr = s_addr.replace(':', '')
s_addr = s_addr[:int(s[1])]

while 1:
    t[s_addr] = s[2]
    try:
        s = f.readline().split()
        s_addr = IPAddress(s[0]).bits()
        s_addr = s_addr.replace(':', '')
        s_addr = s_addr[:int(s[1])]
    except:
        break
f.close()
#END:store prefix2AS mapping in a trie
    
ASN_count = dict()
    
f = open("trpath","r")

for line in f.readlines():
    if line[0] == '#':
        continue
    #print '################'

    ASN_pre = '-1'#AS number of the previous hop
    count = 0#NO. of continous ASN
    start = True

    segment = line.split()
    j = 12
    while 1:
        j = j + 1#j should be >= 13 
        try:
            if segment[j] != 'q':#this hop does respond
                addr = segment[j].split(',')[0]
                addrbits = IPAddress(addr).bits()
                addrbits = addrbits.replace(':','')
                #get this address's AS number (a str)
                ASN = t.value(addrbits, start = 0, end = None)
                #print addr + ': ' + ASN
                if ASN == None:#cannot find ASN
                    if ASN_pre != '-1':
                        if start == True:
                            count = count + 30
                            start = False
                        try:
                            ASN_count[ASN_pre][count] = ASN_count[ASN_pre][count] + 1 
                        except:
                            #1:state.1~30:middle.31~60:start.61~90:end.
                            ASN_count[ASN_pre] = [0] * 91 
                            ASN_count[ASN_pre][count] = ASN_count[ASN_pre][count] + 1 
                        ASN_pre = '-1'
                        count = 0
                    else:
                        if start == True:#first hop no ASN
                            start = False
                        pass

                else:#can find the corresponding ASN
                    #print 'ASN_pre = ' + ASN_pre
                    #print 'ASN = ' + ASN
                    if ASN == ASN_pre:
                        count = count + 1
                    else:
                        if ASN_pre != '-1':
                            if start == True:
                                count = count + 30
                                start = False
                            try:
                                ASN_count[ASN_pre][count] = ASN_count[ASN_pre][count] + 1 
                            except:
                                ASN_count[ASN_pre] = [0] * 91 
                                ASN_count[ASN_pre][count] = ASN_count[ASN_pre][count] + 1 
                            ASN_pre = ASN
                            count = 1
                        else:
                            ASN_pre = ASN
                            count = 1

            else:#the hop does not respond
                #print 'q'
                if ASN_pre != '-1':
                    if start == True:
                        count = count + 30 
                        start = False
                    try:
                        ASN_count[ASN_pre][count] = ASN_count[ASN_pre][count] + 1 
                    except:
                        ASN_count[ASN_pre] = [0] * 91 
                        ASN_count[ASN_pre][count] = ASN_count[ASN_pre][count] + 1 
                    ASN_pre = '-1'
                    count = 0
                else:
                    if start == True:#first hop no response
                        start = False
                    pass

        except:#end of path
            if count > 0:
                count = count + 60
                try:
                   ASN_count[ASN_pre][count] = ASN_count[ASN_pre][count] + 1 
                except:
                   ASN_count[ASN_pre] = [0] * 91 
                   ASN_count[ASN_pre][count] = ASN_count[ASN_pre][count] + 1 
                ASN_pre = '-1'
                count = 0
                
            break
f.close()

f = open('output', 'a')
for ASN in ASN_count.keys():
    f.write(ASN + ':')
    for i in range(1, 31):
        if ASN_count[ASN][i] > 0:
            f.write(str(i) + '(' + str(ASN_count[ASN][i]) + '), ')
    for i in range(31, 61):
        if ASN_count[ASN][i] > 0:
            f.write(str(i - 30) + '(' + str(ASN_count[ASN][i]) + 'S), ')
    for i in range(61, 91):
        if ASN_count[ASN][i] > 0:
            f.write(str(i - 60) + '(' + str(ASN_count[ASN][i]) + 'E), ')
    f.write('\n')
f.close()
