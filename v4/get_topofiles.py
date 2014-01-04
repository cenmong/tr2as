import os

flist = list()

for i in range(1, 4):
    '''
    monitors = list()
    f = open('./get4mon/t' + str(i) + 'monitor_list', 'r')
    for line in f:
        monitors.append(line[:-1])
    f.close()
    mcount = len(monitors)
    '''
    f = open('./get4mon/t' + str(i) + 'daily-creation.log', 'r') 
    rdlist = list()
    for line in f:
        if line[0] == '#':
            continue
        segment = line.split()[1]
        rd = segment.split('.')[-5]
        if rd not in rdlist:
            rdlist.append(rd)

    #choose the second round
    flist = list()
    pullrd = rdlist[1]
    f.close()

    f = open('./get4mon/t' + str(i) + 'daily-creation.log', 'r') 
    for line in f:
        if line[0] == '#':
            continue
        segment = line.split()[1]
        if segment.split('.')[-5] == pullrd:
            flist.append(segment)
    f.close()

    hdname = 'chenmeng/A2A6CFC5A6CF97E5'

    f = open('file_list', 'a')
    f.write('team ' + str(i) + '\n')
    for fl in flist:
        f.write(fl + '\n')
    f.close()

    for f in flist:
        os.system('wget -np -m -P /media/' + hdname + '/ --http-user=chenm11@mails.tsinghua.edu.cn\
                --http-password=cenmong123 --no-check-certificate\
                https://topo-data.caida.org/team-probing/' + f)

        os.system('gzip -d /media/' + hdname +\
                '/topo-data.caida.org/team-probing/' + f)

        os.system('sc_analysis_dump /media/' + hdname +\
                '/topo-data.caida.org/team-probing/' + f[:-3] + ' > /media/' + hdname\
                + '/topo-data.caida.org/team-probing/' + f[:-9]) 

        os.system('rm /media/' + hdname +\
                '/topo-data.caida.org/team-probing/' + f[:-3])
