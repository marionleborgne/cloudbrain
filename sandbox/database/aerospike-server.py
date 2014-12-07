__author__ = 'marion'


# import the module
import aerospike

# Configuration for the client
config = {
    'hosts': [('127.0.0.1', 3000)]
}

# Create a client and connect to the database
client = aerospike.client(config).connect()

# Records are addressable via a tuple of (namespace, set, key)
key = ('test', 'demo', 'foo')

# Write a record
client.put(key, {
    'name': 'John Doe', 'age': 32
})

# Read a record
(key, metadata, record) = client.get(key)
print key, record

client.remove(key)

# Close Connection to Cluster
client.close()