var express = require('express');
var app = express();

app.use(express.static(__dirname + '/static'));
app.listen(80);