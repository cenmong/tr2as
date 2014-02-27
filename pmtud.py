import os
import time

f12 = open('trpath/12resultv6', 'r')#They are generated in ASTR.get_dict
f23 = open('trpath/23resultv6', 'r')

d12 = []
d23 = []

#choose the same destination as the path along which tunnel may exist
#store these destinations in lists
for line in f12.readlines():
    des = line.split()[2]
    if des not in d12:
        d12.append(des)
print len(d12)

for line in f23.readlines():
    des = line.split()[2]
    if des not in d23:
        d23.append(des)
print len(d23)

f12.close()
f23.close()

fexist = os.path.exists('12st1500')
if fexist:
    os.system('rm 12st1500')
fexist = os.path.exists('23st1500')
if fexist:
    os.system('rm 23st1500')
f12 = open('12st1500', 'a')
f23 = open('23st1500', 'a')

fexist = os.path.exists('tmpfile')
if fexist:
    os.system('rm tmpfile')

c12 = 0
c23 = 0

for d in d12:
    os.system('tracepath6 ' + d + ' > tmpfile')
    #time.sleep(300)
    bingo = False
    f = open('tmpfile', 'r')
    for line in f.readlines():
        try:
            tp = line.split()[3]
            pmtu = line.split()[4]
            if tp == 'pmtu' and int(pmtu) < 1500:
                print pmtu
                c12 += 1
                bingo = True#find pmtu < 1500
                break
        except:
            pass
    f.close()
    if bingo == True:
        f12.write(d + ':\n')
        f = open('tmpfile', 'r')
        for line in f.readlines():
            f12.write(line)
        f12.write('-------------------------------\n')
        f.close()
    os.system('rm tmpfile')

for d in d23:
    os.system('tracepath6 ' + d + ' > tmpfile')
    #time.sleep(300)
    bingo = False
    f = open('tmpfile', 'r')
    for line in f.readlines():
        try:
            tp = line.split()[3]
            pmtu = line.split()[4]
            if tp == 'pmtu' and int(pmtu) < 1500:
                print pmtu
                c23 += 1
                bingo = True#find pmtu < 1500
                break
        except:
            pass
    f.close()
    if bingo == True:
        f23.write(d + ':\n')
        f = open('tmpfile', 'r')
        for line in f.readlines():
            f23.write(line)
        f23.write('-------------------------------\n')
        f.close()
    os.system('rm tmpfile')

f12.write('all count: ' + str(c12))
f23.write('all count: ' + str(c23))
f12.close()
f23.close()
