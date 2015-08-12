![x](https://raw.githubusercontent.com/marionleborgne/cloudbrain/master/cb-logo-low-res.png)

##Overview
CloudBrain is a platform for real-time EEG data analysis and visualization. [EEG](http://en.wikipedia.org/wiki/Electroencephalography) is the recording of electrical activity along the scalp. In other words, brainwaves.
<br>
<br>
CloudBrain enables you to:
- **Stream EEG data** into a central database.
- **Analyze EEG data** by computing aggregates.
- **Visualize EEG data** and patterns in real-time.

# Getting started with Cloudbrain

## Option 1: Quick-start!
This makes use of the demo version of cloudbrain running at `http://cloudbrain.rocks`. Let's send and get data using prebuilt binaries.

### Publishers: send data to cloudbrain
* On OSX, run `./cloudbrain/publishers/bin/osx/main`
* On Ubuntu, run `./cloudbrain/publishers/bin/ubuntu/main`
* Use `--help` to get more info about how to use the publishers. For example, `./cloudbrain/publishers/bin/osx/main --help`

### Subscribers: get data from cloudbrain and write to a file
* On OSX, run `./cloudbrain/subscribers/bin/osx/file_writer`
* On Ubuntu, run `./cloudbrain/subscribers/bin/ubuntu/file_writer`
* Use `--help` to get more info about how to use the subscribers. For example, `./cloudbrain/subscribers/bin/osx/file_writer --help`

### PyInstaller
* Cloudbrain's binaries were generated with PyInstaller
* `pip install pyinstaller`
* `pyinstaller --clean --onefile -y <python_file>`


## Option 2: Install Cloudbrain from scratch 

### Dependencies 
* Install RabbitMQ
* Install Cassandra
* Install `node` and `npm`
* `npm install rabbit.js`
* `pip install requirements.txt`

### Run the App

#### Start RabbitMQ
* Get RabbitMQ.
* Change to your RabbitMQ directory. 
* Start RabbitMQ: `sh sbin/rabbit-server start`

#### Start the Publisher
* Run `python cloudbrain/publishers/main.py`

#### Start Cassandra
* Get Cassandra.
* Change to your Cassandra directory.
* Start Cassandra: `sh bin/cassandra start`
* Generate Cassandra schema: `python database/generate_cassandra_schema.py`
* Execute schema: `bin/cqlsh -f <path_to_cassandra_schema>/cassandra_schema.cql`


#### Run MetricStore
* Start listening and storing data with `python database/metric_store.py`

#### Start the REST API
* Run `python api/web_api.py`

#### Start the UI
* Open `ui/chart.html` in your browser.

# About Cloudbrain

## CloudBrain @ [The Exploratorium](http://www.exploratorium.edu) of San Francisco
CloudBrain was in use at the Exploratorium as part of the Exhibit called [*Cognitive Technologies*](http://www.exploratorium.edu/press-office/press-releases/new-exhibition-understanding-influencing-brain-activity-opens). 
All the EEG headsets in the exhibit are sending data to CloudBrain. This data is being routed to booths where visitors can control different things with their brain. For visitors who are willing to share their data, CloudBrain computes aggregates and displays a baseline of the average brain. On the central screen, visitors can see everyone else's live EEG data. Each radar chart shows the state of the main brainwaves (alpha, beta, theta, gamma, delta). This is particularly interesting to see how one's brain compares to others, or to understand how it reacts to different stimuli.

## Cloudbrain's data visualizations

### Aggregated data (bar charts)
![x](https://raw.githubusercontent.com/marionleborgne/cloudbrain/master/data-aggregates.png)

### Live EEG data (radar charts)
![x](https://raw.githubusercontent.com/marionleborgne/cloudbrain/master/radar-charts.png)

### Live EEG data (line charts)
![x](https://raw.githubusercontent.com/marionleborgne/cloudbrain/master/timeserie-data.png)

