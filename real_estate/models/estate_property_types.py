from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property types"

    name = fields.Char("Type", required=True)
    active = fields.Boolean("Active", default=True)