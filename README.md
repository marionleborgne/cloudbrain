![x](https://raw.githubusercontent.com/marionleborgne/cloudbrain/master/docs/images/cb-logo-low-res.png)

#Overview

Cloudbrain is a platform for real-time sensor data analysis and visualization. 
<br>
One type of sensor data that works well with cloudbrain is EEG data. [EEG](http://en.wikipedia.org/wiki/Electroencephalography) is the recording of electrical activity along the scalp. In other words, brainwaves.
<br>
<br>
Cloudbrain enables you to:
- **Stream sensor data** into a central database.
- **Analyze sensor data** to find spatial and temporal patterns.
- **Visualize sensor data** and patterns in real-time.

# Getting started with cloudbrain

## Option 1: Quick-start!
This makes use of the demo version of cloudbrain running at [`demo.cloudbrain.rocks`](http://demo.cloudbrain.rocks).
* Publishers send data to cloudbrain.
* Subscribers receive data from cloudbrain.

### Install liblo

On Linux, install the liblo package. 

If you're on OSX, make sure you have [homebrew](http://brew.sh/) and the OSX command line utilities installed
Then install liblo through brew
* `brew install liblo`

### Clone
* `git clone https://github.com/marionleborgne/cloudbrain.git`
* `cd cloudbrain`

### Install
* `python setup.py install --user`

### Publishers: send data to cloudbrain
* Run `python cloudbrain/publishers/sensor_publisher.py`
* Use the `--help` flag for the docs.

You can stream some Muse mock data using:
* `python cloudbrain/publishers/sensor_publisher.py --mock -n muse -i octopicorn`

### Subscribers: get data from cloudbrain
* Write data to a file: `python cloudbrain/subscribers/file_writer_subscriber.py`
* Use the `--help` flag for the docs.

For the mock data streamed above, the command would be:
* `python cloudbrain/subscribers/file_writer_subscriber.py -i octopicorn -n muse -m eeg`

## Option 2: Install cloudbrain from scratch 

### Setup 
* `python setup.py install`

#### RabbitMQ

* Install RabbitMQ and start it.
* Create cloudbrain user: `rabbitmqctl add_user cloudbrain cloudbrain`
* Grant permissions: `rabbitmqctl set_permissions cloudbrain ".*" ".*" ".*"`

### Send data to cloudbrain
* Run `python cloudbrain/publishers/sensor_publisher.py`
* Use the `--help` flag for the docs.

### Get data from cloudbrain
* Write data to a file: `python cloudbrain/subscribers/file_writer_subscriber.py`
* Use the `--help` flag for the docs.

### Store data 
* Install Cassandra and start it.
* `cd cloudbrain/datastore`
* Generate Cassandra schema: `python generate_cassandra_schema.py`
* Execute schema: `bin/cqlsh -f <path_to_cassandra_schema>/cassandra_schema.cql`
* Start storing data: `python cloudbrain/subscribers/cassandra_pika_subscriber.py`

### Visualize data
Start the demo UI:
* `cd cloudbrain/demo_ui`
* `npm install`
* `bower install`
* Start the REST API server `python cloudbrain/datastore/rest_api_server.py`
* Open `demo_ui/index.html` in your browser.

### [Optional] Generate binaries
* Install PyInstaller `pip install pyinstaller`
* For the publishers: `cd cloudbrain/publishers/bin/`
* Make the scripts executable `chmod +x *.sh`
* On OSX, generate OSX binaries: `sh package_publisher_osx.sh`
* On Ubuntu,  generate Ubuntu binaries: `sh package_publisher_ubuntu.sh`
* For the Subscribers `cd cloudbrain/subscribers/bin/`
* Make the scripts executable `chmod +x *.sh`
* On OSX, generate OSX binaries: `sh package_subscriber_osx.sh`
* On Ubuntu,  generate Ubuntu binaries: `sh package_subscriber_ubuntu.sh`

# API Documentation
For this example, let's use the demo API server `demo.apiserver.cloudbrain.rocks`, the device name `muse` and the device id `octopicorn`.

## Raw Data
* [Raw EEG](http://demo.apiserver.cloudbrain.rocks/data?device_name=openbci&metric=eeg&device_id=octopicorn) for the OpenBCI: `GET http://demo.apiserver.cloudbrain.rocks/data?device_name=openbci&metric=eeg&device_id=octopicorn`
* [Raw EEG](http://demo.apiserver.cloudbrain.rocks/data?device_name=muse&metric=eeg&device_id=octopicorn) for the Muse: `GET http://demo.apiserver.cloudbrain.rocks/data?device_name=muse&metric=eeg&device_id=octopicorn`
* [Mellow](http://demo.apiserver.cloudbrain.rocks/data?device_name=muse&metric=mellow&device_id=octopicorn) metric for the Muse:  `GET http://demo.apiserver.cloudbrain.rocks/data?device_name=muse&metric=mellow&device_id=octopicorn`
* [Concentration](http://demo.apiserver.cloudbrain.rocks/data?device_name=muse&metric=concentration&device_id=octopicorn) metric for the Muse: `GET http://demo.apiserver.cloudbrain.rocks/data?device_name=muse&metric=concentration&device_id=octopicorn`
* Etc...

## Power bands
[Power Bands](http://demo.apiserver.cloudbrain.rocks/power_bands?device_name=muse&device_id=octopicorn) for the Muse. Get alpha, beta, gamma, theta, delta values all at once, for the same timestamp.
* `GET http://demo.apiserver.cloudbrain.rocks/power_bands?device_name=muse&device_id=octopicorn`

## Registered devices
 Get the list of [device IDs](http://demo.apiserver.cloudbrain.rocks/registered_devices) IDs that are publishing to cloudbrain
* `GET http://demo.apiserver.cloudbrain.rocks/registered_devices`

## Device metadata
Get the list of [device names](http://demo.apiserver.cloudbrain.rocks/device_names) supported by cloudbrain
*  `GET http://demo.apiserver.cloudbrain.rocks/device_names`

# About cloudbrain

## Cloudbrain @ [The Exploratorium](http://www.exploratorium.edu) of San Francisco
CloudBrain was in use at the Exploratorium as part of the Exhibit called [Cognitive Technologies](http://www.exploratorium.edu/press-office/press-releases/new-exhibition-understanding-influencing-brain-activity-opens). 

[William](http://github.com/flysonic10) wrote an [excellent post about our work for the the Exploratorium Exhibit](http://willmakesthings.com/cognitive-technologies-the-exploratorium).

All the EEG headsets in the exhibit are sending data to CloudBrain. This data is being routed to booths where visitors can control different things with their brain. For visitors who are willing to share their data, CloudBrain computes aggregates and displays a baseline of the average brain. On the central screen, visitors can see everyone else's live EEG data. Each radar chart shows the state of the main brainwaves (alpha, beta, theta, gamma, delta). This is particularly interesting to see how one's brain compares to others, or to understand how it reacts to different stimuli.

Over 30 people played a role in the project, many of them building insanely awesome booths connected to CloudBrain: 3D-printed lighted flowers, Virtual Reality rock levitation, EEG/Heart Rate Variability correlation, and EEG reactive light tables, a brain-controlled robotic arm, 3D brain reconstructions, and fMRI algorithms. It. Was. Awesome.

Many thanks to my teamates:
* [William](http://github.com/flysonic10)
* [James](https://github.com/cyb3rnetic)
* [David](https://github.com/dvidsilva)

## Cloudbrain's data visualizations

### Aggregated data (bar charts)
![x](https://raw.githubusercontent.com/marionleborgne/cloudbrain/master/docs/images/data-aggregates.png)

### Live EEG data (radar charts)
![x](https://raw.githubusercontent.com/marionleborgne/cloudbrain/master/docs/images/radar-charts.png)

### Live EEG data (line charts)
![x](https://raw.githubusercontent.com/marionleborgne/cloudbrain/master/docs/images/timeserie-data.png)

