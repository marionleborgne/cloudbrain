#!flask/bin/python
from flask import Flask
from database.cassandra_repository import CassandraRepository
from database.cassandra_settings import KEYSPACE
from database.cassandra_settings import MUSE_COLUMN_FAMILY

import time
import json

app = Flask(__name__)
muse_cassandra_repo = CassandraRepository(KEYSPACE, MUSE_COLUMN_FAMILY)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/muse/eeg')
def get_metric():

    # /!\ work in progress
    # todo: clean and add the rest of the endpoints
    path = '/muse/eeg'
    time_horizon = 5  # in ms
    now = int(time.time() * 1000)
    start_row_key = '%s_%s' % (path, now)
    end_row_key = '%s_%s' % (path, now - time_horizon)
    data = muse_cassandra_repo.get_range(start_row_key, end_row_key)
    result = json.dumps([d for d in data])
    return result


if __name__ == '__main__':
    app.run(debug=True)
