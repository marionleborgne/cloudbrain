importScripts('//cdn.jsdelivr.net/sockjs/1.0.0/sockjs.min.js');

var conn;

self.addEventListener('message', function(e) {
  var data = e.data;
  console.log('WORKER', e);
  switch (data.cmd) {
    case 'start':
      connect(data.conf);
      break;
    case 'stop':
      disconnect();
      // self.close(); // Terminates the worker.
      break;
  }
}, false);

function connect(configuration) {
    disconnect();

    conn = new SockJS('http://localhost:31415/rt-stream');

    conn.onopen = function() {
      conn.send(JSON.stringify(configuration));
      self.postMessage({ type: 'connected' });
    };

    conn.onmessage = function(e) {
      self.postMessage({ type: 'msg', msg: e.data});
    };

    conn.onclose = function() {
      self.postMessage({ type: 'disconnected' });
      conn = null;
    };
}

function disconnect() {
  if (conn != null) {
    conn.close();
    conn = null;
  }
}
