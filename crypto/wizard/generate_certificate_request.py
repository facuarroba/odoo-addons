# -*- coding: utf-8 -*-
from openerp.osv import fields,osv
from openerp.tools.translate import _
from M2Crypto import X509

class generate_certificate_request(osv.osv_memory):
    def _get_company_id(self, cr, uid, context={}):
        res = self.pool.get('res.users').read(cr, uid, [uid], ['company_id'], context=context)
        if res and res[0]['company_id']:
            return res[0]['company_id'][0]
        return False

    _name = 'crypto.generate_certificate_request'

    _columns = {
        'company_id': fields.many2one('res.company', 'Company'),
        'name_c':  fields.char('Country (C)', size=2),
        'name_sp': fields.char('State or Province Name (ST/SP)', size=64),
        'name_l':  fields.char('Locality Name (L)', size=64),
        'name_o':  fields.char('Organization Name (O)', size=64),
        'name_ou': fields.char('Organization Unit Name (OU)', size=64),
        'name_cn': fields.char('Common name (CN)', size=64),
        'name_gn': fields.char('Given Name (GN)', size=64),
        'name_sn': fields.char('Surname (SN)', size=64),
        'name_email': fields.char('E-mail Addres (EMail)', size=64),
        'name_serialnumber': fields.char('Serial Number (serialNumber)', size=64),
    }

    _defaults = {
        'company_id': _get_company_id,
    }

    def onchange_company_id(self, cr, uid, ids, company_id, context=None):
        v={}
        if company_id:
            company=self.pool.get('res.company').browse(cr,uid,company_id)
            try:
                v['name_c'] = company.partner_id.country_id.code
                v['name_sp'] = company.partner_id.state_id.name
                v['name_l'] = company.partner_id.city
                v['name_o'] = company.name
                v['name_cn'] = company.partner_id.name
                v['name_email'] = company.partner_id.email
            except:
                pass
        return {'value': v }

    def on_generate(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        active_ids = context['active_ids']
        pairkey_obj = self.pool.get('crypto.pairkey')
        for wizard in self.browse(cr, uid, ids):
            name = X509.X509_Name()
            if wizard.name_c:  name.C  = wizard.name_c
            if wizard.name_sp: name.SP = wizard.name_sp
            if wizard.name_l:  name.L  = wizard.name_l
            if wizard.name_o:  name.O  = wizard.name_o
            if wizard.name_ou: name.OU = wizard.name_ou
            if wizard.name_cn: name.CN = wizard.name_cn
            if wizard.name_gn: name.GN = wizard.name_gn
            if wizard.name_sn: name.SN = wizard.name_sn
            if wizard.name_email: name.EMail = wizard.name_email
            if wizard.name_serialnumber: name.serialNumber = wizard.name_serialnumber
            pairkey_obj.generate_certificate_request(cr, uid, active_ids, name)
        return {'type': 'ir.actions.act_window_close'}


    def on_cancel(self, cr, uid, ids, context):
        return {}

generate_certificate_request()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
