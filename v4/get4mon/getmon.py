for i in range(1, 4):
    f = open('t' + str(i) + 'daily-creation.log', 'r')
    monitors = list()
    for line in f.readlines():
        if line[0] == '#':
            continue
        segment = line.split()[1]
        mon = segment.split('.')[-3]
        if mon in monitors:
            continue
        else:
            monitors.append(mon)
    f.close()

    f = open('t' + str(i) + 'monitor_list', 'a')
    for m in monitors:
        f.write(m + '\n')
    f.close()
