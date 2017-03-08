// Core Application

const ROOT_DIR="/srv/Lab/Radio-Bretzel/";

var fs = require('fs');
var express = require('express');
var multer = require('multer');	
var app = express();
var port = 8082;


app.get('/', (req, res) => {
	res.send('<html><body><form action="/" method="post" enctype="multipart/form-data"><input type="file" name="file"/><input type="submit"/></form></body></html>')
})
app.post('/', multer({dest: './upload/'}).single('file'), function (req, res) {
	console.log(req.file);
	res.status(204).end()
});

app.listen(port, () => {
	console.log('Serveur sur port :'+port);
})