from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property offers"

    price = fields.Float("Price")
    status = fields.Selection(string="Status", copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=True)
    property_id = fields.Many2one(comodel_name="estate.property", string="Property", required=True)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline")
    validity = fields.Integer(string="Validity (days)")


    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            current_date = record.create_date if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(current_date, days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            creation_date = fields.Date.to_date(record.create_date)
            record.validity = (record.date_deadline - creation_date).days

    # model >> model_create_multi (updated in odoo 17?)
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals['price'] < self.env['estate.property'].browse(vals['property_id']).best_price:
                raise UserError("Can't make offers with a lower amount than the best offer.") 
            self.env['estate.property'].browse(vals['property_id'])['state'] = 'offer_received'
        return super().create(vals_list)

    def action_confirm_offer(self):
        self.ensure_one()
        self.status = "accepted"
        linked_property = self.env['estate.property'].browse(self.property_id)
        linked_property['selling_price'] = self.price
        linked_property['buyer_id'] = self.partner_id
        return True

    def action_cancel_offer(self):
        self.ensure_one()
        self.status = "refused"
        return True
