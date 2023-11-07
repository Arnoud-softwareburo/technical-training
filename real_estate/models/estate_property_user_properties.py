from odoo import fields, models, api


class UsersEstateProperty(models.Model):
    _inherit = "res.users"

    # , domain=[('active', '=', True)]
    property_ids = fields.One2many(string="Properties", comodel_name="estate.property", inverse_name="salesman_id")
    