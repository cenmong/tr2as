# This py should be standalone so I can make people help me download files from
# other machines
# My basic idea:
# (1)IPv6 traceroute: get files of a whole (or many) month 
# (2)v4 traceroute: get N (default to 1) cycles for each team & month
# TODO:separate download and processing. Pay special attension (or use other
# way) to the 'rm' command. It killed me twice, man! Besides, I should run
# download at least twice to continue any middleway-stopped file.
import os
from env import *
########################################IPv6##########################################
for ym in yearmonth6:
    year = ym[0]
    month = ym[1]
    #download files
    #-np: ignore parent link
    os.system('wget -np -P ' + hdname + ' -c -m -r -A.gz --http-user=chenm11@mails.tsinghua.edu.cn\
            --http-password=cenmong123 --no-check-certificate\
            https://topo-data.caida.org/topo-v6/list-8.ipv6.allpref/' + year +\
            '/' + month + '/')
    # get file list and process them
    os.system('lynx -dump -auth=chenm11@mails.tsinghua.edu.cn:cenmong123\
            https://topo-data.caida.org/topo-v6/list-8.ipv6.allpref/' + year +\
            '/' + month + '/ > filehtml6')# filehtml6 contains file list
    f = open('filehtml6', 'r')
    flist = open('metadata/6files' + year + month, 'a')
    for line in f.readlines():
        if line.split('.')[-1] != 'gz\n':
            continue
        topofile = line.split('//')[1]
        flist.write(topofile.replace('.warts.gz', ''))
        topofile = topofile.replace('\n', '')
        os.system('gzip -d ' + hdname + topofile)# unzip the files
        topofile = topofile.replace('.gz', '')# names of the unzipped files
        os.system('sc_analysis_dump ' + hdname + topofile + ' > ' + hdname
                + topofile.replace('.warts', ''))# parse files
        # TODO:check whether parsed file exists before rm
        os.system('rm ' + hdname + topofile)# remove old unparsed files

    f.close()
    flist.close()
    os.system('rm filehtml6')
########################################IPv4##########################################
for ym in yearmonth4:
    year = ym[0]
    month = ym[1]
    number = ym[2]
    for i in range(1, 4):# from 1 to 3
        #get my cycle
        os.system('lynx -dump -auth=chenm11@mails.tsinghua.edu.cn:cenmong123\
                https://topo-data.caida.org/team-probing/list-7.allpref24/team-'+\
                str(i) + '/daily/' + year + '/ > cyclehtml4')# cyclehtml4 contains cycle list
        f = open('cyclehtml4', 'r')
        cyclelist = []
        string = year + month# e.g., '201401'
        for line in f.readlines():
            if line.count('[') > 0:
                continue
            if line.count(string) > 0:
                cyclelist.append(line)
        mycycle = cyclelist[number - 1]
        mycycle = mycycle.split('//')[1].replace('\n', '')
        f.close()
        os.system('rm cyclehtml4')
        # download all files in the cycle
        os.system('wget -np -P ' + hdname + ' -c -m -r -A.gz --http-user=chenm11@mails.tsinghua.edu.cn\
                --http-password=cenmong123 --no-check-certificate\
                https://' + mycycle)
        # get file list and process them
        os.system('lynx -dump -auth=chenm11@mails.tsinghua.edu.cn:cenmong123\
                https://' + mycycle + '> filehtml4')
        f = open('filehtml4', 'r')
        #flist = open('metadata/4files' + year + month + str(number), 'a')
        for line in f.readlines():
            if line.split('.')[-1] != 'gz\n':
                continue
            topofile = line.split('//')[1]
            #flist.write(topofile.replace('.warts.gz', ''))
            topofile = topofile.replace('\n', '')
            os.system('gzip -d ' + hdname + topofile)# unzip
            topofile = topofile.replace('.gz', '')
            os.system('sc_analysis_dump ' + hdname + topofile + ' > ' + hdname
                    + topofile.replace('.warts', ''))# parse 
            os.system('rm ' + hdname + topofile)# remove old unparsed file
        f.close()
        #flist.close()
        os.system('rm filehtml4')
#################################pfx2AS files######################################
for ymd in ymd_pfx2as:
    year = ymd[0]
    month = ymd[1]
    day = ymd[2]
    string = year + month +day
    os.system('wget -nc -P ./metadata/ http://data.caida.org/datasets/routing/routeviews6-prefix2as/' +\
            year + '/' + month + '/' +\
            'routeviews-rv6-' + string + '-1200.pfx2as.gz')
    os.system('gzip -d ./metadata/' + 'routeviews-rv6-' + string + '-1200.pfx2as.gz')# unzip
    os.system('wget -nc -P ./metadata/ http://data.caida.org/datasets/routing/routeviews-prefix2as/' +\
            year + '/' + month + '/' +\
            'routeviews-rv2-' + string + '-1200.pfx2as.gz')
    os.system('gzip -d ./metadata/' + 'routeviews-rv2-' + string + '-1200.pfx2as.gz')# unzip
