from V6Dict import *
from V4Dict import *
import os

hd_name = 'chenmeng/A2A6CFC5A6CF97E5'#different in different computers

d6 = V6Dict()
d6.set_hdname(hd_name)
d6.get_trie('routeviews-rv6-20131224-1200.pfx2as')
dict6 = d6.get_dict('6file_list')
d6.get_output('6output')#don't change this string
exist_c6 = d6.exist_c 
as_c6 = len(dict6.keys())
exist_per_as6 = float(exist_c6)/float(as_c6)

d4 = V4Dict()
d4.set_hdname(hd_name)
d4.get_trie('routeviews-rv2-20131226-1200.pfx2as')
dict4 = d4.get_dict('4file_list_test')
d4.get_output('4output')#don't change this string
exist_c4 = d4.exist_c 
as_c4 = len(dict4.keys())
exist_per_as4 = float(exist_c4)/float(as_c4)

print 'analyzing v4/v6 results...'
fexist = os.path.exists('alloutput')
if fexist == True:
    os.system('rm alloutput')

f = open('alloutput', 'a')
count = 0
for ASN in dict6.keys():
    if ASN in dict4.keys():
        count += 1
        d6.print_ASN(f, ASN)
        d4.print_ASN(f, ASN)
        f.write('---------------------------------------\n')
    else:
        pass
        
f.write('count = ' + str(count) + '\n')
f.write('v6 exist per as: ' + str(exist_per_as6) + '\n')
f.write('v4 exist per as: ' + str(exist_per_as4) + '\n')
f.close()
