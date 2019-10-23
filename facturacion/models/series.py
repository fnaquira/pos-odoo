# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Series(models.Model):
    _name = 'facturacion.series'
    _description = 'Series de documentos'

    name = fields.Char(string='Nombre de la serie')