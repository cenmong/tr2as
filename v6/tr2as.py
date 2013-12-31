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
print 'trie generation complete...'

#START:store statistics in a dict
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
#END:store statistics in a dict
print 'dict generation complete...'

#START:output statistics into a file
ge4_c = 0
e1_c = 0
e2_c = 0
e3_c = 0
le2_c = 0
le3_c = 0

f = open('output', 'a')
for ASN in ASN_count.keys():
    ge4 = False

    for i in range (1, 91):
        if ASN_count[ASN][i] > 0:
            if i not in range (1, 4) and i not in range (31, 34) and i not in\
            range(61, 64):
                ge4 = True
                break

    if ge4 == True:
        ge4_c = ge4_c + 1
        f.write('********************************************** >=4 ***********************************************\n')
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
        continue

    f.write('********************************************** <=3 ***********************************************\n')
    has1 = False
    has2 = False
    has3 = False
    le3_c = le3_c + 1
    if ASN_count[ASN][1] > 0 or ASN_count[ASN][31] > 0 or ASN_count[ASN][61] > 0:
        has1 = True
    if ASN_count[ASN][2] > 0 or ASN_count[ASN][32] > 0 or ASN_count[ASN][62] > 0:
        has2 = True
    if ASN_count[ASN][3] > 0 or ASN_count[ASN][33] > 0 or ASN_count[ASN][63] > 0:
        has3 = True

    if has1 == True and has2 == False and has3 == False:
        f.write('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ ==1 $$$$$$$$$$$$$$$$$$$$$$$$$$$\n')
        e1_c = e1_c + 1
        le2_c = le2_c + 1
        f.write(ASN + ':')
        for i in range(1, 4):
            if ASN_count[ASN][i] > 0:
                f.write(str(i) + '(' + str(ASN_count[ASN][i]) + '), ')
        for i in range(31, 34):
            if ASN_count[ASN][i] > 0:
                f.write(str(i - 30) + '(' + str(ASN_count[ASN][i]) + 'S), ')
        for i in range(61, 64):
            if ASN_count[ASN][i] > 0:
                f.write(str(i - 60) + '(' + str(ASN_count[ASN][i]) + 'E), ')
        f.write('\n')
        continue

    if has1 == False and has2 == True and has3 == False:
        f.write('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ ==2 $$$$$$$$$$$$$$$$$$$$$$$$$$$\n')
        e2_c = e2_c + 1
        le2_c = le2_c + 1
        f.write(ASN + ':')
        for i in range(1, 4):
            if ASN_count[ASN][i] > 0:
                f.write(str(i) + '(' + str(ASN_count[ASN][i]) + '), ')
        for i in range(31, 34):
            if ASN_count[ASN][i] > 0:
                f.write(str(i - 30) + '(' + str(ASN_count[ASN][i]) + 'S), ')
        for i in range(61, 64):
            if ASN_count[ASN][i] > 0:
                f.write(str(i - 60) + '(' + str(ASN_count[ASN][i]) + 'E), ')
        f.write('\n')
        continue

    if has1 == True and has2 == True and has3 == False:
        f.write('$$$$$$$$$$$$$$$$$$$$$$$$$$ <=2 other $$$$$$$$$$$$$$$$$$$$$$$$\n')
        le2_c = le2_c + 1
        f.write(ASN + ':')
        for i in range(1, 4):
            if ASN_count[ASN][i] > 0:
                f.write(str(i) + '(' + str(ASN_count[ASN][i]) + '), ')
        for i in range(31, 34):
            if ASN_count[ASN][i] > 0:
                f.write(str(i - 30) + '(' + str(ASN_count[ASN][i]) + 'S), ')
        for i in range(61, 64):
            if ASN_count[ASN][i] > 0:
                f.write(str(i - 60) + '(' + str(ASN_count[ASN][i]) + 'E), ')
        f.write('\n')
        continue

    if has1 == False and has2 == False and has3 == True:
        f.write('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ ==3 $$$$$$$$$$$$$$$$$$$$$$$$$$$\n')
        e3_c = e3_c + 1
        f.write(ASN + ':')
        for i in range(1, 4):
            if ASN_count[ASN][i] > 0:
                f.write(str(i) + '(' + str(ASN_count[ASN][i]) + '), ')
        for i in range(31, 34):
            if ASN_count[ASN][i] > 0:
                f.write(str(i - 30) + '(' + str(ASN_count[ASN][i]) + 'S), ')
        for i in range(61, 64):
            if ASN_count[ASN][i] > 0:
                f.write(str(i - 60) + '(' + str(ASN_count[ASN][i]) + 'E), ')
        f.write('\n')
        continue

    f.write('$$$$$$$$$$$$$$$$$$$$$$$$$$ <=3 other $$$$$$$$$$$$$$$$$$$$$$$$\n')
    f.write(ASN + ':')
    for i in range(1, 4):
        if ASN_count[ASN][i] > 0:
            f.write(str(i) + '(' + str(ASN_count[ASN][i]) + '), ')
    for i in range(31, 34):
        if ASN_count[ASN][i] > 0:
            f.write(str(i - 30) + '(' + str(ASN_count[ASN][i]) + 'S), ')
    for i in range(61, 64):
        if ASN_count[ASN][i] > 0:
            f.write(str(i - 60) + '(' + str(ASN_count[ASN][i]) + 'E), ')
    f.write('\n')

f.write('**************************************STATISTICS*********************************\n')
total = le3_c + ge4_c
f.write('total:' + str(total) + '\n')
f.write('==1:' + str(e1_c) + '(' + str(float(e1_c)/float(total) * 100) +'%)\n')
f.write('==2:' + str(e2_c) + '(' + str(float(e2_c)/float(total) * 100) +'%)\n')
f.write('==3:' + str(e3_c) + '(' + str(float(e3_c)/float(total) * 100) +'%)\n')
f.write('<=2:' + str(le2_c) + '(' + str(float(le2_c)/float(total) * 100) +'%)\n')
f.write('<=3:' + str(le3_c) + '(' + str(float(le3_c)/float(total) * 100) +'%)\n')
f.write('>=4:' + str(ge4_c) + '(' + str(float(ge4_c)/float(total) * 100) +'%)\n')

f.close()
#END:output statistics into a file
print 'output complete!'
