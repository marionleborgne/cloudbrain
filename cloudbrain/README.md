# CloudBrain

### Install 
* Install RabbitMQ
* Install Cassandra
* Install `node` and `npm`
* `npm install rabbit.js`
* `sudo pip install requirements.txt`

### Run the App

#### Start RabbitMQ
* Get RabbitMQ.
* Change to your RabbitMQ directory. 
* Start RabbitMQ: `sh sbin/rabbit-server start`

#### Start the Connector
* [TODO] Describe how to start the various connectors.

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