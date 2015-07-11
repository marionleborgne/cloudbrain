# CloudBrain

### Dependencies
* rabbit.js
* cassandra-driver
* pika
* flask

### Install
* Install RabbitMQ
* Install Cassandra
* Install `node` and `npm`
* `npm install rabbit.js`
* `sudo pip install cassandra-driver`
* `sudo pip install pika`
* `sudo pip install flask`

### Run the App

#### Start RabbitMQ
* Get RabbitMQ.
* Change to your RabbitMQ directory. 
* Start RabbitMQ: `sh sbin/rabbit-server start`

#### Start the Connector
* [TODO]

#### Start Cassandra
* Get Cassandra.
* Change to your Cassandra directory.
* Start Cassandra: `sh bin/cassandra start`
* Generate Cassandra schema: `python database/generate_cassandra_schema.py`
* Execute schema: `bin/cqlsh -f <path_to_cassandra_schema>/cassandra_schema.cql`


#### Run MetricStore
* `python listener/metric_store.py`

#### Start the REST API
* Run `python api/web_api.py`

#### Start the UI
* Open `ui/chart.html` in your browser. You should see a live chart with real-time anomalies.