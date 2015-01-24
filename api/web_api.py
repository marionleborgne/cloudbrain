#!flask/bin/python
from flask import Flask, render_template, request, redirect, current_app
import json
from random import random
from functools import wraps
import re

# add the shared settings file to namespace
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))
import settings
from router.spacebrew_router import SpacebrewRouter

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
sp_router = SpacebrewRouter(server=settings.CLOUDBRAIN_ADDRESS)
sp_config_cache = {
    "subscriptions": {

    },
    "routes": {

    }
}

def support_jsonp(f):
    """Wraps JSONified output for JSONP"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + f() + ')'
            return current_app.response_class(content, mimetype='application/json')
        else:
            return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('api-doc.html'), 200

@app.route('/about')
def about():
    return render_template('about.html'), 200

@app.route('/api-doc')
def doc():
    return render_template('api-doc.html'), 200

@app.route('/spacebrew')
def spacebrew():
    return redirect("http://spacebrew.github.io/spacebrew/admin/admin.html?server=cloudbrain.rocks")

# NOTE - I removed this from my branch because we're using /patch for the routing
@app.route("/link", methods=['GET'])
def link():
    publisher = request.args.get('publisher', None)
    subscriber = request.args.get('subscriber', None)
    pub_metric = request.args.get('pub_metric', None)
    sub_metric = request.args.get('sub_metric', None)
    sub_ip = request.args.get('sub_ip', None)
    pub_ip = request.args.get('pub_ip', None)
    response = sp_router.link(pub_metric, sub_metric, publisher, subscriber, pub_ip, sub_ip)
    return response, 200

# NOTE - I removed this from my branch because we're using /patch for the routing
@app.route("/unlink", methods=['GET'])
def unlink():
    publisher = request.args.get('publisher', None)
    subscriber = request.args.get('subscriber', None)
    pub_metric = request.args.get('pub_metric', None)
    sub_metric = request.args.get('sub_metric', None)
    sub_ip = request.args.get('sub_ip', None)
    pub_ip = request.args.get('pub_ip', None)
    response = sp_router.unlink(pub_metric, sub_metric, publisher, subscriber, pub_ip, sub_ip)
    return response, 200

@app.route("/patch", methods=['POST'])
def patch():
    # Lookup Muse Headset by RFID Tag ID
    rfid = request.form["rfid"]
    muse = settings.TAGS[rfid]

    # Lookup Booth Number by SparkCore Serial Number
    core = request.form["core"]
    booth = settings.CORES[core]

    # Get IP address for the Booth
    ip = settings.BOOTHS[booth]["ip"]

    # Get current Spacebrew configuration state
    spacebrew_configs = sp_router.get_spacebrew_config()

    for spacebrew_config in spacebrew_configs:
        # This hash defines a client
        if type(spacebrew_config) is dict and 'config' in spacebrew_config:
            # Use only Booth configs since we control the Muse config
            config_name = spacebrew_config['config']['name'].encode('ascii', 'ignore')
            if re.match("booth-\d+", config_name):
                # Set booth subscriptions
                sp_config_cache["subscriptions"][config_name] = []
                for message in spacebrew_config['config']['subscribe']['messages']:
                    sp_config_cache["subscriptions"][config_name].append(message["name"].encode('ascii', 'ignore'))

        # TODO: Cache existing routes so we can hand-route things then disconnect them automatically
        # # This hash defines the routes
        # if 'route' in spacebrew_config:
        #     booth_identity = spacebrew_config['route']['subscriber']['clientName']
        #     muse_identity = spacebrew_config['route']['publisher']['clientName']
        #     print "Found route between for %s and %s" % (muse_identity, booth_identity)

    # Unlink subscription routes for requested Booth and Muse
    if booth in sp_config_cache["routes"]:
        # Remove route from cache
        previous_muse = sp_config_cache["routes"].pop(booth)

        # Inform the booth it has been connected from the previous muse
        sp_router.disconnect_event(booth, 'muse-%s' % previous_muse)

        # For each subscription, unlink it
        for data_channel in sp_config_cache["subscriptions"][booth]:
            # Keep these data channels
            if data_channel != "connect" and data_channel != "disconnect":
                sp_router.unlink(data_channel, data_channel, 'muse-%s' % previous_muse, booth, ip)

    # Link subscription routes for requested Booth and Muse
    if booth in sp_config_cache["subscriptions"]:
        # Inform the booth it has been connected to a new muse
        sp_router.connect_event(booth, 'muse-%s' % muse)

        # For each subscription, link it
        for data_channel in sp_config_cache["subscriptions"][booth]:
            if data_channel == "connect" or data_channel == "disconnect":
                sp_router.link(booth + '-' + data_channel, data_channel, 'router', booth, ip)
            else:
                sp_router.link(data_channel, data_channel, 'muse-%s' % muse, booth, ip)

        # Add route to cache
        sp_config_cache["routes"][booth] = muse

    return 'OK'

@app.route("/data", methods=['GET'])
@support_jsonp
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

@app.route("/data/aggregates", methods=['GET'])
@support_jsonp
def aggregates():
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

@app.route("/data/visitors", methods=['GET'])
@support_jsonp
def nb_visitors():

    visitors = random() * 100000

    mock_data = {
        "visitors": visitors
    }

    return json.dumps(mock_data)

@app.route("/data/aggregates/fft", methods=['GET'])
@support_jsonp
def fft_aggregates():

    # mock values
    alpha = random() * 10
    beta = random() * 10
    gamma = random() * 10
    theta = random() * 10

    mock_data = {
        "alpha": {'avg': alpha, 'std': 0.1},
        "beta":  {'avg': beta, 'std': 0.1},
        "gamma":  {'avg': gamma, 'std': 0.1},
        "theta":  {'avg': theta, 'std': 0.1}
    }

    return json.dumps(mock_data)



if __name__ == '__main__':
    app.run('0.0.0.0', 8080)
