![x](https://raw.githubusercontent.com/marionleborgne/cloudbrain/master/api/static/images/cb-logo.png)

##Overview
CloudBrain is a platform for real-time EEG data analysis and visualization. [EEG](http://en.wikipedia.org/wiki/Electroencephalography) is the recording of electrical activity along the scalp. In other words, brainwaves.
<br>
CloudBrain enables you to:
1. **Stream EEG data** into a central universally accessible database.
2. **Detect patterns** by analyzing EEG data.
4. **Visualize data** and patterns in real-time.

![x](https://raw.githubusercontent.com/marionleborgne/cloudbrain/master/CloudBrain.png)


##Getting started with CloudBrain
- An instance of CloudBrain is currently running at http://cloudbrain.rocks.
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

##CloudBrain's Architecture
- `connectors`: connectors for [OpenBCI](http://openbci.com), [Muse](http://www.choosemuse.com/), [Neurosky](http://neurosky.com/) and [Spacebrew](https://github.com/Spacebrew/spacebrew) sending data to CloudBrain
- `listeners`: CloudBrain Listeners to get the live data data for [OpenBCI](http://openbci.com),[Muse](http://www.choosemuse.com/), [Neurosky](http://neurosky.com/) and [Spacebrew](https://github.com/Spacebrew/spacebrew)
- `ui`: contains the UI & web API to retrieve the history of data, route live data, or retrieve data aggregated data (see [cloudbrain.rocks/api](http://cloudbrain.rocks/api) for the API documentation)
- `router`: router to update spacebrew routes (for our [Exploratorium](http://www.exploratorium.edu/) exhibition)
- `spacebrew`: python websocket wrapper to interface with [Spacebrew](https://github.com/Spacebrew/spacebrew)
- `database` : python wrapper to read and write data to cassandra


##Reading data from CloudBrain
- Open a new terminal tab and run:
<br>
`cd cloudbrain/listeners`
<br>
`python example_spacebrew_client.py --name=YOUR_NAME_HERE`
- The last command will register your booth to cloudbrain’s spacebrew
- Check if you booth is in the column “subscridbers” of the [SpaceBrew interface](http://spacebrew.github.io/spacebrew/admin/admin.html?server=cloudbrain.rocks).

## Infrastructure @ The Exploratorium
Infrastructure v2.0 for the [Exploratorium of San Francisco](http://www.exploratorium.edu/). The exhibit is called [*Cognitive Technology*](http://www.exploratorium.edu/press-office/press-releases/new-exhibition-understanding-influencing-brain-activity-opens) and starts on February 2015.

![x](https://raw.githubusercontent.com/marionleborgne/cloudbrain/master/infra.png)
