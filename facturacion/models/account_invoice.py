# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AccountInvoice(models.Model):
	_inherit = 'account.invoice'
	
	serie_id = fields.Many2one(comodel_name='facturacion.series',
		string='Serie Electrónica')