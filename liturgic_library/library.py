from openerp import models, fields, api
from openerp import tools

class LiturgicLibrary(models.Model):
    _name = 'liturgic.library'
    
    name = fields.Char(string='Library',required=True)
    

class LiturgicDocument(models.AbstractModel):
    _name = 'liturgic.document'
    
    name=fields.Char(string='Name',required=True)
    
    
class LiturgicScore(models.Model):
    _name = 'liturgic.score'
    _inherit='liturgic.document'
    
    