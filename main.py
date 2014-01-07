from ASTR import *
import os

hd_name = 'chenmeng/A2A6CFC5A6CF97E5'#different in different computers

#-------------------------------IPv6 start-------------------------------#
astr6 = ASTR('ipv6')
astr6.set_hdname(hd_name)
astr6.get_dict('flist/6file_list', 'pfx2as/routeviews-rv6-20131224-1200.pfx2as')

astr6.get_output('6output')#don't change this string
exists = [10, 100, 1000]
lvalues = [1, 2, 4]
dict6 = astr6.classify(exists, lvalues)

exist_c6 = astr6.exist_c 
as_c6 = len(dict6.keys())
exist_per_as6 = float(exist_c6)/float(as_c6)

#-------------------------------IPv4 start-------------------------------#
astr4 = ASTR('ipv4')
astr4.set_hdname(hd_name)
astr4.get_dict('flist/4file_list_test', 'pfx2as/routeviews-rv2-20131226-1200.pfx2as')

astr4.get_output('4output')#don't change this string
exists = [50, 500, 5000]
lvalues = [1, 2, 4]
dict4 = astr4.classify(exists, lvalues)

exist_c4 = astr4.exist_c 
as_c4 = len(dict4.keys())
exist_per_as4 = float(exist_c4)/float(as_c4)

#-------------------------------IPv4/IPv6 analysis-------------------------------#
print 'analyzing v4/v6 results...'
#start:check file existence#
fexist = os.path.exists('alloutput')
if fexist == True:
    os.system('rm alloutput')
#end:check file existence#

#start:check file existence#
fexist = os.path.exists('intrestingAS')
if fexist == True:
    os.system('rm intrestingAS')
#end:check file existence#

#start:finding interesting ASes#
f = open('alloutput', 'a')
f1 = open('intrestingAS', 'a')
count_exist = 0
count_lvalue = 0
count_both = 0
for ASN in dict6.keys():
    if ASN in dict4.keys():
        if dict6[ASN][-3] == 1 and dict6[ASN][-1] > 0 and\
        dict4[ASN][-2] > 1 and dict4[ASN][-1] > 0:
            astr6.print_ASN(f1, ASN)
            astr4.print_ASN(f1, ASN)
            f1.write('------------------------------------\n')
        #if dict4[ASN][-3] == 1 and dict4[ASN][-1] > 0 and\
        #dict6[ASN][-2] > 1 and dict6[ASN][-1] > 0:
        #    astr6.print_ASN(f1, ASN)
        #    astr4.print_ASN(f1, ASN)
        #    f1.write('************************************\n')
        if dict4[ASN][-3] == 1:
            astr6.print_ASN(f1, ASN)
            astr4.print_ASN(f1, ASN)
            f1.write('************************************\n')
        if abs(dict6[ASN][-1] - dict4[ASN][-1]) >= 2 or\
        abs(dict6[ASN][-2] - dict4[ASN][-2]) >= 2:
            astr6.print_ASN(f, ASN)
            astr4.print_ASN(f, ASN)
        if abs(dict6[ASN][-1] - dict4[ASN][-1]) >= 2 and\
        abs(dict6[ASN][-2] - dict4[ASN][-2]) >= 2:
            f.write('large value diverse\n')
            count_both += 1
        elif abs(dict6[ASN][-1] - dict4[ASN][-1]) >= 2:
            count_exist += 1
            f.write('existence diverse\n')
        elif abs(dict6[ASN][-2] - dict4[ASN][-2]) >= 2:
            count_lvalue += 1
            f.write('large value diverse\n')
    else:
        pass
        
f.write('count_both = ' + str(count_both) + '\n')
f.write('count_exist = ' + str(count_exist) + '\n')
f.write('count_lvalue = ' + str(count_lvalue) + '\n')
f.write('v6 exist per as: ' + str(exist_per_as6) + '\n')
f.write('v4 exist per as: ' + str(exist_per_as4) + '\n')
f.close()
f1.close()
#end:finding interesting ASes#
