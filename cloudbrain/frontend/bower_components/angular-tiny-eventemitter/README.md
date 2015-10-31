# angular-tiny-eventemitter

> Tiny event emitter for Angular.JS.

[![Build Status](https://travis-ci.org/rubenv/angular-tiny-eventemitter.png?branch=master)](https://travis-ci.org/rubenv/angular-tiny-eventemitter)

## Installation
Add angular-tiny-eventemitter to your project:

```
bower install --save angular-tiny-eventemitter
```

Add it to your HTML file:

```html
<script src="bower_components/angular-tiny-eventemitter/dist/angular-tiny-eventemitter.min.js"></script>
```

Reference it as a dependency for your app module:

```js
angular.module('myApp', ['rt.eventemitter']);
```

## Usage

Simply inject it as a service:

```js
angular.module('myApp').factory('MyType', function (eventEmitter) {
    function MyType(something) {
        this.value = something;
    }
    
    // Add event emitter methods to MyType.
    eventEmitter.inject(MyType);

    return MyType;
});
```

You can then use all the normal event emitter methods:

```js
angular.module('myApp').controller('TestCtrl', function ($scope, MyType) {
    var thing = new MyType(123);

    function logTheEvent(arg1, arg2) {
        console.log('Got event: ' + arg1 + ', ' + arg2);
    }

    thing.on('event', logTheEvent);

    $scope.$on('$destroy', function () {
        // Remember to avoid memory leaks!
        thing.off('event', logTheEvent);
    });

    thing.emit('event', 4, 8);
});
```

Alternatively, you can pass a $scope as the first parameter to on() or once() and the listener will be automatically unregistered if the $scope is destroyed.

```js
angular.module('myApp').controller('TestCtrl', function ($scope, MyType) {
    var thing = new MyType(123);

    function logTheEvent(arg1, arg2) {
        console.log('Got event: ' + arg1 + ', ' + arg2);
    }

    // Passing $scope will register a $destroy event for you.
    thing.on($scope, 'event', logTheEvent);

    thing.emit('event', 4, 8);
});
```

## License 

    (The MIT License)

    Copyright (C) 2014 by Ruben Vermeersch <ruben@rocketeer.be>

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
