from openerp import models, fields, api
from openerp import tools

class CelebrationType(models.Model):
    _name='celebration.type'
    
    name = fields.Char(string='Celebration Type')
    color = fields.Integer(string='Color')
    
class Celebration(models.Model):
    _name='celebration'
    _inherit=['calendar.event']
    
    celebrant_ids = fields.Many2many('res.partner','celebration_celebrant_rel','celebration_id','partner_id',string='Celebrant')
    partner_ids = fields.Many2many('res.partner', 'celebration_res_partner_rel','celebration_id','partner_id', string='Attendees', states={'done': [('readonly', True)]})
    alarm_ids = fields.Many2many('calendar.alarm', 'calendar_alarm_celebration_rel','celebration_id','alarm_id', string='Reminders', ondelete="restrict", copy=False)
    attendee_ids= fields.One2many('celebration.attendee', 'event_id', 'Attendees', ondelete='cascade')
    
class CelebrationAttendee(models.Model):
    _name='celebration.attendee'
    _inherit='calendar.attendee'
    
    event_id = fields.Many2one('celebration', 'Celebration linked', ondelete='cascade')
    
    @api.multi
    def create_attendees(self):
        
        current_user = self.env.user
        res = {}
        for event in self:
            attendees = {}
            for att in event.attendee_ids:
                attendees[att.partner_id.id] = True
            new_attendees = []
            new_att_partner_ids = []
            for partner in event.partner_ids:
                if partner.id in attendees:
                    continue
                access_token = self.new_invitation_token(event, partner.id)
                values = {
                    'partner_id': partner.id,
                    'event_id': event.id,
                    'access_token': access_token,
                    'email': partner.email,
                }

                if partner.id == current_user.partner_id.id:
                    values['state'] = 'accepted'

                att_id = self.env['calendar.attendee'].create( values)
                new_attendees.append(att_id)
                new_att_partner_ids.append(partner.id)

                if not current_user.email or current_user.email != partner.email:
                    mail_from = current_user.email or tools.config.get('email_from', False)
                    if not self.env.context.get('no_email'):
                        if self.pool['calendar.attendee']._send_mail_to_attendees(att_id, email_from=mail_from):
                            self.message_post(event.id, body=_("An invitation email has been sent to attendee %s") % (partner.name,), subtype="calendar.subtype_invitation")

            if new_attendees:
                self.write([event.id], {'attendee_ids': [(4, att) for att in new_attendees]})
            if new_att_partner_ids:
                self.message_subscribe([event.id], new_att_partner_ids)

            # We remove old attendees who are not in partner_ids now.
            all_partner_ids = [part.id for part in event.partner_ids]
            all_part_attendee_ids = [att.partner_id.id for att in event.attendee_ids]
            all_attendee_ids = [att.id for att in event.attendee_ids]
            partner_ids_to_remove = map(lambda x: x, set(all_part_attendee_ids + new_att_partner_ids) - set(all_partner_ids))

            attendee_ids_to_remove = []

            if partner_ids_to_remove:
                attendee_ids_to_remove = self.env["celebration.attendee"].search([('partner_id.id', 'in', partner_ids_to_remove), ('event_id.id', '=', event.id)])
                if attendee_ids_to_remove:
                    attendee_ids_to_remove.unlink()

            res[event.id] = {
                'new_attendee_ids': new_attendees,
                'old_attendee_ids': all_attendee_ids,
                'removed_attendee_ids': attendee_ids_to_remove
            }
        return res