#Basic idea:
#(1)IPv6 traceroute: get a whole month
#(2)v4 traceroute: get N (default to 1) cycles for each team/month
import os
from env import *
########################################IPv6##########################################
for ym in yearmonth6:
    year = ym[0]
    month = ym[1]
    #download files
    os.system('wget -r --level=0 -np -m -P /media/' + hdname + '/ --http-user=chenm11@mails.tsinghua.edu.cn\
            --http-password=cenmong123 --no-check-certificate\
            https://topo-data.caida.org/topo-v6/list-8.ipv6.allpref/' + year +\
            '/' + month + '/')
    #get file list and process them
    os.system('lynx -dump -auth=chenm11@mails.tsinghua.edu.cn:cenmong123\
            https://topo-data.caida.org/topo-v6/list-8.ipv6.allpref/' + year +\
            '/' + month + '/ > filehtml6')#filehtml6 contains file list
    f = open('filehtml6', 'r')
    for line in f.readlines():
        if line.split('.')[-1] != 'gz\n':
            continue
        topofile = '/' + line.split('//')[1]
        topofile = topofile.replace('\n', '')
        os.system('gzip -d /media/' + hdname + topofile)#unzip
        topofile = topofile.replace('.gz', '')
        os.system('sc_analysis_dump /media/' + hdname + topofile + ' > /media/' + hdname
                + topofile.replace('.warts', ''))#parse 
        os.system('rm /media/' + hdname + topofile)#remove old unparsed file

    f.close()
    os.system('rm filehtml6')
########################################IPv4##########################################
for ym in yearmonth4:
    year = ym[0]
    month = ym[1]
    number = ym[2]
    for i in range(1, 4):#from 1 to 3
        #get my cycle
        os.system('lynx -dump -auth=chenm11@mails.tsinghua.edu.cn:cenmong123\
                https://topo-data.caida.org/team-probing/list-7.allpref24/team-'+\
                str(i) + '/daily/' + year + '/ > cyclehtml4')#cyclehtml4 contains cycle list
        f = open('cyclehtml4', 'r')
        cyclelist = []
        string = year + month#e.g., '201401'
        for line in f.readlines():
            if line.count('[') > 0:
                continue
            if line.count(string) > 0:
                cyclelist.append(line)
        mycycle = cyclelist[number - 1]
        mycycle = mycycle.split('//')[1].replace('\n', '')
        f.close()
        os.system('rm cyclehtml4')
        #download all files in the cycle
        os.system('wget -r --level=0 -np -m -P /media/' + hdname + '/ --http-user=chenm11@mails.tsinghua.edu.cn\
                --http-password=cenmong123 --no-check-certificate\
                https://' + mycycle)
        #get file list and process them
        os.system('lynx -dump -auth=chenm11@mails.tsinghua.edu.cn:cenmong123\
                https://' + mycycle + '> filehtml4')
        f = open('filehtml4', 'r')
        for line in f.readlines():
            if line.split('.')[-1] != 'gz\n':
                continue
            topofile = '/' + line.split('//')[1]
            topofile = topofile.replace('\n', '')
            os.system('gzip -d /media/' + hdname + topofile)#unzip
            topofile = topofile.replace('.gz', '')
            os.system('sc_analysis_dump /media/' + hdname + topofile + ' > /media/' + hdname
                    + topofile.replace('.warts', ''))#parse 
            os.system('rm /media/' + hdname + topofile)#remove old unparsed file
                    
        f.close()
        os.system('rm filehtml4')
