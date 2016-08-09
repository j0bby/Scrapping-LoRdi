var graph = require('fbgraph'),
    app = require('express')(),
    server = require('http').createServer(app);

// this should really be in a config file!
var conf = {
    client_id: '1639558156360604',
    client_secret: 'b44a6e6e008f9d96c79f187696b51169',
    scope: 'public_profile',
    redirect_uri: 'http://localhost:3000/auth/facebook'
};


graph.setVersion("2.7");
// Routes

app.get('/', function(req, res) {
    res.sendFile(__dirname + '/index.html');
});
var param = {
    fields: "created_time,full_picture,from,message"
};
app.get('/auth/facebook', function(req, res) {

    // we don't have a code yet
    // so we'll redirect to the oauth dialog
    if (!req.query.code) {
        var authUrl = graph.getOauthUrl({
            "client_id": conf.client_id,
            "redirect_uri": conf.redirect_uri,
            "scope": conf.scope
        });

        if (!req.query.error) { //checks whether a user denied the app facebook login/permissions
            res.redirect(authUrl);
        } else { //req.query.error == 'access_denied'
            res.send('access denied');
        }
        return;
    }

    // code is set
    // we'll send that and get the access token
    graph.authorize({
        "client_id": conf.client_id,
        "redirect_uri": conf.redirect_uri,
        "client_secret": conf.client_secret,
        "code": req.query.code
    }, function(err, facebookRes) {

        res.redirect('/UserHasLoggedIn');
        graph.get("1458535937750336/feed", function(err, res) {
            res.data.forEach(function(obj) {
                if(obj.message){
                    if(obj.message.indexOf("kallax") !== -1){
                        graph.get('/'+obj.id,param,function(err2,res2){
                            console.log(res2);
                        })
                    }
                }
            });
        });
    });


});


// user gets sent here after being authorized
app.get('/UserHasLoggedIn', function(req, res) {
    res.sendFile(__dirname + '/log.html');
});



server.listen(3000);