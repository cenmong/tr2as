import matplotlib.pyplot as plt 
import numpy as np
from aslist import ixpas
from main import dict6, dict4

# e: total existence count
# v: largest value in 1~150
# all
elist6 = []
vlist6 = []
elist4 = []
vlist4 = []

e_max2in6 = []
v_max2in6 = []
e_max3in6 = []
v_max3in6 = []
e_max2in4 = []
v_max2in4 = []
e_max3in4 = []
v_max3in4 = []

#transient
telist6 = []
tvlist6 = []
telist4 = []
tvlist4 = []

te_max2in6 = []
tv_max2in6 = []
te_max3in6 = []
tv_max3in6 = []
te_max2in4 = []
tv_max2in4 = []
te_max3in4 = []
tv_max3in4 = []

#ixp
ixp6 = []
eixp6 = []
vixp6 = []
ixp4 = []
eixp4 = []
vixp4 = []

# v6 set value
for k in dict6.keys():
    elist6.append(dict6[k][0])
    vlist6.append(dict6[k][-4])
    telist6.append(dict6[k][-5])
    tvlist6.append(dict6[k][-6])
    try:
        if int(k) in ixpas:
            eixp6.append(dict6[k][0])
            vixp6.append(dict6[k][-4])
            ixp6.append(k)
    except:
        pass
    #TODO:existence cannot be too few -- that can be noise
    if k in dict4.keys():
        if dict6[k][-4] == 2:
            # store its value in v4 because we want to plot it in v4 figure
            e_max2in6.append(dict4[k][0])
            v_max2in6.append(dict4[k][-4])
        elif dict6[k][-4] == 3:
            e_max3in6.append(dict4[k][0])
            v_max3in6.append(dict4[k][-4])
        if dict6[k][-6] == 2:
            te_max2in6.append(dict4[k][-5])
            tv_max2in6.append(dict4[k][-6])
        elif dict6[k][-6] == 3:
            te_max3in6.append(dict4[k][-5])
            tv_max3in6.append(dict4[k][-6])

# v4 set value
for k in dict4.keys():
    elist4.append(dict4[k][0])
    vlist4.append(dict4[k][-4])
    telist4.append(dict4[k][-5])
    tvlist4.append(dict4[k][-6])
    try:
        if int(k) in ixpas:
            eixp4.append(dict4[k][0])
            vixp4.append(dict4[k][-4])
            ixp4.append(k)
    except:
        pass
    if k in dict6.keys():# k is dual stack AS number
        if dict4[k][-4] == 2:
            e_max2in4.append(dict6[k][0])
            v_max2in4.append(dict6[k][-4])
        elif dict4[k][-4] == 3:
            e_max3in4.append(dict6[k][0])
            v_max3in4.append(dict6[k][-4])
        if dict4[k][-6] == 2:
            te_max2in4.append(dict6[k][-5])
            tv_max2in4.append(dict6[k][-6])
        elif dict4[k][-6] == 3:
            te_max3in4.append(dict6[k][-5])
            tv_max3in4.append(dict6[k][-6])

# definitions for the axes
left = 0.1
width = 0.65
bottom = 0.1
height = 0.1
left_h = left + width + 0.02

rect_scatter = [left, bottom, width, height]
rect_histy = [left_h, bottom, 0.2, height]

###all
##v4
plt.figure(1, figsize=(16, 12))

axScatter = plt.axes(rect_scatter)
axHisty = plt.axes(rect_histy)

axScatter.plot(elist4, vlist4, ',')
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
##v6
plt.figure(2, figsize=(16, 12))

axScatter = plt.axes(rect_scatter)
axHisty = plt.axes(rect_histy)

axScatter.plot(elist6, vlist6, ',')
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

###all + ixp
##v4
plt.figure(3, figsize=(16, 12))

axScatter = plt.axes(rect_scatter)
axHisty = plt.axes(rect_histy)

axScatter.plot(elist4, vlist4, ',')
axScatter.plot(eixp4, vixp4, 'ro')
for i, txt in enumerate(ixp4):
    axScatter.annotate(txt, (eixp4[i], vixp4[i]))
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
##v6
plt.figure(4, figsize=(16, 12))

