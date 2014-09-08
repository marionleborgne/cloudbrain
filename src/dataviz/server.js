var express = require('express');
var app = express();
var cors = require('cors');

app.use(express.static(__dirname + '/static'));
app.use(cors());
app.listen(8080);

app.all('*', function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "X-Requested-With");
    next();
});
