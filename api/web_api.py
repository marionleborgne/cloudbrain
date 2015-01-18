#!flask/bin/python
from flask import Flask, render_template, request, redirect, current_app
import json
from random import random
from functools import wraps

# add the shared settings file to namespace
import sys
from os.path import dirname, abspath
sys.path.insert(0, dirname(dirname(abspath(__file__))))
import settings
from router.spacebrew_router import SpacebrewRouter

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
sp_router = SpacebrewRouter(server=settings.CLOUDBRAIN_ADDRESS)


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

@app.route("/link", methods=['GET'])
def link():
    publisher = request.args.get('publisher', None)
    subscriber = request.args.get('subscriber', None)
    pub_metric = request.args.get('pub_metric', None)
    sub_metric = request.args.get('sub_metric', None)
    sub_ip = request.args.get('sub_ip', None)
    sp_router.link(pub_metric, sub_metric, publisher, subscriber, sub_ip)
    return redirect("http://spacebrew.github.io/spacebrew/admin/admin.html?server=cloudbrain.rocks")

@app.route("/unlink", methods=['GET'])
def unlink():
    publisher = request.args.get('publisher', None)
    subscriber = request.args.get('subscriber', None)
    pub_metric = request.args.get('pub_metric', None)
    sub_metric = request.args.get('sub_metric', None)
    sub_ip = request.args.get('sub_ip', None)
    sp_router.unlink(pub_metric, sub_metric, publisher, subscriber, sub_ip)
    return redirect("http://spacebrew.github.io/spacebrew/admin/admin.html?server=cloudbrain.rocks")

@app.route("/patch", methods=['POST'])
def patch():
    core = request.form["core"]
    rfid = request.form["rfid"]

    print settings.CORES[core]
    print settings.TAGS[rfid]

    muse = settings.TAGS[rfid]
    booth = settings.CORES[core]
    metrics = settings.BOOTHS[booth]["required_routes"]
    ip = settings.BOOTHS[booth]["ip"]

    #Unlink existing required routes connected to Booth
    museids = {v: k for k, v in settings.TAGS.items()}
    for museid in museids:
        for metric in metrics:
            sp_router.unlink(metric[0], metric[1], 'muse-%s' % museid, booth, ip)

    #Link Booth
    for metric in metrics:
        sp_router.link(metric[0], metric[1], 'muse-%s' % muse, booth, ip)

    return redirect("http://spacebrew.github.io/spacebrew/admin/admin.html?server=cloudbrain.rocks")

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
