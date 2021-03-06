from patricia import *
from netaddr import *
import os
from env import *

class ASTR():
    def __init__(self, string):
        if string == 'ipv4':
            self.tp = 4
        elif string == 'ipv6':
            self.tp = 6
        self.ASN_count = dict()# key: AS Number. value: integer list.
        self.t = trie(None)# px2AS trie
        self.exist_c = 0# the total number of existence of all ASes
        self.none_c = 0# the total number of all Nones(no corresponding AS) 
        self.p_c = 0# the total number of all p's(no response)

    # Used in get_dict() when mapping IPs to AS numbers.
    # Read the prefix2as file and build a trie on which a node stands for a prefix
    # and the values stored in tree nodes are AS numbers.
    def get_trie(self, filename):
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
        print 'IPv' + str(self.tp) + ': trie generation complete...'
       
    #used in get_dict(). Increase ASN_pre's dict value in position pos
    def increase_dict(self, ASN_pre, pos):
        ac = self.ASN_count
        try:
            ac[ASN_pre][pos] += 1 
        except:
            ac[ASN_pre] = [0] * 171 
            # 0: total existence count
            # 1~50:middle (transient). 51~100:start. 101~150:end.
            # 151~170:attributes
            # -1:existence level (unused)
            # -2:largest value level (unused)
            # -4:the largest value
            # -5:total existence of transit situations (sum of 1~50)
            # -6:largest value of transit situations (max of 1~50)
            # -7:==1 if only has value 2. ==2 if has both 1 and 2.
            # -8:==1 if only has value 3. ==2 if only has both 2 and 3. ==3 if has
            # all 1 and 2 and 3. ==4 if only has both 1 and 3.
            ac[ASN_pre][pos] += 1

        # ASx ASy ASy ASy ASz should only add 1 existence to ASy!
        ac[ASN_pre][0] += 1
        self.exist_c += 1
        '''
        if pos - 100 > 0:
            ac[ASN_pre][0] += pos - 100
            self.exist_c += pos - 100
        elif pos - 50 > 0:
            ac[ASN_pre][0] += pos - 50
            self.exist_c += pos - 50
        else:
            ac[ASN_pre][0] += pos
            self.exist_c += pos
        '''
    def get_dict(self, file_list, file_pfx2as, yearmonth):
        # If output files (4output and 6output) has already been generated,
        # here we directly use them to conduct the dict, which significantly saves time :)
        if self.tp == 4:
            has_output = os.path.exists('output/' + str(self.tp) + 'output' +
                    yearmonth[0] + yearmonth[1] + str(yearmonth[2]))
        if self.tp == 6:
            has_output = os.path.exists('output/' + str(self.tp) + 'output' +
                    yearmonth[0] + yearmonth[1])
        if has_output == True:
            print str(self.tp) + 'output already exist and dict will be generated using it...'
            ac = self.ASN_count
            if self.tp == 4:
                f = open('output/' + str(self.tp) + 'output' +
                        yearmonth[0] + yearmonth[1] + str(yearmonth[2]), 'r')
            if self.tp == 6:
                f = open('output/' + str(self.tp) + 'output' +
                        yearmonth[0] + yearmonth[1], 'r')
            for line in f.readlines():
                if line.split(' = ')[0] == 'exist_c':
                    self.exist_c = int(line.split(' = ')[1])
                    continue
                if line.split(' = ')[0] == 'none_c ':
                    self.none_c  = int(line.split(' = ')[1])
                    continue
                if line.split(' = ')[0] == 'p_c':
                    self.p_c = int(line.split(' = ')[1])
                    continue
                if line[0] == '*' or line == '' or line == '\n':
                    continue
                temp = line.split(':')
                if temp[0] == '>=4':
                    ASN = temp[1]
                    try:
                        values = temp[2]
                    except:
                        continue
                else:
                    try:
                        ASN = temp[2]
                        values = temp[3]
                    except:
                        continue
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

        # If no output yet (first time process of these data)
        self.get_trie(file_pfx2as)
        f0 = open(file_list, 'r')
        # I temprarily # everything about pmtud because it is still an
        # immature idea that need further research
        '''
        as12 = []
        as23 = []
        f12 = open('as12in6', 'r')#as12/23in6 are generated in main.py.
        for line in f12:
            as12.append(line.split('|')[0])
        f23 = open('as23in6', 'r')
        for line in f23:
            as23.append(line.split('|')[0])
        f1212 = open('12resultv6', 'a')#TODO: I use it before I create it!!!
        f2323 = open('23resultv6', 'a')
        '''
        for ff in f0:
            print 'reading file: ' + ff.replace('\n', '')
            if self.tp == 4:
                f = open(hdname + ff.replace('\n', ''), 'r')
            else:
                f = open(hdname + ff.replace('\n', ''), 'r')
            
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
                                '''
                                if self.tp == 6:
                                    if ASN in as12:
                                        f1212.write(line)
                                    elif ASN in as23:
                                        f2323.write(line)
                                '''
                                if ASN_pre == '-1':#ASN is the first one
                                    count = 1
                                    ASN_pre = ASN
                                else:#ASN is not the first one
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
        '''
        f12.close()
        f23.close()
        f1212.close()
        f2323.close()
        '''
        return self.ASN_count
        print 'IPv' + str(self.tp) + ': dict generation complete...'

    # This function sets many important attribute values for each AS.
    # I temporarily # anything about classification because it is still
    # inmature
    def set_attri(self):
        '''
        num = len(counts)
        state1 = -1
        state2 = -1
        '''
        lvalue = -1# largest value
        ac = self.ASN_count

        for k in ac.keys():
            '''
            for i in xrange(0, num):
                if ac[k][0] <= counts[i]:
                    state1 = i
                    break
            if state1 == -1:#larger than counts[num - 1]
                state1 = num
            '''
            # get the largest value from 1~150
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
            '''
            for i in xrange(0, num):
                if lvalue <= lvalues[i]:
                    state2 = i
                    break
            if state2 == -1:#larger than lvalues[num - 1]
                state2 = num

            # Actually I don't care about attributes -1 and -2 now
            ac[k][-1] = state1
            ac[k][-2] = state2
            '''
            ac[k][-4] = lvalue

            #set three important attributes in pos -5 -6 -7 and -8
            for j in xrange(1, 51):
                ac[k][-5] += ac[k][j]
                if ac[k][j] > 0 and j > ac[k][-6]:
                    ac[k][-6] = j
            # AS k has largest value 2
            if ac[k][-4] == 2:
                if ac[k][1] != 0 or ac[k][51] != 0 or ac[k][101] != 0:
                    ac[k][-7] = 2
                else:
                    ac[k][-7] = 1
            # AS k has largest value 3 
            if ac[k][-4] == 3:
                if ac[k][2] != 0 or ac[k][52] != 0 or ac[k][102] != 0:
                    if ac[k][1] != 0 or ac[k][51] != 0 or ac[k][101] != 0:
                        ac[k][-8] = 3
                    else:
                        ac[k][-8] = 2
                elif ac[k][1] != 0 or ac[k][51] != 0 or ac[k][101] != 0:
                    ac[k][-8] = 4
                else:
                    ac[k][-8] = 1
                        
            '''
            state1 = -1
            state2 = -1
            '''
            lvalue = -1

        return ac 

    #used by get_output() to print info of each AS
    def print_ASN(self, f, ASN):
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
