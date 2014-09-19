![x](https://github.com/marionleborgne/cloudbrain/blob/master/screenshot.png)

## CloudBrain

Real-time data analysis of brainwaves in the cloud. Detect patterns and map your mind states to actions.

The [EEG](http://en.wikipedia.org/wiki/Electroencephalography) data (brainwaves) currently comes from the [OpenBCI](http://openbci.com) board - an affordable open-source EEG headset.   In reality, you can virtualy send any data to cloudbrain.  For more info, see [Getting Data Into CloudBrain](http://ebrain.io/getting-data-into-cloudbrain).   Currently, there is only one connector type (the OpenBCI connector - See `utils/udp_server.py`).   But since these connectors are vey easy to make, I am hopping to have more biosensors feeding CloudBrain with data soon.  For example, the breathing sensor [Spire](https://spire.io/) would be a good one.

## Cloudbrain Demo

There is a live demo of Cloudbrain available at [cloudbrain.rocks](http://cloudbrain.rocks). For uploading brainwaves into Cloubdrain, see next section.

<div markdown="0"><a href="https://cloudbrain.rocks" class="btn btn-sucess">Live Demo</a></div>

## How to feed Cloudbrain with [OpenBCI](http://openbci.com) data

![x](https://raw.github.com/marionleborgne/cloudbrain/master/openbci.png)

1. `cd utils`
2. run `udp_server.py` to send openBCI brain waves data via UDP.

Note: Make sure that pipeline (the data pipeline) is listening on the same port as the one used by OpenBCI UDP Server :-)

## Install

1. `sudo pip install -r requirements.txt` for the easy bits

2. Install numpy, scipy, pandas, patsy, statsmodels, msgpack_python in that
order.

2. You may have trouble with SciPy. If you're on a Mac, try:

* `sudo port install gcc48`
* `sudo ln -s /opt/local/bin/gfortran-mp-4.8 /opt/local/bin/gfortran`
* `sudo pip install scipy`

On Debian, apt-get works well for Numpy and SciPy. On Centos, yum should do the
trick. If not, hit the Googles, yo.

3. `cp src/settings.py.example src/settings.py`

4. Add directories: 

``` 
sudo mkdir /var/log/cloudbrain
sudo mkdir /var/run/cloudbrain
sudo mkdir /var/log/redis
sudo mkdir /var/dump/
```

5. Download and install the latest Redis release

7. Start 'er up

* `cd cloudbrain/bin`
* `sudo redis-server redis.conf`
* `sudo ./pipeline.d start`
* `sudo ./analyzer.d start`
* `sudo ./webapp.d start`

By default, the webapp is served on port 1500.

9. Check the log files to ensure things are running.

### Gotchas

* If you already have a Redis instance running, it's recommended to kill it and
restart using the configuration settings provided in bin/redis.conf

* Be sure to create the log directories.

### Hey! Nothing's happening!
Of course not. You've got no data! For a quick and easy test of what you've 
got, run this:
```
cd utils
python seed_data.py
```
This will ensure that the pipeline
service is properly set up and can receive data. 

Once you get real data flowing through your system, the Analyzer will be able
start analyzing for anomalies!

##Licence
CloudBrain's backend is an adaptation from Skyline, a monitoring tool for cloud infrastructures. The MIT licence of Skyline is included [here](https://github.com/marionleborgne/cloudbrain/blob/master/LICENSE.md). 
