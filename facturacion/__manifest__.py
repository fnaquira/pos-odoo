# -*- coding: utf-8 -*-
{
    'name' : 'Facturacion',
    'version' : '1.0',
    'summary': 'Modulo basico para facturacion en Peru',
    'description': """
Core mechanisms for the accounting modules. To display the menuitems, install the module account_invoicing.
    """,
    'depends' : ['account'],
    'data': [
		  'data/series.xml',
		  'views/series_view.xml',
		  'views/account_invoice_view.xml',
    ]
}
