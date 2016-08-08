var app = require('express')(),
    server = require('http').createServer(app);

app.get('/', function(req, res) {
    res.sendFile(__dirname + '/index.html');
});

server.listen(8070);