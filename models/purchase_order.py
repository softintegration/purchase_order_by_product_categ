# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    categ_id = fields.Many2one('product.category', 'Product Category',required=True)

    @api.onchange('categ_id')
    def on_change_categ_id(self):
        self.order_line = False

    @api.constrains('categ_id','order_line')
    def _check_order_line_categ_unicity(self):
        """ Check that all the selected products have the same category"""
        if self.categ_id and self.order_line:
            order_line_categ_id = self._get_order_line_categ()
            if len(order_line_categ_id) > 1:
                raise UserError(_("All the products must belongs to the same category!"))
            if order_line_categ_id[0].id != self.categ_id.id:
                raise UserError(_("All the products must belongs to the purchase order category!"))



    def _get_order_line_categ(self):
        return self.order_line.mapped("product_id").mapped("categ_id")
