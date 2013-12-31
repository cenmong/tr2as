from getmon import monitors
import os

flist = list()

f = open('cycle-completion.log', 'r') 
for line in f.readlines():
    if line[0] == '#':
        continue
    segment = line.split()[2]
    mon = segment.split('.')[-3] 
    if mon in monitors:
        flist.append(segment)
        monitors.remove(mon)
f.close()

print flist[0].split('.')[-5]
print flist[-1].split('.')[-5]
print flist
print len(flist)

f = open('v6file_list', 'a')
for fl in flist:
    f.write(fl + '\n')

os.system('wget -np -m -P 任意目录 --http-user=chenm11@mails.tsinghua.edu.cn\
        --http-password=cenmong123 --no-check-certificate\
        https://topo-data.caida.org/topo-v6/list-8.ipv6.allpref/2013/12/topo-v6.l8.20131201.1385856603.hkg-cn.warts.gz')

#from mechanize import Browser
'''These work quite well
b = Browser()
b.set_handle_robots(False)
page = b.open('http://www.baidu.com')
html = page.read()
print html
'''
'''
b = Browser()
b.set_handle_robots(False)
page = b.open('https://topo-data.caida.org/')
html = page.read()
print html
'''
