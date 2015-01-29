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
sp_router = SpacebrewRouter(server=settings.EXPLO_BRAINSERVER_IP)
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
            content = str(callback) + '(' + str(f()) + ')'
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

@app.route('/explo')
def explo():
    return render_template('cloudbrain.html'), 200

@app.route('/average')
def average():
    return render_template('average.html'), 200

@app.route('/radarcharts')
def radarcharts():
    return render_template('radar.html'), 200

@app.route('/form')
def consent_form():
    return render_template('form.html'), 200

@app.route('/thank-you')
def thanks():
    return render_template('thanks.html'), 200


@app.route('/api-doc')
def doc():
    return render_template('api-doc.html'), 200

@app.route('/spacebrew')
def spacebrew():
    return redirect("http://spacebrew.github.io/spacebrew/admin/admin.html?server=cloudbrain.rocks")



@app.route('/post', methods = ['POST'])
def post():
    # Get the parsed contents of the form data
    json = request.json
    print(json)


@app.route("/set_tag", methods=['GET'])
@support_jsonp
def set_tag():
    r = request.args.get('number', None)
    return r, 200

@app.route("/set_gender", methods=['GET'])
@support_jsonp
def set_gender():
    r = request.args.get('gender', None)
    return r, 200

@app.route("/set_age", methods=['GET'])
@support_jsonp
def set_age():
    r = request.args.get('age', None)
    return r, 200

@app.route("/approved", methods=['GET'])
@support_jsonp
def approved():
    r = request.args.get('choice', None)
    return r, 200

@app.route("/link", methods=['GET'])
@support_jsonp
def link():
    publisher = request.args.get('publisher', None)
    subscriber = request.args.get('subscriber', None)
    pub_metric = request.args.get('pub_metric', None)
    sub_metric = request.args.get('sub_metric', None)
    sub_ip = request.args.get('sub_ip', None)
    pub_ip = request.args.get('pub_ip', None)
    response = sp_router.link(pub_metric, sub_metric, publisher, subscriber, pub_ip, sub_ip)
    return response, 200


@app.route("/unlink", methods=['GET'])
@support_jsonp
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
@support_jsonp
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
        # Adding logging for disconnection here

        # For each subscription, unlink it
        for data_channel in sp_config_cache["subscriptions"][booth]:
            # Keep these data channels
            if data_channel != "connect" and data_channel != "disconnect":
                sp_router.unlink(data_channel, data_channel, 'muse-%s' % previous_muse, booth, ip)

    # Link subscription routes for requested Booth and Muse
    if booth in sp_config_cache["subscriptions"]:
        # Inform the booth it has been connected to a new muse
        sp_router.connect_event(booth, 'muse-%s' % muse)
        # Adding logging for connection here

        # For each subscription, link it
        for data_channel in sp_config_cache["subscriptions"][booth]:
            if data_channel == "connect" or data_channel == "disconnect":
                sp_router.link(booth + '-' + data_channel, data_channel, 'router', booth, ip)
            else:
                sp_router.link(data_channel, data_channel, 'muse-%s' % muse, booth, ip)

        # Add route to cache
        sp_config_cache["routes"][booth] = muse

    return 'OK', 200

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

    mock_data = {
        "visitors": 12
    }

    return json.dumps(mock_data)

@app.route("/data/aggregates/fft", methods=['GET'])
@support_jsonp
def fft_aggregates():

    # mock values
    alpha = 0.5 - random()
    beta = 0.5 - random()
    gamma = 0.5 - random()
    theta = 0.5 - random()
    delta = 0.5 - random()

    mock_data = {
        "alpha": {'avg': alpha},
        "beta":  {'avg': beta},
        "gamma":  {'avg': gamma},
        "theta":  {'avg': theta},
        "delta":  {'avg': delta}
    }

    return json.dumps(mock_data)



if __name__ == '__main__':
    app.run('0.0.0.0', 8080)
