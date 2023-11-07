from odoo import fields, models, api
from odoo.exceptions import UserError


garden_possible_orientations = [('N', 'North'),
                                    ('E', 'East'),
                                    ('S', 'South'),
                                    ('W', 'West')]

estate_possible_states = [('new', 'New'),
                          ('offer_received', 'Offer Received'),
                          ('offer_accepted', 'Offer Accepted'),
                          ('sold', 'Sold'),
                          ('canceled', 'Canceled')]


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate basic properties"

    name = fields.Char("Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From", default=fields.Date.add(fields.Date.today(), months=3), copy=False)
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Size Garden")
    garden_orientation = fields.Selection(string="Orientation Garden", selection=garden_possible_orientations)
    state = fields.Selection(string='State', selection=estate_possible_states, default='new', required=True, copy=False)
    estate_property_type_id = fields.Many2one("estate.property.type", string="Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many(comodel_name="estate.property.offer", inverse_name="property_id", string="Offers")
    active = fields.Boolean("Active", default=True)
    total_area = fields.Float(compute="_compute_total_area", string="Total Area (sqm)")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area


    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            #offer_prices = [offer.price for offer in record.offer_ids if offer.status not in ["refused"]]
            #record.best_price = max(offer_prices) if offer_prices else 0

            offer_prices = record.offer_ids.filtered(lambda o: o.status not in ["refused"]).mapped("price")
            record.best_price = max(offer_prices) if offer_prices else 0

    @api.onchange("garden")
    def _onchange_partner_id(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "N"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_new_or_canceled(self):
        if self.state not in ["new", "canceled"]:
            raise UserError("Can't delete properties that are not new or canceled.")

    def button_property_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("Canceled properties can not be sold.")
            else:
                record.state = "sold"
        return True

    def button_property_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties can not be canceled")
            else:
                record.state = "canceled"
        return True
