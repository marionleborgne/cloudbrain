![x](https://raw.githubusercontent.com/marionleborgne/cloudbrain/master/api/static/images/cb-logo.png)

##Overview
- `connectors`: connectors for [OpenBCI](http://openbci.com), [Muse](http://www.choosemuse.com/), [Neurosky](http://neurosky.com/) and [Spacebrew](https://github.com/Spacebrew/spacebrew) sending data to CloudBrain
- `listeners`: CloudBrain Listeners to get the live data data for [OpenBCI](http://openbci.com),[Muse](http://www.choosemuse.com/), [Neurosky](http://neurosky.com/) and [Spacebrew](https://github.com/Spacebrew/spacebrew)
- `api`: contains the web API to retrieve the history of data, route live data, or retrieve data aggregated data (see [cloudbrain.rocks](http://cloudbrain.rocks) for the API documentation)
- `router`: router to update spacebrew routes (for our [Exploratorium](http://www.exploratorium.edu/) exhibition)
- `spacebrew`: python websocket wrapper to interface with [Spacebrew](https://github.com/Spacebrew/spacebrew)
- `database` : python wrapper to read and write data to cassandra

![x](https://raw.githubusercontent.com/marionleborgne/cloudbrain/master/explo-infrastructure.png)

##Getting started with CloudBrain
- An instance of CloudBrain is currently running at [cloudbrain.rocks](http://cloudbrain.rocks). This is also where you can find CloudBrain's API documentation.
- The packages that you want to use are `connectors` and `listeners`. Connectors will allow you to send live data to CloudBrain. Listeners will allow you to read live data from CloudBrain.
- Routing of live data is done via SpaceBrew (currently running on the CloudBrain server). To visualize how the data is being routed you can go to [this interface](http://spacebrew.github.io/spacebrew/admin/admin.html?server=cloudbrain.rocks).

##Sending data to CloudBrain
- Install the [MuseIO SDK](http://www.choosemuse.com/developer-kit/)
- Pair your Muse via Bluetooth.
- Start MuseIO: open a terminal or command prompt and run: `muse-io --osc osc.udp://localhost:9090`
- Open a new terminal tab and run:
<br>
`git clone https://github.com/marionleborgne/cloudbrain`
<br>
`cd cloudbrain/connectors/spacebrew`
<br>
`pip install websocket-client`
`python spacebrew_server.py --name=YOUR_NAME_HERE`
- The last command will register your muse to CloudBrain's Spacebrew
- Check if you muse is in the column “publishers” of the [SpaceBrew interface](http://spacebrew.github.io/spacebrew/admin/admin.html?server=cloudbrain.rocks).


##Reading data from CloudBrain
- Open a new terminal tab and run:
<br>
`cd cloudbrain/listeners`
<br>
`python example_spacebrew_client.py --name=YOUR_NAME_HERE`
- The last command will register your booth to cloudbrain’s spacebrew
- Check if you booth is in the column “subscridbers” of the [SpaceBrew interface](http://spacebrew.github.io/spacebrew/admin/admin.html?server=cloudbrain.rocks).
