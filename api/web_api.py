#!flask/bin/python
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

import json
from random import random


@app.route('/')
def index():
    return render_template('index.html'), 200


@app.route('/about')
def about():
    return render_template('about.html'), 200


@app.route('/api-doc')
def doc():
    return render_template('api-doc.html'), 200


@app.route("/data", methods=['GET'])
def data():
    user_id = request.args.get('userId', None)
    metric = request.args.get('metric', None)
    start = int(request.args.get('start', None))
    end = int(request.args.get('end', None))

    # mock data. will be replaced by real data soon
    mock_data = []
    for timestamp in range(start, end):
        if metric == 'eeg':
            value = ['/muse/eeg', random() * 100, random() * 100, random() * 100, random() * 100]
        elif metric == 'acc':
            value = ['/muse/acc', random() * 100, random() * 100, random() * 100]
        elif metric == 'concentration':
            value = ['/muse/elements/experimental/concentration', random()]
        elif metric == 'mellow':
            value = ['/muse/elements/experimental/mellow', random()]
        else:
            value = [random()]
        datapoint = {
            "userId": user_id,
            "metric": metric,
            "value": value,
            "timestamp": timestamp}
        mock_data.append(datapoint)

    return json.dumps(mock_data)


@app.route("/aggregate", methods=['GET'])
def aggregate():
    user_id = request.args.get('userId', None)
    metric = request.args.get('metric', None)
    aggregateType = request.args.get('aggregateType', None)

    # mock data. will be replaced by real data soon
    if metric == 'eeg':
        value = ['/muse/eeg', random() * 100, random() * 100, random() * 100, random() * 100]
    elif metric == 'acc':
        value = ['/muse/acc', random() * 100, random() * 100, random() * 100]
    elif metric == 'concentration':
        value = ['/muse/elements/experimental/concentration', random()]
    elif metric == 'mellow':
        value = ['/muse/elements/experimental/mellow', random()]
    else:
        value = [random()]

    mock_data = {
        "userId": user_id,
        "metric": metric,
        "value": value,
        "aggregateType": aggregateType}

    return json.dumps(mock_data)

if __name__ == '__main__':
    app.run('0.0.0.0', 8080)
