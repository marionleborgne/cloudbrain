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

    if (!connUrl || !deviceName || !deviceId) {
        throw Error('SockJS connection URL or device information not specified');
    }

    // Private fields
    var _connUrl = connUrl;

    // Public fields
    this.conn = null;
    this.channelSubs = {
        'eeg': [],
        'alpha_absolute': [],
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
    var self = this;
    if (self.conn) {
        self.conn.close();
        self.conn = null;
    }
};

RtDataStream.prototype.connect = function (onOpenCallback, onCloseCallback) {
    var self = this;

    self.disconnect();

    self.conn = new SockJS(this.connUrl);

    self.conn.onopen = function () {
        if (onOpenCallback) {
            onOpenCallback();
        }
    };

    // Pay attention: it dispaches only messages tight to a channel/metric
    self.conn.onmessage = function (e) {
        var jsonContent = JSON.parse(e.data);
        var fromChannel = jsonContent.metric;
        if (_isMetricAllowed.call(self, self, fromChannel)) {
            delete jsonContent.metric;
            self.channelSubs[fromChannel].forEach(function (cb) {
                cb(jsonContent);
            });
        }
    };

    self.conn.onclose = function () {
        Object.keys(self.channelSubs).forEach(function (key) {
            self.channelSubs[key].length = 0;
        });
        if (onCloseCallback) {
            onCloseCallback();
        }
        self.conn = null;
    };
};


// Methods
RtDataStream.prototype.subscribe = function (channel, onMessageCb) {
    var self = this;

    var configuration = {
        type: 'subscription',
        deviceName: this.deviceName,
        deviceId: this.deviceId,
        metric: channel
    };

    if (self.channelSubs[channel]) {
        self.channelSubs[channel].push(onMessageCb);
    }

    self.conn.send(JSON.stringify(configuration));
};

RtDataStream.prototype.unsubscribe = function (channel, onMessageCb) {
    var self = this;

    var unsubscriptionMsg = {
        type: 'unsubscription',
        metric: channel
    };

    if (self.channelSubs[channel]) {
        self.channelSubs[channel].splice(
            self.channelSubs[channel].indexOf(onMessageCb), 1);
    }

    self.conn.send(JSON.stringify(unsubscriptionMsg));
};


})();
