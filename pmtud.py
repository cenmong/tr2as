import os
import time

f12 = open('trpath/12resultv6', 'r')
f23 = open('trpath/23resultv6', 'r')

d12 = []
d23 = []

for line in f12.readlines():
    des = line.split()[2]
    if des not in d12:
        d12.append(des)

for line in f23.readlines():
    des = line.split()[2]
    if des not in d23:
        d23.append(des)

f12.close()
f23.close()

f12 = open('12lt1500', 'a')
f23 = open('23lt1500', 'a')

for d in d12:
    os.system('tracepath6 ' + d + ' > tmpfile')
    #time.sleep(300)
    bingo = False
    f = open('tmpfile', 'r')
    for line in f.readlines():
        try:
            pmtu = line.split()[4]
            print pmtu
            if int(pmtu) < 1500:
                bingo = True#find pmtu < 1500
        except:
            pass
    if bingo == True:
        for line in f.readlines():
            f12.write(line)
        f12.write('-------------------------------\n')
    f.close()

f12.close()
f23.close()
