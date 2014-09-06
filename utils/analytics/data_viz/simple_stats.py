__author__ = 'marion'
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#df = pd.read_csv("../data/motor_image1.csv", index_col = 'time')
df = pd.read_csv("../data/jim_10filt.csv", index_col = 'time')

print df

basic_stats = df.describe()

print "=== BASIC STATS ==="
print basic_stats
print ""


#Get mean of channel_0
channel_0_mean = df['channel_0'].mean()
print "==> channel_0 mean : %s" % channel_0_mean

#Get percentile/quantiles
channel_0_q30 = df['channel_0'].quantile(q=0.3)

print "==> channel1 30th percentile : %s" % channel_0_q30

ts = pd.Series(np.random.randn(1000))

df = pd.DataFrame(np.random.randn(1000,4), index=ts.index, columns=list('ABCD'))

plt.figure()
df.plot()
plt.show()


