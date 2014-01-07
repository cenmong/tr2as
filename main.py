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

#-------------------------plot something, you know...--------------------------#
import matplotlib.pyplot as plt 
import numpy as np
from aslist import ixpas

elist6 = []
elist4 = []
vlist6 = []
vlist4 = []

ixp6 = []
eixp6 = []
vixp6 = []
ixp4 = []
eixp4 = []
vixp4 = []

e12in6 = []
v12in6 = []
e23in6 = []
v23in6 = []
e12in4 = []
v12in4 = []
e23in4 = []
v23in4 = []

for k in dict6.keys():
    elist6.append(dict6[k][0])
    vlist6.append(dict6[k][-4])
    try:
        if int(k) in ixpas:
            eixp6.append(dict6[k][0])
            vixp6.append(dict6[k][-4])
            ixp6.append(k)
    except:
        pass
    if k in dict4.keys():
        if dict6[k][-7] == 1:
            e12in6.append(dict4[k][0])
            v12in6.append(dict4[k][-4])
        elif dict6[k][-8] == 1:
            e23in6.append(dict4[k][0])
            v23in6.append(dict4[k][-4])
for k in dict4.keys():
    elist4.append(dict4[k][0])
    vlist4.append(dict4[k][-4])
    try:
        if int(k) in ixpas:
            eixp4.append(dict6[k][0])
            vixp4.append(dict6[k][-4])
            ixp4.append(k)
    except:
        pass
    if k in dict6.keys():#only plot these special v4 ASes in v6 fig
        if dict4[k][-7] == 1:
            e12in4.append(dict6[k][0])
            v12in4.append(dict6[k][-4])
        elif dict4[k][-8] == 1:
            e23in4.append(dict6[k][0])
            v23in4.append(dict6[k][-4])
'''
for k in dict6.keys():
    if dict6[k][-5] > 0:
        elist6.append(dict6[k][-5])
        vlist6.append(dict6[k][-6])
for k in dict4.keys():
    if dict4[k][-5] > 0:
        elist4.append(dict4[k][-5])
        vlist4.append(dict4[k][-6])
'''
# definitions for the axes
left, width = 0.1, 0.65
bottom, height = 0.1, 0.65
left_h = left + width + 0.02

rect_scatter = [left, bottom, width, height]
rect_histy = [left_h, bottom, 0.2, height]

#****************************IPv4***************************#
plt.figure(1, figsize=(16, 12))

axScatter = plt.axes(rect_scatter)
axHisty = plt.axes(rect_histy)

axScatter.plot(elist4, vlist4, ',')
'''
axScatter.plot(eixp4, vixp4, 'ro')
for i, txt in enumerate(ixp4):
    axScatter.annotate(txt, (eixp4[i], vixp4[i]))
'''
axScatter.plot(e12in6, v12in6, 'ro')
axScatter.plot(e23in6, v23in6, 'bo')
axScatter.set_xlabel('Number of existence')
axScatter.set_xscale('log')
axScatter.set_ylabel('largest value')

binwidth = 1
ymax = np.max(vlist4)
ylim = ymax + 1
axScatter.set_ylim( (0, ylim) )
ybins = np.arange(0, ylim + binwidth, binwidth)
axHisty.hist(vlist4, bins = ybins, orientation='horizontal')
axHisty.set_ylim( axScatter.get_ylim() )
plt.show()

#**************************IPv6****************************#
plt.figure(2, figsize=(16, 12))

axScatter = plt.axes(rect_scatter)
axHisty = plt.axes(rect_histy)

axScatter.plot(elist6, vlist6, ',')
'''
axScatter.plot(eixp6, vixp6, 'ro')
for i, txt in enumerate(ixp6):
    axScatter.annotate(txt, (eixp6[i], vixp6[i]))
'''
axScatter.plot(e12in4, v12in4, 'ro')
axScatter.plot(e23in4, v23in4, 'bo')
axScatter.set_xlabel('Number of existence')
axScatter.set_xscale('log')
axScatter.set_ylabel('largest value')

binwidth = 1
ymax = np.max(vlist6)
ylim = ymax + 1
axScatter.set_ylim( (0, ylim) )
ybins = np.arange(0, ylim + binwidth, binwidth)
axHisty.hist(vlist6, bins = ybins, orientation='horizontal')
axHisty.set_ylim( axScatter.get_ylim() )
plt.show()
