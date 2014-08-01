__author__ = 'marion'
import pandas

data_frame = pandas.read_csv("data/motor_image1.csv", index_col = 'time')

basic_stats = data_frame.describe()

print "=== BASIC STATS ==="
print basic_stats
print ""


#Get mean of channel_0
channel_0_mean = data_frame['channel_0'].mean()
print "==> channel_0 mean : %s" % channel_0_mean

#Get percentile/quantiles
channel_0_q30 = data_frame['channel_0'].quantile(q=0.3)

print "==> channel1 30th percentile : %s" % channel_0_q30
