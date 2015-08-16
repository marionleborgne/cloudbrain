![x](https://raw.githubusercontent.com/marionleborgne/cloudbrain/master/cloudbrain/ui/images/cb-logo-low-res.png)

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
This makes use of the demo version of cloudbrain running at `http://cloudbrain.rocks`.
* Publishers send data to cloudbrain.
* Subscribers receive data from cloudbrain.

### Install
* `python setup.py install`

### Publishers: send data to cloudbrain
* Run `python cloudbrain/publishers/sensor_publisher.py`
* Use the `--help` flag for the docs.

### Subscribers: get data from cloudbrain
* Write data to a file: `python cloudbrain/subscribers/file_writer_subscriber.py`
* Use the `--help` flag for the docs.

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
* `cd cloudbrain/ui`
* `npm install`
* `bower install`
* Start the REST API server `python cloudbrain/datastore/rest_api_server.py`
* Open `ui/index.html` in your browser.

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
![x](https://raw.githubusercontent.com/marionleborgne/cloudbrain/master/cloudbrain/ui/images/data-aggregates.png)

### Live EEG data (radar charts)
![x](https://raw.githubusercontent.com/marionleborgne/cloudbrain/master/cloudbrain/ui/images/radar-charts.png)

### Live EEG data (line charts)
![x](https://raw.githubusercontent.com/marionleborgne/cloudbrain/master/cloudbrain/ui/images/timeserie-data.png)

