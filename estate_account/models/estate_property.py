from odoo import models


class EstatePropertyInherit(models.Model):
    _inherit = "estate.property"

    def button_property_sold(self):
        # todo part 2 of invoice creation
        # https://www.odoo.com/documentation/master/developer/tutorials/getting_started/14_other_module.html#invoice-creation

        # todo (not in this file)
        # add fancy status
        # https://www.odoo.com/documentation/master/developer/tutorials/getting_started/12_sprinkles.html
        return super().inherited_action()
