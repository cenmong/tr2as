import matplotlib.pyplot as plt 
import numpy as np
from aslist import ixpas
from main.py import dict6, dict4

# e: total existence count
# v: largest value in 1~150
elist6 = []
vlist6 = []
elist4 = []
vlist4 = []

ixp6 = []
eixp6 = []
vixp6 = []
ixp4 = []
eixp4 = []
vixp4 = []

e12in6 = []
v12in6 = []
e23in6 = []
v23in6 = []
e12in4 = []
v12in4 = []
e23in4 = []
v23in4 = []

for k in dict6.keys():
    elist6.append(dict6[k][0])
    vlist6.append(dict6[k][-4])
    try:
        if int(k) in ixpas:
            eixp6.append(dict6[k][0])
            vixp6.append(dict6[k][-4])
            ixp6.append(k)
    except:
        pass
    if k in dict4.keys():
        if dict6[k][-7] == 1:
            e12in6.append(dict4[k][0])
            v12in6.append(dict4[k][-4])
        elif dict6[k][-8] == 1:
            e23in6.append(dict4[k][0])
            v23in6.append(dict4[k][-4])
for k in dict4.keys():
    elist4.append(dict4[k][0])
    vlist4.append(dict4[k][-4])
    try:
        if int(k) in ixpas:
            eixp4.append(dict6[k][0])
            vixp4.append(dict6[k][-4])
            ixp4.append(k)
    except:
        pass
    if k in dict6.keys():# k is dual stack AS number
        if dict4[k][-7] == 1:
            e12in4.append(dict6[k][0])
            v12in4.append(dict6[k][-4])
        elif dict4[k][-8] == 1:
            e23in4.append(dict6[k][0])
            v23in4.append(dict6[k][-4])
'''
for k in dict6.keys():
    if dict6[k][-5] > 0:
        elist6.append(dict6[k][-5])
        vlist6.append(dict6[k][-6])
for k in dict4.keys():
    if dict4[k][-5] > 0:
        elist4.append(dict4[k][-5])
        vlist4.append(dict4[k][-6])
'''
# definitions for the axes
left, width = 0.1, 0.65
bottom, height = 0.1, 0.65
left_h = left + width + 0.02

rect_scatter = [left, bottom, width, height]
rect_histy = [left_h, bottom, 0.2, height]

#****************************IPv4***************************#
plt.figure(1, figsize=(16, 12))

axScatter = plt.axes(rect_scatter)
axHisty = plt.axes(rect_histy)

axScatter.plot(elist4, vlist4, ',')
'''
axScatter.plot(eixp4, vixp4, 'ro')
for i, txt in enumerate(ixp4):
    axScatter.annotate(txt, (eixp4[i], vixp4[i]))
'''
axScatter.plot(e12in6, v12in6, 'ro')
axScatter.plot(e23in6, v23in6, 'bo')
axScatter.set_xlabel('Number of existence')
axScatter.set_xscale('log')
axScatter.set_ylabel('largest value')

binwidth = 1
ymax = np.max(vlist4)
ylim = ymax + 1
axScatter.set_ylim( (0, ylim) )
ybins = np.arange(0, ylim + binwidth, binwidth)
axHisty.hist(vlist4, bins = ybins, orientation='horizontal')
axHisty.set_ylim(axScatter.get_ylim() )
plt.show()

#**************************IPv6****************************#
plt.figure(2, figsize=(16, 12))

axScatter = plt.axes(rect_scatter)
axHisty = plt.axes(rect_histy)

axScatter.plot(elist6, vlist6, ',')
'''
axScatter.plot(eixp6, vixp6, 'ro')
for i, txt in enumerate(ixp6):
    axScatter.annotate(txt, (eixp6[i], vixp6[i]))
'''
axScatter.plot(e12in4, v12in4, 'ro')
axScatter.plot(e23in4, v23in4, 'bo')
axScatter.set_xlabel('Number of existence')
axScatter.set_xscale('log')
axScatter.set_ylabel('largest value')

binwidth = 1
ymax = np.max(vlist6)
ylim = ymax + 1
axScatter.set_ylim( (0, ylim) )
ybins = np.arange(0, ylim + binwidth, binwidth)
axHisty.hist(vlist6, bins = ybins, orientation='horizontal')
axHisty.set_ylim(axScatter.get_ylim() )
plt.show()

