var Odoo = require('odoo-xmlrpc');

var odoo = new Odoo({
	url: 'localhost',
	port: 8070,
	db: 'bd11_tecsup',
	username: 'admin',
	password: 'admin'
});

// Connect to Odoo
odoo.connect(function (err) {
	if (err) { return console.log(err); }
	console.log('Connected to Odoo server.');
	var inParams = [];
	inParams.push([]);
	var params = [];
	params.push(inParams);
	odoo.execute_kw('facturacion.series', 'search_read', params, function (err, value) {
		if (err) { return console.log(err); }
		console.log('Result: ', value);
	});
});