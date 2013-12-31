f = open('cycle-completion.log', 'r')
monitors = list()
for line in f.readlines():
    if line[0] == '#':
        continue
    segment = line.split()[2]
    mon = segment.split('.')[-3]
    if mon in monitors:
        continue
    else:
        monitors.append(mon)
f.close()
