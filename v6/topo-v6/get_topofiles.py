from getmon import monitors

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
