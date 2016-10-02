from openerp import models, fields


class CalendarEventType(models.Model):
    _inherit = 'calendar.event.type'

    is_liturgic = fields.Boolean('Is Liturgic')


class Celebration(models.Model):
    _inherit = 'calendar.event'

    celebrant_id = fields.Many2one('res.partner',
                                   domain=[('company_type', '=', 'person')],
                                   string='Celebrant')
