import pylab as pp
import mpld3 as mp
fig = pp.figure()
pp.plot([3,1,4,1,5], 'ks-', mec='w', mew=5, ms=20)
mp.save_html(fig,'templates/Sample.html')

