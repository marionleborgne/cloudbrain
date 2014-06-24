## CloudBrain

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

6. Start 'er up

* `cd cloudbrain/bin`
* `sudo redis-server redis.conf`
* `sudo ./horizon.d start`
* `sudo ./analyzer.d start`
* `sudo ./webapp.d start`

By default, the webapp is served on port 1500.

7. Check the log files to ensure things are running.

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
This will ensure that the Horizon
service is properly set up and can receive data. 

Once you get real data flowing through your system, the Analyzer will be able
start analyzing for anomalies!