axScatter = plt.axes(rect_scatter)
axHisty = plt.axes(rect_histy)

axScatter.plot(elist6, vlist6, ',')
axScatter.plot(eixp6, vixp6, 'ro')
for i, txt in enumerate(ixp6):
    axScatter.annotate(txt, (eixp6[i], vixp6[i]))
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

###transient
##v4
plt.figure(5, figsize=(16, 12))

axScatter = plt.axes(rect_scatter)
axHisty = plt.axes(rect_histy)

axScatter.plot(telist4, tvlist4, ',')
axScatter.set_xlabel('Number of existence')
axScatter.set_xscale('log')
axScatter.set_ylabel('largest value')

binwidth = 1
ymax = np.max(tvlist4)
ylim = ymax + 1
axScatter.set_ylim( (0, ylim) )
ybins = np.arange(0, ylim + binwidth, binwidth)
axHisty.hist(tvlist4, bins = ybins, orientation='horizontal')
axHisty.set_ylim(axScatter.get_ylim() )
plt.show()
##v6
plt.figure(6, figsize=(16, 12))

axScatter = plt.axes(rect_scatter)
axHisty = plt.axes(rect_histy)

axScatter.plot(telist6, tvlist6, ',')
axScatter.set_xlabel('Number of existence')
axScatter.set_xscale('log')
axScatter.set_ylabel('largest value')

binwidth = 1
ymax = np.max(tvlist6)
ylim = ymax + 1
axScatter.set_ylim( (0, ylim) )
ybins = np.arange(0, ylim + binwidth, binwidth)
axHisty.hist(tvlist6, bins = ybins, orientation='horizontal')
axHisty.set_ylim(axScatter.get_ylim() )
plt.show()

###largest value 2 and 3
##of v6 plotted in v4
plt.figure(7, figsize=(16, 12))

axScatter = plt.axes(rect_scatter)
axHisty = plt.axes(rect_histy)

axScatter.plot(elist4, vlist4, ',')
axScatter.plot(e_max2in6, v_max2in6, 'ro')
axScatter.plot(e_max3in6, v_max3in6, 'bo')
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
##of v4 plotted in v6
plt.figure(8, figsize=(16, 12))

axScatter = plt.axes(rect_scatter)
axHisty = plt.axes(rect_histy)

axScatter.plot(elist6, vlist6, ',')
axScatter.plot(e_max2in4, v_max2in4, 'ro')
axScatter.plot(e_max3in4, v_max3in4, 'bo')
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

###largest transient value 2 and 3
##of v6 plotted in transient v4
plt.figure(9, figsize=(16, 12))

axScatter = plt.axes(rect_scatter)
axHisty = plt.axes(rect_histy)

axScatter.plot(telist4, tvlist4, ',')
axScatter.plot(te_max2in6, tv_max2in6, 'ro')
axScatter.plot(te_max3in6, tv_max3in6, 'bo')
axScatter.set_xlabel('Number of existence')
axScatter.set_xscale('log')
axScatter.set_ylabel('largest value')

binwidth = 1
ymax = np.max(tvlist4)
ylim = ymax + 1
axScatter.set_ylim( (0, ylim) )
ybins = np.arange(0, ylim + binwidth, binwidth)
axHisty.hist(tvlist4, bins = ybins, orientation='horizontal')
axHisty.set_ylim(axScatter.get_ylim() )
plt.show()
##of v4 plotted in transient v6
plt.figure(10, figsize=(16, 12))

axScatter = plt.axes(rect_scatter)
axHisty = plt.axes(rect_histy)

axScatter.plot(telist6, tvlist6, ',')
axScatter.plot(te_max2in4, tv_max2in4, 'ro')
axScatter.plot(te_max3in4, tv_max3in4, 'bo')
axScatter.set_xlabel('Number of existence')
axScatter.set_xscale('log')
axScatter.set_ylabel('largest value')

binwidth = 1
ymax = np.max(tvlist6)
ylim = ymax + 1
axScatter.set_ylim( (0, ylim) )
ybins = np.arange(0, ylim + binwidth, binwidth)
axHisty.hist(tvlist6, bins = ybins, orientation='horizontal')
axHisty.set_ylim(axScatter.get_ylim() )
plt.show()
