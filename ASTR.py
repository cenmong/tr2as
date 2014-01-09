from patricia import *
from netaddr import *
import os

class ASTR():
    def __init__(self, string):
        if string == 'ipv4':
            self.tp = 4#type:4 or 6
        elif string == 'ipv6':
            self.tp = 6
        self.ASN_count = dict()
        self.hdname = 'chenmeng/A2A6CFC5A6CF97E5'#hard dist where traceroute data are stored
        self.t = trie(None)#px2AS trie
        self.exist_c = 0# the number of existence of all ASes
        self.none_c = 0#number of all Nones(no corresponding AS) 
        self.p_c = 0#number of all p's

    def set_hdname(self, string):
        self.hdname = string

    def get_trie(self, filename):#change filename into file_list if possible
        f = open(filename, 'r')
        s = f.readline().split()
        s_addr = IPAddress(s[0]).bits()
        if self.tp == 4:
            s_addr = s_addr.replace('.', '')
        else:
            s_addr = s_addr.replace(':', '')
        s_addr = s_addr[:int(s[1])]

        while 1:
            self.t[s_addr] = s[2]
            try:
                s = f.readline().split()
                s_addr = IPAddress(s[0]).bits()
                if self.tp == 4:
                    s_addr = s_addr.replace('.', '')
                else:
                    s_addr = s_addr.replace(':', '')
                s_addr = s_addr[:int(s[1])]
            except:
                break
        f.close()
        print str(self.tp) + ': trie generation complete...'
        
    def increase_dict(self, ASN_pre, pos):#used by get_dict()
        ac = self.ASN_count
        try:
            ac[ASN_pre][pos] += 1 
        except:
            #0:existence number.1~50:middle.51~100:start.101~150:end.
            #151~160:state values
            #-1:existence level
            #-2:largest value level
            #-4:largest value
            #-5:existence of transit situations
            #-6:largest value of transit situations
            #-7:==1 if only has value 1 and 2
            #-8:==1 if only has value 2 and 3
            ac[ASN_pre] = [0] * 161 
            ac[ASN_pre][pos] += 1

        #record number of existence
        if pos - 100 > 0:
            ac[ASN_pre][0] += pos - 100
            self.exist_c += pos - 100
        elif pos - 50 > 0:
            ac[ASN_pre][0] += pos - 50
            self.exist_c += pos - 50
        else:
            ac[ASN_pre][0] += pos
            self.exist_c += pos

    def get_dict(self, file_list, file_pfx2as):
        has_output = os.path.exists(str(self.tp) + 'output')
        if has_output == True:
            print str(self.tp) + 'output exist. For speed, dict will be generated basing on it...'
            ac = self.ASN_count
            f = open(str(self.tp) + 'output', 'r')
            for line in f.readlines():
                if line[0] == '*':#end of file
                    break
                temp = line.split(':')
                if temp[0] == '>=4':
                    ASN = temp[1]
                    values = temp[2]
                else:
                    ASN = temp[2]
                    values = temp[3]
                ac[ASN] = [0] * 161
                values = values.split('), ')
                for v in values:
                    try:
                        v = v.split('(')
                        if 'S' in v[1]:
                            ii = int(v[1].replace('S', ''))
                            ac[ASN][50 + int(v[0])] = ii
                            ac[ASN][0] += ii 
                            self.exist_c += ii
                        elif 'E' in v[1]:
                            ii = int(v[1].replace('E', ''))
                            ac[ASN][100 + int(v[0])] = ii
                            ac[ASN][0] += ii 
                            self.exist_c += ii
                        else:
                            ac[ASN][int(v[0])] = int(v[1])
                            ac[ASN][0] += int(v[1]) 
                            self.exist_c += int(v[1])
                    except:#end of line
                        break
            f.close()
            return ac

        self.get_trie(file_pfx2as)
        f0 = open(file_list, 'r')
        as12 = []
        as23 = []
        f12 = open('as12in6', 'r')
        for line in f12:
            as12.append(line.split('|')[0])
        f23 = open('as23in6', 'r')
        for line in f23:
            as23.append(line.split('|')[0])
        f1212 = open('12resultv6', 'a')
        f2323 = open('23resultv6', 'a')
        for ff in f0:
            print 'reading file: ' + ff[:-10]
            if self.tp == 4:
                f = open('/media/' + self.hdname +\
                    '/topo-data.caida.org/team-probing/' + ff[:-10], 'r')
            else:
                f = open('/media/' + self.hdname +\
                    '/topo-data.caida.org/topo-v6/' + ff[:-10], 'r')
            

            for line in f.readlines():
                if line[0] == '#':
                    continue

                ASN_pre = '-1'#AS number of the previous hop, -1: initial value
                count = 0#No. of continous ASN
                count_none = 0#No.of continues 'p' and None
                count_none_none = 0
                count_none_p = 0
                start = True

                segment = line.split()
                j = 12
                while 1:
                    j += 1#the first hop is j == 13 
                    try:
                        if segment[j] != 'q':#this hop does respond
                            addr = segment[j].split(',')[0]
                            addrbits = IPAddress(addr).bits()
                            if self.tp == 4:
                                addrbits = addrbits.replace('.', '')
                            else:
                                addrbits = addrbits.replace(':', '')
                            #get this address's AS number (a str)
                            ASN = self.t.value(addrbits, start = 0, end = None)                        
                            if ASN == None:#cannot find ASN
                                self.none_c += 1
                                if ASN_pre != '-1':#this is not starting nones
                                    count_none += 1
                                    count_none_none += 1
                                else:# ASN_pre == -1 means this is the start
                                    #we just omit the starting *s and Nones
                                    start = False

                            else:#can find the corresponding ASN
                                if self.tp == 6:
                                    if ASN in as12:
                                        f1212.write(line)
                                    elif ASN in as23:
                                        f2323.write(line)
                                if ASN_pre == '-1':#the first ASN
                                    count = 1
                                    ASN_pre = ASN
                                else:
                                    if ASN == ASN_pre:#* and None can lies in between
                                        count += 1
                                    else:
                                        if start == True:#ASN_pre is the starting AS
                                            count += 50
                                            start = False
                                        self.increase_dict(ASN_pre, count + count_none)
                                        self.none_c -= count_none_none
                                        self.p_c -= count_none_p
                                        ASN_pre = ASN
                                        count = 1
                                        count_none = 0
                                        count_none_none = 0
                                        count_none_p = 0

                        else:#the hop does not respond
                            self.p_c += 1
                            if ASN_pre != '-1':#this is not starting nones
                                count_none += 1
                                count_none_p += 1
                            else:# ASN_pre == -1 means this is the start
                                start = False

                    except:#end of path
                        if count > 0:
                            count += 100
                            self.increase_dict(ASN_pre, count + count_none)
                            self.none_c -= count_none_none
                            self.p_c -= count_none_p
                        break
            f.close()
        f0.close()
        f12.close()
        f23.close()
        f1212.close()
        f2323.close()
        return self.ASN_count
        #END:store statistics in a dict
        print str(self.tp) + ': dict generation complete...'

    def classify(self, counts, lvalues):#x,y:lists of boundary values
        num = len(counts)
        state1 = -1
        state2 = -1
        lvalue = -1#large value
        ac = self.ASN_count

        for k in ac.keys():
            for i in xrange(0, num):
                if ac[k][0] <= counts[i]:
                    state1 = i
                    break
            if state1 == -1:#larger than counts[num - 1]
                state1 = num
            #if state1 != 0:
            #    print 'state1 = ' + str(state1)

            for j in xrange(1, 51):
                if ac[k][j] > 0:
                    if j > lvalue:
                        lvalue = j
            for j in xrange(51, 101):
                if ac[k][j] > 0:
                    if j - 50 > lvalue:
                        lvalue = j - 50
            for j in xrange(101, 151):
                if ac[k][j] > 0:
                    if j - 100 > lvalue:
                        lvalue = j - 100

            for i in xrange(0, num):
                if lvalue <= lvalues[i]:
                    state2 = i
                    break
            if state2 == -1:#larger than lvalues[num - 1]
                state2 = num
            #print 'state2 = ' + str(state2)

            ac[k][-1] = state1
            ac[k][-2] = state2
            ac[k][-4] = lvalue

            for j in xrange(1, 51):#only care about transit situations
                ac[k][-5] += ac[k][j]
                if ac[k][j] > 0 and j > ac[k][-6]:
                    ac[k][-6] = j

            if ac[k][-4] == 2:
                if ac[k][1] != 0 or ac[k][51] != 0 or ac[k][101] != 0:
                    ac[k][-7] = 1
            if ac[k][-4] == 3:
                if ac[k][2] != 0 or ac[k][52] != 0 or ac[k][102] != 0:
                    ac[k][-8] = 1

            state1 = -1
            state2 = -1
            lvalue = -1

        return ac 

    def print_ASN(self, f, ASN):#used by get_output
        ac = self.ASN_count
        f.write(ASN + ':')
        for i in xrange(1, 51):
            if ac[ASN][i] > 0:
                f.write(str(i) + '(' + str(ac[ASN][i]) + '), ')
        for i in xrange(51, 101):
            if ac[ASN][i] > 0:
                f.write(str(i - 50) + '(' + str(ac[ASN][i]) + 'S), ')
        for i in xrange(101, 151):
            if ac[ASN][i] > 0:
                f.write(str(i - 100) + '(' + str(ac[ASN][i]) + 'E), ')
        f.write('\n')
        
    def get_output(self, filename):
        fexist = os.path.exists(filename)
        if fexist == True:
            os.system('rm ' + filename)

        ge4_c = 0
        e1_c = 0
        e2_c = 0
        e3_c = 0
        le2_c = 0
        le3_c = 0

        f = open(filename, 'a')
        for ASN in self.ASN_count.keys():
            ge4 = False

            for i in xrange (1, 151):
                if self.ASN_count[ASN][i] > 0:
                    if i not in xrange (1, 4) and i not in xrange (51, 54) and i not in\
                    xrange(101, 104):
                        ge4 = True
                        break

            if ge4 == True:
                ge4_c += 1
                f.write('>=4:')
                self.print_ASN(f, ASN)
                continue

            le3_c += 1
            f.write('<=3:')
            has1 = False
            has2 = False
            has3 = False
            if self.ASN_count[ASN][1] > 0 or self.ASN_count[ASN][51] > 0 or\
            self.ASN_count[ASN][101] > 0:
                has1 = True
            if self.ASN_count[ASN][2] > 0 or self.ASN_count[ASN][52] > 0 or\
            self.ASN_count[ASN][102] > 0:
                has2 = True
            if self.ASN_count[ASN][3] > 0 or self.ASN_count[ASN][53] > 0 or\
            self.ASN_count[ASN][103] > 0:
                has3 = True

            if has1 == True and has2 == False and has3 == False:
                f.write('==1:')
                e1_c += 1
                le2_c += 1
                self.print_ASN(f, ASN)
                continue

            if has1 == False and has2 == True and has3 == False:
                f.write('==2:')
                e2_c += 1
                le2_c += 1
                self.print_ASN(f, ASN)
                self.ASN_count[ASN][-3] = 1 
                continue

            if has1 == True and has2 == True and has3 == False:
                f.write('<=2 other:')
                le2_c += 1
                self.print_ASN(f, ASN)
                continue

            if has1 == False and has2 == False and has3 == True:
                f.write('==3:')
                e3_c += 1
                self.print_ASN(f, ASN)
                continue

            f.write('<=3 other:')
            self.print_ASN(f, ASN)

        f.write('**************************************STATISTICS*********************************\n')
        total = le3_c + ge4_c
        f.write('total:' + str(total) + '\n')
        f.write('==1:' + str(e1_c) + '(' + str(float(e1_c)/float(total) * 100) +'%)\n')
        f.write('==2:' + str(e2_c) + '(' + str(float(e2_c)/float(total) * 100) +'%)\n')
        f.write('==3:' + str(e3_c) + '(' + str(float(e3_c)/float(total) * 100) +'%)\n')
        f.write('<=2:' + str(le2_c) + '(' + str(float(le2_c)/float(total) * 100) +'%)\n')
        f.write('<=3:' + str(le3_c) + '(' + str(float(le3_c)/float(total) * 100) +'%)\n')
        f.write('>=4:' + str(ge4_c) + '(' + str(float(ge4_c)/float(total) * 100) +'%)\n')

        f.write('exist_c = ' + str(self.exist_c) + '\n')
        f.write('none_c = ' + str(self.none_c) + '\n')
        f.write('p_c = ' + str(self.p_c) + '\n')

        f.close()
        print str(self.tp) + ': output complete!'

