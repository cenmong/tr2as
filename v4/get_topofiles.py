import os

flist = list()

for i in range(1, 4):
    monitors = list()
    f = open('./get4mon/t' + str(i) + 'monitor_list', 'r')
    for line in f:
        monitors.append(line[:-1])
    f.close()
    mcount = len(monitors)

    d = dict()
    f = open('./get4mon/t' + str(i) + 'daily-creation.log', 'r') 
    for line in f:
        if line[0] == '#':
            continue
        segment = line.split()[1]
        date = segment.split('.')[-4]
        try:
            dict[date] = dict[date] + 1
        except:
            dict[date] = 1

    for line in f:
        if line[0] == '#':
            continue
    f.close()
'''
f = open('6monitor_list', 'r')
for line in f.readlines():
    monitors.append(line[:-1])
f.close()
print monitors

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

print flist[0].split('.')[-5]#start date
print flist[-1].split('.')[-5]#end date

hdname = 'chenmeng/A2A6CFC5A6CF97E5'

f = open('6file_list', 'a')
for fl in flist:
    f.write(fl + '\n')
f.close()

for f in flist:
    os.system('wget -np -m -P /media/' + hdname + '/ --http-user=chenm11@mails.tsinghua.edu.cn\
            --http-password=cenmong123 --no-check-certificate\
            https://topo-data.caida.org/topo-v6/' + f)

    os.system('gzip -d /media/' + hdname +\
            '/topo-data.caida.org/topo-v6/' + f)

    os.system('sc_analysis_dump /media/' + hdname +\
            '/topo-data.caida.org/topo-v6/' + f[:-3] + ' > /media/chenmeng/' + hdname\
            + '/topo-data.caida.org/topo-v6/' + f[:-9]) 

    os.system('rm /media/' + hdname +\
            '/topo-data.caida.org/topo-v6/' + f[:-3])
'''
