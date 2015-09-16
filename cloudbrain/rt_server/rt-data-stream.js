/*
 * TODO: Encapsulate this code. E.g., integrate it inside an angular service.
 */
var RtDataStream;

(function() { 'use strict';

function _isMetricAllowed(rtDataStream, metric) {
    return Object.keys(rtDataStream.channelSubs).indexOf(metric) >= 0;
}

// Constructor
RtDataStream = function (connUrl, deviceName, deviceId) {
    // Super call
    Object.call(this);

    if (!connUrl || !deviceName || deviceId) {
        throw Error('SockJS connection URL or device information not specified');
    }

    // Private fields
    var _connUrl = connUrl;

    // Public fields
    this.conn = null;
    this.channelSubs = {
        'eeg': [],
        'power_bands': [],
    };

    // Property definition
    Object.defineProperty(this, 'connUrl', {
        enumerable: true,
        get: function () { return _connUrl; },
        set: function (value) {
            // noop || throw Error('You cannot reset the connection URL!');
        }
    });

    Object.defineProperty(this, 'deviceName', {
        enumerable: true,
        get: function () { return deviceName; },
        set: function (value) { }
    });

    Object.defineProperty(this, 'deviceId', {
        enumerable: true,
        get: function () { return deviceId; },
        set: function (value) { }
    });
};

// Inheritance (no inheritance for now)
RtDataStream.prototype = Object.create(Object.prototype);
RtDataStream.prototype.constructor = Object;

// Methods
RtDataStream.prototype.disconnect = function () {
    if (this.conn) {
        this.conn.close();
        this.conn = null;
    }
};

RtDataStream.prototype.connect = function (onOpenCallback, onCloseCallback) {
    this.disconnect();

    this.conn = new SockJS(this.connUrl);

    this.conn.onopen = function () {
        if (onOpenCallback) {
            onOpenCallback();
        }
    };

    // Pay attention: it dispaches only messages tight to a channel/metric
    this.conn.onmessage = function (e) {
        var fromChannel = e.data.metric;
        if (_isMetricAllowed.call(this, this, fromChannel)) {
            delete e.data.metric;
            this.channelSubs[fromChannel].forEach(function (cb) {
                cb(e.data);
            });
        }
    };

    this.conn.onclose = function () {
        Object.keys(this.channelSubs).forEach(function (key) {
            this.channelSubs[key].length = 0;
        });
        if (onCloseCallback) {
            onCloseCallback();
        }
        this.conn = null;
    };
};


// Methods
RtDataStream.prototype.subscribe = function (channel, onMessageCb) {
    var configuration = {
        deviceName: this.deviceName,
        deviceId: this.deviceId,
        metric: channel
    };

    if (this.channelSubs[channel]) {
        this.channelSubs[channel].push(onMessageCb);
    }

    this.conn.send(JSON.stringify(configuration));
};

RtDataStream.prototype.unsubscribe = function (channel, onMessageCb) {
    if (this.channelSubs[channel]) {
        this.channelSubs[channel].splice(
            this.channelSubs[channel].indexOf(onMessageCb), 1);
    }
};


})();
