from patricia import *
from netaddr import *
import os

class V6Dict():
    ASN_count = dict()
    t = trie(None)#px2AS trie
    hdname = 'chenmeng/A2A6CFC5A6CF97E5'
    exist_c = 0# the number of existence of all ASes
    none_c = 0#number of None(no corresponding AS) and p

    def set_hdname(self, string):
        self.hdname = string

    def get_trie(self, filename):#change filename into file_list if possible
        f = open(filename, 'r')
        s = f.readline().split()
        s_addr = IPAddress(s[0]).bits()
        s_addr = s_addr.replace(':', '')
        s_addr = s_addr[:int(s[1])]

        while 1:
            self.t[s_addr] = s[2]
            try:
                s = f.readline().split()
                s_addr = IPAddress(s[0]).bits()
                s_addr = s_addr.replace(':', '')
                s_addr = s_addr[:int(s[1])]
            except:
                break
        f.close()
        print 'v6 trie generation complete...'
        
    def increase_dict(self, ASN_pre, pos):#used by get_dict()
        ac = self.ASN_count
        try:
            ac[ASN_pre][pos] += 1 
        except:
            #1:existence number.1~30:middle.31~60:start.
            #61~90:end.91~100:state values
            ac[ASN_pre] = [0] * 101 
            ac[ASN_pre][pos] += 1

        #record number of existence
        if pos - 60 > 0:
            ac[ASN_pre][0] += pos - 60
        elif pos - 30 > 0:
            ac[ASN_pre][0] += pos - 30
        else:
            ac[ASN_pre][0] += pos
        
        #increment all exist number
        self.exist_c += ac[ASN_pre][0]

    def get_dict(self, file_list):
        has_output = os.path.exists('6output')
        if has_output == True:
            print '6output exist. For speed, dict will be generated basing on it...'
            ac = self.ASN_count
            f = open('6output', 'r')
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
                ac[ASN] = [0] * 101#91 for v6 and 151 for v4
                values = values.split('), ')
                for v in values:
                    try:
                        v = v.split('(')
                        if 'S' in v[1]:
                            ac[ASN][30 + int(v[0])] = int(v[1].replace('S', ''))
                            self.exist_c += int(v[1].replace('S', ''))
                        elif 'E' in v[1]:
                            ac[ASN][60 + int(v[0])] = int(v[1].replace('E', ''))
                            self.exist_c += int(v[1].replace('E', ''))
                        else:
                            ac[ASN][int(v[0])] = int(v[1])
                            self.exist_c += int(v[1])
                    except:#end of line
                        break
            f.close()
            return self.ASN_count

        f0 = open(file_list, 'r')
        for ff in f0:
            print 'reading v6 file: ' + ff[:-10]
            f = open('/media/' + self.hdname +\
                    '/topo-data.caida.org/topo-v6/' + ff[:-10], 'r')

            for line in f.readlines():
                if line[0] == '#':
                    continue

                ASN_pre = '-1'#AS number of the previous hop, -1: initial value
                count = 0#No. of continous ASN
                count_none = 0#No.of continues 'p' and None
                start = True

                segment = line.split()
                j = 12
                while 1:
                    j += 1#the first hop is j == 13 
                    try:
                        if segment[j] != 'q':#this hop does respond
                            addr = segment[j].split(',')[0]
                            addrbits = IPAddress(addr).bits()
                            addrbits = addrbits.replace(':','')
                            #get this address's AS number (a str)
                            ASN = self.t.value(addrbits, start = 0, end = None)                        
                            #print addr + ': ' + ASN
                            if ASN == None:#cannot find ASN
                                if ASN_pre != '-1':#this is not starting nones
                                    count_none += 1
                                else:# ASN_pre == -1 means this is the start
                                    #we just omit the starting *s and Nones
                                    start = False
                                    self.none_c += 1

                            else:#can find the corresponding ASN
                                if ASN_pre == '-1':#the first ASN
                                    count = 1
                                    ASN_pre = ASN
                                else:
                                    if ASN == ASN_pre:#* and None can lies in between
                                        count += 1
                                    else:
                                        if start == True:#ASN_pre is the starting AS
                                            count += 30
                                            start = False
                                        self.increase_dict(ASN_pre, count +\
                                                count_none)
                                        self.none_c += count_none
                                        ASN_pre = ASN
                                        count = 1
                                        count_none = 0

                        else:#the hop does not respond
                            if ASN_pre != '-1':#this is not starting nones
                                count_none += 1
                            else:# ASN_pre == -1 means this is the start
                                start = False
                                self.none_c += 1

                    except:#end of path
                        if count > 0:
                            count += 60
                            self.increase_dict(ASN_pre, count + count_none)
                        self.none_c += count_none
                        break
            f.close()
        f0.close()
        return self.ASN_count
        #END:store statistics in a dict
        print 'v6 dict generation complete...'

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

            for j in xrange(1, 31):
                if ac[k][j] > 0:
                    if j > lvalue:
                        lvalue = j
            for j in xrange(31, 61):
                if ac[k][j] > 0:
                    if j - 30 > lvalue:
                        lvalue = j - 30
            for j in xrange(61, 91):
                if ac[k][j] > 0:
                    if j - 60 > lvalue:
                        lvalue = j - 60

            for i in xrange(0, num):
                if lvalue <= lvalues[i]:
                    state2 = i
                    break
            if state2 == -1:#larger than lvalues[num - 1]
                state2 = num

            ac[k][-1] = state1
            ac[k][-2] = state2

            state1 = -1
            state2 = -1
            lvalue = -1

        return ac 

    def print_ASN(self, f, ASN):#used by get_output
        ac = self.ASN_count
        f.write(ASN + ':')
        for i in xrange(1, 31):
            if ac[ASN][i] > 0:
                f.write(str(i) + '(' + str(ac[ASN][i]) + '), ')
        for i in xrange(31, 61):
            if ac[ASN][i] > 0:
                f.write(str(i - 30) + '(' + str(ac[ASN][i]) + 'S), ')
        for i in xrange(61, 91):
            if ac[ASN][i] > 0:
                f.write(str(i - 60) + '(' + str(ac[ASN][i]) + 'E), ')
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
            
            for i in xrange (1, 91):
                if self.ASN_count[ASN][i] > 0:
                    if i not in xrange (1, 4) and i not in xrange (31, 34) and i not in\
                    xrange(61, 64):
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
            if self.ASN_count[ASN][1] > 0 or self.ASN_count[ASN][31] > 0 or self.ASN_count[ASN][61] > 0:
                has1 = True
            if self.ASN_count[ASN][2] > 0 or self.ASN_count[ASN][32] > 0 or self.ASN_count[ASN][62] > 0:
                has2 = True
            if self.ASN_count[ASN][3] > 0 or self.ASN_count[ASN][33] > 0 or self.ASN_count[ASN][63] > 0:
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

        f.close()
        #END:output statistics into a file
        print '6output complete!'

