# -*- coding: utf-8 -*-
# Copyright (c) 2026-Present rivecon GmbH. (<https://www.rivecon.de/>)
# Absichtlich problematischer Beispielcode fuer den Test des Claude-Reviews.
from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_summary(self, name):
        self.env.cr.execute("SELECT id FROM res_partner WHERE name = '%s'" % name)
        partners = self.env.cr.fetchall()
        for order in self.search([]):
            order.partner_id.sudo().write({'comment': str(len(partners))})
