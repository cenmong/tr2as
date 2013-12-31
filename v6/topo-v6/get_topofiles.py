from getmon import monitors

flist = list()

f = open ('cycle-completion.log', 'r') 
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
