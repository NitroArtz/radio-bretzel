// Core Application

// TEMPORARY CONF LOCATION
/*	Host usual information	*/
const HOSTNAME = "";
const DOMAIN = "";
const FQDN = "localhost";	//localhost here for dev
const LOCAL_IP = "127.0.0.1";	//127.0.0.1 here for dev
const PUBLIC_IP = "";
const port = 8082;


//APPLICATION STARTS HERE
//imports
var fs = require('fs');
var express = require('express');
var multer = require('multer');
var app = express();
var container=require('dockerode');

//routes
//	index
app.get('/', (req,res) =>{
	res.send('<html><body><h3>Hello You. It works. :O for </h3><ul><a href="/upload"><li>Upload</li></a><a href="/stream/test"><li>Test Stream</li></a></ul></body></html>').end();
});


//	upload
app.get('/upload', (req, res) => {
	res.send('<html><body><form action="/upload" method="post" enctype="multipart/form-data"><input type="file" name="file"/><input type="submit"/></form></body></html>')
});
app.post('/upload', multer({dest: './upload/'}).single('file'), function (req, res) {
	console.log(req.file);
	res.status(204).end()
});


// 	stream
app.get('/stream/test', (req,res) =>{
	res.send('<html><body><h3>Stream Test</h3><div><audio src="http://'+FQDN+':8000/test" controls>Marche plus ? :(</audio></div></body></html>').end();
});

// CREATING NEW STREAM TEST
app.get('/stream/test2', (req,res) =>{
	res.send('<html><body><h3>Stream Test 2</h3><div><audio src="http://'+FQDN+':8000/test" controls>Marche plus ? :(</audio></div></body></html>').end();
});
app.get('/stream/generate', (req,res) =>{
	//Do files exist ?


	//Run CT
//	docker.run('liquidsoap-bretzel', ["./string.liq"] , )

	res.send('<html>bo</html>').end();
});


//	auth
app.post('/auth/check', (req,res) =>{
	res.setHeader('icecast-auth-test', 1);
	res.send().end();
	console.log('/auth/check');
});



app.listen(port, () => {
	console.log('Serveur sur port : '+port);
	console.log('Redirection vers port 80 (Merci la Baleine !)')
});
