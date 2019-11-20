# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import Warning
import requests
import json
import logging
log = logging.getLogger(__name__)

URL = 'https://dniruc.apisperu.com/api/v1/'
TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImZuYXF1aXJhQHRlY3N1cC5lZHUucGUifQ.vTZ_wTjLjAnipAdvYz8xmLBEbvdmFPzpECLGjDHrMqs'

class ResPartner(models.Model):
	_inherit = 'res.partner'
	
	tipo_doc_id = fields.Many2one(comodel_name='facturacion.documentos',
		string='Tipo de documento')
    
	@api.multi
	@api.onchange('vat','tipo_doc_id')
	def onchange_doc(self):
		for partner in self:
			log.info('----------------')
			log.info('Inicia nuestra validacion')
			log.info(partner.vat)
			log.info(partner.tipo_doc_id)
			if partner.tipo_doc_id.code in ('1','6') and partner.vat is not False:
				tipo_doc = False
				if partner.tipo_doc_id.code == '1' and len(partner.vat) == 8:
					tipo_doc = 'dni'
				if partner.tipo_doc_id.code == '6' and len(partner.vat) == 11:
					tipo_doc = 'ruc'
				if tipo_doc:
					respuesta = self.get_doc(tipo_doc,partner.vat)
					if not respuesta:
						raise Warning("Server not responding now, try again later")
					if not respuesta[0]:
						raise Warning(respuesta[1])
					try:
						respuesta_json = json.loads(respuesta[1].decode())
					except ValueError as e:
						raise Warning(("Server response content is not serializable to JSON object: %s" % e))
					if tipo_doc == 'ruc':
						partner.name = respuesta_json['razonSocial']
						partner.street = respuesta_json['direccion']
					if tipo_doc == 'dni':
						partner.name = respuesta_json['nombres'] + ' ' + respuesta_json['apellidoPaterno'] + ' ' + respuesta_json['apellidoMaterno']
	
	def get_doc(self,tipo_doc,vat):
		s = requests.Session()
		try:
			r = s.get(URL+tipo_doc+'/'+vat+'?token='+TOKEN, verify=False)
		except requests.exceptions.RequestException as e:
			return (False, e)
		if r.status_code == 200:
			return (True, r.content)
		else:
			return (False, 'Tenemos un problema!')
	
	@api.constrains('tipo_doc_id','vat')
	def _check_unique_vat(self):
		for partner in self:
			if not partner.vat:
				return True
			same_vat_count = self.search_count([
				('tipo_doc_id','=',partner.tipo_doc_id.id),
				('vat','=',partner.vat)
			])
			if same_vat_count > 1:
				raise Warning('Ya existe una entidad con ese documento!')
