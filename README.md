CloudBrain
==========

##Overview
- `connectors`: Connectors for [OpenBCI](http://openbci.com), Muse, Neurosky and [Spacebrew](https://github.com/Spacebrew/spacebrew) sending data to cloudbrain
- `listeners`: Cloudbrain Listeners to get the live data data for [OpenBCI](http://openbci.com), Muse, Neurosky and [Spacebrew](https://github.com/Spacebrew/spacebrew)
- `api`: Cloudbrain's web API to retrieve the history of data, route live data, or retrieve data aggregated data (see [cloudbrain.rocks](http://cloudbrain.rocks) for the API documentation)
- `router`: Router to update spacebrew routes (for our [Exploratorium](http://www.exploratorium.edu/) exhibition)
- `spacebrew`: python websocket wrapper to interface with [Spacebrew](https://github.com/Spacebrew/spacebrew)
- `database` : Cassandra python client

##About CloudBrain
- An instance of CloudBrain is currently running at [cloudbrain.rocks](http://cloudbrain.rocks). This is also where you can find CloudBrain's API documentation.
- The packages that you want to use are `connectors` and `listeners`. Connectors will allow you to send live data to CloudBrain. Listeners will allow you to read live data from CloudBrain. 
- Routing of live data is done via SpaceBrew (currently running on the CloudBrain server). To visualize how the data is being routed you can go to [this interface](http://spacebrew.github.io/spacebrew/admin/admin.html?server=cloudbrain.rocks).

##Sending data to CloudBrain
- Install the [MuseIO SDK](http://www.choosemuse.com/developer-kit/)
- Pair your Muse via Bluetooth.
- Start MuseIO: open a terminal or command prompt and run: `muse-io --osc osc.udp://localhost:9090`
- Open a new terminal tab and run: 
-- `git clone https://github.com/marionleborgne/cloudbrain`
-- `cd cloudbrain/connectors/spacebrew`
-- `python spacebrew_server.py --name=YOUR_NAME_HERE`
- The last command will register your muse to cloudbrain’s spacebrew
- Check if you muse is in the column “publishers” of the [SpaceBrew interface](http://spacebrew.github.io/spacebrew/admin/admin.html?server=cloudbrain.rocks).


##Reading data fromCloudBrain
- Open a new terminal tab and run:
1. `cd cloudbrain/listeners`
2. `python example_spacebrew_client.py --name=YOUR_NAME_HERE`
- The last command will register your booth to cloudbrain’s spacebrew
- Check if you booth is in the column “subscridbers” of the [SpaceBrew interface](http://spacebrew.github.io/spacebrew/admin/admin.html?server=cloudbrain.rocks).
