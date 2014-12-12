cloudbrain
==========

Files that can be run are in the following directories:

- `connectors`: Connectors for openBCI, Muse, Neurosky and Spacebrew sending data to cloudbrain
- `listeners`: Cloudbrain Listeners stroring data in Cassandra (again, for openBCI, Muse, Neurosky and Spacebrew )
- `api`: Web API to request history of data from cloudbrain (need to be cleaned up and enhanced with more endpoints -- only has one for now)
- `router`: Router to update spacebrew routes


Other directories contain:
- `spacebrew`: python websocket wrapper to interface with Spacebrew
- `database` : Cassandra python client
