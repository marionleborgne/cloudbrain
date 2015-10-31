angular.module('rt.eventemitter', []).factory('eventEmitter', function () {
  var key = '_listeners';
  function on($scope, event, fn) {
    if (typeof $scope === 'string') {
      fn = event;
      event = $scope;
      $scope = null;
    }
    if (!this[key]) {
      this[key] = {};
    }
    var events = this[key];
    if (!events[event]) {
      events[event] = [];
    }
    events[event].push(fn);
    var self = this;
    if ($scope) {
      $scope.$on('$destroy', function () {
        self.off(event, fn);
      });
    }
    return this;
  }
  function once($scope, event, fn) {
    if (typeof $scope === 'string') {
      fn = event;
      event = $scope;
      $scope = null;
    }
    var self = this;
    var cb = function () {
      fn.apply(this, arguments);
      self.off(event, cb);
    };
    this.on($scope, event, cb);
    return this;
  }
  function off(event, fn) {
    if (!this[key] || !this[key][event]) {
      return this;
    }
    var events = this[key];
    if (!fn) {
      delete events[event];
    } else {
      var listeners = events[event];
      var index = listeners.indexOf(fn);
      if (index > -1) {
        listeners.splice(index, 1);
      }
    }
    return this;
  }
  function emit(event) {
    if (!this[key] || !this[key][event]) {
      return;
    }
    // Making a copy here to allow `off` in listeners.
    var listeners = this[key][event].slice(0);
    var params = [].slice.call(arguments, 1);
    for (var i = 0; i < listeners.length; i++) {
      listeners[i].apply(null, params);
    }
    return this;
  }
  return {
    inject: function (cls) {
      var proto = cls.prototype || cls;
      proto.on = on;
      proto.once = once;
      proto.off = off;
      proto.emit = emit;
    }
  };
});