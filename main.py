from ASTR import *
import os
from env import *

################################ IPv6
astr6 = ASTR('ipv6')# create an ASTR object
# I temperarily only use 1 pfx2as file and 1 file list
# In the future, I will loop over all pfx2as files and file lists
# , and get many ASTR objects each corresponds to a certain time
astr6.get_dict('metadata/6files' + yearmonth6[0][0] + yearmonth6[0][1], 'metadata/routeviews-rv6-' +\
        ymd_pfx2as[0][0] + ymd_pfx2as[0][1] + ymd_pfx2as[0][2] + '-1200.pfx2as', yearmonth6[0])
astr6.get_output('output/6output' + yearmonth6[0][0] + yearmonth6[0][1])# don't change this string
#exists = [10, 100, 1000]
#lvalues = [1, 2, 4]
#dict6 = astr6.set_attri(exists, lvalues)
dict6 = astr6.set_attri()# set attributes of each AS

exist_per_as6 = float(astr6.exist_c)/float(len(dict6.keys()))

################################ IPv4
astr4 = ASTR('ipv4')
astr4.get_dict('metadata/4files' + yearmonth4[0][0] + yearmonth4[0][1] +\
        str(yearmonth4[0][2]), 'metadata/routeviews-rv2-' +\
        ymd_pfx2as[0][0] + ymd_pfx2as[0][1] + ymd_pfx2as[0][2] + '-1200.pfx2as', yearmonth4[0])
astr4.get_output('output/4output' + yearmonth4[0][0] + yearmonth4[0][1] +\
        str(yearmonth4[0][2]))
#exists = [50, 500, 5000]
#lvalues = [1, 2, 4]
#dict4 = astr4.set_attri(exists, lvalues)
dict4 = astr4.set_attri()

exist_per_as4 = float(astr4.exist_c)/float(len(dict4.keys()))

################################ Finding interesting ASes
print 'analyzing combined v4/v6 results...'
fexist = os.path.exists('output/alloutput')
if fexist == True:
    os.system('rm output/alloutput')
f = open('output/alloutput', 'a')
f.write('v6 exist per as: ' + str(exist_per_as6) + '\n')
f.write('v4 exist per as: ' + str(exist_per_as4) + '\n')

candidate_as = []
tunnel_as = []
for a in dict6.keys():
    if (dict6[a][-4] == 2 or dict6[a][-4] == 3) and dict6[a][0] > 10:
        if a not in dict4.keys():
            continue
        if dict4[a][-4] > 3 and dict4[a][0]> 10:
            candidate_as.append(a)
            if (dict6[a][-6] == 2 or dict6[a][-6] == 3) and dict6[a][-5] > 10:
                if dict4[a][-6] > 3 and dict4[a][-5] > 10:
                    tunnel_as.append(a)
                    #print a, dict6[a][-6], dict4[a][-6]

#print candidate_as
#print tunnel_as

f.close()
