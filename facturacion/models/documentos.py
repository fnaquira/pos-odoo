# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Documentos(models.Model):
	_name = 'facturacion.documentos'
	_description = 'Documentos para las entidades'

	name = fields.Char(string='Nombre del documento')
	code = fields.Char(string='Codigo del documento')